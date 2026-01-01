import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import os

app = Flask(__name__)

# ==============================================================================
# 1. SETUP MODEL PATH
# ==============================================================================
MODEL_PATH = r"C:\Users\arpan\Downloads\cascade-compost-classifier\models"

AMMONIA_MODEL_FILE = os.path.join(MODEL_PATH, "Ripan_model_prediksi_ammonia.pkl")
MATURITY_MODEL_FILE = os.path.join(MODEL_PATH, "Ripan_model_maturity_hybrid.pkl")

# Load Models Global
print(f"⏳ Sedang memuat model dari: {MODEL_PATH} ...")

try:
    if not os.path.exists(AMMONIA_MODEL_FILE) or not os.path.exists(MATURITY_MODEL_FILE):
        raise FileNotFoundError("Salah satu file .pkl tidak ditemukan di path tersebut.")

    model_ammonia = joblib.load(AMMONIA_MODEL_FILE)
    model_maturity = joblib.load(MATURITY_MODEL_FILE)
    print("✅ Semua model berhasil dimuat dan Siap!")
except Exception as e:
    print(f"❌ Error Fatal: {e}")
    print(f"   Pastikan file ada di folder: {MODEL_PATH}")
    exit()

# Mapping Label (Sesuai training sebelumnya)
LABEL_MAP = {0: 'MENTAH', 1: 'SETENGAH MATANG', 2: 'MATANG'}

# ==============================================================================
# 2. ROUTES
# ==============================================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Ambil data dari Form HTML
        # Kita gunakan float() agar input angka desimal terbaca aman
        temp = float(request.form['temperature'])
        mc = float(request.form['mc'])
        ph = float(request.form['ph'])

        # ============================================================
        # TAHAP 1: PREDIKSI AMMONIA
        # ============================================================
        # Buat DataFrame dengan nama kolom persis seperti saat training
        input_ammonia = pd.DataFrame([[temp, mc, ph]], 
                                     columns=['Temperature', 'MC(%)', 'pH'])
        
        # Lakukan prediksi (hasilnya array, ambil elemen pertama)
        pred_ammonia_val = model_ammonia.predict(input_ammonia)[0]

        # ============================================================
        # TAHAP 2: PREDIKSI KEMATANGAN (HYBRID)
        # ============================================================
        # Input untuk tahap 2 harus 4 kolom: Temp, MC, pH, dan Ammonia Hasil Prediksi
        input_maturity = pd.DataFrame([[temp, mc, ph, pred_ammonia_val]], 
                                      columns=['Temperature', 'MC(%)', 'pH', 'Ammonia(mg/kg)'])
        
        # Prediksi Status (Output: 0, 1, atau 2)
        pred_status_code = model_maturity.predict(input_maturity)[0]
        
        # Ubah kode angka menjadi Teks (Mentah/Matang)
        pred_status_text = LABEL_MAP.get(pred_status_code, "Unknown")

        # ============================================================
        # TAHAP 3: PERSIAPAN OUTPUT UI
        # ============================================================
        # Tentukan warna badge untuk tampilan Bootstrap
        status_color = "danger" # Default Merah (Mentah)
        
        if pred_status_text == "SETENGAH MATANG":
            status_color = "warning" # Kuning
        elif pred_status_text == "MATANG":
            status_color = "success" # Hijau

        # Kirim variabel ke template HTML
        return render_template('index.html', 
                               prediction_text=f'{pred_status_text}',
                               ammonia_value=f'{pred_ammonia_val:.2f} mg/kg',
                               color_class=status_color,
                               input_temp=temp,
                               input_mc=mc,
                               input_ph=ph,
                               show_result=True)

    except Exception as e:
        # Jika ada error, tampilkan di layar
        return render_template('index.html', error_text=f"Terjadi Kesalahan Sistem: {str(e)}")

if __name__ == "__main__":
    print("🚀 Menjalankan Server Flask...")

    app.run(debug=True)
