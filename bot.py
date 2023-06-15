from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import mysql.connector
from PIL import Image
import io
import base64
import tempfile

token = "***" # this is where telegram token goes

# Function for the /start command
def start(update, context):
    hellotext = "Привет! Я твой поставщик фотографий животных в одёжке :) Нажми кнопку, чтобы получить серотонин."
    my_keyboard = ReplyKeyboardMarkup([['Хочу серотонина']], resize_keyboard=True)
    update.message.reply_text(hellotext, reply_markup=my_keyboard)

# Function for errors from the dispatcher
def error(update, context):
    errortext = "Кажется, произошла какая-то ошибка :( Наши выдры-программисты обязательно с ней разберутся"
    update.message.reply_text(errortext)

# Function for sending image
def serotonin(update, context):
    # Establishing MySQL connection
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

    def convertTuple(tup):
        justbytes = b''.join(tup)
        return justbytes

    justbytes = convertTuple(tuple_record[0])

    base64_str = base64.b64encode(justbytes).decode('utf-8')

    imgdata = base64.b64decode(base64_str)
    petPic = Image.open(io.BytesIO(imgdata))

    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
        petPic.save(temp_file.name)
        temp_file.seek(0)  # Reset the file pointer to the beginning

        # Send the image to the user
        context.bot.send_photo(chat_id=update.message.chat_id, photo=temp_file)

    cursor.close()
    conn.close()

# Function for answering to everything that is unplanned
def unknown(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Пока я умею только делиться фотографиями, поболтать лучше с Алисой.")

updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.regex('Хочу серотонина'), serotonin))
dispatcher.add_handler(MessageHandler(Filters.text, unknown))

updater.start_polling()


