import telebot
import telebot.types as types
from download_videos_yt import Descargar
import os

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
		bot.send_message(
			call.message.chat.id,
			"Ingrese la URL del video de YouTube:"
		)
		bot.register_next_step_handler(
			call.message,
			lambda message: verificar_url(message, call.data) 
		)

	elif call.data == "download_audio":
		# Aquí va el código para descargar el audio
		bot.send_message(
			call.message.chat.id,
			"Ingrese la URL del video de YouTube para extraer el audio:"
		)
		bot.register_next_step_handler(
			call.message,
			lambda message: verificar_url(message, call.data)
		)



def verificar_url(message, call_data):
	if "youtu.be" in message.text:
		if call_data == "download_video":
			descargar_video_o_audio(message, "bajar_video")
		elif call_data == "download_audio":
			descargar_video_o_audio(message, "bajar_audio")
	elif "youtube.com" in message.text and "/watch?v=" in message.text:
		if call_data == "download_video":
			descargar_video_o_audio(message, "bajar_video")
	else:
		bot.send_message(
			message.chat.id,
			"URL no válida. Por favor, ingrese una URL de Youtube."
		)
		bot.register_next_step_handler(
			message,
			lambda message: verificar_url(message, call_data)
		)



def descargar_video_o_audio(message, tipo_descarga):
	URL = message.text
	ruta = Descargar(URL, tipo_descarga)
	subir_video_a_telegram(message, ruta, tipo_descarga)



def subir_video_a_telegram(message, ruta_video, tipo_descarga):
	try:
		file_size = os.path.getsize(ruta_video) # Obtener el tamaño del archivo en bytes
		max_size = 50 * 1024 * 1024  # 50 MB

		if tipo_descarga == "bajar_video":
			if file_size < max_size:
				with open(ruta_video, 'rb') as video:
					bot.send_video(message.chat.id, video, timeout=2000)
			else: # Si el archivo es mayor a 50 MB, enviarlo como documento
				with open(ruta_video, 'rb') as video:
					bot.send_document(message.chat.id, video, timeout=2000)

		elif tipo_descarga == "bajar_audio":
			if file_size < max_size:
				with open(ruta_video, 'rb') as audio:
					bot.send_audio(message.chat.id, audio, timeout=2000)
			else: # Si el archivo es mayor a 50 MB, enviarlo como documento
				with open(ruta_video, 'rb') as audio:
					bot.send_document(message.chat.id, audio, timeout=2000)
	except Exception as e:
		bot.send_message(message.chat.id, f"Error al enviar el archivo {ruta_video}: {str(e)}")


bot.polling(timeout=2000, long_polling_timeout=2000)