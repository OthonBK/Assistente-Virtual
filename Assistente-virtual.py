import speech_recognition as sr
from gtts import gTTS
import os
import signal
import datetime
import pyaudio
import io
import sounddevice as sd
import soundfile as sf
import subprocess
import webbrowser
import pywhatkit

# Função para falar a resposta
def speak(text):
    tts = gTTS(text=text, lang='pt-br')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)

    audio_bytes.seek(0)

    data, fs = sf.read(audio_bytes)

    sd.play(data, fs)
    sd.wait()

    audio_bytes.close()

# Função para ouvir a entrada do usuário
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language='pt-BR')
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()

# Função para tocar música no YouTube
def play_music():
    speak("Qual música você gostaria de ouvir?")
    music = get_audio()
    speak(f"Tocando {music} no YouTube.")
    pywhatkit.playonyt(music)

# Função para executar o assistente virtual
def run():
    speak("Olá, eu sou BK, como posso ajudar?")
    discord_process = None # inicializa a variável para evitar erro
    while True:
        text = get_audio()

        if "olá" in text:
            speak("Olá! Como vai você?")
        elif "que horas são" == text:
            now = datetime.datetime.now()
            speak("São " + str(now.hour) + " horas e " + str(now.minute) + " minutos.")
        elif "abrir discord" in text:
            discord_process = subprocess.Popen(["C:/Users/User/AppData/Local/Discord/app-1.0.9011/Discord.exe"])
        elif "fecha o discord" in text:
            if discord_process is not None: # verifica se o Discord está aberto
                discord_process.terminate() # comando para fechar o processo do Discord
                speak("Discord fechado.")
            else:
                speak("O Discord não está aberto.")       
        elif "pesquisar" in text:
            search_term = text.split("pesquisar")[-1].strip()
            if search_term:
                url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(url)
                speak(f"Pesquisando por {search_term}")
            else:
                speak("Não entendi o que você quer pesquisar.")
        elif "tocar música" in text:
            play_music()
        elif "encerrar" in text:
            # pede ao usuário o nome do aplicativo a ser encerrado
            speak("Qual aplicativo você gostaria de encerrar?")
            app_name = get_audio()
            # verifica se o usuário forneceu o nome do aplicativo
            if app_name:
                # formata o nome do aplicativo para a sintaxe correta do comando taskkill
                app_name = app_name.replace(" ", "").lower() + ".exe"
                try:
                    # executa o comando taskkill
                    subprocess.call(["taskkill", "/f", "/im", app_name])
                    speak(f"{app_name} encerrado com sucesso.")
                except Exception as e:
                    speak(f"Ocorreu um erro ao encerrar o {app_name}.")
                    print(e)
            else:
                speak("Não entendi o nome do aplicativo.")

run()