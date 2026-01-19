import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import yt_dlp

# المعلومات الأساسية
TOKEN = '7629672684:AAH_8H3XyvI8CofU4r2zI_M-fJmC9E_Rj8A'
CHANNEL_ID = '@cdhfu6'  # معرف قناتك للاشتراك الإجباري

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except BadRequest:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_sub(update, context):
        await update.message.reply_text("أهلاً بك! أرسل رابط تيك توك وسأحمله لك بدون علامة مائية.")
    else:
        await update.message.reply_text(f"عذراً! يجب عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه:\n{CHANNEL_ID}")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        await update.message.reply_text(f"توقف! يجب أن تشترك في القناة أولاً:\n{CHANNEL_ID}")
        return

    url = update.message.text
    if "tiktok.com" in url:
        msg = await update.message.reply_text("جاري التحميل بدون علامة مائية... ⏳")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await update.message.reply_video(video=open('video.mp4', 'rb'), caption="تم التحميل بواسطة بوت عمر ✅")
            await msg.delete()
            os.remove('video.mp4')
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ: {e}")
    else:
        await update.message.reply_text("يرجى إرسال رابط تيك توك صحيح.")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    app.run_polling()
