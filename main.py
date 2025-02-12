import telebot
from telebot import types
import sqlite3
from config import BOT_TOKEN, WELCOME_MESSAGE

# conexión a la base de datos
db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

# creación de la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    correo TEXT
)""")
db.commit()

# conexión al bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_select = cursor.execute("SELECT nombre FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if user_select is None:
        bot.send_message(message.chat.id, "HOLA, PARA PODER COMENZAR\nTIENES QUE IDENTIFICARTE.")
        msg = bot.send_message(message.chat.id, "¿Cuál es tu nombre?")
        bot.register_next_step_handler(msg, obtener_nombre)
    else:
        bot.send_message(message.chat.id, f"¡Hola {user_select[0]}! Ya estás registrado. ¡Gracias por usar nuestro bot!")

def obtener_nombre(message):
    user_id = message.chat.id
    nombre = message.text.strip()
    msg = bot.send_message(message.chat.id, f"Hola {nombre}, ahora bríndame tu correo electrónico:")
    bot.register_next_step_handler(msg, lambda msg: obtener_correo(msg, user_id, nombre))

def obtener_correo(message, user_id, nombre):
    correo = message.text.strip()
    cursor.execute("INSERT OR IGNORE INTO users (id, nombre, correo) VALUES (?, ?, ?)", (user_id, nombre, correo))
    db.commit()
    bot.send_message(message.chat.id, "¡Gracias por identificarte! 🎉")

# ASCII Art con "SMITH"
ascii_smith = """
     ▄████████   ▄▄▄▄███▄▄▄▄    ▄█      ███        ▄█    █▄    
  ███    ███ ▄██▀▀▀███▀▀▀██▄ ███  ▀█████████▄   ███    ███   
  ███    █▀  ███   ███   ███ ███▌    ▀███▀▀██   ███    ███   
  ███        ███   ███   ███ ███▌     ███   ▀  ▄███▄▄▄▄███▄▄ 
▀███████████ ███   ███   ███ ███▌     ███     ▀▀███▀▀▀▀███▀  
         ███ ███   ███   ███ ███      ███       ███    ███   
   ▄█    ███ ███   ███   ███ ███      ███       ███    ███   
 ▄████████▀   ▀█   ███   █▀  █▀      ▄████▀     ███    █▀    
                                                             
"""
print(ascii_smith)

bot.polling(none_stop=True)
