from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
from phi.assistant import Assistant

class FunctionScript(BaseModel):
    functionName: list = Field(..., description="Görevi gerçekleştirmek için sadece gerekli fonksiyonlari listele(string). Lamba, kapi,polisiAra,ambulansiAra,robotSüpürgeyiCalistir veya pencere")
    Value: str = Field(..., description="Görevi gerçekleştirmek için değer.")
    
def Lamba(value):
    return "Lamba: "+value

def pencere(value):
    return "Pencere: "+  value
def kapi(value):
    return "Kapının: "+  value
def polisiAra(value):
    return "Polisi ara: "+  value
def ambulansiAra(value):
    return "Ambulansı ara: "+  value
def robotSüpürgeyiCalistir(value):
    return "Robot süpürgeyi çalıştır: "+  value

func_assistant = Assistant(
    description="Ev otomasyonu asistanısınız.",
    output_model=FunctionScript,
)

answer = func_assistant.run("Yere bir şey dökülmüş")

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