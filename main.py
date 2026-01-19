import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest
import yt_dlp

# المعلومات الأساسية
TOKEN = '8479972730:AAHgQTs99BAjgf-Lf45yRpS1QP_u10Lkpyw'
CHANNEL_ID = '@cdhfu6'

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_sub(update, context):
        await update.message.reply_text("هلا بيك! أرسل رابط تيك توك واختار الصيغة اللي تعجبك. ✨")
    else:
        await update.message.reply_text(f"عذراً، اشترك بالقناة أولاً:\n{CHANNEL_ID}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        await update.message.reply_text(f"اشترك هنا أولاً: {CHANNEL_ID}")
        return

    url = update.message.text
    if "tiktok.com" in url:
        keyboard = [
            [InlineKeyboardButton("فيديو MP4 🎬", callback_data=f"video|{url}")],
            [InlineKeyboardButton("موسيقى MP3 🎵", callback_data=f"audio|{url}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("اختار نوع التحميل:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("أرسل رابط تيك توك صحيح.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, url = query.data.split("|")
    
    msg = await query.message.edit_text("جاري التحميل... ⏳")
    
    try:
        if action == "video":
            ydl_opts = {'format': 'best', 'outtmpl': 'download.mp4', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await query.message.reply_video(video=open('download.mp4', 'rb'))
            os.remove('download.mp4')
        else:
            ydl_opts = {'format': 'bestaudio', 'outtmpl': 'download.mp3', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await query.message.reply_audio(audio=open('download.mp3', 'rb'))
            os.remove('download.mp3')
        
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"خطأ: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت المطور يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
