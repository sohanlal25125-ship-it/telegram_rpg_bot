"""
/factoryboard command - Factory leaderboard
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def factoryboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View factory leaderboard"""
    user_id = update.effective_user.id
    
    # Get top factories by production
    factories = list(db.db.factory.find()
        .sort("production", -1)
        .limit(10))
    
    if not factories:
        await update.message.reply_text("❌ No factories yet")
        return
    
    board_text = "<b>🏭 FACTORY LEADERBOARD</b>\n\n"
    
    for idx, factory in enumerate(factories, 1):
        owner = db.get_user(factory['user_id'])
        if owner:
            board_text += f"{idx}. @{owner['username']}\n"
            board_text += f"   Level: {factory.get('level', 1)}\n"
            board_text += f"   Production: {factory.get('production', 0)} units\n"
            board_text += f"   Workers: {factory.get('workers', 0)}\n"
            board_text += f"   Revenue: {factory.get('money_generated', 0):,} 💰\n\n"
    
    await update.message.reply_text(board_text, parse_mode="HTML")
    logger.info(f"Factory board viewed by {user_id}")

factoryboard_handler = CommandHandler('factoryboard', factoryboard_command)