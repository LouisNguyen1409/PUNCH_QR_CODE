from gtts import gTTS
import os

def generate_audio():
    # OK Audio
    tts_ok = gTTS(text='OK', lang='en')
    tts_ok.save("ok.mp3")
    print("Generated ok.mp3")

    # Wrong Audio (Vietnamese "Sai")
    tts_sai = gTTS(text='Sai', lang='vi')
    tts_sai.save("sai.mp3")
    print("Generated sai.mp3")

if __name__ == "__main__":
    generate_audio()
