import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from phi.assistant import Assistant
from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint

class FunctionScript(BaseModel):
    functionName: list = Field(..., description="Görevi gerçekleştirmek için sadece gerekli fonksiyonlari listele(string). Lamba, kapi,polisiAra,ambulansiAra,robotSüpürgeyiCalistir veya pencere")
    Value: str = Field(..., description="Görevi gerçekleştirmek için değer.")

def Lamba(value):
    return "Lamba: " + value

def pencere(value):
    return "Pencere: " + value

def kapi(value):
    return "Kapının: " + value

def polisiAra(value):
    return "Polisi ara: " + value

def ambulansiAra(value):
    return "Ambulansı ara: " + value

def robotSüpürgeyiCalistir(value):
    return "Robot süpürgeyi çalıştır: " + value

func_assistant = Assistant(
    description="Ev otomasyonu asistanısınız.",
    output_model=FunctionScript,
)

# Sesi metne dönüştürme
model_path = "./vosk-model-small-tr-0.3"
if not os.path.exists(model_path):
    print("Lütfen doğru model dizinini belirtiniz!")
    exit(1)

model = Model(model_path)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)
stream.start_stream()

recognizer = KaldiRecognizer(model, 16000)

print("cambaz demeden dinlemeyeceğim, dur dediğinizde duracağım...")

aktif_dinleme = False  # Başlangıçta dinleme pasif olarak ayarlandi

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        if 'text' in result:
            print(result['text'])  # Algılanan metni yazdır
            if "cambaz" in result['text']:
                aktif_dinleme = True  # "cambaz" kelimesi iledinlemeyi aktif et
                print("Artık dinliyorum...")
            elif "dur" in result['text'] and aktif_dinleme:
                aktif_dinleme = False  # "Dur" kelimesi ile dinlemeyi pasif et
                print("Dinlemeyi durduruyorum, tekrar cambaz demelisiniz...")
            if aktif_dinleme:
                answer = func_assistant.run(result['text'])

                for f in answer.functionName:
                    if f == "Lamba":
                        pprint(Lamba(answer.Value))
                    elif f == "pencere":
                        pprint(pencere(answer.Value))
                    elif f == "kapi":
                        pprint(kapi(answer.Value))
                    elif f == "polisiAra":
                        pprint(polisiAra(answer.Value))
                    elif f == "ambulansiAra":
                        pprint(ambulansiAra(answer.Value))
                    elif f == "robotSüpürgeyiCalistir":
                        pprint(robotSüpürgeyiCalistir(answer.Value))

        else:
            if aktif_dinleme:
                partial_result = json.loads(recognizer.PartialResult())
                if 'partial' in partial_result:
                    print("Dinleme: ", partial_result['partial'])

stream.stop_stream()
stream.close()
p.terminate()
