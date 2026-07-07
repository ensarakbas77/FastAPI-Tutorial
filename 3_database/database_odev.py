"""
Database Ödevi

Bu ödevde küçük bir şirket çalışan kayıt sistemi geliştireceğiz.
Amaç, SQLite veritabanı ile FastAPI yapısını birlikte kullanarak çalışan ekleme ve çalışan listeleme işlemlerini gerçekleştirmektir.
Bu dosyada tablo oluşturma, çalışan ekleme ve çalışan listeleme işlemlerini fonksiyonlar halinde yazacağız.
Daha sonra bu fonksiyonları FastAPI endpointleri ile kullanacağız.
Test işlemlerini Swagger arayüzü üzerinden yapacağız.

Talimatlar:
1. sqlite3 kullanarak sirket.db adında bir veritabanı bağlantısı oluşturun
2. calisanlar adında bir tablo oluşturun
3. Bu tabloda id, isim, bolum ve yas alanları bulunsun
4. veritabani_baglantisi_olustur() adında bir fonksiyon yazın
5. tablo_olustur() adında bir fonksiyon yazın
6. calisan_ekle() adında bir fonksiyon yazın
7. tum_calisanlari_getir() adında bir fonksiyon yazın
8. CalisanModel adında bir Pydantic model tanımlayın
9. /calisan-ekle adında bir POST endpoint yazın
10. /calisanlar adında bir GET endpoint yazın
11. Uygulamayı çalıştırın ve Swagger üzerinden test edin

Swagger ile test:
- Uygulamayı şu komutla çalıştırın: uvicorn main:app --reload
- Tarayıcıdan şu adrese gidin: http://127.0.0.1:8000/docs
- Önce /calisan-ekle endpointi ile yeni çalışan ekleyin
- Sonra /calisanlar endpointi ile tüm çalışanları listeleyin
"""

import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 8. CalisanModel adında bir Pydantic model tanımlayın
class EmployeeModel(BaseModel):
    name: str
    department: str
    age: int

# 1. sqlite3 kullanarak sirket.db adında bir veritabanı bağlantısı oluşturun
# 4. veritabani_baglantisi_olustur() adında bir fonksiyon yazın
def database_connection():
    return sqlite3.connect("company.db")

# 2. calisanlar adında bir tablo oluşturun
# 3. Bu tabloda id, isim, bolum ve yas alanları bulunsun
# 5. tablo_olustur() adında bir fonksiyon yazın
def create_table():
    conn = database_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """
    ) 

    conn.commit()
    conn.close()

# 6. calisan_ekle() adında bir fonksiyon yazın
def add_employee(name: str, department: str, age: int):
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO employees (name, department, age)
            VALUES (?, ?, ?)
        """, (name, department, age)
    )

    conn.commit()
    conn.close()

# 7. tum_calisanlari_getir() adında bir fonksiyon yazın
def get_all_employee():
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT * FROM employees
        """
    )
    records = cursor.fetchall()
    conn.close()
    return records


# EKSTRA ÖZELLİKLER: update ve delete 
def update_employee(id: int, name: str, department: str, age: int):
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE employees SET name = ?, department = ?, age = ? 
            WHERE id = ?
        """, (name, department, age, id)
    )
    conn.commit()
    conn.close()


def delete_employee(id):
    conn = database_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM employees WHERE id = ?
        """, (id,)
    )
    conn.commit()
    conn.close()


# 9. /calisan-ekle adında bir POST endpoint yazın
@app.post("/add-employee")
def add_employee_endpoint(data: EmployeeModel):

    add_employee(data.name, data.department, data.age)

    return {
        "status": "Successful",
        "message": "Record added to the database",
        "data": {
            "name": data.name,
            "department": data.department,
            "age": data.age
        }
    }


# 10. /calisanlar adında bir GET endpoint yazın
@app.get("/employees")
def get_all_employee_endpoint():

    records = get_all_employee()

    results = []
    for record in records:
        results.append({
            "id": record[0],
            "name": record[1],
            "department": record[2],
            "age": record[3] 
    })

    return {
        "status": "Successful",
        "total_record_number": len(results),
        "data": results
    }


# update /put endpointi
@app.put("/update-employee/{id}")
def update_employee_endpoint(id: int, data: EmployeeModel):

    update_employee(id, data.name, data.department, data.age)

    return {
        "status": "Successful",
        "message": "Employee record updated"
    }

# delete /delete endpointi
@app.delete("/delete-employee/{id}")
def delete_employee_endpoint(id: int):

    delete_employee(id)

    return {
        "status": "Successful",
        "message": "Employee record deleted"
    }


# Uygulama açıldığında tabloyu hazırlıyoruz
create_table()

# 11. Uygulamayı çalıştırın ve Swagger üzerinden test edin
# uvicorn database_odev:app --reload --port 8000
