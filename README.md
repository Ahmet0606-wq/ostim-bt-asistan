# 🎓 OSTİM Teknik Üniversitesi - Akıllı BT Asistanı (AI Chatbot)

Bu proje, OSTİM Teknik Üniversitesi öğrenci ve personeline 7/24 destek sağlamak amacıyla geliştirilmiş, **Google Gemini AI** destekli otonom bir Bilgi İşlem (BT) asistanıdır. Sektörel proje kapsamında geliştirilmiştir ve kurumsal iş yükünü hafifletmeyi hedefler.

🔗 **Canlı Demo:** [Ostim BT Asistanı'nı Deneyin](https://ostim-bt-asistan.onrender.com/)

## 🚀 Projenin Amacı ve Kapsamı
Üniversite kampüsü içerisindeki ağ sorunları (Wi-Fi), donanım destek talepleri, yazıcı kurulumları ve genel e-posta ayarları gibi sıkça sorulan teknik sorulara anında, doğru ve kurumsal bir dille yanıt vermek. 

Sistem "Prompt Engineering" teknikleriyle sınırlandırılmış olup, sadece kampüs ve BT destek konularında yanıt üretmekte, dışarıdan gelen alakasız soruları reddetmektedir.

## 🛠️ Kullanılan Teknolojiler (Tech Stack)
* **Backend:** Python, Flask
* **Yapay Zeka (AI):** Google Gemini API
* **Veritabanı:** SQLite (Loglama ve Dinamik Soru-Cevap Yönetimi)
* **Frontend:** HTML5, CSS3 (Responsive Tasarım)
* **Deployment:** Render.com, Gunicorn

## ✨ Öne Çıkan Özellikler
1. **7/24 Kesintisiz Destek:** Kullanıcıların mesai saatlerinden bağımsız olarak temel BT sorunlarını çözebilmesi.
2. **Güvenli Yönetici (Admin) Paneli:** Session (oturum) yönetimi ile korunan, şifreli bir yönetici paneli.
3. **Dinamik Veritabanı:** Admin paneli üzerinden yapay zekaya anında yeni soru-cevap öğretebilme özelliği.
4. **Loglama Sistemi:** Yapay zekanın cevaplayamadığı veya bilmediği sorular veritabanına kaydedilir, böylece BT ekibi bu talepleri inceleyip sisteme yeni cevaplar ekleyebilir.

## ⚙️ Kurulum (Geliştiriciler İçin)
Bu projeyi kendi bilgisayarınızda (localhost) çalıştırmak isterseniz aşağıdaki adımları izleyebilirsiniz:

1. Depoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/Ahmet0606-wq/ostim-bt-asistan.git](https://github.com/KULLANICI_ADIN/ostim-bt-asistan.git)
2. Gerekli Python kütüphanelerini kurun:
      pip install -r requirements.txt
3.  API Anahtarınızı ortam değişkeni olarak ekleyin (Windows için):
      set GEMINI_API_KEY=sizin_api_anahtariniz
4. Uygulamayı Başlatın:
     python app.py
5. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

## 👨‍💻 Geliştirici
* **Ahmet Buğra Öner** 
* OSTİM Teknik Üniversitesi - Bilgisayar Programcılığı

---
*Not: Bu proje OSTİM Teknik Üniversitesi "GRS 202 Sektörel Proje" dersi kapsamında geliştirilmiştir.*
