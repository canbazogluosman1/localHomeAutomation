import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json  # JSON parsing için

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

aktif_dinleme = False  # Başlangıçta dinlemeyi pasif olarak ayarla

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        if 'text' in result:
            print(result['text'])  # Algılanan metni yazdır
            if "cambaz" in result['text']:
                aktif_dinleme = True  # "cambaz" kelimesi algılandı, dinlemeyi aktif et
                print("Artık dinliyorum...")
            elif "dur" in result['text'] and aktif_dinleme:
                aktif_dinleme = False  # "Dur" kelimesi algılandı, dinlemeyi pasif et
                print("Dinlemeyi durduruyorum, tekrar cambaz demelisiniz...")
            if aktif_dinleme:
                # "cambaz" kelimesinden sonra yapılacak özel işlemler burada tanımlanabilir
                print("Özel işlem: ", result['text'])  # Özel işlem için gelen metni yazdır
    else:
        if aktif_dinleme:
            partial_result = json.loads(recognizer.PartialResult())
            if 'partial' in partial_result:
                print("Dinleme: ", partial_result['partial'])  # Aktif dinleme durumunda kısmi sonuçları yazdır

stream.stop_stream()
stream.close()
p.terminate()
