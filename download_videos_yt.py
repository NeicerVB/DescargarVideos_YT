from pytube import YouTube
import subprocess
import os
import time

def Descargar(URL, tipo_descarga):
    yt = YouTube(URL)

    fileName = None
    
    # Descargar video
    if tipo_descarga == "bajar_video":
        fileName = descargar_video(yt)
    elif tipo_descarga == "bajar_audio":
        fileName = descargar_audio(yt)

    # Devolvemos archivo descargado
    return fileName

def descargar_video(yt):

    # Obtener los archivos de audio y video con mejor calidad
    video_stream = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Descargar el audio y video
    video_stream.download(output_path="./Videos", filename="video.mp4")
    audio_stream.download(output_path="./Videos", filename="audio.mp3")

    # Combinar el audio y video con ffmpeg
    fecha = time.strftime("%Y-%m-%d_%Hh%M_%S")
    fileName = f"Videos/{fecha}.mp4"
    subprocess.run(
        [
            "N:/FFmpeg/FFmpeg/bin/ffmpeg.exe",
            "-i", "Videos/video.mp4",
            "-i", "Videos/audio.mp3",
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            fileName
        ]
    )

    # Eliminamos los archivos de audio y video para liberar espacio
    os.remove("Videos/video.mp4")
    os.remove("Videos/audio.mp3")

    return fileName

def descargar_audio(yt):

    # Obtener el archivo de audio con mejor calidad
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Descargar el audio
    audio_stream.download(output_path="./Videos", filename="audio.mp3")

    # Renombrar el archivo de audio con la fecha actual
    fecha = time.strftime("%Y-%m-%d_%Hh%M_%S")
    fileName = f"Videos/{fecha}.mp3"
    os.rename("Videos/audio.mp3", fileName)

    return fileName

