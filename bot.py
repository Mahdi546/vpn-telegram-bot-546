import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# -------------------------
# تنظیمات
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_KEY = "b7a92b4cd1a2ced29e06059c61f624be"
API_URL = "https://vpn-telegram.com/api/v1/key-activate/free-key"

# -------------------------
# هندلر /start
# -------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "برای دریافت کانفیگ VPN دستور زیر رو بزن:\n"
        "/vpn"
    )

# -------------------------
# هندلر /vpn
# -------------------------


async def vpn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        response = requests.post(
            API_URL,
            json={"public_key": PUBLIC_KEY, "user_tg_id": user_id},
            timeout=15
        )

        data = response.json()
        if not data.get("result"):
            await update.message.reply_text("❌ خطا در دریافت VPN، بعداً امتحان کن")
            return

        vpn_data = data["data"]
        config_url = vpn_data["config_url"]
        traffic_gb = vpn_data["traffic_limit_gb"]

        text = (
            "✅ VPN شما آماده است\n\n"
            "🔗 لینک کانفیگ (کپی کن):\n"
            f"`{config_url}`\n\n"
            f"📦 حجم: {traffic_gb} GB"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception:
        await update.message.reply_text("⚠️ خطای سرور، بعداً دوباره امتحان کن")


# -------------------------
# اجرای بات
# -------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vpn", vpn))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

