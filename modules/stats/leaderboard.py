"""
/leaderboard command - View leaderboards
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View top players"""
    users = db.get_leaderboard('level', 10)
    
    lb_text = "<b>🏆 TOP 10 PLAYERS</b>\n\n"
    for idx, user in enumerate(users, 1):
        lb_text += f"{idx}. @{user['username']} - Level {user['level']}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("💰 Money", callback_data="lb_money"),
            InlineKeyboardButton("⭐ Level", callback_data="lb_level"),
        ],
        [
            InlineKeyboardButton("👨‍👩‍👧‍👦 Family", callback_data="lb_family"),
            InlineKeyboardButton("🏭 Factory", callback_data="lb_factory"),
        ],
    ]
    
    await update.message.reply_text(
        lb_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    logger.info(f"Leaderboard viewed by {update.effective_user.id}")

async def moneyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View richest players"""
    users = db.get_leaderboard('money', 10)
    
    lb_text = "<b>💰 RICHEST PLAYERS</b>\n\n"
    for idx, user in enumerate(users, 1):
        lb_text += f"{idx}. @{user['username']} - {user['money']:,} 💰\n"
    
    await update.message.reply_text(lb_text, parse_mode="HTML")

leaderboard_handler = CommandHandler('leaderboard', leaderboard_command)
moneyboard_handler = CommandHandler('moneyboard', moneyboard_command)