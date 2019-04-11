import numpy as np
import cv2
import time
import rtmidi

#Initial stuff
cap = cv2.VideoCapture(0)
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
n_in_rows = 10
rows = 8
width = int(cap.get(3))
height = int(cap.get(4))
color_low = np.array([0, 100, 0])
color_high = np.array([80, 255, 80])
previous_note = [0x80, 80, 0]
notearray = [72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101, 103, 105, 107, 108]

#Open midi
if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Vidi")

# Setup
print("VIDI by Thierry und Fia. Press q to quit.")
print("Video is " + str(width) + "x" + str(height) + " big")
while(True):
    setting = input("Color Mode? R/G/B/Y/P/C/W/Mult: ")
    if(setting == "R" or setting == ""):
        color_low = np.array([0, 0, 100])
        color_high = np.array([80, 80, 255])
        break
    elif(setting == "G"):
        color_low = np.array([0, 100, 0])
        color_high = np.array([80, 255, 80])
        break
    elif(setting == "B"):
        color_low = np.array([100, 0, 0])
        color_high = np.array([255, 80, 80])
        break
    elif(setting == "Y"):
        color_low = np.array([0, 100, 100])
        color_high = np.array([80, 255, 255])
        break
    elif(setting == "P"):
        color_low = np.array([100, 0, 100])
        color_high = np.array([255, 80, 255])
        break
    elif(setting == "C"):
        color_low = np.array([100, 100, 0])
        color_high = np.array([255, 255, 80])
        break
    elif(setting == "W"):
        color_low = np.array([200, 200, 200])
        color_high = np.array([255, 255, 255])
        break
    elif(setting == "Mult"):
        color_low[0] = np.array([0, 100, 0])
        color_high[0] = np.array([80, 255, 80])
        color_low[1] = np.array([0, 100, 0])
        color_high[1] = np.array([80, 255, 80])
        color_low[2] = np.array([0, 100, 0])
        color_high[2] = np.array([80, 255, 80])
        break
    print("Wrong input")
while(True):
    setting = input("Top Down Loudness? 0-15: ")
    try:
        if(setting == ""):
            rows = 15
            break
        elif(int(setting) <= 15 and int(setting) >= 0):
            rows = int(setting)
            break
        else:
            print("Number between 0 and 15.")
    except: 
        print("Please insert number")
while(True):
    setting = input("Sideway Number of Notes? 0-22: ")
    try: 
        if(setting == ""):
            n_in_rows = 22
            break
        elif(int(setting) <= 22 and int(setting) >= 0):
            n_in_rows = int(setting)
            break
        else:
            print("Number between 0 and 22.")
    except: 
        print("Please insert number")
while(True):
    setting = input("Chromatic, Pentatonic or Maj Scale? C/M/P: ")
    if(setting == "C"):
        notearray = [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94]
        break
    elif(setting == "P"):
        notearray = [69, 72, 74, 76, 79, 81, 84, 86, 88, 91, 93, 96, 98, 100, 103, 105, 108, 110, 112, 115, 117, 120]
        break
    elif(setting == "M"):
        break
    elif(setting == ""):
        break
    print("Wrong input")

# Update frame 
while(True):
    # Get frame from camera and flip 
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    origframe = frame

    # Mask matching color
    mask = cv2.inRange(frame, color_low, color_high)
    frame = cv2.bitwise_and(frame,frame, mask=mask)

    # Slice frame into rectangles
    framearray = []
    for i in range(rows):
        framerow = []
        for j in range(n_in_rows):
            framerow.append(cv2.cvtColor(frame[i*(height/rows):(i+1)*(height/rows), j*(width/n_in_rows):(j+1)*(width/n_in_rows)], cv2.COLOR_BGR2GRAY))
        framearray.append(framerow)

    # Find brightest rectangle
    brightest = [0,0,1000] #x, y, brightness
    for i in range(rows):
        for j in range(n_in_rows):
            rectbrightness = np.sum(framearray[i][j])
            if rectbrightness > brightest[2]:
                brightest = [i, j, rectbrightness]

    # Highlight rectangle in frame
    frame = cv2.rectangle(frame, (int((width/n_in_rows)*brightest[1]), int((height/rows)*brightest[0])), (int((width/n_in_rows)*(brightest[1]+1)), int((height/rows)*(brightest[0]+1))), (0,0,255),3)

    # Play midi note
    note_to_play = [0x90, notearray[brightest[1]], int((brightest[0]/rows)*128)]
    if(previous_note != note_to_play):
        midiout.send_message([0x80, previous_note[1], 0])
        midiout.send_message(note_to_play)
        previous_note=note_to_play

    print("Brightest part:" + str(brightest) + " Midi note played: " + str(note_to_play))

    # Add Grid to frame
    for i in range(rows+1):
        cv2.line(frame, (0, int((height/rows)*(i))), (width, int((height/rows)*(i))), (255, 255, 255), 1, 1)
    for i in range(n_in_rows+1):
        cv2.line(frame, (int((width/n_in_rows)*(i)), 0), (int((width/n_in_rows)*(i)), height), (255, 255, 255), 1, 1)

    # Display the frame
    cv2.imshow('VIDI',frame)
    cv2.imshow('Original',origframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release midi/capture after finished
cap.release()
cv2.destroyAllWindows()
del midiout
