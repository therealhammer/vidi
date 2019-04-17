#!/usr/bin/env python3

# Important imports
import numpy as np
import cv2
import rtmidi
import tkinter as tk
import time

# Global Program State Variable
ProgState = ""

# Class for each Color/Note Object
class note:
	name = "Name"
	midiout = 0
	r = 0
	g = 0
	b = 0
	r_range = 0
	g_range = 0
	b_range = 0
	scalearray = []
	possiblenotes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
	previousnote = [0,0,0]

	def getMidiPorts(self):
		return rtmidi.MidiOut().get_ports()

	def closeMidi(self):
		try:
			self.midiout.close_port()
		except:
			del midiout

	def getMidi(self):
		return midiout.get_port_name()

	def setMidi(self, portname):
		if(self.midiout != 0):
			self.midiout.close_port()
		self.midiout = rtmidi.MidiOut()
		available_ports = self.midiout.get_ports()
		for i, item in enumerate(available_ports):
			if(portname == item and not self.midiout.is_port_open()):
				self.midiout.open_port(i, self.name)
				print("Opened" + str(i) + item + portname)
		if(self.midiout == 0):
			self.midiout.open_virtual_port(self.name)
		
	def getColor(self):
		return np.array([self.r, self.g, self.b])

	def getRange(self):
		return np.array([self.r_range, self.g_range, self.b_range])

	def getColorNoNP(self):
		return [int(self.b), int(self.g), int(self.r)]

	def getColorHex(self):
		returner = '#%02x%02x%02x' % (self.r, self.g, self.b)
		return returner

	def setColor(self, rgb):
		self.r = rgb[2]
		self.g = rgb[1]
		self.b = rgb[0]

	def playNote(self, notenr, loudness):
		notetoplay = [0x90, self.scalearray[notenr], loudness]
		if(self.previousnote != notetoplay):
			self.midiout.send_message([0x80, self.previousnote[1], 0])
			self.midiout.send_message(notetoplay) 
			self.previousnote = notetoplay

	def getColorLow(self):
		r = self.r - self.r_range
		g = self.g - self.g_range
		b = self.b - self.b_range
		return np.array([b, g, r])

	def getColorHigh(self):
		r = self.r + self.r_range
		g = self.g + self.g_range
		b = self.b + self.b_range
		return np.array([b, g, r])

	def setScale(self, scale, startnote):
		self.scalearray = []
		if(type(startnote) == type(str())):
			startnote = self.possiblenotes.index(startnote) + 36
		if (scale == "Chromatic"):
			for i in range(40):
				self.scalearray.append(startnote + i)
		elif(scale == "Maj"):
			j = 0
			for i in range(0, 40, 7):
				self.scalearray.append(startnote + 0 + j)
				self.scalearray.append(startnote + 2 + j)
				self.scalearray.append(startnote + 4 + j)
				self.scalearray.append(startnote + 5 + j)
				self.scalearray.append(startnote + 7 + j)
				self.scalearray.append(startnote + 9 + j)
				self.scalearray.append(startnote + 11 + j)
				j = j +12
		elif(scale == "Min"):
			j = 0
			for i in range(0, 40, 7):
				self.scalearray.append(startnote + 0 + j)
				self.scalearray.append(startnote + 2 + j)
				self.scalearray.append(startnote + 3 + j)
				self.scalearray.append(startnote + 5 + j)
				self.scalearray.append(startnote + 7 + j)
				self.scalearray.append(startnote + 8 + j)
				self.scalearray.append(startnote + 10 + j)
				j = j +12
		elif(scale == "Pentatonic"):
			j = 0
			for i in range(0, 40, 5):
				self.scalearray.append(startnote + 0 + j)
				self.scalearray.append(startnote + 2 + j)
				self.scalearray.append(startnote + 4 + j)
				self.scalearray.append(startnote + 7 + j)
				self.scalearray.append(startnote + 9 + j)
				j = j +12
		elif(scale == "Blues"):
			j = 0
			for i in range(0, 40, 6):
				self.scalearray.append(startnote + 0 + j)
				self.scalearray.append(startnote + 3 + j)
				self.scalearray.append(startnote + 5 + j)
				self.scalearray.append(startnote + 6 + j)
				self.scalearray.append(startnote + 7 + j)
				self.scalearray.append(startnote + 10 + j)
				j = j +12

