from PyQt5 import uic

# .ui dosyasının yolu
ui_file = "SecondHandCar.ui"
# Çıktı olarak oluşturulacak .py dosyasının yolu
py_file = "SecondHandCar.py"

# .ui dosyasını .py dosyasına dönüştür
with open(py_file, "w", encoding="utf-8") as fout:
    uic.compileUi(ui_file, fout)