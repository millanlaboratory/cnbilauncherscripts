from appJar import gui
from screeninfo import get_monitors



global app 

def chooseTaskSet(button):
	global app
	if button == "Validate":
		if app.getRadioButton("taskset") == "Flexion":
			print("mi_fes_flexion")
		elif app.getRadioButton("taskset") == "Extension":
			print("mi_fes_extension")
		
	elif button == "Cancel":
		print(str(-1))
	app.stop()

# app.go
app=gui()
padding = 10;
app.setGuiPadding(padding, padding)
app.addRadioButton("taskset", "Flexion")
app.addRadioButton("taskset", "Extension")
app.addButtons(["Validate", "Cancel"], chooseTaskSet)
app.setLocation(get_monitors()[0].width/2, get_monitors()[0].height/2)

app.go()
