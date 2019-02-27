import argparse
import getpass
import os

parser = argparse.ArgumentParser()
parser.add_argument("--modality", help="For which task you are setting FES values", required = True)
parser.add_argument("--subject", 	help="For which subject you are setting FES values", required = True)
parser.add_argument("--session",    help="For which session you are setting FES values", required = True)
args, unknown = parser.parse_known_args()
modality = args.modality
subject = args.subject
session = args.session

user = getpass.getuser()
dataPath = "/home/" + user + "/data"
resourcesPath = dataPath + "/" + subject + "/" + session + "/"
if modality == "online":
	#print(resourcesPath + "mi_stroke_prot_online.xml")
	print(resourcesPath + "mi_stroke_prot.xml")
else:
	print(resourcesPath + "mi_stroke_prot.xml")