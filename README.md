Ev Otomasyonu Asistanı

Bu proje, Vosk ve PyAudio kullanarak Türkçe sesli komutları algılayıp ev otomasyonu görevlerini gerçekleştirebilen bir Python uygulamasıdır. Uygulama, belirli anahtar kelimeleri ("cambaz" ve "dur") dinleyerek aktif dinlemeye başlar veya durur. Algılanan komutlara göre belirlenen işlevler (lamba açmak/kapatmak, kapı kilitlemek/kilidini açmak vs.) çalıştırılır.

Özellikler:

- Sesli komut aktivasyonu ve deaktivasyonu
- Çeşitli ev otomasyon işlevlerinin sesli komutlarla kontrolü
- Dinamik komut işleme

Gereksinimler:

- Python 3.6+
- PyAudio
- Vosk
- Rich

Kurulum:

git clone https://github.com/canbazogluosman1/localHomeAutomation.git
pip install -r requirements.txt

Kullanim:

python homeAutomation.py

Uygulama çalıştırıldığında, "cambaz" demeden aktif dinlemeye başlamaz. "cambaz" dediğinizde dinlemeye başlar ve "dur" dediğinizde dinlemeyi durdurur.

Yapilandirma:

"model_path" değişkenini, Vosk modelinin yolu ile güncelleyin:

model_path = "./vosk-model-small-tr-0.3"
