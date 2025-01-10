import sqlite3
import sys
from PyQt5.QtWidgets import *
from SecondHandCar import *
import glob
import pandas as pd
import data as data
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QFileDialog


class StreamRedirector(QObject):
    new_text = pyqtSignal(str)

    def write(self, text):
        self.new_text.emit(text)

    
def redirect_output():
    global output_stream
    output_stream = StreamRedirector()
    output_stream.new_text.connect(ui.QPlanText_Terminal.appendPlainText)  
    sys.stdout = output_stream
    sys.stderr = output_stream

class DataLoaderThread(QThread):
    data_loaded = pyqtSignal()  

    def run(self):
        
        self.load_data()
        
        

    
    def load_data(self):
        try:
            baglanti = sqlite3.connect("SecondHandCar.db")
            islem = baglanti.cursor()


            with baglanti as conn:
                conn.execute("DELETE FROM Cars;")
            baglanti.commit()

            
            islem.execute("""
                CREATE TABLE IF NOT EXISTS Cars (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                engineType TEXT NOT NULL,
                year TEXT NOT NULL,
                km INTEGER NOT NULL,
                fuelType TEXT NOT NULL,
                gearType TEXT NOT NULL,
                warrantyStatus TEXT NOT NULL,
                price INTEGER NOT NULL
            )
            """)

            
            csv_file="araba_verileri.csv"
            print(f"İşleniyor: {csv_file}")
            df = pd.read_csv(csv_file)  
            df = df[['brand', 'model', 'engineType', 'year', 'km', 'fuelType', 'gearType', 'warrantyStatus', 'price']]
            df.to_sql('Cars', baglanti, if_exists='append', index=False) 

            
            self.data_loaded.emit()

        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")
        finally:
            
            self.quit()


class PullDataThread(QThread):
    data_pulled = pyqtSignal()

    def run(self):
        self.pull_data()

    def pull_data(self):
        page_from()
        page_to()
        
        
        try:
        
    
            data.veri_cek(page_from(),page_to())
            self.load_data()
        except Exception as e:
            print(f"Veri çekme sırasında hata: {e}")

    def load_data(self):
        try:
            baglanti = sqlite3.connect("SecondHandCar.db")
            islem = baglanti.cursor()

            with baglanti as conn:
                conn.execute("DELETE FROM Cars;")
            baglanti.commit()

            islem.execute("""
                CREATE TABLE IF NOT EXISTS Cars (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                engineType TEXT NOT NULL,
                year TEXT NOT NULL,
                km INTEGER NOT NULL,
                fuelType TEXT NOT NULL,
                gearType TEXT NOT NULL,
                warrantyStatus TEXT NOT NULL,
                price INTEGER NOT NULL
            )
            """)

            csv_file = "updated_araba_verileri.csv"
            print(f"İşleniyor: {csv_file}")
            df = pd.read_csv(csv_file)  
            df = df[['brand', 'model', 'engineType', 'year', 'km', 'fuelType', 'gearType', 'warrantyStatus', 'price']]
            df.to_sql('Cars', baglanti, if_exists='append', index=False) 

            self.data_pulled.emit()
        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()



pull_data_thread = PullDataThread()


def datapull():
    pull_data_thread.start()
    pull_data_thread.data_pulled.connect(load_data_to_ui)

ui.btnPullData.clicked.connect(datapull)

def load_data():
        try:
            baglanti = sqlite3.connect("SecondHandCar.db")
            islem = baglanti.cursor()


            with baglanti as conn:
                conn.execute("DELETE FROM Cars;")
            baglanti.commit()

            
            islem.execute("""
                CREATE TABLE IF NOT EXISTS Cars (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                engineType TEXT NOT NULL,
                year TEXT NOT NULL,
                km INTEGER NOT NULL,
                fuelType TEXT NOT NULL,
                gearType TEXT NOT NULL,
                warrantyStatus TEXT NOT NULL,
                price INTEGER NOT NULL
            )
            """)

            
            csv_file= "updated_araba_verileri.csv"
            
            print(f"İşleniyor: {csv_file}")
            df = pd.read_csv(csv_file)  
            df = df[['brand', 'model', 'engineType', 'year', 'km', 'fuelType', 'gearType', 'warrantyStatus', 'price']]
            df.to_sql('Cars', baglanti, if_exists='append', index=False) 

            
        except Exception as e:
            print(f"Veri yükleme sırasında hata: {e}")







baglanti = sqlite3.connect("SecondHandCar.db")
islem = baglanti.cursor()





def get_all_brands():
    ui.cmbBrand.addItem("All")
    islem.execute("SELECT DISTINCT brand FROM Cars")
    return [row[0] for row in islem.fetchall()]

def get_all_models():
    ui.cmbModel.addItem("All")
    islem.execute("SELECT DISTINCT model FROM Cars")
    return [row[0] for row in islem.fetchall()]

def get_all_engineTypes():
    ui.cmbEngineType.addItem("All")
    islem.execute("SELECT DISTINCT engineType FROM Cars")
    return [row[0] for row in islem.fetchall()]

