"""
/friend command - Add friend
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def friend_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add friend"""
    user_id = update.effective_user.id
    
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Use /start first")
        return
    
    if not context.args:
        await update.message.reply_text(
            "👥 <b>ADD FRIEND</b>\n\nUsage: /friend @username",
            parse_mode="HTML"
        )
        return
    
    target_username = context.args[0].lstrip('@')
    target = db.db.users.find_one({"username": target_username})
    
    if not target:
        await update.message.reply_text("❌ User not found")
        return
    
    if target['user_id'] == user_id:
        await update.message.reply_text("❌ Can't friend yourself!")
        return
    
    if target['user_id'] in user.get('friends', []):
        await update.message.reply_text(f"✅ Already friends")
        return
    
    db.db.users.update_one(
        {"user_id": user_id},
        {"$addToSet": {"friends": target['user_id']}}
    )
    
    await update.message.reply_text(
        f"✅ <b>FRIEND ADDED!</b>\n\n@{target['username']} is now your friend!",
        parse_mode="HTML"
    )

friend_handler = CommandHandler('friend', friend_command)