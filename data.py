from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re






def veri_cek(page_from,page_to):
 
  
  start = time.time()



  options = Options()
  options.add_argument("--headless")

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=options)

  driver.get("https://www.google.com")

  
  with open("updated_araba_verileri.csv", "w", encoding="utf-8", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(
          ["brand", "model", "engineType",  "year", "km", "fuelType", "gearType", "warrantyStatus",
          "price"])
      
      range_page_from = int(page_from)
      range_page_to = int(page_to)
      for page_number in range(range_page_from,range_page_to+1):
          driver.get(f"https://dod.com.tr/arac-arama?sayfa={page_number}")
          print(f"{page_number}. sayfa verisi çekiliyor.")  
          try:
              
              WebDriverWait(driver, 20).until(
                  EC.presence_of_all_elements_located((By.CLASS_NAME, "do-vehicle-card__container"))
              )
          except Exception as e:
              print(f"Sayfa {page_number} yüklenirken hata oluştu: {e}")
              continue  

        
          cars = driver.find_elements(By.CLASS_NAME, "do-vehicle-card__container")

          if not cars:  
              print(f"Sayfa {page_number} boş veya erişilemiyor.")
              continue  

          for car in cars:
              try:
                  brand_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__title")
                  model_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__summary")
                  detail_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__specs-summary")
                  price_element = car.find_element(By.CLASS_NAME, "do-vehicle-card__price")

                 
                  details = detail_element.text.split(",")

                  
                  year = next((d for d in details if re.match(r"\b\d{4}\b", d)), "Bilinmiyor")

                  
                  kilometre_raw = next((d for d in details if "km" in d), "0")
                  kilometre = re.sub(r"[^\d]", "", kilometre_raw)  

                  
                  fuel_type = next((d for d in details if "Dizel" in d or "Benzin" in d or "Hibrit" in d), "Bilinmiyor")

                 
                  transmission = next((d for d in details if "Manuel" in d or "Otomatik" in d or "Tiptronic" in d),
                                      "Bilinmiyor")

                
                  guarantee_status = next((d for d in details if "Garant" in d), "Bilinmiyor")

                  
                  price_raw = price_element.text.replace("\n", "")
                  price = re.sub(r"[^\d]", "", price_raw)

                  brand = brand_element.text.split("\n")
                  model = model_element.text

                 
                  writer.writerow([*brand, model, year, kilometre, fuel_type, transmission, guarantee_status, price])
                  
              except Exception as e:
                  print(f"Bir hata oluştu: {e}")
                  writer.writerow(["Veri bulunamadı"] * 10)
          print(f"{page_number}. sayfa verisi çekildi.")      

  driver.quit()
  end = time.time()
  print("Veri çekilirken geçen süre: ",end-start)