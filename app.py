from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
import sqlite3
import os
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)
app.secret_key = "ostim_chatbot_gizli_anahtar" 
DB_NAME = "ostim_chatbot.db"

# --- YENİ NESİL YAPAY ZEKA AYARLARI (google-genai) ---
# Kendi API anahtarını buraya ekle
API_KEY = "AIzaSyDoMRIRlIlJUF308dyv5GIA2T8KRsM_rms"
client = genai.Client(api_key=API_KEY)

# İnternet araması için en stabil ve hızlı model
MODEL_ID = "gemini-2.5-flash" 

# -----------------------------
# ARAYÜZ (HTML) ROTALARI
# -----------------------------
# -----------------------------
# ARAYÜZ (HTML) ROTALARI
# -----------------------------
# -----------------------------
# ARAYÜZ VE GÜVENLİK (LOGIN) ROTALARI
# -----------------------------
# Kendi admin bilgilerini buraya yazabilirsin
ADMIN_KULLANICI = "admin"
ADMIN_SIFRE = "ostim123"

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    # Zaten giriş yapılmışsa direkt admin'e at
    if session.get("logged_in"):
        return redirect("/admin")

    if request.method == "POST":
        # Kullanıcı HTML Form veya Fetch(JSON) ile veri yollamış olabilir, ikisini de yakalayalım
        if request.is_json:
            data = request.get_json()
            kullanici = data.get("username")
            sifre = data.get("password")
            if kullanici == ADMIN_KULLANICI and sifre == ADMIN_SIFRE:
                session["logged_in"] = True
                return jsonify({"success": True, "redirect": "/admin"})
            return jsonify({"success": False, "message": "Hatalı şifre!"}), 401
        
        else:
            kullanici = request.form.get("username")
            sifre = request.form.get("password")
            if kullanici == ADMIN_KULLANICI and sifre == ADMIN_SIFRE:
                session["logged_in"] = True
                return redirect("/admin")
            
            # --- YENİ ŞIK HATA EKRANI ---
            hata_sayfasi = """
            <!DOCTYPE html>
            <html lang="tr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Giriş Başarısız</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                    .error-card { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #dc3545; }
                    h2 { color: #dc3545; margin-bottom: 10px; }
                    p { color: #6c757d; margin-bottom: 25px; }
                    .btn { background-color: #0d6efd; color: white; padding: 10px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: 0.3s; }
                    .btn:hover { background-color: #0b5ed7; }
                </style>
            </head>
            <body>
                <div class="error-card">
                    <h2>⚠️ Giriş Başarısız!</h2>
                    <p>Hatalı kullanıcı adı veya şifre girdiniz.</p>
                    <br>
                    <a href="/login" class="btn">Geri Dön ve Tekrar Dene</a>
                </div>
            </body>
            </html>
            """
            return hata_sayfasi, 401

    # GET isteği gelirse sadece login sayfasını göster
    return send_from_directory(".", "login.html")

@app.route("/admin")
def admin_page():
    # İŞTE KİLİT BURASI: Ziyaretçi kartı (session) yoksa Login sayfasına geri kov!
    if not session.get("logged_in"):
        return redirect("/login")
    
    return send_from_directory(".", "admin.html")

# İsteğe bağlı: Güvenli çıkış yapmak için
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/login")

@app.route("/<path:path>")
def serve_pages(path):
    return send_from_directory(".", path)

