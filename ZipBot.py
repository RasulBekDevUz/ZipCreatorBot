import telebot
import zipfile
import os
import time


API_KEY = "5687244773:AAHb7wpCSZN3zDacTfrpHdSDQxeDHntUj-A"

bot = telebot.TeleBot(API_KEY)

global messageVar
foldername ="ziplandi"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Developer', url='https://t.me/RasulDeveloper'))
    markup.add(telebot.types.InlineKeyboardButton(text='Botni gruhga qoshish+', url='https://t.me/ZipCreatorBot?startgroup=true'))

    bot.reply_to(message, "Asalomu aleykum file larni ziplovchi botga hush kelibsiz botdan foydalanish uchun /zip burugini bering ", reply_markup=markup)

@bot.message_handler(commands=['zip'])
def handle_zip(message):
    global messageVar
    messageVar = message
    global folder_name
    folder_name = str(message.from_user.id) + str(int(time.time()))
    os.mkdir(folder_name)
    # Send message asking for file
    msg = bot.send_message(chat_id=message.chat.id, text="File ni menga yuboring !")
    bot.register_next_step_handler(msg, handle_files, folder_name=folder_name)

# Function to handle files sent by user
def handle_files(message, folder_name):
    # Check if the message contains a document
    if message.document:
        print("file detected")
        # Download the file and save it in the folder
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)
        msg = bot.send_message(message.chat.id,"Kutib turing file lar ziplanmoqda")
        with open(os.path.join(folder_name, message.document.file_name), 'wb') as f:
            f.write(file)
        bot.delete_message(chat_id=message.chat.id,message_id=msg.message_id)
            
    elif message.photo:
        print("Photo Detected")
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        print(file_info)
        file = bot.download_file(file_info.file_path)
        with open(os.path.join(folder_name, file_info.file_path.split("/")[-1]), 'wb') as f:
            f.write(file)
    keyboard = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton("File yuklash +", callback_data="yes")
    no_button = telebot.types.InlineKeyboardButton("Zip ni olish", callback_data="no")
    keyboard.add(yes_button, no_button)
    bot.send_message(chat_id=message.chat.id, text="Yana file yuklaysizmi yoki zipni olmoqchimisiz ?", reply_markup=keyboard)
        
        
@bot.callback_query_handler(func=lambda x: True)
def callback_handler(callback_query):
    global folder_name
    global messageVar
    data = callback_query.data
    if data == "yes":
        msg = bot.send_message(chat_id=messageVar.chat.id, text="ziplash uchun file >>> ")
        bot.register_next_step_handler(msg, handle_files, folder_name=folder_name)
        bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    elif data == "no":
        # bot.answer_callback_query(callback_query.id, text="You chose NO.")
        zip_file_name = folder_name + ".zip"
        with zipfile.ZipFile(zip_file_name, 'w') as zip:
            for file in os.listdir(folder_name):
                zip.write(os.path.join(folder_name, file))
        # Send the zip file to user
        with open(zip_file_name, 'rb') as f:
            bot.send_document(chat_id=messageVar.chat.id, document=f)
        # Delete the zip file and folder
        os.remove(zip_file_name)
        for file in os.listdir(folder_name):
            os.remove(os.path.join(folder_name, file))
        os.rmdir(folder_name)  
        bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


print("Bot Ishga tushdi...")
bot.polling()
