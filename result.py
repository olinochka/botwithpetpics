from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import ReplyKeyboardMarkup
import mysql.connector
from PIL import Image
import io
import base64

token = "***" # this is where telegram token goes

# function for the /start command
def start(update, context):
    hellotext = "Привет! Я твой поставщик фотографий животных в одёжке :) Нажми кнопку, чтобы получить серотонин."
    my_keyboard = ReplyKeyboardMarkup([['Хочу серотонина']], resize_keyboard = True)
    update.message.reply_text(hellotext, reply_markup = my_keyboard)

# function for errors from the dispatcher
def error(update, context):
    errortext = "Кажется, произошла какая-то ошибка :( Наши выдры-программисты обязательно с ней разберутся"
    update.message.reply_text(errortext)

# function for sending image
def serotonin(update, context):
    # establishing mysql connection
    conn = mysql.connector.connect(
    host="***",
    port='3306',
    user="***",
    password="***",
    database ="***"
    )
    
    query = ("SELECT pic FROM pets ORDER BY RAND() LIMIT 1")

    cursor = conn.cursor(buffered=True)
    cursor.execute(query)
    tuple_record = cursor.fetchall()

    # print(tuple_record)
    # print(tuple_record[0])
    # print(type(tuple_record[0]))
    # print(type(tuple_record))

    def convertTuple(tup):
        justbytes = b''.join(tup)
        return justbytes

    justbytes = convertTuple(tuple_record[0])
    base64_str = base64.b64encode(justbytes).decode('utf-8')
    imgdata = base64.b64decode(str(base64_str))
    petPic = Image.open(io.BytesIO(imgdata))
    petPic.save('/home/olina/projects/forBot/test.jpeg')
    updater.bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/olina/projects/forBot/test.jpeg', 'rb'))

    cursor.close()
    conn.close()

# function for answering to everything that is unplanned
def unknown(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Пока я умею только делиться фотографиями, поболтать лучше с Алисой.")

updater = None
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.regex('Хочу серотонина'), serotonin))
dispatcher.add_handler(MessageHandler(Filters.text, unknown))

updater.start_polling()


