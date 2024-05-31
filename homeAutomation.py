import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
import time
import requests

ESP8266_IP = "192.168.1.12"  # ESP8266'nın IP adresi

class FunctionScript(BaseModel):
    functionName: List[str] = Field(..., description="Görevi gerçekleştirmek için sadece gerekli fonksiyonları listele (string) ve true yada false degerleri döndür. Lamba, kapi, polisiAra, ambulansiAra, robotSüpürgeyiCalistir veya pencere")
    Value: str = Field(..., description="Görevi gerçekleştirmek için değer.")

def Lamba(value):
    try:
        if value.lower() == "true":
            response = requests.get(f"http://{ESP8266_IP}/ledon")
            if response.status_code == 200:
                return "Lamba açıldı."
            else:
                return f"Error: {response.status_code}"
        elif value.lower() == "false":
            response = requests.get(f"http://{ESP8266_IP}/ledoff")
            if response.status_code == 200:
                return "Lamba kapatıldı."
            else:
                return f"Error: {response.status_code}"
    except Exception as e:
        return f"HTTP request failed: {e}"
    return "Geçersiz lamba komutu."

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

def getMyAssistant(keep_alive):
    func_assistant = Assistant(
        #llm=Ollama(model="llama3", keep_alive=keep_alive),
        description="Ev otomasyonu asistanısınız.",
        output_model=FunctionScript,
        monitoring=True,
    )
    return func_assistant

def getMyStream():
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
    return recognizer, stream, p

def main(func_assistant=None, stream=None, recognizer=None, p=None):
    global aktif_dinleme  
    if not func_assistant or not stream or not recognizer:
        return
    
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        if 'text' in result:
            print(result['text'])  # Algılanan metni yazdır
            if "cambaz" in result['text']:
                aktif_dinleme=True# "cambaz" kelimesi ile dinlemeyi aktif et
                print("Artık dinliyorum...")
            elif "dur" in result['text'] and aktif_dinleme:
                aktif_dinleme = False  # "dur" kelimesi ile dinlemeyi pasif et
                print("Dinlemeyi durduruyorum, tekrar cambaz demelisiniz...")
            if aktif_dinleme:
                try:
                    start = time.time()
                    print("burasi result",result['text'])
                    if result['text'] and result['text'] != "cambaz":
                        answer = func_assistant.run(result['text'])
                        print("answer",answer)
                        for f in answer.functionName:
                            if f.lower() == "lamba":
                                pprint(Lamba(answer.Value))
                            elif f.lower() == "pencere":
                                pprint(pencere(answer.Value))
                            elif f.lower() == "kapi":
                                pprint(kapi(answer.Value))
                            elif f.lower() == "polisiara":
                                pprint(polisiAra(answer.Value))
                            elif f.lower() == "ambulansiar":
                                pprint(ambulansiAra(answer.Value))
                            elif f.lower() == "robotsüpürgeyicalistir":
                                pprint(robotSüpürgeyiCalistir(answer.Value))
                except Exception as e:
                    print("The error is: ", e)
                    stopStream(stream, p)
                finally:
                    print(f'Time: {time.time() - start}')
        else:
            if aktif_dinleme:
                partial_result = json.loads(recognizer.PartialResult())
                if 'partial' in partial_result:
                    print("Dinleme: ", partial_result['partial'])

def stopStream(stream, p):
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    recognizer, stream, p = getMyStream()
    func_assistant = getMyAssistant(keep_alive=True)
    print("cambaz demeden dinlemeyeceğim, dur dediğinizde duracağım...")
    while True:
        try:
            main(func_assistant=func_assistant, stream=stream, recognizer=recognizer, p=p)
        except Exception as e:
            print("The error is: ", e)
