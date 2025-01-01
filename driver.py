from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

start = time.time()

options = Options()
options.add_argument("--headless")

path = "C:\\Program Files (x86)\\chromedriver.exe"
service = Service(executable_path=path)

driver = webdriver.Chrome(service=service)

with open("arabalar_motor_hacmi.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # CSV dosyasına başlıkları yazıyoruz
    writer.writerow(
        ["Marka", "Model", "Motor Hacmi",  "Yıl", "Kilometre", "Yakıt Tipi", "Vites Türü", "Garanti Durumu",
         "Fiyat"])

    for page_number in range(1,94):
        driver.get(f"https://dod.com.tr/arac-arama?sayfa={page_number}")

        try:
            # Sayfa içeriğinin yüklenmesini bekliyoruz (do-vehicle-card__container öğesinin görünür olmasını)
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "do-vehicle-card__container"))
            )
        except Exception as e:
            print(f"Sayfa {page_number} yüklenirken hata oluştu: {e}")
            continue  # Eğer sayfa yüklenmediyse, sonraki sayfaya geç

        # Sayfa yüklendikten sonra araçları alıyoruz
        cars = driver.find_elements(By.CLASS_NAME, "do-vehicle-card__container")

        if not cars:  # Eğer araç bulunamazsa (yani sayfa boşsa)
            print(f"Sayfa {page_number} boş veya erişilemiyor.")
            continue  # Boş sayfayı atla

        for car in cars:
            try:
                brand_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__title")
                model_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__summary")
                detail_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__specs-summary")
                price_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__price")

                # Detaylar listesini alıyoruz
                details = detail_element.text.split(",")

                # Yıl bilgisi
                year = next((d for d in details if re.match(r"\b\d{4}\b", d)), "Bilinmiyor")

                # Kilometre bilgisi
                kilometre_raw = next((d for d in details if "km" in d), "0")
                kilometre = re.sub(r"[^\d]", "", kilometre_raw)  # Sadece rakamları bırak

                # Yakıt tipi
                fuel_type = next((d for d in details if "Dizel" in d or "Benzin" in d or "Hibrit" in d), "Bilinmiyor")

                # Vites türü (Manuel, Otomatik, Tiptronic)
                transmission = next((d for d in details if "Manuel" in d or "Otomatik" in d or "Tiptronic" in d),
                                    "Bilinmiyor")

                # Garanti durumu
                guarantee_status = next((d for d in details if "Garant" in d), "Bilinmiyor")

                # Fiyat bilgisi
                price_raw = price_element.text.replace("\n", "")
                price = re.sub(r"[^\d]", "", price_raw)

                brand = brand_element.text.split("\n")
                model = model_element.text

                # Yazıyoruz
                writer.writerow([*brand, model, year, kilometre, fuel_type, transmission, guarantee_status, price])

            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                writer.writerow(["Veri bulunamadı"] * 10)

driver.quit()
end = time.time()
print(end - start)



