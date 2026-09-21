from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

from urllib3.util import url

# Настройки парсинга
BASE_URL = "https://www.list.am/ru/category/452/{page}?gl=1" # Исследуемая стартовая страница
PAGES = 3 # Количество исследуемых страниц
DELAY = 5 # Задержка между переходами по страницам
OUTPUT = "list.csv" # Файл вывода данных

# Сбор данных с конкретной страницы
def parse_link(browser):
    contentr = browser.find_element(By.ID, "contentr")
    all_dls = contentr.find_elements(By.CSS_SELECTOR, "div.dl")
    main_block = all_dls[1] # Выбираем основной блок объявлений, откидывая рекламные
    elements = main_block.find_elements(By.CLASS_NAME, "category-data-list-grid-card__destination")
    page_data = [] # Список элементов со страницы
    for element in elements:
        try:
            link = element.get_attribute("href")
            title = element.find_element(By.CLASS_NAME, "l").text
            price = element.find_element(By.CLASS_NAME, "p").text
            condition = element.find_element(By.CLASS_NAME, "at").text
            location = element.find_element(By.CLASS_NAME, "category-data-list-card__grid-bottom").text
            page_data.append({"title": title, "price": price, "condition": condition, "location": location, "link": link})
        except Exception as e:
            print(f"Error: {e}")
            continue
    return page_data

# Настройки обхода проверок на бота
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Открываем нужную ссылку и разворачиваем окно
browser = webdriver.Chrome(options=options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {value: false});"})

# Проходим по всем страницам и собираем данные
all_data = []
for page in range(1, PAGES+1):
    url = BASE_URL.format(page=page)
    print(f"\nСтраница {page} : {url}")
    browser.get(url)
    time.sleep(DELAY)
    page_data = parse_link(browser)
    print(f"Найдено карточек: {len(page_data)}")
    all_data += page_data

browser.quit()

#Вывод информации о повторяющихся объявлениях
unique_data = list({item["link"]: item for item in all_data}.values())
print(f"🗑 Удалено дублей: {len(all_data) - len(unique_data)}")
print(f"✅ Уникальных: {len(unique_data)}")


with open('list.csv', 'w', newline="", encoding="utf-8-sig") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["title", "price", "condition", "location", "link"], delimiter=";")
    writer.writeheader()
    writer.writerows(unique_data)

print(f"\n✅ Сохранено {len(unique_data)} записей в list.csv")