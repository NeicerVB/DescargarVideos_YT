import telebot
import telebot.types as types
import re
from download_videos_yt import Descargar_Video_YT

bot = telebot.TeleBot("7475116863:AAGDbBYKL8Cu4ijSNHwCmEmBKMXFvRMlq6Q")

@bot.message_handler(commands=['start'])
def tabla_fija(message):
	# Creamos una instancia de la clase InlienKeyboardMarkup
	# que es la que nos permite crear botones en línea
	inline_table = types.InlineKeyboardMarkup()

	# 1. Creamos los botones que queremos que tenga nuestro menú
	option_download_video = types.InlineKeyboardButton(text='📹 Descargar Video', callback_data='download_video')
	option_download_video_audio = types.InlineKeyboardButton(text='🎧 Descargar Música', callback_data='download_audio')

	# 2. Añadimos los botones a la instancia de la clase InlineKeyboardMarkup
	inline_table.add(option_download_video, option_download_video_audio)

	# 3. Enviamos el mensaje con la instancia de la clase InlineKeyboardMarkup
	bot.send_message(message.chat.id, text="Elija una opción", reply_markup=inline_table)



@bot.callback_query_handler(func=lambda call: True)
def consulta(call):
	if call.data == "download_video":
		# Aquí va el código para descargar el video
		bot.send_message(call.message.chat.id, "Ingrese la URL del video de YouTube:")
		bot.register_next_step_handler(call.message, verificar_url)
	elif call.data == "download_audio":
		# PENDIENTE
		bot.send_message(call.message.chat.id, "Ingrese la URL del video de YouTube para extraer el audio:")
		bot.register_next_step_handler(call.message, verificar_url)
		bot.answer_callback_query(call.id, "Funcionalidad no disponible")



def verificar_url(message):
	if "youtu.be" in message.text:
		descargar_video(message)
	else:
		bot.send_message(message.chat.id, "URL no válida. Por favor, ingrese una URL de Youtube.")
		bot.register_next_step_handler(message, verificar_url)



def descargar_video(message):
	URL = message.text
	ruta_video = Descargar_Video_YT(URL)
	subir_video_a_telegram(message, ruta_video)



def subir_video_a_telegram(message, ruta_video):
	try:
		with open(ruta_video, 'rb') as video:
			bot.send_video(message.chat.id, video, timeout=120)
	except Exception as e:
		bot.send_message(message.chat.id, f"Error al enviar el video {video}")



bot.polling(timeout=120, long_polling_timeout=120)