"""
/familyboard command - Family leaderboard
"""
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from database import db
import logging

logger = logging.getLogger(__name__)

async def familyboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Family leaderboard"""
    user_id = update.effective_user.id
    
    # Get families by size
    families = []
    for family in db.db.families.find():
        family_size = (
            len(family.get('children', [])) +
            len(family.get('parents', [])) +
            len(family.get('grandchildren', [])) +
            len(family.get('siblings', [])) +
            (1 if family.get('partner') else 0) + 1
        )
        families.append({
            'user_id': family['user_id'],
            'size': family_size
        })
    
    # Sort by size
    families.sort(key=lambda x: x['size'], reverse=True)
    
    board_text = "<b>👨‍👩‍👧‍👦 FAMILY LEADERBOARD</b>\n\n"
    
    for idx, fam in enumerate(families[:10], 1):
        user = db.get_user(fam['user_id'])
        if user:
            board_text += f"{idx}. @{user['username']} - {fam['size']} members\n"
    
    await update.message.reply_text(board_text, parse_mode="HTML")
    logger.info(f"Family board viewed by {user_id}")

familyboard_handler = CommandHandler('familyboard', familyboard_command)