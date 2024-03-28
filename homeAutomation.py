# from phi.assistant import Assistant

# assistant = Assistant(description="You a codding Assistants who is Expert of coding in python.")
# assistant.print_response("write a script to find first 100 prime number. output is a JSON put everything under key  'markdown' and code will be under 'code'key in JSON")

from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
from phi.assistant import Assistant
#TODO Streamlit arayüz yapilacak

class FunctionScript(BaseModel):
    functionName: list = Field(..., description="Görevi gerçekleştirmek için sadece gerekli fonksiyonlari listele(string). turnLight, openDoor,callPolice,callAmbulance,runVacuumCleanerRobot veya closeWindow")
    Value: str = Field(..., description="Görevi gerçekleştirmek için değer.")
    
def turnLight(value):
    return "turn on the light :"+value

def closeWindow(value):
    return "close the window :"+  value
def openDoor(value):
    return "open the door :"+  value
def callPolice(value):
    return "call the police :"+  value
def callAmbulance(value):
    return "call the ambulance :"+  value
def runVacuumCleanerRobot(value):
    return "run the vacuum cleaner robot :"+  value

func_assistant = Assistant(
    description="Ev otomasyonu asistanısınız.",
    output_model=FunctionScript,
)

answer = func_assistant.run("yerleri süpür göremiyorum cok karanlik isigi ac")

for f in answer.functionName:
    if f == "turnLight":
        pprint(turnLight(answer.Value))
    elif f == "closeWindow":
        pprint(closeWindow(answer.Value))
    elif f == "openDoor":
        pprint(openDoor(answer.Value))
    elif f == "callPolice":
        pprint(callPolice(answer.Value))
    elif f == "callAmbulance":
        pprint(callAmbulance(answer.Value))
    elif f == "runVacuumCleanerRobot":
        pprint(runVacuumCleanerRobot(answer.Value))