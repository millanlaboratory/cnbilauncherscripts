import sys
import getpass
import os

subject = sys.argv[1]
user = getpass.getuser()
path = "/home/" + user + "/data/" + subject + "/resources"
authorizedMovementFile = path + "/AuthorizedMovements.json"
if os.path.isfile(authorizedMovementFile):
	print(authorizedMovementFile)
else:
	print(-1);