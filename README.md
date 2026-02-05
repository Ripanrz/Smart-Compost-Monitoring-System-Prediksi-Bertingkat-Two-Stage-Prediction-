# 🌱 Model Prediksi Bertingkat (Two-Stage Prediction): Estimasi Kadar Amonia & Klasifikasi Status Kematangan Kompos

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Extra Trees](https://img.shields.io/badge/Model-Extra_Trees-green)
![K-Means](https://img.shields.io/badge/Model-K_Means-purple)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange.svg)
![Flask](https://img.shields.io/badge/Deployment-Flask-lightgrey.svg)

Proyek ini mengembangkan sistem **Machine Learning Bertingkat (Cascade System)** untuk memantau kualitas proses pengomposan.  
Pendekatan ini dirancang untuk mengatasi keterbatasan **sensor fisik Ammonia (mg/kg)** yang mahal, dengan memanfaatkan konsep **Virtual Sensor berbasis AI**.

---

## 📸 Tampilan Antarmuka

![Tampilan Dashboard](cascade-compost-classifier/Dashboard_Compost.png)

---

## 🚀 Gambaran Umum Sistem

Sistem bekerja melalui **dua tahap prediksi utama**:

1. **Tahap 1 – Virtual Sensor Ammonia**  
   Memprediksi kadar **Ammonia (mg/kg)** berdasarkan data sensor murah:
   - Suhu
   - Kelembaban / Moisture Content (MC)
   - pH

2. **Tahap 2 – Klasifikasi Kematangan Kompos**  
   Menentukan status kematangan kompos:
   - **Mentah**
   - **Setengah Matang**
   - **Matang**

   dengan menggunakan:
   - Data sensor fisik (Suhu, MC, pH)
   - Hasil prediksi Amonia dari Tahap 1

---

## 🔁 Alur Kerja (Prediction Pipeline)

```mermaid
graph LR
    A[Input Sensor] -->|Suhu, MC, pH| B(Model 1: Estimasi Amonia)
    B -->|Output: Amonia mg/kg| C{Input Gabungan}
    A --> C
    C -->|Suhu, MC, pH, Amonia| D(Model 2: Klasifikasi Kematangan)
    D -->|Output| E[Status: MATANG / SETENGAH MATANG / MENTAH]
