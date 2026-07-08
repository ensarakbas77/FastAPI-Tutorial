"""
Veri Analiz Servisi Projesi

Proje tanıtımı:
    - bir csv dosyası okuyabilen
    - temel analizler yapabilen
    - sonuçları veritabanına kaydeden
    - geçmiş analiz kayıtlarını listeleyebilen
bir veri analiz servisi geliştirme.

Proje senaryosu:
    - kullanıcı csv dosyası yükler
    - sistem csv (veri) dosyası okur, temel analizler yapar ve sonuçları kaydeder
    - sonrasında kullanıcı geçmiş analizleri listeleyebilecek ve isterse tek bir analiz kaydının detayını görebilecek

Plan/Program:
    1. gerekli kütüphanelerin içeriye aktarılması
    2. logging altyapısının kurulması
    3. fastapi app oluşturma
    4. veritabanı altyapısı hazırlama
    5. veri analizi yapan yardımcı fonksiyonların ve db işlemleri yapan fonksiyonların tanımlanması
    6. csv yükleme endpointinin yazılması
    7. analiz geçmişi listeleyen endpoint yazılması
    8. tekil analizi listeleyen endpoint yazılması
    9. request ile client testi yapmak
    10. tüm sistem testi
"""

# 1. gerekli kütüphanelerin içeriye aktarılması
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime
from io import BytesIO

# 2. logging altyapısının kurulması
logging.basicConfig(
    filename='analysis_service.log',
    level=logging.INFO,
    format='%(levelname)s | %(asctime)s | %(message)s',
    encoding='utf-8'
)

# 3. fastapi app oluşturma
app = FastAPI(
    title="Veri Analiz Servisi",
)

# 4. veritabanı altyapısı hazırlama
def init_db():
    conn = sqlite3.connect('analysis_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            column_count INTEGER NOT NULL,
            column_names TEXT NOT NULL,
            numeric_column_count INTEGER NOT NULL,
            missing_values INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# 5. veri analizi yapan yardımcı fonksiyonların ve db işlemleri yapan fonksiyonların tanımlanması
def analyze_csv_file(file_bytes: bytes, filename: str) -> dict:
    
    try:
        dataframe = pd.read_csv(BytesIO(file_bytes))

        # temel analiz bilgileri
        row_count = len(dataframe)
        column_count = len(dataframe.columns)
        column_names = list(dataframe.columns)
        numeric_column_count = len(dataframe.select_dtypes(include=['number']).columns)
        missing_values = int(dataframe.isnull().sum().sum())

        return {
            "filename": filename,
            "row_count": row_count,
            "column_count": column_count,
            "column_names": column_names,
            "numeric_column_count": numeric_column_count,
            "missing_values": missing_values,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logging.error(f"CSV analiz edilirken bir hata oluştu: {e}")
        raise HTTPException(status_code=400, detail="CSV dosyası analiz edilemedi. Lütfen geçerli bir CSV dosyası yükleyin.")


# analizi db ye kaydet
def save_analysis_result(analysis_result: dict) -> int:
    try:
        conn = sqlite3.connect('analysis_results.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analysis_history (filename, row_count, column_count, column_names, numeric_column_count, missing_values, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_result["filename"],
            analysis_result["row_count"],
            analysis_result["column_count"],
            json.dumps(analysis_result["column_names"], ensure_ascii=False),
            analysis_result["numeric_column_count"],
            analysis_result["missing_values"],
            analysis_result["created_at"]
        ))
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close() 

        return analysis_id
    except Exception as e:
        logging.error(f"Analiz sonucu veritabanına kaydedilirken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="Analiz sonucu veritabanına kaydedilemedi.")


# tüm analiz sonuçlarını db den al
def get_all_analysis_history():
    try:
        conn = sqlite3.connect('analysis_results.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, filename, row_count, column_count, created_at FROM analysis_history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()

        analysis_history = []
        for row in rows:
            analysis_history.append({
                "id": row[0],
                "filename": row[1],
                "row_count": row[2],
                "column_count": row[3],
                "created_at": row[4]
            })

        return analysis_history
    except Exception as e:
        logging.error(f"Analiz geçmişi veritabanından alınırken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="Analiz geçmişi veritabanından alınamadı.")

# 1 tane analiz sonucunu db den al
def get_analysis_by_id(analysis_id: int):
    try:
        conn = sqlite3.connect('analysis_results.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM analysis_history WHERE id = ?', (analysis_id,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            logging.error(f"Analiz kaydı bulunamadı: ID {analysis_id}")
            raise HTTPException(status_code=404, detail="Analiz kaydı bulunamadı.")

        return {
            "id": row[0],
            "filename": row[1],
            "row_count": row[2],
            "column_count": row[3],
            "column_names": json.loads(row[4]),
            "numeric_column_count": row[5],
            "missing_values": row[6],
            "created_at": row[7]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Analiz kaydı veritabanından alınırken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="Analiz kaydı veritabanından alınamadı.")
    
# 6. csv yükleme endpointinin yazılması
# dosyayı alır, kontrol eder, veri analizini çalıştırır ve sonucu db ye kaydeder
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):

    logging.info(f"/upload_csv/ endpointi çağrıldı: filename = {file.filename}")

    # dosya uzantısı kontrolü
    if not file.filename.endswith('.csv'):
        logging.error(f"Geçersiz dosya uzantısı: {file.filename}")
        raise HTTPException(status_code=400, detail="Geçersiz dosya uzantısı. Lütfen bir CSV dosyası yükleyin.")
    
    try:
        # dosyasını içeriğini oku
        file_bytes = await file.read()

        # boş dosya kontrolü
        if not file_bytes:
            logging.error(f"Boş dosya yüklendi: {file.filename}")
            raise HTTPException(status_code=400, detail="Boş dosya yüklendi. Lütfen geçerli bir CSV dosyası yükleyin.")
        
        # veri analizi yapalım
        analysis_result = analyze_csv_file(file_bytes, file.filename)

        # analiz sonucunu db ye kaydet
        analysis_id = save_analysis_result(analysis_result)

        logging.info(f"CSV dosyası başarıyla yüklendi ve analiz edildi: filename = {file.filename}, analysis_id = {analysis_id}")

        return {"message": "CSV dosyası başarıyla yüklendi ve analiz edildi.", "analysis_id": analysis_id}

    except Exception as e:
        logging.error(f"CSV dosyası işlenirken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="CSV dosyası işlenirken bir hata oluştu.")

# 7. analiz geçmişi listeleyen endpoint yazılması
@app.get("/analysis-history/")
async def list_analysis_history():
    logging.info("/analysis-history/ endpointi çağrıldı.")
    try:
        analysis_history = get_all_analysis_history()

        logging.info(f"Toplam kayıt sayısı: {len(analysis_history)}")

        return {"analysis_history": analysis_history}
    except Exception as e:
        logging.error(f"Analiz geçmişi alınırken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="Analiz geçmişi alınırken bir hata oluştu.")

# 8. tekil analizi listeleyen endpoint yazılması
@app.get("/analysis/{analysis_id}/")
async def get_analysis(analysis_id: int):
    logging.info(f"/analysis/{analysis_id}/ endpointi çağrıldı.")
    try:
        analysis_detail = get_analysis_by_id(analysis_id)

        logging.info(f"Analiz kaydı bulundu: ID = {analysis_id}")

        return {"analysis_detail": analysis_detail}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Analiz kaydı alınırken bir hata oluştu: {e}")
        raise HTTPException(status_code=500, detail="Analiz kaydı alınırken bir hata oluştu.")