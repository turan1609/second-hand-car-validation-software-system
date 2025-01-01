import csv
import sqlite3
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from SecondHandCar import *
from PyQt5.QtWidgets import QFileDialog


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

# Veritabanı bağlantısı
baglanti = sqlite3.connect('SecondHandCar.db')
islem = baglanti.cursor()

# Veritabanı tablosunu oluştur (eğer yoksa)
islem.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
''')
baglanti.commit()

# Veritabanı bağlantısı
conn = sqlite3.connect('SecondHandCar.db')
cursor = conn.cursor()



# Veritabanındaki mevcut verileri kontrol et
def reset_id_and_import_data(file_path):
    try:
        # Eski verileri temizle (isteğe bağlı)
        cursor.execute('DELETE FROM Cars')
        conn.commit()

        # `sqlite_sequence` tablosunu sıfırlayarak id'yi 1'den başlat
        cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "Cars"')
        conn.commit()

        # CSV dosyasındaki verileri veritabanına ekle
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Başlık satırını geç

            # CSV dosyasındaki verileri satır satır kontrol et
            print("CSV Dosyasındaki Veriler:")
            for row in reader:
                print(row)  # CSV satırlarını yazdırarak kontrol edin

                # Satırın uzunluğunun beklenen 9 sütuna sahip olup olmadığını kontrol et
                if len(row) == 9:
                    try:
                        # Araç verilerinin veritabanında mevcut olup olmadığını kontrol et
                        cursor.execute('''
                            SELECT COUNT(*) FROM Cars WHERE brand = ? AND model = ? AND engineType = ? AND year = ? AND km = ? AND fuelType = ? AND gearType = ? AND warrantyStatus = ? AND price = ?
                        ''', tuple(row))
                        count = cursor.fetchone()[0]

                        # Eğer araç zaten varsa, eklemeyi atla
                        if count == 0:
                            # Veritabanına ekleme işlemi
                            cursor.execute('''
                            INSERT INTO Cars (brand, model, engineType, year, km, fuelType, gearType, warrantyStatus, price)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', tuple(row))
                        else:
                            print(f"Araç zaten veritabanında mevcut: {row}")

                    except sqlite3.Error as e:
                        print(f"Veritabanı hatası (satır eklenirken): {e}")
                        continue  # Eğer bir hata varsa bu satırı atla ve diğerlerini işlemeye devam et
                else:
                    print(f"Uyarı: Geçersiz satır uzunluğu (satırda 9 sütun bekleniyor): {row}")

        # Veritabanına işlemi kaydet
        conn.commit()
        print("Veriler başarıyla veritabanına aktarıldı.")

        # Veritabanındaki tüm verileri yazdırarak kontrol et
        cursor.execute('SELECT * FROM Cars')
        rows = cursor.fetchall()
        print("Veritabanındaki tüm veriler:")
        for row in rows:
            print(row)

    except FileNotFoundError:
        print("CSV dosyası bulunamadı. Lütfen dosya yolunun doğru olduğundan emin olun.")
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        conn.close()  # Bağlantıyı her durumda kapat


# CSV dosyasını veritabanına aktarma
reset_id_and_import_data('arabalar_motor_hacmi.csv')  # Veriyi veritabanına ekleme






def get_all_brands():
    islem.execute("SELECT DISTINCT brand FROM Cars")
    brands = [row[0] for row in islem.fetchall()]
    return ["All"] + brands  # "All" seçeneğini en başa ekle

def get_all_models():
    islem.execute("SELECT DISTINCT model FROM Cars")
    models = [row[0] for row in islem.fetchall()]
    return ["All"] + models  # "All" seçeneğini en başa ekle

def get_all_engineTypes():
    islem.execute("SELECT DISTINCT engineType FROM Cars")
    engine_types = [row[0] for row in islem.fetchall()]
    return ["All"] + engine_types  # "All" seçeneğini en başa ekle

def get_all_years():
    # Yılları veritabanından küçükten büyüğe sıralı şekilde çek
    islem.execute("SELECT DISTINCT year FROM Cars ORDER BY year ASC")
    years = [row[0] for row in islem.fetchall()]
    print(f"Year: {years}")  # Veritabanından çekilen yılları yazdır
    return ["All"] + years  # "All" seçeneğini en başa ekle

def get_all_fuel_types():
    islem.execute("SELECT DISTINCT fuelType FROM Cars")
    fuel_types = [row[0] for row in islem.fetchall()]
    print(f"Fuel Types: {fuel_types}")  # Veritabanından çekilen yakıt türlerini yazdır
    return ["All"] + fuel_types  # "All" seçeneğini en başa ekle

def get_all_gear_types():
    islem.execute("SELECT DISTINCT gearType FROM Cars")
    gear_types = [row[0] for row in islem.fetchall()]
    print(f"Gear Types: {gear_types}")  # Veritabanından çekilen vites türlerini yazdır
    return ["All"] + gear_types  # "All" seçeneğini en başa ekle

def get_all_warranty_statuses():
    islem.execute("SELECT DISTINCT warrantyStatus FROM Cars")
    warranty_statuses = [row[0] for row in islem.fetchall()]
    print(f"Warranty Statuses: {warranty_statuses}")  # Veritabanından çekilen garanti durumlarını yazdır
    return ["All"] + warranty_statuses  # "All" seçeneğini en başa ekle








