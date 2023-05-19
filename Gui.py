import tkinter as tk
import pygame
import math
from tkinter import filedialog
from EOGProject import PreprocessingEOGSignal,ReadSignal,FeatureExtracionByPeaks
from joblib import load
import pyaudio
import wave

model = load('./modelKNN100.0Peaks.knn')

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

up = False
down = False
left = False
right = False
blink = False
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
        blink = True 
    elif prediction == 2:
        print('Right')
        
    elif prediction == 3:
        print('Left')
        
    elif prediction == 4:
        print('Up')
        
    print("predict",prediction)


player = Player('hun.wav')
player2 = Player('output3.wav')
player3 = Player('sleep.wav')
player4 = Player('output5.wav')

# set up Pygame
pygame.init()


# set the dimensions of the screen
size = width, height = 900, 600
screen = pygame.display.set_mode(size)

# set the colors for the eyes and pupils
eye_color = (255, 255, 255)
pupil_color = (0, 0, 0)

# set the radius and position of the eyes
eye_radius = 50
left_eye_pos = (350, 300)
right_eye_pos = (550, 300)

# set the radius and position of the pupils
pupil_radius = 20
left_pupil_pos = left_eye_pos
right_pupil_pos = right_eye_pos

# set the state of the eyes (open or closed)
left_eye_open = True
right_eye_open = True
blink_timer = 0
blink_duration = 20

# set the state of the eyes (center or moved)
moved_timer = 0
moved_duration = 200




# define a function to move the pupils based on keyboard input
def move_pupils():
    global left_pupil_pos, right_pupil_pos, moved_timer
    keys = pygame.key.get_pressed()
    # move pupils based on arrow keys
    if keys[pygame.K_UP]:
        left_pupil_pos = get_new_pos(left_eye_pos, math.pi/2, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, math.pi/2, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif keys[pygame.K_DOWN]:
        left_pupil_pos = get_new_pos(left_eye_pos, -math.pi/2, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, -math.pi/2, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif keys[pygame.K_LEFT]:
        left_pupil_pos = get_new_pos(left_eye_pos, math.pi, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, math.pi, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif keys[pygame.K_RIGHT]:
        left_pupil_pos = get_new_pos(left_eye_pos, 0, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, 0, eye_radius - pupil_radius)
        moved_timer = moved_duration
    # blink when space bar is pressed
    if keys[pygame.K_SPACE]:
        global blink_timer, left_eye_open, right_eye_open
        left_pupil_pos = get_new_pos(left_eye_pos, 0, 1000)
        right_pupil_pos = get_new_pos(right_eye_pos, 0, 1000)
        moved_timer = moved_duration
        if blink_timer == 0:
            blink_timer = blink_duration
            left_eye_open = False
            right_eye_open = False

# define a function to get the new position of a pupil based on the eye position and angle
def get_new_pos(eye_pos, angle, max_distance):
    distance = min(max_distance, max(0, max_distance - pygame.mouse.get_pos()[1]/10))
    return (int(eye_pos[0] + distance * math.cos(angle)), int(eye_pos[1] - distance * math.sin(angle)))

# create a Tkinter window with a canvas
root = tk.Tk()
root.resizable(False,False)
root.title('EOG Interface')
root.geometry("900x600")

# Create a PhotoImage object with the image file
image = tk.PhotoImage(file='eat.PNG')
drinkImage = tk.PhotoImage(file='drink.png')
sleepImage = tk.PhotoImage(file='sleep1.png')
bathroomImage = tk.PhotoImage(file='bathroom.png')
backImage = tk.PhotoImage(file='signal11.jpg')

canvas = tk.Canvas(root, width=900, height=600)
canvas.create_image(0, 0, anchor='nw', image=backImage)
canvas.pack()
# Create buttons with the image and place the button into the root window
eatButton = tk.Button(root, image=image,width=150,height=150,command=player.play)
eatButton.place(relx=0.5,rely=0.17,anchor='center')
eatButton.bind('<Enter>', button_entered)
eatButton.bind('<Leave>', button_left)

drinkButton = tk.Button(root, image=drinkImage,width=150,height=150,command=player2.play)
drinkButton.place(relx=0.5,rely=0.83,anchor='center')
drinkButton.bind('<Enter>', button_entered)
drinkButton.bind('<Leave>', button_left)

sleepButton = tk.Button(root, image=sleepImage,width=150,height=150,command=player3.play)
sleepButton.place(relx=0.1,rely=0.5,anchor='center')
sleepButton.bind('<Enter>', button_entered)
sleepButton.bind('<Leave>', button_left)


bathroomButton = tk.Button(root, image=bathroomImage,width=150,height=150,command=player4.play)
bathroomButton.place(relx=0.9,rely=0.5,anchor='center')
bathroomButton.bind('<Enter>', button_entered)
bathroomButton.bind('<Leave>', button_left)

loadSignalButton = tk.Button(root,text="Load Signal",command=select_file)
loadSignalButton.place(relx=0.1,rely=0.9,anchor='center')
# define a function to update the canvas with the current state of the eyes
def update_canvas():
    global blink_timer, left_eye_open, right_eye_open, left_pupil_pos, right_pupil_pos, moved_timer
    
    # move the pupils based on keyboard input and blink when space bar is pressed
    move_pupils()

    # decrement blink timer and update eye state
    if blink_timer > 0:
        blink_timer -= 1
        if blink_timer == 0:
            left_eye_open = True
            right_eye_open = True

    # decrement moved timer and return eyes to center if necessary
    if moved_timer > 0:
        moved_timer -= 1
        if moved_timer == 0:
            left_pupil_pos = left_eye_pos
            right_pupil_pos = right_eye_pos

    # convert eye_color and pupil_color to hexadecimal strings
    eye_color_hex = '#%02x%02x%02x' % eye_color
    pupil_color_hex = '#%02x%02x%02x' % pupil_color

    # draw the eyes and pupils
    canvas.delete("all")
    canvas.create_image(0, 0, anchor='nw', image=backImage)
    canvas.create_oval(left_eye_pos[0]-eye_radius, left_eye_pos[1]-eye_radius, left_eye_pos[0]+eye_radius, left_eye_pos[1]+eye_radius, fill=eye_color_hex)
    canvas.create_oval(left_pupil_pos[0]-pupil_radius, left_pupil_pos[1]-pupil_radius, left_pupil_pos[0]+pupil_radius, left_pupil_pos[1]+pupil_radius, fill=pupil_color_hex)
    canvas.create_oval(right_eye_pos[0]-eye_radius, right_eye_pos[1]-eye_radius, right_eye_pos[0]+eye_radius, right_eye_pos[1]+eye_radius, fill=eye_color_hex)
    canvas.create_oval(right_pupil_pos[0]-pupil_radius, right_pupil_pos[1]-pupil_radius, right_pupil_pos[0]+pupil_radius, right_pupil_pos[1]+pupil_radius, fill=pupil_color_hex)

    # canvas.create_image(0, 0, anchor='nw', image=backImage)
    # draw eyelids if eyes are closed
    if not left_eye_open:
        canvas.create_line(left_eye_pos[0]-eye_radius, left_eye_pos[1], left_eye_pos[0]+eye_radius, left_eye_pos[1], width=10)
    if not right_eye_open:
        canvas.create_line(right_eye_pos[0]-eye_radius, right_eye_pos[1], right_eye_pos[0]+eye_radius, right_eye_pos[1], width=10)
    # update the display
    canvas.after(10, update_canvas)
# start the Tkinter main loop
update_canvas()
root.mainloop()

# quit Pygame
pygame.quit() 