import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import os

# جلب القيم من متغيرات البيئة في Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

# إعداد OpenAI API
openai.api_key = OPENAI_API_KEY

# دالة للرد على الرسائل باستخدام OpenAI
def chat_with_ai(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # يمكنك استخدام "gpt-3.5-turbo" إذا كنت تستخدم الإصدار المجاني
            messages=[{"role": "user", "content": text}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

# دالة لمعالجة رسائل المستخدمين
def handle_message(update: telegram.Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = chat_with_ai(user_message)
    update.message.reply_text(ai_response)

# تشغيل البوت
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # استقبال الرسائل النصية
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
