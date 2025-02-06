import requests
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# إعداد التوكنات
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # ضع توكن بوت تيليجرام هنا
DEEPSEEK_API_KEY = "sk-f16232f7e219486a927e242e475abd5b"  # ضع مفتاح DeepSeek API هنا

# دالة للرد على الرسائل باستخدام DeepSeek API
def chat_with_deepseek(text):
    url = "https://api.deepseek.com/v1/completions"  # URL الأساسي لـ DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": text,
        "max_tokens": 150,
        "temperature": 0.7,  # درجة الحرارة (اختياري)
        "top_p": 1,  # اختياري
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # للتحقق من الأخطاء في الاستجابة
        result = response.json()  # الحصول على نتيجة الاستجابة
        return result['choices'][0]['text'].strip()  # إعادة النص من الاستجابة
    except Exception as e:
        return f"❌ حدث خطأ أثناء الاتصال بـ DeepSeek: {str(e)}"

# دالة لمعالجة رسائل المستخدمين
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = chat_with_deepseek(user_message)
    await update.message.reply_text(ai_response)

# تشغيل البوت
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # استقبال الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
