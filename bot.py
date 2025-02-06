import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
def handle_photo(update, context):
    # الحصول على الصورة من الرسالة
    photo_file = update.message.photo[-1].get_file()
    photo_url = photo_file.file_url
    
    # إزالة الخلفية
    image_data = remove_background(photo_url)
    
    if image_data:
        # إرسال الصورة بدون خلفية
        update.message.reply_photo(photo=image_data)
    else:
        update.message.reply_text("حدث خطأ أثناء إزالة الخلفية.")

# دالة لتحديث البوت
def start(update, context):
    update.message.reply_text("مرحباً! أرسل لي صورة لأقوم بإزالة الخلفية عنها.")

def main():
    # إعداد البوت باستخدام التوكن الذي تم تخزينه في المتغيرات البيئية
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    
    # إضافة المعالجين
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    
    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