def get_all_years():
    ui.cmbYear.addItem("All")
    islem.execute("SELECT DISTINCT year FROM Cars")
    return  [row[0] for row in islem.fetchall()]

def get_all_fuel_types():
    ui.cmbFuelType.addItem("All")
    islem.execute("SELECT DISTINCT fuelType FROM Cars")
    return [row[0] for row in islem.fetchall()]

def get_all_gear_types():
    ui.cmbGearType.addItem("All")
    islem.execute("SELECT DISTINCT gearType FROM Cars")
    return [row[0] for row in islem.fetchall()]

def get_all_warranty_statuses():
    ui.cmbWarranty.addItem("All")
    islem.execute("SELECT DISTINCT warrantyStatus FROM Cars")
    return [row[0] for row in islem.fetchall()]




def load_data_to_ui():
    ui.tableWidget.setRowCount(0)
    ui.statusbar.showMessage("Tablo tercihleri temizlendi.", 3000)
    ui.cmbBrand.clear()
    ui.cmbYear.clear()
    ui.cmbModel.clear()
    ui.cmbEngineType.clear()
    ui.cmbFuelType.clear()
    ui.cmbGearType.clear()
    ui.cmbWarranty.clear()
    ui.PullDataYearFrom.clear()
    ui.PullDataYearTo.clear()
    ui.cmbBrand.addItems(get_all_brands())
    ui.cmbYear.addItems(get_all_years())
    ui.cmbModel.addItems(get_all_models())
    ui.cmbEngineType.addItems(get_all_engineTypes())
    ui.cmbFuelType.addItems(get_all_fuel_types())
    ui.cmbGearType.addItems(get_all_gear_types())
    ui.cmbWarranty.addItems(get_all_warranty_statuses())
    print("Database'ten gelen veri Combobox'lara aktarıldı.")
    







filters_dict = {}

def save_filters():
    global filters_dict
    filters_dict = {
        "brand": ui.cmbBrand.currentText(),
        "model": ui.cmbModel.currentText(),
        "price_min": ui.lneMin_2.text().strip(),
        "price_max": ui.lneMin.text().strip(),
        "km_min": ui.lneMax_2.text().strip(),
        "km_max": ui.lneMax.text().strip(),
        "engine_type": ui.cmbEngineType.currentText(),
        "fuel_type": ui.cmbFuelType.currentText(),
        "gear_type": ui.cmbGearType.currentText(),
        "warranty": ui.cmbWarranty.currentText(),
        "year": ui.cmbYear.currentText(),
    }

def show_results():
    save_filters() 
    try:
       
        
        
        query = "SELECT DISTINCT * FROM cars WHERE 1=1"
        filters = []

        
        
        brand = ui.cmbBrand.currentText()
        if brand != "All":
            query += " AND brand = ?"
            filters.append(brand)

        model = ui.cmbModel.currentText()
        if model != "All":
            query += " AND model = ?"
            filters.append(model) 

        price_min = ui.lneMin_2.text().strip()
        price_max = ui.lneMin.text().strip()
        if price_min and price_max:
            query += " AND  CAST(price AS INTEGER) BETWEEN ? AND ?"
            filters.append(int(price_min))
            filters.append(int(price_max))

        km_min = ui.lneMax_2.text().strip()
        km_max = ui.lneMax.text().strip()
        if km_min and km_max:
            query += " AND CAST(km AS INTEGER) BETWEEN ? AND ?"
            filters.append(int(km_min))  
            filters.append(int(km_max))   
        
        
        EngineType = ui.cmbEngineType.currentText()
        if EngineType != "All":
            query += " AND EngineType = ?"
            filters.append(EngineType)

        FuelType = ui.cmbFuelType.currentText()
        if FuelType != "All":
            query += " AND FuelType= ?"
            filters.append(FuelType)   
        
        GearType = ui.cmbGearType.currentText()
        if GearType != "All":
            query += " AND GearType= ?"
            filters.append(GearType)

        Warranty = ui.cmbWarranty.currentText()
        if Warranty != "All":
            query += " AND WarrantyStatus= ?"
            filters.append(Warranty)
       

        year = ui.cmbYear.currentText()
        if year != "All":
            query += " AND year= ?"
            filters.append(year)

        print(query)
        print(filters)

       
        islem.execute(query, tuple(filters))
        kayitlar = islem.fetchall()

        if kayitlar:
            
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "ID", "Brand","Model", "Engine Type", "Year", "Km",
                "Fuel Type", "Gear Type", "Warranty Status","Price"
            ])

            
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi): 
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
            
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")
    reset_comboboxes()

def reset_comboboxes():
    try:
        
        ui.cmbBrand.setCurrentText("All")
        ui.cmbModel.setCurrentText("All")
        ui.cmbEngineType.setCurrentText("All")
        ui.cmbYear.setCurrentText("All")
        ui.cmbFuelType.setCurrentText("All")
        ui.cmbGearType.setCurrentText("All")
        ui.cmbWarranty.setCurrentText("All")
        

        
        ui.statusbar.showMessage("Tüm filtreler sıfırlandı.", 3000)
    except Exception as e:
        print(f"ComboBox sıfırlama sırasında hata oluştu: {e}")

