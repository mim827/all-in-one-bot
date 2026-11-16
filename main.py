import os, asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = "@virallink72882"

async def is_joined(user_id, context):
    try:
        m = await context.bot.get_chat_member(CHANNEL, user_id)
        return m.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_joined(user.id, context):
        await update.message.reply_text(f"👋 হ্যালো {user.first_name}!\n\n✅ তুমি চ্যানেলে Join আছো। এখন বট ব্যবহার করতে পারবা।")
    else:
        await update.message.reply_text(f"⚠️ প্রথমে আমাদের চ্যানেলে Join করো!\n\n👉 https://t.me/virallink72882\n\nJoin করে আবার /start দাও।")

async def delete_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text: return
    if msg.chat.type == "private": return

    # Admin দের লিংক ডিলিট হবে না
    try:
        member = await context.bot.get_chat_member(msg.chat.id, msg.from_user.id)
        if member.status in ["administrator", "creator"]:
            return
    except: pass

    text = msg.text.lower()
    if any(x in text for x in ["http://", "https://", "t.me/", "telegram.me/", "www.", ".com", ".xyz", ".top", ".in"]):
        try:
            await msg.delete()
            w = await context.bot.send_message(msg.chat.id, f"⚠️ @{msg.from_user.username or msg.from_user.first_name}, গ্রুপে লিংক দেওয়া নিষেধ!")
            await asyncio.sleep(5)
            await w.delete()
        except: pass

if __name__ == "__main__":
    from flask import Flask
    import threading
    app = Flask(__name__)
    @app.route('/')
    def home(): return "Bot is Live!"
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()

    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_link))
    app_bot.run_polling()
