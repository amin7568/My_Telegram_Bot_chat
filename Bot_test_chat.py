# ----------------------------------------------------------------------------------------------------------------------------------
from keep_alive import keep_alive
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
# ----------------------------------------------------------------------------------------------------------------------------------
#save data from user
conversations = []
save01 = 0
save02 = 0
chat_id_sender = 0
# ----------------------------------------------------------------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save01 = 0
    save02 = 0
    chat_id_sender = 0
    if update.effective_user.id == 6157614517:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = f"""
    Hi {update.message.chat.first_name or "نداری"} , {update.message.chat.last_name or "نداری" }
    شما ادمین هستید
    """)
    
    if update.effective_user.id != 6157614517:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = f"""
    Hi {update.message.chat.first_name or "نداری"} , {update.message.chat.last_name or "نداری" }
    """)
        username = str(update.message.chat.username)
        conversations.append(username)
        await context.bot.send_message(chat_id = 6157614517, text = f"""New Member:
First Name: {update.message.chat.first_name or 'none'}
Last Name: {update.message.chat.last_name or 'none'}
Username: @{update.message.chat.username or 'none'}
User ID: {update.effective_user.id}
                                       """)
        await context.bot.send_message(text = "از منوی زیر انتخاب کن"   , chat_id=update.effective_chat.id ,  reply_markup = InlineKeyboardMarkup(
            [
                                [InlineKeyboardButton("چت با ادمین", callback_data="number01")],
                                [InlineKeyboardButton("برگشت", callback_data="number02")]
                                ]
            ))
# ----------------------------------------------------------------------------------------------------------------------------------
async def Get_and_Send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global save01 , save02 , chat_id_sender
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if data == "number01":
        await context.bot.editMessageText(text = "پیام خود را وارد کنید:" , chat_id = chat_id, message_id = message_id)
        chat_id_sender = chat_id
        save01 = 1

    if data == "number02":
        await context.bot.delete_message(chat_id = chat_id, message_id = message_id)

    if data == "number03":
        await context.bot.send_message(text = "پاسخ خود را ارسال کنید" , chat_id = 6157614517)
        save02 = 1
# ----------------------------------------------------------------------------------------------------------------------------------
async def omumi1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global save01 , save02 , chat_id_sender 
    if save01 == 1:
        await context.bot.send_message(text = "پیام شما برای ادمین ارسال شد" , chat_id = chat_id_sender)
        await context.bot.send_message(text = f"""کاربر با آیدی زیر پیام فرستاد:
@{update.message.chat.username or 'none'}
{update.effective_message.text}
"""
                                        , chat_id = 6157614517 , 
                                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("پاسخ خود را بفرستید", callback_data="number03")]])
                                        )
        save01 = 0
        
    if save02 == 1:
        chat_id = chat_id_sender
        await context.bot.send_message(text =f"""پاسخ ادمین:
                                       {update.message.text}
                                       """ , chat_id = chat_id
                                       )
        save02 = 0
# ----------------------------------------------------------------------------------------------------------------------------------
async def members_List(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in conversations:
        await context.bot.send_message(chat_id = 6157614517, text = f"""اعضای بات:
@{member}
                                       """)
# ----------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
        
    application = ApplicationBuilder().token("7887522959:AAE4Y7E0dAJIuW74mM9YgY8_HSiOvuAkSjo").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('information', members_List))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND& (~filters.COMMAND)), omumi1))
    application.add_handler(CallbackQueryHandler(Get_and_Send))
    keep_alive()
    application.run_polling(allowed_updates = Update.ALL_TYPES)

