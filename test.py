from undetected_chromedriver import Chrome, ChromeOptions
import threading
import time
from tqdm import tqdm
import subprocess
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_referer(referer):
    random_length = random.randint(4, 8)
    random_letters = ''.join(random.choices(string.ascii_lowercase, k=random_length))
    return referer.replace('redirect', random_letters)

def click_button(driver, button_id):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
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

    print(f"Browser {browser_id} - Proxy: {proxy}")  # Afișează adresa IP proxy utilizată

    with open("agent.txt", "r") as file:
        user_agents = file.read().splitlines()

    user_agent = random.choice(user_agents)
    options.add_argument(f"--user-agent={user_agent}")

    referer = generate_random_referer(referer)
    options.add_argument(f"--referer={referer}")  # Adaugă refering page

    print(f"Browser {browser_id} - User Agent: {user_agent}")  # Afișează user agent-ul utilizat
    print(f"Browser {browser_id} - Referer: {referer}")  # Afișează referer-ul utilizat

    driver = Chrome(options=options)
    try:
        driver.get(url)
    except Exception as e:
        print(f"Exception in thread {threading.current_thread().name}: {e}")

    for _ in tqdm(range(15), desc=f"Browser {browser_id}"):
        time.sleep(1)
        if _ % 3 == 0:
            click_button(driver, "return-to-youtube")

    driver.quit()
    driver.service.process.send_signal(subprocess.signal.CTRL_BREAK_EVENT)  # Închide procesul browserului

# URL-uri pentru fiecare browser
urls = [
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    "https://www.youtube.com/watch?v=bJdaBuyNQ14",
    
]

# Refering page-uri
referers = [
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    "https://redirect.com",
    
]

while True:
    threads = []
    
    for i in range(10):
        url = random.choice(urls)
        referer = random.choice(referers)
        
        thread = threading.Thread(target=run_browser, args=(url, referer, i+1))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(5)
