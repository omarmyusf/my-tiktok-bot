import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import yt_dlp

# المعلومات الأساسية
TOKEN = '7629672684:AAH_8Hx7VnshhYf5-8-LhO2n2XpYp2f8' # تأكد من كتابة التوكن كاملاً هنا
CHANNEL_ID = '@cdhfu6'

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except BadRequest:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_sub(update, context):
        await update.message.reply_text("هلا بيك عيوني! ✨\nتم التحقق من اشتراكك. ارسل لي رابط تيك توك الآن.")
    else:
        await update.message.reply_text(f"عذراً عزيزي، يجب عليك الاشتراك في القناة أولاً لاستخدام البوت:\n{CHANNEL_ID}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        await update.message.reply_text(f"يجب الاشتراك بالقناة أولاً: {CHANNEL_ID}")
        return

    url = update.message.text
    if "tiktok.com" in url:
        msg = await update.message.reply_text("جاري تحميل الفيديو، انتظر قليلاً... ⏳")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await update.message.reply_video(video=open('video.mp4', 'rb'))
            await msg.delete()
            os.remove('video.mp4')
        except Exception as e:
            await msg.edit_text(f"حدث خطأ أثناء التحميل: {str(e)}")
    else:
        await update.message.reply_text("أرسل رابط تيك توك صحيح من فضلك.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
                
