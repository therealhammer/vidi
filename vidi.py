#!/usr/bin/env python3
import numpy as np
import cv2
import rtmidi
import tkinter as tk

ProgState = ""

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
		self.midiout = rtmidi.MidiOut()
		available_ports = self.midiout.get_ports()
		for i, item in enumerate(available_ports):
			if(portname == item and not self.midiout.is_port_open()):
				self.midiout.open_port(i, self.name)
				print("Opened" + str(i) + item + portname)
		else:
			return "No Port available. Opened none"
		
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
			self.midiout.send_message([0x90, self.previousnote[1], 0])
			self.midiout.send_message(notetoplay) 
			self.previousnote =notetoplay

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
			basenote = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
			startnote = basenote.index(startnote) + 36
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
			for i in range(0, 40, 5):
				self.scalearray.append(startnote + 0 + j)
				self.scalearray.append(startnote + 3 + j)
				self.scalearray.append(startnote + 5 + j)
				self.scalearray.append(startnote + 6 + j)
				self.scalearray.append(startnote + 7 + j)
				self.scalearray.append(startnote + 10 + j)
				j = j +12


class vidi:
	tkwindow = tk.Tk()
	settingsframe = tk.Frame(tkwindow)
	cap = cv2.VideoCapture(0)
	rows = 0
	n_in_rows = 0
	width = int(cap.get(3))
	height = int(cap.get(4))
	notearray = []
	def setup(self):
		print("VIDI by Thierry und Fia. Press q to quit.")
		print("Video is " + str(self.width) + "x" + str(self.height) + " big")
		self.tkwindow.title("VIDI Main Menu")
		self.settingsframe.grid(column=0,row=0, sticky=(tk.N,tk.W,tk.E,tk.S) )
		tk.Label(self.settingsframe, text="Width:").grid(row = 0, column = 0, sticky=(tk.E))
		tk.Label(self.settingsframe, text="Height:").grid(row = 1, column = 0, sticky=(tk.E))
		addButton = tk.Button(self.settingsframe, text='Add new color', command=lambda: self.newColor(self))
		addButton.grid(row = 100, column = 10)
		widthSlider = tk.Scale(self.settingsframe, from_=1, to=40, orient=tk.HORIZONTAL)
		widthSlider.grid(row = 0, column = 1)
		heightSlider = tk.Scale(self.settingsframe, from_=1, to=30, orient=tk.HORIZONTAL)
		heightSlider.grid(row = 1, column = 1)
		startButton = tk.Button(self.settingsframe, text='Start Midi', command=lambda: self.startLoop(self, heightSlider.get(), widthSlider.get()))
		startButton.grid(row = 101, column = 10)
		self.tkwindow.mainloop()

	def newColor(self):
		o = note()
		self.notearray.append(o)
		self.editColor(self, self.notearray[-1])

	def editColor(self, o):
		self.getColorWindow(self, o)
		self.noteSettings(self, o)
		self.updateNotes(self)

	def updateNotes(self):
		i = 0
		for o in self.notearray:
			tk.Button(self.settingsframe, text="Edit" , command=lambda: self.editColor(self, o)).grid(row=i, column=3)
			tk.Label(self.settingsframe, text=o.name, background=o.getColorHex()).grid(row=i, column=2)
			i = i + 1
	
	def getColorWindow(self, o):
		global ProgState
		ProgState = "SELECTCOL"
		cv2.namedWindow('getColor')
		cv2.setMouseCallback('getColor', self.mouseEvent)
		cv2.createTrackbar('Range R','getColor',0,255,self.sliderEvent)
		cv2.createTrackbar('Range G','getColor',0,255,self.sliderEvent)
		cv2.createTrackbar('Range B','getColor',0,255,self.sliderEvent)
		cv2.setTrackbarPos('Range R','getColor', 30)
		cv2.setTrackbarPos('Range G','getColor', 30)
		cv2.setTrackbarPos('Range B','getColor', 30)
		midpoint = (self.width//2, self.height//2)
		while(ProgState != "END"):
			ret, frame = self.cap.read()
			frame = cv2.flip(frame, 1)
			newcol = frame[self.height//2, self.width//2]
			text = ""
			o.r_range = cv2.getTrackbarPos('Range R','getColor')
			o.g_range = cv2.getTrackbarPos('Range G','getColor')
			o.b_range = cv2.getTrackbarPos('Range B','getColor')
			if(ProgState == "SELECTCOL"):
				cv2.circle(frame, midpoint, 15, [int(newcol[0]), int(newcol[1]), int(newcol[2])] , 4)
				text = "Double Click to get color"
			elif(ProgState == "NEWCOL"):
				o.setColor(newcol)
				ProgState = "SETRANGE"
				text = "Color Set"
			elif(ProgState == "SETRANGE"):
				frame = self.maskFrame(self, frame, o.getColorLow(), o.getColorHigh())
				text = "Double Click to set range"
				maxLoc = self.brightestGaussian(self, frame, 21)
				cv2.circle(frame, maxLoc, 21, [255,255,255], 2)
				cv2.circle(frame, midpoint, 15, o.getColorNoNP(), 4)
			cv2.putText(frame, text, (0, int(self.height//1.1)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
			cv2.imshow('getColor', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		ProgState = ""
		cv2.destroyWindow("getColor")

	def noteSettings(self, o):
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

		name = tk.StringVar(mainframe)
		name.set(o.name)
		NameWdg = tk.Entry(mainframe, textvariable=name)
		NameWdg.grid(row=0, column=1, sticky=tk.W)

		ports = o.getMidiPorts()
		ports.append("None")
		miditkvar = tk.StringVar(mainframe)
		miditkvar.set("None")
		midiDrop = tk.OptionMenu(mainframe, miditkvar, *ports)
		midiDrop.grid(row=1, column=1, sticky=tk.W)

		ColorWdg = tk.Text(mainframe, height=1, width=10, background=o.getColorHex())
		ColorWdg.grid(row=2, column=1, sticky=tk.W)
		ColorWdg.insert(tk.END, str(o.getColor()))
		ColorWdg.config(state=tk.DISABLED)

		RangeWdg = tk.Text(mainframe, height=1, width=10)
		RangeWdg.grid(row=3, column=1, sticky=tk.W)
		RangeWdg.insert(tk.END, str(o.getRange()))
		RangeWdg.config(state=tk.DISABLED)

		noteArray = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
		notetkvar = tk.StringVar(mainframe)
		notetkvar.set("c")
		StartNote = tk.OptionMenu(mainframe, notetkvar, *noteArray)
		StartNote.grid(row=4, column=1, sticky=tk.W)

		scaleArray = ["Chromatic", "Maj", "Min", "Pentatonic", "Blues"]
		scaletkvar = tk.StringVar(mainframe)
		scaletkvar.set("Chromatic")
		NoteScale = tk.OptionMenu(mainframe, scaletkvar, *scaleArray)
		NoteScale.grid(row=5, column=1, sticky=tk.W)

		finishButton = tk.Button(mainframe, text="Save", command=lambda: f.set(1))
		finishButton.grid(row = 6, column = 4)
		tknote.protocol("WM_DELETE_WINDOW", self.checkBoxEvent)
		tknote.wait_variable(f)
		#TODO Saven der Einstellungen

		o.name = name.get()
		o.setMidi(miditkvar.get())
		o.setScale(scaletkvar.get(), notetkvar.get())
		tknote.destroy()

	def startLoop(self, rows, n_in_rows):
		global ProgState
		cv2.namedWindow('VIDI')
		cv2.setMouseCallback('VIDI', self.mouseEvent)
		ProgState = "MAINLOOP"
		while(ProgState == "MAINLOOP"):
			ret, origframe = self.cap.read()
			origframe = cv2.flip(origframe, 1)
			mask = cv2.inRange(origframe, np.array([0,0,0]), np.array([0,0,0]))
			frame = cv2.bitwise_and(origframe, origframe, mask=mask)
			frames = []
			for o in self.notearray:
				mask = cv2.inRange(origframe, o.getColorLow(), o.getColorHigh())
				frames.append(cv2.bitwise_and(origframe, origframe, mask=mask))#TODO
				#spot = self.brightestGaussian(self, frames[-1], 21)
				#rect = [int((spot[0]/self.height)*n_in_rows), int((spot[1]/self.width)*rows)]
				rect = self.brightestOld(self, frames[-1], rows, n_in_rows)
				frames[-1] = cv2.rectangle(frames[-1], (int((self.width/n_in_rows)*rect[1]), int((self.height/rows)*rect[0])), (int((self.width/n_in_rows)*(rect[1]+1)), int((self.height/rows)*(rect[0]+1))), o.getColorNoNP(),3)
				frame = cv2.add(frame, frames[-1])
				o.playNote(rect[1], int((rect[0]/rows)*128))
			frame = self.addGrid(self, frame, rows, n_in_rows)
			cv2.imshow("VIDI", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cv2.destroyWindow("VIDI")
			

	def addGrid(self, frame, rows, n_in_rows):
		color = (255, 255, 255)
		for i in range(rows+1):
			cv2.line(frame, (0, int((self.height/rows)*(i))), (self.width, int((self.height/rows)*(i))), color, 1, 1)
		for i in range(n_in_rows+1):
			cv2.line(frame, (int((self.width/n_in_rows)*(i)), 0), (int((self.width/n_in_rows)*(i)), self.height), color, 1, 1)
		return frame

	def mouseEvent(event, x, y, flags, param):
		global ProgState
		if(event == cv2.EVENT_LBUTTONDBLCLK):
			if(ProgState == "SELECTCOL"):
				ProgState = "NEWCOL"
			elif(ProgState == "SETRANGE"):
				ProgState = "END"
			elif(ProgState == "MAINLOOP"):
				ProgState = "MAINLOOPEND"

	def sliderEvent(x):
		pass
	
	def checkBoxEvent(*x):
		pass

	def maskFrame(self, frame, colLow, colHigh):
		mask = cv2.inRange(frame, colLow,  colHigh)
		frame = cv2.bitwise_and(frame,frame, mask=mask)
		return frame

	def brightestGaussian(self, frame, radius):
		x = 0
		y = 0
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (radius, radius), 0)
		(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
		return maxLoc
	
	def brightestOld(self, frame, rows, n_in_rows):
		framearray = []
		for i in range(rows):
			framerow = []
			for j in range(n_in_rows):
				rect = frame[i*(self.height/rows):(i+1)*(self.height/rows), j*(self.width/n_in_rows):(j+1)*(self.width/n_in_rows)]
				framerow.append(cv2.cvtColor(rect, cv2.COLOR_BGR2GRAY))
			framearray.append(framerow)

		brightest = [0,0,1000] #x, y, brightness
		for i in range(rows):
			for j in range(n_in_rows):
				rectbrightness = np.sum(framearray[i][j])
				if rectbrightness > brightest[2]:
					brightest = [i, j, rectbrightness]

		return (brightest[0], brightest[1])

vid = vidi
vid.setup(vid)
