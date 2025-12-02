from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ✅ BotFather token
TOKEN = "8184216330:AAFhsKUM-gLE_G-E7imWqaXrVXQjVGOgnrY"

# ✅ Your channel username
CHANNEL_USERNAME = "@edustashofficial"

# Subjects for each class
subjects = {
    "9": ["Math", "Science", "Language", "Sst", "English"], 
    "10": ["Math", "Science", "Language", "Sst", "English"],
    "11": ["Math", "Physics", "Chemistry", "Biology", "English", "Physical Education", "Fine arts", "IT", "CSE"], 
    "12": ["Math", "Physics", "Chemistry", "Biology", "Physical Education", "Fine arts", "IT", "CSE", "English"],
}

# Dummy links for Notes and PDFs (replace with actual links)
notes_links = {sub: f"{sub} Notes Link" for cls in subjects.values() for sub in cls}
pdf_links = {sub: f"{sub} PDF Link" for cls in subjects.values() for sub in cls}

# Check if user is a member of the channel
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except:
        return False

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_member = await check_membership(update, context)
    if not is_member:
        await update.message.reply_text(
            f"❌ You must join our channel to use this bot:\n{CHANNEL_USERNAME}"
        )
        return

    # ✅ Welcome message
    await update.message.reply_text(
        f"🎉 Welcome {update.effective_user.first_name}! You are now verified as a member of {CHANNEL_USERNAME}.\n"
        "You can now access all classes, subjects, Notes, and PYQs."
    )

    # Class buttons
    keyboard = [[InlineKeyboardButton(f"Class {i}", callback_data=f"class_{i}")] for i in ["9","10","11","12"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Select your class to get Notes and PYQs:",
        reply_markup=reply_markup
    )

# Handle inline button clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Class selection → subjects
    if data.startswith("class_"):
        class_number = data.split("_")[1]
        keyboard = [[InlineKeyboardButton(sub, callback_data=f"subject_{sub}_{class_number}")] for sub in subjects[class_number]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Select subject for Class {class_number}:",
            reply_markup=reply_markup
        )

    # Subject selection → type (Notes/PDF)
    elif data.startswith("subject_"):
        parts = data.split("_")
        subject_name = parts[1]
        class_number = parts[2]

        keyboard = [
            [InlineKeyboardButton("📓 Notes", callback_data=f"type_notes_{subject_name}_{class_number}")],
            [InlineKeyboardButton("📄 PYQs / PDF", callback_data=f"type_pdf_{subject_name}_{class_number}")],
            [InlineKeyboardButton("🔙 Back to Subjects", callback_data=f"class_{class_number}")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Select type for {subject_name} Class {class_number}:",
            reply_markup=reply_markup
        )

    # Type selection → send link
    elif data.startswith("type_"):
        parts = data.split("_")
        content_type = parts[1]  # notes or pdf
        subject_name = parts[2]
        class_number = parts[3]

        if content_type == "notes":
            link = notes_links.get(subject_name, "Link not found")
            text = f"📓 Notes for {subject_name} Class {class_number}:\n{link}"
        elif content_type == "pdf":
            link = pdf_links.get(subject_name, "Link not found")
            text = f"📄 PYQs / PDF for {subject_name} Class {class_number}:\n{link}"

        # Buttons after showing Notes/PDF
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Subjects", callback_data=f"class_{class_number}")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )

    # Main menu
    elif data == "main_menu":
        keyboard = [[InlineKeyboardButton(f"Class {i}", callback_data=f"class_{i}")] for i in ["9","10","11","12"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="Select your class to get Notes and PYQs:",
            reply_markup=reply_markup
        )

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


