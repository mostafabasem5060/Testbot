import openai
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# إعداد التوكنات
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # ضع توكن بوت تيليجرام هنا
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ضع مفتاح OpenAI API هنا

# إعداد OpenAI API
openai.api_key = OPENAI_API_KEY

# دالة للرد على الرسائل باستخدام OpenAI
def chat_with_ai(text):
    try:
        # استخدام واجهة completions الجديدة في OpenAI
        response = openai.completions.create(
            model="gpt-4",  # يمكنك استخدام "gpt-3.5-turbo" إذا كنت تستخدم الإصدار المجاني
            prompt=text,
            max_tokens=150
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}"

# دالة لمعالجة رسائل المستخدمين
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    ai_response = chat_with_ai(user_message)
    await update.message.reply_text(ai_response)

# تشغيل البوت
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # استقبال الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
