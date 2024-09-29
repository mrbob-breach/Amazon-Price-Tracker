from bs4 import BeautifulSoup
import requests
import smtplib
import os

URL = "https://www.amazon.com/dp/B07NTVKQN3/?coliid=I32HUMGYLGG4WA&colid=TCQA7EOYBMII&ref_=list_c_wl_lv_ov_lig_dp_it&th=1"
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
BUY_PRICE = 240

response = requests.get(
    URL,
    headers={
        "Accept-Language":"en-US,en;q=0.9",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
)

soup = BeautifulSoup(response.text, "html.parser")

product = soup.find(id="productTitle").getText()
product = " ".join(product.split())
price = float(soup.find(class_="a-offscreen").getText().split("$")[1])

if price < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n"
                f"{product} is now ${price}\n"
                f"{URL}".encode('UTF-8')
        )
        print("Sent price email")
