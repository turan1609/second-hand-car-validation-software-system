from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import re

start = time.time()

options = Options()
options.add_argument("--headless")

path = "C:\\Program Files (x86)\\chromedriver.exe"
service = Service(executable_path=path)

driver = webdriver.Chrome(service=service)

with open("car_Data_File.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(
        ["Marka","Model","Motor Hacmi","Güç","Yıl","Kilometre","Yakıt Tipi","Vites Türü","Garanti Durumu","Fiyat"])

    for page_number in range(1, 100):
        driver.get(f"https://dod.com.tr/arac-arama?sayfa={page_number}")
        time.sleep(1)

        cars = driver.find_elements(By.CLASS_NAME, "do-vehicle-card__container")

        for car in cars:
            try:
                brand_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__title")
                model_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__summary")
                detail_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__specs-summary")
                price_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__price")


                details = detail_element.text.split(",")


                year = next((d for d in details if re.match(r"\b\d{4}\b", d)), "Bilinmiyor")


                kilometre_raw = next((d for d in details if "km" in d), "0")
                kilometre = re.sub(r"[^\d]", "", kilometre_raw)  # Sadece rakamları bırak


                fuel_type = next((d for d in details if "Dizel" in d or "Benzin" in d or "Hibrit" in d), "Bilinmiyor")


                transmission = next((d for d in details if "Manuel" in d or "Otomatik" in d or "Tiptronic" in d), "Bilinmiyor")


                guarantee_status = next((d for d in details if "Garant" in d), "Bilinmiyor")


                price_raw = price_element.text.replace("\n", "")
                price = re.sub(r"[^\d]", "", price_raw)

                brand = brand_element.text.split("\n")
                model = model_element.text


                writer.writerow([*brand,model,year,kilometre,fuel_type,transmission,guarantee_status,price])

            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                writer.writerow(["Veri bulunamadı"] * 10)

driver.quit()
end = time.time()
print(end - start)