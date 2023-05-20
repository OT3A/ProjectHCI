import tkinter as tk
import pygame
import math
from tkinter import filedialog
from EOGProject import PreprocessingEOGSignal,ReadSignal,FeatureExtracionByPeaks
from joblib import load
import pyaudio
import wave

model = load('./modelKNN100.0Peaks.knn')


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
globalpre =''
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
    update_canvas(prediction)
    update_button_color(prediction)

    
print(globalpre)





sleep = False
eat = False
drink = False
bathroom = False


def update_button_color(prediction):
    global sleep , eat,drink,bathroom
    if(prediction==4):
        bathroomButton.config(bg='SystemButtonFace')
        sleepButton.config(bg='SystemButtonFace')
        drinkButton.config(bg='SystemButtonFace')
        eatButton.config(bg="red")
        sleep = False
        eat = True
        drink = False
        bathroom = False
    elif(prediction==2):
        eatButton.config(bg='SystemButtonFace')
        sleepButton.config(bg='SystemButtonFace')
        drinkButton.config(bg='SystemButtonFace')
        bathroomButton.config(bg='red')
        sleep = False
        eat = False
        drink = False
        bathroom = True
    elif(prediction==0):
        eatButton.config(bg='SystemButtonFace')
        sleepButton.config(bg='SystemButtonFace')
        bathroomButton.config(bg='SystemButtonFace')
        drinkButton.config(bg='red')
        sleep = False
        eat = False
        drink = True
        bathroom = False
    elif(prediction==3):
        eatButton.config(bg='SystemButtonFace')
        bathroomButton.config(bg='SystemButtonFace')
        drinkButton.config(bg='SystemButtonFace')    
        sleepButton.config(bg='red')
        sleep = True
        eat = False
        drink = False
        bathroom = False
    elif prediction == 1:
        playSound()  
        sleep = False
        eat = False
        drink = False
        bathroom = False
        
        

def playSound():
    if (sleep==False and eat==False and drink==False and bathroom==True):
        sound.play()
    elif (sleep==False and eat==False and drink==True and bathroom==False):
        sound.play()
    elif (sleep==False and eat==True and drink==False and bathroom==False):
        sound.play()
    elif (sleep==True and eat==False and drink==False and bathroom==False):
        sound.play()





# set up Pygame
pygame.init()

sound = pygame.mixer.Sound('soud.mp3')


# set the dimensions of the screen
size = width, height = 150, 50
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
def move_pupils(predictMove):
    global left_pupil_pos, right_pupil_pos, moved_timer
    keys = pygame.key.get_pressed()
    # move pupils based on arrow keys
    if predictMove == 4:
        left_pupil_pos = get_new_pos(left_eye_pos, math.pi/2, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, math.pi/2, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif predictMove == 0:
        left_pupil_pos = get_new_pos(left_eye_pos, -math.pi/2, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, -math.pi/2, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif predictMove == 3:
        left_pupil_pos = get_new_pos(left_eye_pos, math.pi, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, math.pi, eye_radius - pupil_radius)
        moved_timer = moved_duration
    elif predictMove == 2:
        left_pupil_pos = get_new_pos(left_eye_pos, 0, eye_radius - pupil_radius)
        right_pupil_pos = get_new_pos(right_eye_pos, 0, eye_radius - pupil_radius)
        moved_timer = moved_duration
    # blink when space bar is pressedx
    if predictMove == 1:
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
eatButton = tk.Button(root, image=image,width=150,height=150)
eatButton.place(relx=0.5,rely=0.17,anchor='center')
# eatButton.bind('<Enter>', button_entered)
# eatButton.bind('<Leave>', button_left)

drinkButton = tk.Button(root, image=drinkImage,width=150,height=150,)
drinkButton.place(relx=0.5,rely=0.83,anchor='center')
# drinkButton.bind('<Enter>', button_entered)
# drinkButton.bind('<Leave>', button_left)

sleepButton = tk.Button(root, image=sleepImage,width=150,height=150,)
sleepButton.place(relx=0.1,rely=0.5,anchor='center')
# sleepButton.bind('<Enter>', button_entered)
# sleepButton.bind('<Leave>', button_left)


bathroomButton = tk.Button(root, image=bathroomImage,width=150,height=150,)
bathroomButton.place(relx=0.9,rely=0.5,anchor='center')
# bathroomButton.bind('<Enter>', button_entered)
# bathroomButton.bind('<Leave>', button_left)

loadSignalButton = tk.Button(root,text="Load Signal",command = select_file)
loadSignalButton.place(relx=0.1,rely=0.9,anchor='center')


# define a function to update the canvas with the current state of the eyes
def update_canvas(predictMove):
    global blink_timer, left_eye_open, right_eye_open, left_pupil_pos, right_pupil_pos, moved_timer
    print(globalpre)
    # move the pupils based on keyboard input and blink when space bar is pressed
    move_pupils(predictMove)

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
root.mainloop()

# quit Pygame
pygame.quit() 