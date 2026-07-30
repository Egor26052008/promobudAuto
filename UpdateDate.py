import time
import re
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def create_driver() -> webdriver.Firefox:
    options = Options()
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    return driver




def crawl_all_pages(driver: webdriver.Firefox, interval: float = 5.0) -> None:

    element = driver.find_element(By.CSS_SELECTOR, "a.end[rel='next']")
    href = element.get_attribute("href")

    match = re.search(r"page=(\d+)", href)
    last_page = int(match.group(1)) if match else None

    if last_page is None:
        print("Не удалось определить количество страниц.")
        return

    print(f"Найдено страниц: {last_page}")

    for page in range(1, last_page + 1):
        page_url = f"https://www.promobud.ua/price/self/page={page}/"
        driver.get(page_url)
        print(f"Открыта страница {page}/{last_page}: {page_url}")

        update_date(driver)  # отмечаем чекбоксы и жмём "Обновить" прямо на этой странице

        time.sleep(interval)



def update_date(driver: webdriver.Firefox):
    
    checkbox = driver.find_element(By.CSS_SELECTOR, "input.group[type='checkbox']")

    if not checkbox.is_selected():
        checkbox.click()

    update_button = driver.find_element(By.CSS_SELECTOR, "a.gui-request.gui-fast-open[data-data='page=date_update']")
    update_button.click()




def open_site(url: str) -> None:
    driver = create_driver()

    driver.get(url)
    print(f"Открыт сайт: {driver.title} ({url})")

    print("Напиши 'crawl' и Enter, чтобы запустить обход всех страниц.")
    print("Напиши 'ex' и Enter, чтобы закрыть браузер.")

    while True:
        command = input().strip().lower()

        if command == "ex":
            break
        elif command == "crawl":
            crawl_all_pages(driver, interval=5.0)
        elif command == "check":
            update_date(driver)
        else:
            print("Неизвестная команда. Доступно: 'crawl' или 'ex' или 'check'.")

    driver.quit()




if __name__ == "__main__":
    TARGET_URL = "https://www.promobud.ua/price/company/19973/"
    open_site(TARGET_URL)