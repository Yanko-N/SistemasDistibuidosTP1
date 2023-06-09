import speech_recognition as sr
from gtts import gTTS
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import openai
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
import os

openai.organization = "HERE GOES THE ORG"
openai.api_key = "HERE GOES THE KEY"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


window  = tk.Tk()
window.geometry('800x600')
window.title("Speak2GPT")
window.iconbitmap(resource_path("./Images/icon.ico"))
dir_path = '%s\\Speak2GPT\\' %  os.environ['APPDATA'] 
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Create a photoimage object of the image in the path
photoSpeak = tk.PhotoImage(file = resource_path("./Images/SpeakButton.PNG"))
audioFilePath =resource_path("blipSelect.wav")
# Text Creation
lbl = tk.Text(window, background="#343541", borderwidth=1, width=93, height=18, wrap="word", fg='white')
lbl.place(relx=0.5, rely=0.25, anchor="center")

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(window)
scrollbar.place(relx=0.98, rely=0.25, anchor="center", relheight=0.5)

# Configure the scrollbar to work with the text widget
lbl.configure(yscrollcommand=scrollbar.set)
lbl.delete("1.0", tk.END)
lbl.insert(tk.END, " Clique Alt_L + F para falar \n Clique Ctrl + Enter \n")
scrollbar.configure(command=lbl.yview)




def PesquisaGPT(query):

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "user", "content": query}
      ],
    max_tokens = 1000
  )

  return response['choices'][0]['message']['content']

def playsound(filepath):
  mixer.music.load(filepath)
  mixer.music.play()
  while mixer.music.get_busy(): # check if the file is playing
    pass
  mixer.music.unload()

def ouvir_microfone(label):
 #Habilita o microfone para ouvir o usuario
 microfone = sr.Recognizer()
 with sr.Microphone() as source:
  #Chama a funcao de reducao de ruido disponivel na speech_recognition
  microfone.adjust_for_ambient_noise(source)
  #Avisa ao usuario que esta pronto para ouvir
  playsound(audioFilePath)
  lbl.delete("1.0", tk.END)
  lbl.insert(tk.END, "Pode Falar")
  window.update()
  #Armazena a informacao de audio na variavel
  audio = microfone.listen(source)
  try:
  #Passa o audio para o reconhecedor de padroes do speech_recognition
    frase = microfone.recognize_google(audio,language='pt-PT')
  #Após alguns segundos, retorna a frase falada
  except sr.UnknownValueError:
    frase = "Não entendi. Por favor repita!"
  print(frase)#Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
  lbl.delete("1.0", tk.END)
  #lbl.insert(tk.END,frase)
  window.update()
  return frase
 
def mainLoop():
  
  lbl.delete("1.0", tk.END)
  lbl.insert(tk.END, "Por Favor aguarde")
  window.update()
  tempfile = dir_path + "\\file.mp3"

  mixer.init()
  procura = ouvir_microfone(lbl)

  res = gTTS(text=procura, lang="pt-PT", slow=False)
  res.save(tempfile)

  playsound(tempfile)

  while(procura == "Não entendi. Por favor repita!"):
    procura = ouvir_microfone(lbl)
    res = gTTS(text=procura, lang="pt-PT", slow=False)
    res.save(tempfile)
    playsound(tempfile)

  response = PesquisaGPT(procura)
  lbl.delete("1.0", tk.END)
  lbl.insert(tk.END, response)
  lbl.see(tk.END)
  print(response)

  res = gTTS(text=response, lang="pt-PT", slow=False)
  res.save(tempfile)

  playsound(tempfile)
 



#create listBox
listbox= tk.Listbox(window, width=130, height=10)
listbox.place(relx=0.5,rely=0.64,anchor="center")
# Inserting the listbox items
listbox.insert(1, "Qual é a legislação que protege os direitos das pessoas com deficiência em Portugal?")
listbox.insert(2, "Quais são os princípios-chave da legislação para inclusão de pessoas com deficiência em Portugal?")
listbox.insert(3, "Qual lei trata da acessibilidade em edifícios públicos e privados em Portugal?")
listbox.insert(4, "Quais são os direitos das pessoas com deficiência no trabalho de acordo com a legislação?")
listbox.insert(5, "Qual lei estabelece uma reserva de empregos para pessoas com deficiência em organizações com mais de 75 funcionários?")
listbox.insert(6, "Quais são os apoios financeiros e benefícios disponíveis para pessoas com deficiência em Portugal?")
listbox.insert(7, "Qual é a legislação que protege os direitos das pessoas com deficiência no sistema educacional português?")
listbox.insert(8, "Quais medidas são previstas para promover a inclusão de pessoas com deficiência na escola regular?")
listbox.insert(9, "Qual lei garante a acessibilidade dos transportes públicos em Portugal?")
listbox.insert(10, "Quais são as principais entidades responsáveis por implementar e fiscalizar a legislação sobre pessoas com deficiência em Portugal?")
 
# Function for printing the
# selected listbox value(s)
def selected_item():
     
    # Traverse the tuple returned by
    # curselection method and print
    # corresponding value(s) in the listbox
    for i in listbox.curselection():
        printText(listbox.get(i))
 

#FUNÇÃO QUE RECEBE TEXTO E IMPRIME NO ECRA
def printText(text):
  lbl.delete("1.0", tk.END)
  inputtxt.delete("1.0", tk.END)
  lbl.insert(tk.END, "")
  lbl.insert(tk.END, PesquisaGPT(text))
  lbl.see(tk.END)
  

# Function for getting Input
# from textbox and printing it 
# at label widget
  
def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    if(inp == ""):
      selected_item()
    else:
      printText(inp)
    
  
# TextBox Creation
inputtxt = tk.Text(window,
                   height = 6,
                   width = 60)

inputtxt.place(relx=0.5,
               rely=0.9,
               anchor="center")
  
  
# Button Creation

speakButton = tk.Button(image=photoSpeak, command= mainLoop, background="black", foreground="white",activebackground="#709ae5",
                        height=98,
                        width=100)
speakButton.place(relx=0.1,
            rely=0.9,
            anchor="center")


submitButton = tk.Button(window,
                        text = "Pesquisar", 
                        command = printInput,
                        height=6,
                        width=20)

submitButton.place(relx=0.9,
                   rely=0.9,
                   anchor="center")

window.bind('<Control-Return>',lambda event:printInput())
window.bind('<Alt_L>f',lambda event:mainLoop() )
window.resizable(False, False)
window.mainloop()
