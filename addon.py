import os
import xbmcaddon
import xbmcgui
import subprocess

addon 		= xbmcaddon.Addon()
addonname 	= addon.getAddonInfo('name')
addonpath	= addon.getAddonInfo('path').decode("utf-8")
dialog		= xbmcgui.Dialog()
ffile		= addonpath+"/getedid" 
info = "This script will dump the EDID information to simulate a monitor"
info2 = "Select 'Continue' if you want to use it or 'Cancel' to exit"

def intro():
	intro = dialog.yesno(addonname, info, info2, "", "Cancel", "Continue")
	if intro == True:
		selectionWindow()
	else:
		quit()

def selectionWindow():
	choice = dialog.select(addonname, ['create (will create the EDID dump)',
					 'delete (will delete an existing EDID dump)',
					 'gpu (will show the GPU in use)',
					 'help (will show a help-message)'])
	choice=str(choice)
	if choice == "0":
		command(ffile, "create")
	elif choice == "1":
		command(ffile, "delete")
	elif choice == "2":
		command(ffile, "gpu")
	elif choice == "3":
		hhelp()
	else:
		quit()

def command(comm, arg):
	output = subprocess.Popen([(ffile), (arg)], stdout=subprocess.PIPE).communicate()[0]
	output=str(output)
	if output == "nvidia":
		l = dialog.yesno(addonname, "You are using a supported GPU (NVidia)", "Continue?")
		if l == True:
			selectionWindow()
		else:
			quit()
	if output == "intel":
		l = dialog.yesno(addonname, "You are using a supported GPU (Intel)", "Continue?")
		if l == True:
			selectionWindow()
		else:
			quit()
	if output == "nvidia success":
		dialog.ok(addonname, "The script ran successfully", "You don't need to reboot the machine")
		quit()
	if output == "intel success":
		dialog.ok(addonname, "The script ran successfully", "The machine will reboot after you hit 'OK'")
		os.system("reboot")
	
	else:
		dialog.ok(addonname, "Error", output)
		quit()

def hhelp():
	dialog.ok(addonname, "'create' will create the EDID dump", "'delete' will revert the changes being done by that script", "'gpu' will show which GPU is in use and if it's supported")
	selectionWindow()

intro()

