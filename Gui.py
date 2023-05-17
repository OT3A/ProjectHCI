import tkinter as tk
from tkinter import filedialog
from EOGProject import PreprocessingEOGSignal,ReadSignal,FeatureExtracionByPeaks
from joblib import load
import pyaudio
import wave


# Load and use the model
model = load('D:/PDF/4th year/seconde term/HCI/ProjectHCI/modelKNN100.0Peaks.knn')

class Player:
    CHUNK = 1024

    def __init__(self, filename):
        self.filename = filename

    def play(self):
        self.audio = pyaudio.PyAudio()

        self.file = wave.open(self.filename, 'rb')

        self.stream = self.audio.open(format=self.audio.get_format_from_width(self.file.getsampwidth()),

                                      channels=self.file.getnchannels(),

                                      rate=self.file.getframerate(),

                                      output=True)

        data = self.file.readframes(self.CHUNK)

        while data:
            self.stream.write(data)

            data = self.file.readframes(self.CHUNK)

        self.stream.stop_stream()

        self.stream.close()

        self.file.close()

        self.audio.terminate()

def button_entered(event):
    # Change the background color of the button to red when the mouse enters
    event.widget.config(bg='red')

def button_left(event):
    # Change the background color of the button back to its original color when the mouse leaves
    event.widget.config(bg='SystemButtonFace')

def select_file():
    pathSignalH = filedialog.askopenfilename()
    pathSignalV = filedialog.askopenfilename()
    signalh = ReadSignal(pathSignalH)
    signalv = ReadSignal(pathSignalV)
    signalh = PreprocessingEOGSignal(signalh)
    signalv = PreprocessingEOGSignal(signalv)
    signalh = FeatureExtracionByPeaks(signalh)
    signalv = FeatureExtracionByPeaks(signalv)
    signal = [signalh,signalv]
    prediction = model.predict([signal])
    if prediction == 0:
        print('Down')
    elif prediction == 1:
        print('Blink')
    elif prediction == 2:
        print('Right')
    elif prediction == 3:
        print('Left')
    elif prediction == 4:
        print('Up')
    print("predict",prediction)


    

screen = tk.Tk()

player = Player('hun.wav')
player2 = Player('output3.wav')
player3 = Player('sleep.wav')
player4 = Player('output5.wav')

screen.geometry('900x600')
screen.resizable(False, False)
screen.title('EOG Inerface')
# Create a PhotoImage object with the image file
image = tk.PhotoImage(file='eat.PNG')
drinkImage = tk.PhotoImage(file='drink.png')
sleepImage = tk.PhotoImage(file='sleep1.png')
bathroomImage = tk.PhotoImage(file='bathroom.png')
backImage = tk.PhotoImage(file='signal11.jpg')
# Create a Canvas widget with backgreound
canvas = tk.Canvas(screen, width=900, height=600)
canvas.create_image(0, 0, anchor='nw', image=backImage)
canvas.pack()
# Create buttons with the image and place the button into the root window
eatButton = tk.Button(screen, image=image,width=150,height=150,command=player.play)
eatButton.place(relx=0.5,rely=0.17,anchor='center')
eatButton.bind('<Enter>', button_entered)
eatButton.bind('<Leave>', button_left)

drinkButton = tk.Button(screen, image=drinkImage,width=150,height=150,command=player2.play)
drinkButton.place(relx=0.5,rely=0.83,anchor='center')
drinkButton.bind('<Enter>', button_entered)
drinkButton.bind('<Leave>', button_left)

sleepButton = tk.Button(screen, image=sleepImage,width=150,height=150,command=player3.play)
sleepButton.place(relx=0.1,rely=0.5,anchor='center')
sleepButton.bind('<Enter>', button_entered)
sleepButton.bind('<Leave>', button_left)


bathroomButton = tk.Button(screen, image=bathroomImage,width=150,height=150,command=player4.play)
bathroomButton.place(relx=0.9,rely=0.5,anchor='center')
bathroomButton.bind('<Enter>', button_entered)
bathroomButton.bind('<Leave>', button_left)

loadSignalButton = tk.Button(screen,text="Load Signal",command=select_file)
loadSignalButton.place(relx=0.1,rely=0.9,anchor='center')
# Start the event loop
screen.mainloop()