# -----------------------------
# Chat Endpoint (Skorlama ve İnternet Zekası)
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_question = data.get("question", "").strip().lower()

    # 1. ADIM: Veritabanını Oku ve Skorlama ile Eşleştir
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT question_text, answer_text FROM questions")
    rows = cursor.fetchall()
    conn.close()

    db_bilgileri = ""
    en_iyi_cevap = None
    en_yuksek_skor = 0

    temiz_user = user_question.replace("-", "").replace(",", "").replace("?", "").lower()
    user_kelimeler = set(temiz_user.split())

    yasakli_kelimeler = {"nasıl", "nedir", "nerede", "hangi", "kimdir", "için", "gibi", "kadar", "olan", "arıza", "arızası", "sorun", "sorunu", "hata", "hatası", "yardım", "ve", "ile", "bir", "çok"}

    for row in rows:
        db_soru = row[0].lower()
        db_cevap = row[1]
        db_bilgileri += f"- Konu: {row[0]} | Cevap: {row[1]}\n"

        if db_soru == user_question.lower():
            en_iyi_cevap = db_cevap
            break

        temiz_db_soru = db_soru.replace("-", "").replace(",", "").replace("?", "")
        db_kelimeler = set(temiz_db_soru.split())

        ortak_kelimeler = (user_kelimeler & db_kelimeler) - yasakli_kelimeler
        skor = len(ortak_kelimeler)

        if skor > en_yuksek_skor:
            if any(len(k) >= 3 for k in ortak_kelimeler):
                en_yuksek_skor = skor
                en_iyi_cevap = db_cevap

    # Mantıklı eşleşme varsa Google'a gitmeden cevapla
    if en_iyi_cevap:
        return jsonify({"answer": en_iyi_cevap})

    # 2. ADIM: Eşleşme yoksa Yapay Zeka'ya sor (İnternet Araması Etkin)
    prompt_text = f"""
    Sen Ostim Teknik Üniversitesi (OTÜ) Bilgi İşlem Departmanına ait resmi bir kampüs asistanısın. Görevin SADECE üniversite öğrencilerine ve personeline kampüs yaşamı, akademik konular, bilgi işlem hizmetleri ve üniversite ile ilgili konularda yardımcı olmaktır.

    KESİN KURALLAR:
    1. KAPSAM DIŞI: Eğer kullanıcının sorusu Ostim Teknik Üniversitesi, eğitim, bilgi işlem departmanı veya kampüs yaşamı ile İLGİLİ DEĞİLSE (Örn: yemek tarifleri, siyaset, spor sonuçları, oyunlar, genel tarih bilgisi vb.), KESİNLİKLE internette arama yapma ve şu cevabı ver: "Üzgünüm, ben bir üniversite asistanıyım. Sadece Ostim Teknik Üniversitesi ve kampüs konuları hakkında bilgi verebilirim."
    
    2. HAVA DURUMU İSTİSNASI: Eğer kullanıcı kampüs veya Ankara ile ilgili hava durumunu soruyorsa (kampüs yaşamını etkilediği için), internette arama yaparak kısa ve net bir hava durumu bilgisi verebilirsin.
    
    3. VERİTABANI ÖNCELİĞİ: Eğer aşağıdaki 'VERİTABANI BİLGİLERİ' kısmında sorunun cevabı varsa, interneti KULLANMADAN sadece o resmi bilgiyi kullan.

    4. BİLİNMEYEN KONU: Eğer soru üniversite ile ilgiliyse ancak cevabı ne veritabanında ne de internette bulamıyorsan SADECE 'BİLMİYORUM' yaz. (Bu kelime sistemde loglanmak için kritiktir).

    VERİTABANI BİLGİLERİ:
    {db_bilgileri}

    Öğrenci Sorusu: {user_question}
    """

    try:
        # Yeni kütüphane yapısı ile istek atıyoruz
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearchRetrieval())]
            )
        )
        
        ai_cevabi = response.text.strip()

        if "BİLMİYORUM" in ai_cevabi.upper():
            with sqlite3.connect(DB_NAME, timeout=10) as conn_write:
                cursor_w = conn_write.cursor()
                cursor_w.execute("INSERT INTO cevapsiz_sorular (soru) VALUES (?)", (user_question,))
                conn_write.commit()
            return jsonify({"answer": "Üzgünüm, bu konuda resmi bir bilgiye veya güncel bir internet kaynağına ulaşamadım. Sorunuzu yetkililere ilettim."})

        return jsonify({"answer": ai_cevabi})

    except Exception as e:
         # Hata detayını terminale yazdıralım ki ne olduğunu görelim
         print(f"API HATASI: {e}")
         if "429" in str(e):
             return jsonify({"answer": "Şu an Google API günlük sorgu limitine ulaştık. Ancak veritabanına eklediğiniz temel sorulara sorunsuz cevap vermeye devam edebilirim!"})
         return jsonify({"answer": f"Bir bağlantı hatası oluştu: {str(e)}"})
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)