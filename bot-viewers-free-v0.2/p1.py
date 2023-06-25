from undetected_chromedriver import Chrome, ChromeOptions
import threading
import time
from tqdm import tqdm
import subprocess
import random
import string
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_referer(referer):
    random_length = random.randint(4, 11)
    random_letters = ''.join(random.choices(string.ascii_lowercase, k=random_length))
    return referer.replace('redirect', random_letters)

def click_button(driver, button_id):
    try:
        button = WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, button_id)))
        button.click()
    except Exception as e:
        pass

def click_xpath_button(driver, button_xpath):
    try:
        driver.execute_script("""
            var xpath = arguments[0];
            var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (matchingElement) {
                matchingElement.click();
            }
        """, button_xpath)
    except Exception as e:
        pass

def click_ad_skip_button(driver):
    try:
        button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
        )
        button.click()
    except Exception as e:
        pass

def click_play_button(driver):
    try:
        button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-large-play-button.ytp-button"))
        )
        button.click()
    except Exception as e:
        pass

def run_browser(url, referer, browser_id):
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with open("proxy.txt", "r") as file:
        proxies = file.read().splitlines()

    proxy = random.choice(proxies)
    options.add_argument(f"--proxy-server=http://{proxy}")

    print(f"Browser {browser_id} - Proxy: {proxy}")

    with open("agent_old.txt", "r") as file:
        user_agents = file.read().splitlines()

    user_agent = random.choice(user_agents)
    options.add_argument(f"--user-agent={user_agent}")

    referer = generate_random_referer(referer)
    options.add_argument(f"--referer={referer}")

    print(f"Browser {browser_id} - User Agent: {user_agent}")
    print(f"Browser {browser_id} - Referer: {referer}")

    try:
        driver = Chrome(options=options)
        driver.set_window_size(30, 1000)
        driver.set_window_position(500 * (browser_id - 1), 0)
        driver.get(url)
    except TimeoutException:
        print(f"Browser {browser_id} - Connection timed out")
        driver.quit()  # Închide browserul în cazul în care apare eroarea ERR_TIMED_OUT
        return
    except Exception as e:
        print(f"Browser {browser_id} - Proxy no work - Proxy IP: {proxy}")
        driver.quit()  # Închide browserul în cazul în care proxy-ul nu funcționează
        return

    for _ in tqdm(range(60), desc=f"Browser {browser_id}"):
        time.sleep(1)
        if _ % 9 == 0:
            click_button(driver, "return-to-youtube")
            click_ad_skip_button(driver)
            click_play_button(driver)
            click_xpath_button(driver, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape")

    driver.quit()
    driver.service.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)

urls = [
    "https://youtu.be/wgCj5uIQB8s",
    "https://youtu.be/25_4pTIdvTQ",
    "https://youtu.be/UC_qPmRqo8Q",
    "https://youtu.be/JdBDRcCAT_k",
]

referers = [
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
]

while True:
    threads = []

    for i, (url, referer) in enumerate(zip(urls, referers)):
        thread = threading.Thread(target=run_browser, args=(url, referer, i+1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(2)
