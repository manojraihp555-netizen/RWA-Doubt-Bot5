import json
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
)
from telegram.constants import ChatMemberStatus

TOKEN = 8979623107:AAE3Z6kKIR7MnRFwMsVHAMF_7t_UlFeEhzw

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

DB_FILE = "database.json"


def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


db = load_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 RWA Doubt Bot Online!\n\nUse /rules to view rules."
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        db.get(
            "rules",
            "📚 No rules added yet.\nUse /setrules (Admin only).",
        )
    )


async def setrules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    if member.status not in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]:
        return

    text = update.message.text.replace("/setrules", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setrules Your Rules"
        )
        return

    db["rules"] = text
    save_db(db)

    await update.message.reply_text("✅ Rules Updated.")


async def setwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    if member.status not in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]:
        return

    text = update.message.text.replace("/setwelcome", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setwelcome Your Welcome Message"
        )
        return

    db["welcome"] = text
    save_db(db)

    await update.message.reply_text("✅ Welcome message updated.")


async def setexit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    if member.status not in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]:
        return

    text = update.message.text.replace("/setexit", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setexit Your Exit Message"
        )
        return

    db["exit"] = text
    save_db(db)

    await update.message.reply_text("✅ Exit message updated.")


async def setremove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    if member.status not in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]:
        return

    text = update.message.text.replace("/setremove", "").strip()

    if not text:
        await update.message.reply_text(
            "Usage:\n/setremove Your Remove Message"
        )
        return

    db["remove"] = text
    save_db(db)

    await update.message.reply_text("✅ Remove message updated.")
async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member

    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    user = chat_member.new_chat_member.user
    mention = user.mention_html()

    # Welcome
    if (
        old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]
        and new_status == ChatMemberStatus.MEMBER
    ):
        text = db.get(
            "welcome",
            "🎉 Welcome {name} ❤️\n\nRWA Doubt Group me aapka swagat hai."
        )

        text = text.replace("{name}", mention)

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
        text = db.get(
            "exit",
            "👋 {name} group se exit ho gaye."
        )

        text = text.replace("{name}", mention)

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
        text = db.get(
            "remove",
            "🚫 {name} ko admin ne remove kar diya."
        )

        text = text.replace("{name}", mention)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
           
