import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# الحصول على API key من المتغيرات البيئية
remove_bg_api_key = os.getenv('REMOVE_BG_API_KEY')
bot_token = os.getenv('BOT_API_TOKEN')

# دالة لحذف الخلفية باستخدام API من remove.bg
def remove_background(image_url):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_url},
        headers={'X-Api-Key': remove_bg_api_key}
    )
    if response.status_code == 200:
        return response.content
    else:
        return None

# دالة للتعامل مع الصور في التليجرام
async def handle_photo(update: Update, context):
    # الحصول على الصورة من الرسالة
    photo_file = update.message.photo[-1].get_file()
    photo_url = photo_file.file_url
    
    # إزالة الخلفية
    image_data = remove_background(photo_url)
    
    if image_data:
        # إرسال الصورة بدون خلفية
        await update.message.reply_photo(photo=image_data)
    else:
        await update.message.reply_text("حدث خطأ أثناء إزالة الخلفية.")

# دالة لتحديث البوت
async def start(update: Update, context):
    await update.message.reply_text("مرحباً! أرسل لي صورة لأقوم بإزالة الخلفية عنها.")

async def main():
    # إعداد البوت باستخدام التوكن الذي تم تخزينه في المتغيرات البيئية
    application = Application.builder().token(bot_token).build()
    
    # إضافة المعالجين
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # بدء البوت
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
