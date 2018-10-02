import argparse
from appJar import gui
import json
import getpass
import sys

global app 
global data
global dataDouble
global dataSingle
global fileName
global task

parser = argparse.ArgumentParser()
parser.add_argument("--task", help="For which task you are setting FES values", required = True)
parser.add_argument("--subject", 	help="For which subject you are setting FES values", required = True)

args, unknown = parser.parse_known_args()
task = args.task.split("_") #split string into a list
task = task[len(task)-1]
subject = args.subject

def chooseValues(button):
 	global app
 	global task

 	if button == "Validate":
 		if task == "flexion":
	 		data["sequence"][0]["currentIncrementerParameters"][1] = app.getEntry("Max stim biceps") if app.getEntry("Max stim biceps") is not None else data["sequence"][0]["currentIncrementerParameters"][1]
	 		data["sequence"][1]["currentIncrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") is not None else data["sequence"][1]["currentIncrementerParameters"][1]
	 		data["sequence"][0]["currentDecrementerParameters"][1] = app.getEntry("Max stim biceps") if app.getEntry("Max stim biceps") is not None else data["sequence"][0]["currentDecrementerParameters"][1]
	 		data["sequence"][1]["currentDecrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") is not None else data["sequence"][1]["currentDecrementerParameters"][1]
	 		dataDouble["sequence"][0]["current"] = app.getEntry("Sensory stim biceps") if app.getEntry("Sensory stim biceps") is not None else dataDouble["sequence"][0]["current"]
	 		dataDouble["sequence"][1]["current"] = app.getEntry("Sensory stim forearm") if app.getEntry("Sensory stim forearm") is not None else dataDouble["sequence"][1]["current"]
	 	elif task == "extension":
	 		data["sequence"][0]["currentIncrementerParameters"][1] = app.getEntry("Max stim shoulder") if app.getEntry("Max stim shoulder") is not None else data["sequence"][0]["currentIncrementerParameters"][1]
	 		data["sequence"][1]["currentIncrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") is not None else data["sequence"][1]["currentIncrementerParameters"][1]
	 		data["sequence"][0]["currentDecrementerParameters"][1] = app.getEntry("Max stim shoulder") if app.getEntry("Max stim shoulder") is not None else data["sequence"][0]["currentDecrementerParameters"][1]
	 		data["sequence"][1]["currentDecrementerParameters"][1] = app.getEntry("Max stim forearm") if app.getEntry("Max stim forearm") is not None else data["sequence"][1]["currentDecrementerParameters"][1]
	 		dataDouble["sequence"][0]["current"] = app.getEntry("Sensory stim shoulder") if app.getEntry("Sensory stim shoulder") is not None else dataDouble["sequence"][0]["current"]
	 		dataDouble["sequence"][1]["current"] = app.getEntry("Sensory stim forearm") if app.getEntry("Sensory stim forearm") is not None else dataDouble["sequence"][1]["current"]
 		
 		valid = True

 		if data["sequence"][0]["currentIncrementerParameters"][1] < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if data["sequence"][1]["currentIncrementerParameters"][1] < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if data["sequence"][0]["currentIncrementerParameters"][0] < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if data["sequence"][1]["currentIncrementerParameters"][0] < 0:
 			print("Cannot set negative value for stim")
 			valid = False
 		if valid:
	 		with open(fileName, 'w') as outfile:
	 			json.dump(data, outfile, indent=4)
	 		with open(path + "/lowStimDouble.json", 'w') as f:
	 			json.dump(dataDouble, f, indent=4)
	 		with open(path + "/lowStimSingle.json", 'w') as f:
	 			json.dump(dataSingle, f, indent=4)
 	elif button == "Cancel":
 		print(str(-1))
 	app.stop()

user = getpass.getuser()
path = "/home/" + user + "/data/" + subject + "/resources"
fileName = path + "/" + task + ".json"
with open(fileName, 'r') as f:
 	data = json.load(f)
with open(path + "/lowStimDouble.json", 'r') as f:
 	dataDouble = json.load(f)
with open(path + "/lowStimSingle.json", 'r') as f:
	dataSingle = json.load(f)

# # app.go
sys.argv = [sys.argv[0]];
app=gui()
padding = 10;
app.setGuiPadding(padding, padding)
if task == "extension":
	app.addLabelNumericEntry("Max stim shoulder")
	app.addLabelNumericEntry("Max stim forearm")
	app.addLabelNumericEntry("Sensory stim shoulder")
	app.addLabelNumericEntry("Sensory stim forearm")
	app.setEntryDefault("Max stim shoulder", data["sequence"][0]["currentIncrementerParameters"][1])
	app.setEntryDefault("Max stim forearm", data["sequence"][1]["currentIncrementerParameters"][1])
	app.setEntryDefault("Sensory stim shoulder", dataDouble["sequence"][0]["current"])
	app.setEntryDefault("Sensory stim forearm", dataDouble["sequence"][1]["current"])
elif task == "flexion":
	app.addLabelNumericEntry("Max stim biceps")
	app.addLabelNumericEntry("Max stim forearm")
	app.addLabelNumericEntry("Sensory stim biceps")
	app.addLabelNumericEntry("Sensory stim forearm")
	app.setEntryDefault("Max stim biceps", data["sequence"][0]["currentIncrementerParameters"][1])
	app.setEntryDefault("Max stim forearm", data["sequence"][1]["currentIncrementerParameters"][1])
	app.setEntryDefault("Sensory stim biceps", dataDouble["sequence"][0]["current"])
	app.setEntryDefault("Sensory stim forearm", dataDouble["sequence"][1]["current"])

app.addButtons(["Validate", "Cancel"], chooseValues)
app.setLocation(500, 450)

app.go()