# Main Class 
class vidi:
	# Tkinter Window
	tkwindow = tk.Tk()
	settingsframe = tk.Frame(tkwindow)

	# Capturing the main Webcam and getting its size
	cap = cv2.VideoCapture(0)
	width = int(cap.get(3))
	height = int(cap.get(4))

	# Objects of playable Midi-Color connections
	notearray = []

	# Main window 
	def setup(self):
		print("VIDI by Thierry und Fia. Press q to quit.")
		print("Video is " + str(self.width) + "x" + str(self.height) + " big")

		#TKinter setting up main window
		self.tkwindow.title("VIDI Main Menu")
		self.settingsframe.grid(column=0,row=0, sticky=(tk.N,tk.W,tk.E,tk.S) )
		tk.Label(self.settingsframe, text="Width:").grid(row = 0, column = 0, sticky=(tk.E))
		tk.Label(self.settingsframe, text="Height:").grid(row = 1, column = 0, sticky=(tk.E))
		addButton = tk.Button(self.settingsframe, text='Add new color', command=lambda: self.newColor(self))
		addButton.grid(row = 100, column = 10)
		w = tk.IntVar()
		h = tk.IntVar()
		gauss = tk.BooleanVar()
		w.set(12)
		h.set(8)
		tk.Label(self.settingsframe, textvariable=w).grid(row=0, column=1)
		tk.Label(self.settingsframe, textvariable=h).grid(row=1, column=1)
		wSlider = tk.Scale(self.settingsframe, showvalue=False, from_=1, to=40, variable=w, orient=tk.HORIZONTAL)
		wSlider.grid(row = 0, column = 2)
		hSlider = tk.Scale(self.settingsframe, showvalue=False, from_=1, to=30, variable=h, orient=tk.HORIZONTAL)
		hSlider.grid(row = 1, column = 2)
		tk.Radiobutton(self.settingsframe, text="Gauss Filter", variable=gauss, value = True).grid(row=2, column = 1)
		tk.Radiobutton(self.settingsframe, text="Threshhold Filter", variable=gauss, value = False).grid(row=3, column = 1)
		startButton = tk.Button(self.settingsframe, text='Start Midi', command=lambda: self.startLoop(self, h.get(), w.get(), gauss.get()))
		startButton.grid(row = 101, column = 10)
		self.tkwindow.mainloop()

	# Adding a new color object
	def newColor(self):
		o = note()
		self.notearray.append(o)
		self.editColor(self, self.notearray[-1])

	# Editing a color object
	def editColor(self, o):
		self.getColorWindow(self, o)
		self.noteSettings(self, o)
		self.updateNotes(self)

	# Removing a color object
	def deleteColor(self, o):
		self.notearray.remove(o)
		self.updateNotes(self)

	# Updating notes in main window
	def updateNotes(self):
		i = 0
		for tkobject in self.settingsframe.grid_slaves():
			col = int(tkobject.grid_info()["column"]) 
			row = int(tkobject.grid_info()["row"]) 
			if(3 <= col and col <= 5):
				tkobject.grid_forget()
		for o in self.notearray:
			tk.Button(self.settingsframe, text="Edit" , command=lambda note=o: self.editColor(self, note)).grid(row=i, column=4)
			tk.Button(self.settingsframe, text="Delete" , command=lambda note=o: self.deleteColor(self, note)).grid(row=i, column=5)
			tk.Label(self.settingsframe, text=o.name, background=o.getColorHex()).grid(row=i, column=3)
			i = i + 1
		

	# Extracting color from webcam image
	def getColorWindow(self, o):
		global ProgState
		ProgState = "SELECTCOL"

		# Open CV Window setup
		cv2.namedWindow('getColor')
		cv2.setMouseCallback('getColor', self.mouseEvent)
		cv2.createTrackbar('Range R','getColor',0,255,self.sliderEvent)
		cv2.createTrackbar('Range G','getColor',0,255,self.sliderEvent)
		cv2.createTrackbar('Range B','getColor',0,255,self.sliderEvent)
		cv2.setTrackbarPos('Range R','getColor', 30)
		cv2.setTrackbarPos('Range G','getColor', 30)
		cv2.setTrackbarPos('Range B','getColor', 30)
		midpoint = (self.width//2, self.height//2)

		# Loop processing the camera image
		while(ProgState != "END"):
			ret, frame = self.cap.read()
			# Flip frame because mirror image is less confusing than the original
			frame = cv2.flip(frame, 1)
			newcol = frame[self.height//2, self.width//2]
			text = ""
			o.r_range = cv2.getTrackbarPos('Range R','getColor')
			o.g_range = cv2.getTrackbarPos('Range G','getColor')
			o.b_range = cv2.getTrackbarPos('Range B','getColor')

			# Setting the color
			if(ProgState == "SELECTCOL"):
				cv2.circle(frame, midpoint, 15, [int(newcol[0]), int(newcol[1]), int(newcol[2])] , 4)
				text = "Double Click to get color"
			elif(ProgState == "NEWCOL"):
				o.setColor(newcol)
				ProgState = "SETRANGE"
				text = "Color Set"

			# Setting the range
			elif(ProgState == "SETRANGE"):
				frame = self.maskFrame(self, frame, o.getColorLow(), o.getColorHigh())
				text = "Double Click to set range"
				maxLoc = self.brightestGaussian(self, frame, 21)
				cv2.circle(frame, maxLoc, 21, [255,255,255], 2)
				cv2.circle(frame, midpoint, 15, o.getColorNoNP(), 4)

			# Displaying image and text in CV window
			cv2.putText(frame, text, (0, int(self.height//1.1)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
			cv2.imshow('getColor', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		ProgState = ""
		cv2.destroyWindow("getColor")

	# Settings Window for notes and colors
	def noteSettings(self, o):
		# Tkinter main setup
		tknote = tk.Tk()
		f = tk.IntVar(tknote)
		tknote.title("Edit new note")
		mainframe = tk.Frame(tknote)
		mainframe.grid(column=0,row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
		tk.Label(mainframe, text="Name").grid(row = 0, column = 0)
		tk.Label(mainframe, text="Midi Port").grid(row = 1, column = 0)
		tk.Label(mainframe, text="Color RGB").grid(row = 2, column = 0)
		tk.Label(mainframe, text="Range RGB").grid(row = 3, column = 0)
		tk.Label(mainframe, text="Start Note").grid(row = 4, column = 0)
		tk.Label(mainframe, text="Note Scale").grid(row = 5, column = 0)

		# Name of Connection
		name = tk.StringVar(mainframe)
		name.set(o.name)
		NameWdg = tk.Entry(mainframe, textvariable=name)
		NameWdg.grid(row=0, column=1, sticky=tk.W)

		# Set Midi Port
		ports = o.getMidiPorts()
		ports.append("None")
		miditkvar = tk.StringVar(mainframe)
		miditkvar.set("None")
		midiDrop = tk.OptionMenu(mainframe, miditkvar, *ports)
		midiDrop.grid(row=1, column=1, sticky=tk.W)

		# Display color and range
		ColorWdg = tk.Text(mainframe, height=1, width=10, background=o.getColorHex())
		ColorWdg.grid(row=2, column=1, sticky=tk.W)
		ColorWdg.insert(tk.END, str(o.getColor()))
		ColorWdg.config(state=tk.DISABLED)

		RangeWdg = tk.Text(mainframe, height=1, width=10)
		RangeWdg.grid(row=3, column=1, sticky=tk.W)
		RangeWdg.insert(tk.END, str(o.getRange()))
		RangeWdg.config(state=tk.DISABLED)

		# Set start note
		noteArray = o.possiblenotes
		notetkvar = tk.StringVar(mainframe)
		notetkvar.set("c")
		StartNote = tk.OptionMenu(mainframe, notetkvar, *noteArray)
		StartNote.grid(row=4, column=1, sticky=tk.W)

		# Set note scale
		scaleArray = ["Chromatic", "Maj", "Min", "Pentatonic", "Blues"]
		scaletkvar = tk.StringVar(mainframe)
		scaletkvar.set("Chromatic")
		NoteScale = tk.OptionMenu(mainframe, scaletkvar, *scaleArray)
		NoteScale.grid(row=5, column=1, sticky=tk.W)

		# Save button
		finishButton = tk.Button(mainframe, text="Save", command=lambda: f.set(1))
		finishButton.grid(row = 6, column = 4)
		tknote.protocol("WM_DELETE_WINDOW", self.checkBoxEvent)
		tknote.wait_variable(f)

		o.name = name.get()
		o.setMidi(miditkvar.get())
		o.setScale(scaletkvar.get(), notetkvar.get())
		tknote.destroy()

	# Main loop for VIDI
	def startLoop(self, rows, n_in_rows, gauss):
		global ProgState
		cv2.namedWindow('VIDI')
		cv2.setMouseCallback('VIDI', self.mouseEvent)
		ProgState = "MAINLOOP"

		# Main loop displaying the midi grid and image
		while(ProgState == "MAINLOOP"):
			# Get frame and create a black backround frame to add stuff later
			ret, origframe = self.cap.read()
			origframe = cv2.flip(origframe, 1)
			mask = cv2.inRange(origframe, np.array([0,0,0]), np.array([0,0,0]))
			frame = cv2.bitwise_and(origframe, origframe, mask=mask)

			# Process every color-note object in a for loop
			frames = []
			for o in self.notearray:
				# Get mask 
				mask = cv2.inRange(origframe, o.getColorLow(), o.getColorHigh())
				frames.append(cv2.bitwise_and(origframe, origframe, mask=mask))

				# Apply filter and get location of the colored object 
				if (gauss == True):
					rect = self.brightestGaussianRect(self, frames[-1], 21, rows, n_in_rows)
				else:
					rect = self.brightestRect(self, frames[-1], rows, n_in_rows)

				# Surround rectangle with object in it with color
				rectA = (int((self.width/n_in_rows)*rect[1]), int((self.height/rows)*rect[0]))
				rectB = (int((self.width/n_in_rows)*(rect[1]+1)), int((self.height/rows)*(rect[0]+1)))
				frames[-1] = cv2.rectangle(frames[-1], rectA, rectB, o.getColorNoNP(),5)

				# Add masked frame and rectangle to displaying frame
				frame = cv2.add(frame, frames[-1])

				# Play the corresponding midi note
				o.playNote(rect[1], int((rect[0]/rows)*128))

			# Add grid to frame and show 
			frame = self.addGrid(self, frame, rows, n_in_rows)
			cv2.imshow("VIDI", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# Quit Midi loop
		cv2.destroyWindow("VIDI")
			
	# Adding grid to frame
	def addGrid(self, frame, rows, n_in_rows):
		color = (255, 255, 255)
		for i in range(rows+1):
			cv2.line(frame, (0, int((self.height/rows)*(i))), (self.width, int((self.height/rows)*(i))), color, 1, 1)
		for i in range(n_in_rows+1):
			cv2.line(frame, (int((self.width/n_in_rows)*(i)), 0), (int((self.width/n_in_rows)*(i)), self.height), color, 1, 1)
		return frame

	# Change program state
	def mouseEvent(event, x, y, flags, param):
		global ProgState
		if(event == cv2.EVENT_LBUTTONDBLCLK):
			if(ProgState == "SELECTCOL"):
				ProgState = "NEWCOL"
			elif(ProgState == "SETRANGE"):
				ProgState = "END"
			elif(ProgState == "MAINLOOP"):
				ProgState = "MAINLOOPEND"

	# Get only relevant color out of Frame
	def maskFrame(self, frame, colLow, colHigh):
		mask = cv2.inRange(frame, colLow,  colHigh)
		frame = cv2.bitwise_and(frame,frame, mask=mask)
		return frame

	# Get brightest rectangle by gaussian filter
	def brightestGaussianRect(self, frame, radius, rows, n_in_rows):
		spot = self.brightestGaussian(self, frame, radius)
		y = int(n_in_rows*(spot[0]/self.width))
		x = int(rows*(spot[1]/self.height))
		print(str(x) + " " + str(y))
		return (x, y)
		
	# Get brightest spot by gaussian filter
	def brightestGaussian(self, frame, radius):
		x = 0
		y = 0
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (radius, radius), 0)
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
		return maxLoc
	
	# Get brightest rectangle by adding pixels in rectangle together
	def brightestRect(self, frame, rows, n_in_rows):
		# Slice the frame in little frames
		framearray = []
		for i in range(rows):
			framerow = []
			for j in range(n_in_rows):
				rect = frame[i*(self.height/rows):(i+1)*(self.height/rows), j*(self.width/n_in_rows):(j+1)*(self.width/n_in_rows)]
				framerow.append(cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY))
			framearray.append(framerow)

		# Get the brightest frame
		brightest = [0,0,1000] #x, y, brightness
		for i in range(rows):
			for j in range(n_in_rows):
				rectbrightness = np.sum(framearray[i][j])
				if rectbrightness > brightest[2]:
					brightest = [i, j, rectbrightness]
		return (brightest[0], brightest[1])

	# Unused Events
	def sliderEvent(x):
		pass
	
	def checkBoxEvent(*x):
		pass



# Start Program
vid = vidi
vid.setup(vid)