def load_data_to_ui():
    # Brand ComboBox
    ui.cmbBrand.addItems(get_all_brands())
    # Model ComboBox
    ui.cmbModel.addItems(get_all_models())
    ui.cmbEngineType.addItems(get_all_engineTypes())
    ui.cmbYear.addItems(get_all_years())

    # Fuel Type ComboBox
    fuel_types = get_all_fuel_types()
    if fuel_types:
        ui.cmbFuelType.addItems(fuel_types)
    else:
        print("No fuel types found in the database.")

    # Gear Type ComboBox
    gear_types = get_all_gear_types()
    if gear_types:
        ui.cmbGearType.addItems(gear_types)
    else:
        print("No gear types found in the database.")

    # Warranty Status ComboBox
    warranty_statuses = get_all_warranty_statuses()
    if warranty_statuses:
        ui.cmbWarranty.addItems(warranty_statuses)
    else:
        print("No warranty statuses found in the database.")

        # Year ComboBox (Yılları veritabanından alıp ekliyoruz)
    years = get_all_years()
    if years:
        ui.cmbYear.clear()  # ComboBox içeriğini temizle
        ui.cmbYear.addItems([str(year) for year in years])  # Yılları ComboBox'a ekle
        ui.cmbYear.setCurrentIndex(0)  # Varsayılan olarak ilk yılı seç
    else:
        print("No years found in the database.")

# UI'yi yükle
load_data_to_ui()

# Veritabanı bağlantısını kapatma


def clear_widgets():
    layout = ui.scrollAreaWidgetContents_2.layout()

    if layout is not None:
        # Layout içerisindeki tüm widget'ları sil
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()
        print("Tüm widget'lar silindi.")


def show_results():
    clear()
    try:
       

        # Veritabanından kayıtları çekiyoruz
        query = "SELECT DISTINCT * FROM cars WHERE 1=1"
        filters = []

        
        # Marka filtresi
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
            filters.append(price_min)
            filters.append(price_max)

        km_min = ui.lneMax_2.text().strip()
        km_max = ui.lneMax.text().strip()
        if km_min and km_max:
            query += " AND  CAST(km AS INTEGER) BETWEEN ? AND ?"
            filters.append(km_min)
            filters.append(km_max)    
        
        
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


def show_all_results():
    try:
        ui.tableWidget.setRowCount(0) 
       
        sorgu = "SELECT * FROM cars"
        islem.execute(sorgu)
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


# Tabloyu Temizleme Fonksiyonu
def clear():
    try:
        ui.tableWidget.setRowCount(0)
        ui.cmbEngineType.setCurrentIndex()
        ui.cmbModel.setCurrentIndex("All")
        ui.cmbBrand.setCurrentIndex("All")
        ui.cmbFuelType.setCurrentIndex("All")
        ui.cmbGearType.setCurrentIndex("All")
        ui.cmbWarranty.setCurrentIndex("All")
        ui.lneMin.clear()
        ui.lneMax.clear()
        ui.statusbar.showMessage("Tablo ve filtreleme tercihleri temizlendi.", 3000)
    except Exception as e:
        print(f"Temizleme sırasında hata oluştu: {str(e)}")



def download_as_csv():
    try:
        # Tablodaki tüm satırları ve hücreleri almak
        row_count = ui.tableWidget.rowCount()  # Tablo widget'ındaki satır sayısı
        col_count = ui.tableWidget.columnCount()  # Tablo widget'ındaki sütun sayısı

        if row_count > 0:
            # Tabloyu veri çerçevesine (DataFrame) dönüştürme
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = ui.tableWidget.item(row, col)  # Tablo hücresine erişim
                    row_data.append(item.text() if item else '')  # Hücre boşsa, boş bir string ekle
                data.append(row_data)

            # DataFrame oluşturma
            df = pd.DataFrame(data, columns=[
                "ID", "Brand", "Model", "Engine Type", "Year",
                "Km", "Fuel Type", "Gear Type", "Warranty Status", "Price"
            ])

            print("Tablodaki görünen veriler (ilk 5 satır):")
            print(df.head())

            # Dosya kaydetmek için dosya yolunu sorma
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(None, "CSV Dosyasını Kaydet", "", "CSV Files (*.csv);;All Files (*)", options=options)

            if file_path:
                # Verileri düzgün şekilde CSV dosyasına kaydetme
                df.to_csv(file_path, index=False, sep=';', encoding='utf-8')  # Noktalı virgül ayraç olarak kullanılabilir

                ui.statusbar.showMessage(f"Veriler başarıyla '{file_path}' dosyasına kaydedildi.", 5000)
            else:
                ui.statusbar.showMessage("Dosya kaydedilmedi.", 5000)
        else:
            ui.statusbar.showMessage("Tabloda görünen veri yok.", 5000)

    except Exception as e:
        ui.statusbar.showMessage(f"Hata: {e}", 5000)


# Buton bağlantıları
ui.btnShowAllResults.clicked.connect(show_all_results)
ui.btnShowResults.clicked.connect(show_results)  # Show Results butonunu show_results fonksiyonuna bağladık
ui.btnClear.clicked.connect(clear)
ui.btnDownload.clicked.connect(download_as_csv)  # Download butonuna bağladık

sys.exit(uygulama.exec_())





