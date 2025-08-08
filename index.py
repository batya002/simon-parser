import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://en.zalando.de/mens-shoes/"

def get_html_with_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)  # для отладки
        page = browser.new_page()
        page.goto(URL, timeout=60000, wait_until="networkidle")

        # Клик по "Accept cookies" если есть
        try:
            page.click("button:has-text('Accept')", timeout=5000)
            print("✅ Clicked Accept Cookies")
        except:
            print("⚠️ No cookie banner found")

        # Прокрутка вниз
        for _ in range(15):
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(1500)

        # Сохраняем HTML и скриншот
        page.wait_for_timeout(3000)
        page.screenshot(path="zalando.png", full_page=True)
        html = page.content()
        browser.close()
        return html



def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for element in soup.find_all("li", class_="QjLAB7"):
        try:
            brand = element.find("span", class_="OBkCPz")
            name = element.find("span", class_="voFjEy")
            if not brand or not name:
                continue
            full_name = f"{brand.text.strip()} {name.text.strip()}"

            a_tag = element.find("a", class_="_LM")
            product_url = "https://en.zalando.de" + a_tag["href"] if a_tag else None

            img_tag = element.find("img")
            img_url = img_tag["src"] if img_tag else None

            price_section = element.find("section")
            price_spans = price_section.find_all("span") if price_section else []
            current_price = price_spans[1].text.strip() if len(price_spans) > 1 else None
            old_price = price_spans[3].text.strip() if len(price_spans) > 3 else None
            discount = price_spans[5].text.strip() if len(price_spans) > 5 else None

            products.append({
                "name": full_name,
                "url": product_url,
                "image": img_url,
                "price": current_price,
                "old_price": old_price,
                "discount": discount,
            })
        except Exception as e:
            print(f"Error: {e}")
            continue

    return products

def save_to_json(data, filename="zalando_products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    print("Opening Zalando with Playwright...")
    html = get_html_with_playwright()
    print("Parsing products...")
    products = parse_products(html)
    print(f"Found {len(products)} products.")
    save_to_json(products)
    print("Saved to zalando_products.json")

if __name__ == "__main__":
    main()
