import json
import logging
import os
import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
)

# ==========================
# BOT TOKEN
# ==========================

TOKEN = ("8979623107:AAFX2uGlbA6pL4D8K87ca7BU_OCs3a-EirQ")

DB_FILE = "database.json"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ==========================
# DATABASE
# ==========================

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

db = load_db()

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ==========================
# ADMIN CHECK
# ==========================

async def is_admin(update, context):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    )
    # ==========================
# BASIC COMMANDS
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 RWA Doubt Bot Online!\n\nUse /rules to view rules."
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        db.get("rules", "📜 No rules added yet.")
    )

# ==========================
# SET RULES
# ==========================

async def setrules(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return

    text = update.message.text.replace("/setrules", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setrules Your Rules"
        )
        return

    db["rules"] = text
    save_db()

    await update.message.reply_text("✅ Rules Updated.")

# ==========================
# SET WELCOME
# ==========================

async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return

    text = update.message.text.replace("/setwelcome", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setwelcome Your Welcome Message"
        )
        return

    db["welcome"] = text
    save_db()

    await update.message.reply_text("✅ Welcome Message Updated.")

# ==========================
# SET EXIT
# ==========================

async def setexit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return

    text = update.message.text.replace("/setexit", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setexit Your Exit Message"
        )
        return

    db["exit"] = text
    save_db()

    await update.message.reply_text("✅ Exit Message Updated.")

# ==========================
# SET REMOVE
# ==========================

async def setremove(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return

    text = update.message.text.replace("/setremove", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setremove Your Remove Message"
        )
        return

    db["remove"] = text
    save_db()

    await update.message.reply_text("✅ Remove Message Updated.")

# ==========================
# MEMBER UPDATE
# ==========================

async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_member = update.chat_member

    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    user = chat_member.new_chat_member.user
    name = user.mention_html()

    # Welcome
    if (
        old_status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED)
        and new_status == ChatMemberStatus.MEMBER
    ):

        text = db.get("welcome", "🎉 Welcome {name}")
        text = text.replace("{name}", name)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode="HTML",
        )

    # Exit
    elif (
        old_status == ChatMemberStatus.MEMBER
        and new_status == ChatMemberStatus.LEFT
    ):

        text = db.get("exit", "👋 {name} left the group.")
        text = text.replace("{name}", name)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode="HTML",
        )

    # Removed
    elif (
        old_status == ChatMemberStatus.MEMBER
        and new_status == ChatMemberStatus.BANNED
    ):

        text = db.get("remove", "🚫 {name} was removed.")
        text = text.replace("{name}", name)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode="HTML",
        )

# ==========================
# MAIN
# ==========================

def main():

    if not TOKEN:
        raise RuntimeError(
            "TOKEN environment variable is missing."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("setrules", setrules))
    app.add_handler(CommandHandler("setwelcome", setwelcome))
    app.add_handler(CommandHandler("setexit", setexit))
    app.add_handler(CommandHandler("setremove", setremove))

    app.add_handler(
        ChatMemberHandler(
            member_update,
            ChatMemberHandler.CHAT_MEMBER,
        )
    )

    print("🤖 Bot Started...")

    app.run_polling()

if __name__ == "__main__":
    main()
