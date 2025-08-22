import requests
from bs4 import BeautifulSoup
import time
import telebot
from datetime import datetime, timedelta

# === Налаштування ===
TOKEN = "8082612833:AAGoizCW_xCc3-hUzq5KkZxslXSwwnVSvw8"
CHAT_ID = "8272589372"  # дізнатися у @userinfobot
bot = telebot.TeleBot(TOKEN)

URL = "https://www.olx.ua/uk/list/q-iphone-xr/?search%5Bfilter_float_price:from%5D=3000&search%5Bfilter_float_price:to%5D=4000&search%5Border%5D=created_at:desc"

# Список уже відправлених оголошень (щоб не дублювати)
sent_ads = set()

def check_ads():
    global sent_ads
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    ads = soup.find_all("div", {"data-cy": "l-card"})

    new_ads = []
    for ad in ads:
        title_el = ad.find("h6")
        price_el = ad.find("p", {"data-testid": "ad-price"})
        link_el = ad.find("a", href=True)

        if not (title_el and price_el and link_el):
            continue

        title = title_el.text.strip()
        price = price_el.text.strip()
        link = "https://www.olx.ua" + link_el["href"]

        # Унікальний ID = посилання
        if link not in sent_ads and "iphone xr" in title.lower():
            new_ads.append((title, price, link))
            sent_ads.add(link)

    return new_ads

def main():
    while True:
        try:
            new_ads = check_ads()
            for title, price, link in new_ads:
                msg = f"📱 {title}\n💵 {price}\n🔗 {link}"
                bot.send_message(CHAT_ID, msg)
        except Exception as e:
            print("Помилка:", e)

        time.sleep(600)  # чекати 10 хв

if __name__ == "__main__":
    main()
