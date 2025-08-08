from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
import requests
import os

PRODUCTS_FILE = "json/shop_products.json"

def load_existing_ids():
    if not os.path.exists(PRODUCTS_FILE):
        return set()
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return {item["product"]["id"] for item in data if "product" in item}
        except json.JSONDecodeError:
            return set()

def save_products(products):
    existing = []
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                pass
    existing.extend(products)
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def get_product_links(page):
    print(f"🔍 Загружаем страницу: {page}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://shop.simon.com/collections/men?page={page}"
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    product_links = set()
    for a in soup.select("a[href*='/products/']"):
        href = a.get("href")
        if href and href.startswith("/products/"):
            full_url = "https://shop.simon.com" + href.split("?")[0]
            product_links.add(full_url)

    return list(product_links)

def parse_product_page(url):
    clean_url = url.split('?')[0]
    json_url = clean_url + ".json"
    print(f"📦 Обрабатываем товар: {json_url}")

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(json_url, headers=headers)
        data = response.json()
    except Exception as e:
        print(f"❌ Ошибка при получении JSON: {e}")
        return None

    product = data.get("product", {})

    return {
        "id": product.get("id"),
        "title": product.get("title"),
        "handle": product.get("handle"),
        "vendor": product.get("vendor"),
        "product_type": product.get("product_type"),
        "tags": product.get("tags"),
        "body_html": product.get("body_html"),
        "url": url,
        "variants": [
            {
                "id": v.get("id"),
                "title": v.get("title"),
                "price": v.get("price"),
                "sku": v.get("sku"),
                "option1": v.get("option1"),
                "option2": v.get("option2"),
                "option3": v.get("option3"),
            } for v in product.get("variants", [])
        ],
        "images": [
            {"src": img.get("src")} for img in product.get("images", [])
        ],
        "image": {
            "src": product.get("image", {}).get("src")
        } if product.get("image") else None
    }

def run_simon():
    all_products = []
    existing_ids = load_existing_ids()
    page = 1

    while True:
        links = get_product_links(page)
        if not links:
            print("🚫 Товары закончились.")
            break

        new_items = 0

        for i, link in enumerate(links, 1):
            try:
                print(f"[{i}/{len(links)}]")
                item = parse_product_page(link)
                if item and item["id"] not in existing_ids:
                    all_products.append({"product": item})
                    existing_ids.add(item["id"])
                    new_items += 1
                else:
                    print("⏩ Пропущено (уже есть)")
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Ошибка на {link}: {e}")

        if new_items == 0:
            print("🔁 Нет новых товаров на странице, выходим.")
            break

        save_products(all_products)
        all_products.clear()
        page += 1

    print("✅ Готово! Данные сохранены.")

if __name__ == "__main__":
    run_simon()