def show_all_results():

    
    try:
        
        query = "SELECT DISTINCT * FROM cars WHERE 1=1"
        filters = []

        
  
        islem.execute(query)
        kayitlar = islem.fetchall()
        print(query)
        print(filters)
        if kayitlar:
           
            ui.tableWidget.setColumnCount(len(kayitlar[0]))
            ui.tableWidget.setHorizontalHeaderLabels([
                "id", "brand","model", "engineType", "year", "km",
                "fuelType", "gearType", "warrantyStatus","price"
            ])

            
            ui.tableWidget.setRowCount(len(kayitlar))
            for indexSatir, kayitNumarasi in enumerate(kayitlar):
                for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                    ui.tableWidget.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
            
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Genel hata: {e}")
    reset_comboboxes()

def page_to():
        page_for_range_to= ui.PullDataYearTo.text().strip()
        if page_for_range_to=="":
           page_for_range_to = 80
        return  page_for_range_to
    

def page_from():
        page_for_range_from = ui.PullDataYearFrom.text().strip()
        if page_for_range_from=="":
           page_for_range_from= 1
        return  page_for_range_from

def clear():
    try:
        ui.cmbBrand.setCurrentText("All")
        ui.cmbModel.setCurrentText("All")
        ui.cmbEngineType.setCurrentText("All")
        ui.cmbYear.setCurrentText("All")
        ui.cmbFuelType.setCurrentText("All")
        ui.cmbGearType.setCurrentText("All") 
        ui.cmbWarranty.setCurrentText("All")
        ui.tableWidget.setRowCount(0)
        ui.statusbar.showMessage("Tablo tercihleri temizlendi.", 3000)
    except Exception as e:
        print(f"Temizleme sırasında hata oluştu: {str(e)}")

def download_data(): 
    try:
        global filters_dict
        query = "SELECT DISTINCT * FROM cars WHERE 1=1"
        filters = []

        
        if filters_dict.get("brand") and filters_dict["brand"] != "All":
            query += " AND brand = ?"
            filters.append(filters_dict["brand"])

        if filters_dict.get("model") and filters_dict["model"] != "All":
            query += " AND model = ?"
            filters.append(filters_dict["model"])

        if filters_dict.get("price_min") and filters_dict.get("price_max"):
            query += " AND CAST(price AS INTEGER) BETWEEN ? AND ?"
            filters.append(int(filters_dict["price_min"]))
            filters.append(int(filters_dict["price_max"]))

        if filters_dict.get("km_min") and filters_dict.get("km_max"):
            query += " AND CAST(km AS INTEGER) BETWEEN ? AND ?"
            filters.append(int(filters_dict["km_min"]))
            filters.append(int(filters_dict["km_max"]))

        if filters_dict.get("engine_type") and filters_dict["engine_type"] != "All":
            query += " AND EngineType = ?"
            filters.append(filters_dict["engine_type"])

        if filters_dict.get("fuel_type") and filters_dict["fuel_type"] != "All":
            query += " AND FuelType = ?"
            filters.append(filters_dict["fuel_type"])

        if filters_dict.get("gear_type") and filters_dict["gear_type"] != "All":
            query += " AND GearType = ?"
            filters.append(filters_dict["gear_type"])

        if filters_dict.get("warranty") and filters_dict["warranty"] != "All":
            query += " AND WarrantyStatus = ?"
            filters.append(filters_dict["warranty"])

        if filters_dict.get("year") and filters_dict["year"] != "All":
            query += " AND year = ?"
            filters.append(filters_dict["year"])

        
        islem.execute(query, tuple(filters))
        kayitlar = islem.fetchall()

        if kayitlar:
           
            df = pd.DataFrame(kayitlar, columns=[
                "ID", "Brand", "Model", "Engine Type", "Year",
                "Km", "Fuel Type", "Gear Type", "Warranty Status", "Price"
            ])

            
            file_path, _ = QFileDialog.getSaveFileName(
                pencere, "Verileri Kaydet", "", "Excel Dosyası (*.csv)"
            )

            if file_path:  
               
                df.to_csv(file_path, index=False)

                
                print(f"Veriler başarıyla '{file_path}' dosyasına kaydedildi.", 5000)
            else:
                
                print("Dosya kaydedilmedi.", 5000)
        else:
           
            print("Kaydedilecek veri bulunamadı.", 5000)

    except sqlite3.Error as e:
        
        print(f"Veritabanı hatası: {e}", 5000)
    except Exception as e:
        
        print(f"Hata: {e}", 5000)


ui.btnShowAllResults.clicked.connect(show_all_results)
ui.btnShowResults.clicked.connect(show_results)  
ui.btnClear.clicked.connect(clear)
ui.btnDownload.clicked.connect(download_data)  

loader_thread = DataLoaderThread()
loader_thread.data_loaded.connect(load_data_to_ui) 
loader_thread.finished.connect(lambda: print("Veri yükleme tamamlandı."))
loader_thread.start()

redirect_output()

sys.exit(uygulama.exec_())