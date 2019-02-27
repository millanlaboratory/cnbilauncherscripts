from appJar import gui

global app 

def chooseModality(button):
	global app
	if button == "Validate":
		if app.getRadioButton("modality") == "Offline":
			print("offline")
		elif app.getRadioButton("modality") == "Online":
			print("online")
		
	elif button == "Cancel":
		print(str(-1))
	app.stop()

# app.go
app=gui()
padding = 10;
app.setGuiPadding(padding, padding)
app.addRadioButton("modality", "Offline")
app.addRadioButton("modality", "Online")
app.addButtons(["Validate", "Cancel"], chooseModality)
app.setLocation(500, 450)

app.go()
