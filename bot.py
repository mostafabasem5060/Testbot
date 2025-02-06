from flask import Flask, request
import telegram
import requests
import os

TOKEN = "7966771708:AAFziMRBD5NzB1nde6pP4yhjUrbVDo5gPE8"
WEBHOOK_URL = f"https://your-app-name.onrender.com/{TOKEN}"  # سيتم استبدال your-app-name لاحقًا
URL = "https://elmanasa.edurs.net/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/847.96 (KHTML, like Gecko) Chrome/156.4.6478.78 Mobile Safari/637.76"
}

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    """ معالجة الرسائل الواردة من تيليجرام """
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message and update.message.text == "/start":
        page_content = fetch_website()
        update.message.reply_text(page_content)

    return "ok", 200

@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    """ تعيين Webhook للبوت """
    webhook_set = bot.setWebhook(WEBHOOK_URL)
    if webhook_set:
        return "Webhook set successfully!", 200
    return "Failed to set webhook", 400

def fetch_website():
    """ جلب محتوى الموقع """
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        return response.text[:4000]  # إرسال أول 4000 حرف فقط
    except requests.exceptions.RequestException as e:
        return f"حدث خطأ أثناء جلب الصفحة: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
