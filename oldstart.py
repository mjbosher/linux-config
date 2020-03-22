import os
import platform
import importlib
import getpass
import subprocess
from subprocess import Popen, PIPE
import urllib
from urllib import request
user= getpass.getuser()
user = user.rstrip()

filepath = "/media/" + user + "/Back-up/Linux-setup"
print(filepath)
configfolder = '/'.join([filepath,'files'])
targetpath ="/home/" + user + "/Linux-setup/"
passwordfile = '{0}/details.txt'.format(configfolder)
userfile = '{0}/users.txt'.format(configfolder)
copypath = "/home/" + user + "/"
nopass = "{0}/nopass".format(configfolder)
bash = "{0}/bash".format(configfolder)
configfolderhome = '/'.join([targetpath,'files'])   
install = "{0}/install.txt".format(configfolderhome)
uninstall = "{0}/uninstall.txt".format(configfolderhome)
reps = "{0}/reps.txt".format(configfolderhome)
modules = "{0}/imports.txt".format(configfolderhome)
errors = "{0}/errors".format(configfolderhome)
mods = "{0}/mods.py".format(configfolderhome)
class File_Check:
	def config_filecheck():
		if os.path.isdir(targetpath) == False:
			print('Setting up the system now')
			os.system('cp -r ' + filepath + " " + copypath)
			global a
			a = userconfig()
			d = User_Specifics.root_priv_input()              
			File_Check.sudoer_filecheck()
			d.passwordless_user()
			genericconfig()
			a.initiate()
			User_Specifics.make_bash('Flash')

		elif os.path.isdir(targetpath) == True and os.path.isdir(filepath) == True:
			print("Everything is set-up")
			try:    
				urllib.request.urlopen('http://www.yahoo.co.uk')              
				User_Specifics.rep_install()
				User_Specifics.emptyfile()
				User_Specifics.checkforerrors(User_Specifics.prog_install)
				User_Specifics.checkforerrors(User_Specifics.mod_install)
				User_Specifics.removestartup()
			except IOError:
				print('NO INTERNET CONNECTION\n')
		elif os.path.isdir(targetpath) == True and os.path.isdir(copypath) == False:
			print('Setting up the system now')
			os.system('cp -r ' + filepath + " " + targetpath)
			os.system('cp -r ' + filepath + " " + copypath)
			a = userconfig()
			d = User_Specifics.root_priv_input()              
			File_Check.sudoer_filecheck()
			d.passwordless_user()
			genericconfig()
			a.initiate()
			User_Specifics.make_bash('Flash')
	def sudoer_filecheck():
		if os.path.isfile(nopass) == True:
			print("SUDOER EXISTS")
			os.remove(nopass)
			os.mknod(nopass)
			print("EMPTIED THE PSUDOER FILE")
		elif os.path.isfile(nopass) == False:
			os.mknod(nopass)
			print("CREATED THE SUDOER FILE")
		else:
			print("ERROR")

class genericconfig():
	def __init__(self):
		apport = '/'.join([configfolder,'apport'])
		tilda = '/'.join([configfolder, 'tilda'])
		tildascript = '/'.join([configfolder, 'tilda.py'])		
		copyapport = 'sudo cp {0} /etc/default/apport'.format(apport)
		os.system(copyapport)
		os.system('sudo chown root:root /etc/default/apport')
		copytildascript = ('sudo cp {0} /tilda.py').format(tildascript)
		copytilda = ('sudo cp -r {0} /home/tilda').format(tilda)
		os.system(copytildascript)
		os.system(copytilda)
		startupscript = '{0}/startup'.format(configfolder)
		startupscript = 'cp {0} ~/.startup'.format(startupscript)
		os.system(startupscript)

class userconfig():
	def __init__(self):
		self.userlist={}
		self.kb = {}
		username = ''
		while username != 'Exit' or username != 'exit':
			username = input(' input the NAME of the USER to add or type exit to quit: ')
			if username == 'Exit' or username == 'exit':
				break;			
			password =input('input password:')
			kb = input('DISABLE KEYBOARD: ')
			self.userlist[username] = password
			self.kb[username] = kb
	def initiate(self):
		for self.username, self.password in self.userlist.items():
			self.adduser()
			a.generatefiles()
			self.profileconfig()
			

	def adduser(self):
		name = '{0}\n'.format(self.username)
		password = '{0}\n'.format(self.password)
		command = 'adduser {0} --home /home/{0}/  --ingroup michael'.format(self.username)
		command =command.split()
		p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(password  + password + name + '\n'+'\n'+'\n'+'\n'+'y\n')[1]
	def generatefiles(self):
		inputlist = ['profile', 'bash','cleanup','yulia.conf','michael.conf','laptopkb']
		outputlist=['.profile','.bashrc','.cleanup','x.conf','x.conf','.laptopkb']
		outputpath = '/home/{0}'.format(self.username)		
		def gen(x,y):
			newdict = {}
			for i in x:
				name = i
				path = '/'.join([y,i])
				newdict[name] = path
			return(newdict)
		inputpath=(gen(inputlist,configfolder))
		print(inputpath)
		outputpath=(gen(outputlist,outputpath))
		chown='sudo chown {0}:michael'.format(self.username)
		chmod = 'sudo chmod 777'
		def Commands(x,c):		
			commandlist = {}
			for name,path in x.items():
				command = ' '.join([c,path])
				commandlist[name] = command
			return commandlist
		def copy(x,y):
			cp = 'sudo cp -r'
			commands = []
			for name,path in x.items():
				command = ' '.join([cp,path])
				for name1,path1 in y.items():
					if name in path1:
						command = ' '.join([command, path1])
					if name.endswith('.conf') and name in path and 'x.conf' in name1:
						command = ' '.join([command, path1])
				commands.append(command)
			counter = 0
			Commands = {}
			for name,path in x.items():
				for commandname in commands:
					if name in commandname:
						Commands[name] = commandname
			return Commands
						
			
		chmod=(Commands(outputpath,chmod))		
		chown=(Commands(outputpath,chown))
		Copy=(copy(inputpath,outputpath))
		self.fullcommandlist = (Copy,chmod,chown)
		
	def profileconfig(self):
		for i in self.fullcommandlist:
			for name,command in i.items():
				if self.username != 'michael' and command.endswith('.conf') and 'yulia.conf' in command:
					os.system(command)
				elif self.username == 'michael' and command.endswith('.conf') and 'michael.conf' in command:
					print(command)
					os.system(command)
				elif 'x.conf' in command and 'michael.conf' not in command and 'yulia.conf' not in command:
					os.system(command)
				elif 'laptopkb' in command and self.kb[self.username] == 'yes':
					os.system(command)
				elif '.conf' not in command and 'laptopkb' not in command:
					os.system(command)
					print(command)



class User_Specifics():
	def __init__(self, passwords, names):
		self.passwords = passwords
		global thispassword
		thispassword = passwords
		self.names = names
        
	def passwordless_user(self):
		f = open(nopass,'a')
		print("ASSIGNED ROOT PRIVILEDGES TO:")
		for i in self.names:
			f.writelines(i + ' ALL=(ALL) NOPASSWD: ALL\n')
			print(i + ' ALL=(ALL) NOPASSWD: ALL\n')
		f.close()        
		os.system("pwd")
		print("IN SETTINGS DIRECTORY")
		command = ('sudo -i cp ' + nopass + ' /etc/sudoers.d/').split()
		print("COPYING SUDOERS")
		p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
		sudo_prompt = p.communicate(self.passwords  + '\n')[1]        
		print("SUCCESFULLY COPIED SUDOERS\nSUDO NOW HAS PASSWORDLESS ROOT PRIVILEDGES")
		os.system("sudo chmod -R ugo=rwx /home/")
		os.system("sudo chown -R "+user+":"+user + " /home/")
		print("HOMEFOLDER OWNERSHIP AND PERMISSIONS HAVE BEEN CHANGED")
        
	def make_bash(overide):
		if platform.dist() == ('Ubuntu', '17.10', 'artful') or platform.dist == ('Ubuntu', '18.04', 'bionic') or overide == 'Flash':
			print("YOU ARE USING LINUX MATE ZESTY ZAPUS\nCOPYING MATE BASH FILE")
			os.system(" sudo -i mv /home/" + user + "/.bashrc /home/" + user + "/oldbash")
			print("SCRAPPED OLD BASH")
			os.system("sudo -i cp " + bash +' '+ "/home/" + user + "/.bashrc")
			print("BASHFILE SET-UP SUCCESFULLY")
			command = 'su - {0}'.format(user)
			command =command.split()
			p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True)
			sudo_prompt = p.communicate(thispassword + '\n')[1]
		else:
			print("SOMETHING WENT WRONG")

	def emptyfile():
		if os.path.exists(errors):
			os.remove(errors)
			os.mknod(errors)
		else:
			os.mknod(errors)
	def filelist():
		toinstall = [i.rstrip() for i in open(install) if i !='\n']
		comp = [x  for x in os.listdir('/usr/share/applications')]
		installed = set()
		notinstalled = set()	
		def checkfilename(name):
			for i in comp:
				if name in i:
					installed.add(name)
				elif name not in i:
					notinstalled.add(name)
		for i in toinstall:
			checkfilename(i)
		notinstalled = notinstalled - installed
		omit = {'git', 'alien', 'unzip -y', 'libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 -y', 'woeusb -y', 'conky','python-pip', 'python3-pip', 'wmctrl', 'xdotool', 'fcitx.bin', 'gnome-tweak-tool', 'virtualenv', 'wireshark-qt', '-f dpkg --add-architecture i386', 'ettercap-text-only', 'fbreader', 'libavcodec-extra', 'qt4-qtconfig', 'vector'}
		notinstalled = notinstalled - omit
		return(list(notinstalled))
	def importlist():
		imports = [x.split(' ')[1].rstrip() for x in open(mods)]
		missing = set()
		omit = {'libcloud','djlibcloud','fs'}
		for x in imports:
			try:
				importlib.import_module(x)
			except ImportError:
				missing.add(x)
		return(list(missing-omit))
	def checkforerrors(func):
		x = 0
		f = open(errors,'a')
		name = func
		func = func()
		while func != [] or x != 10:
			if x == 10:
				f.write(str(func)+'\n')
				break;
			x = x+1
		f.close()
		if func == User_Specifics.mod_install:
			os.system('gedit ' + errors)
		

	def removestartup():
		f = open(errors)
		lines = [x for x in f]
		if lines == []:
			startupscript = '~/.startup'.format(configfolder)
			startupscript = 'rm {0} ~/'.format(startupscript)
			os.system(startupscript)
			script = '{0}/script'.format(configfolderhome)
			c = 'cp {0} ~/.script'.format(script)
			os.system(c)
			os.system('sudo reboot')
			
		
                        
	def prog_install():
		i = open(install)
		u = open(uninstall)
		installprog = i.readlines()
		uninstallprog = u.readlines()
		DFC = [ x for x in uninstallprog]
		for line in DFC:
			line = line.rstrip()
			os.system("sudo -i apt purge " + line +  " -y")
			print("UNINSTALLED " + line)
			DFC = [ x for x in installprog]
                
		for line in DFC:
			line = line.rstrip()
			os.system("sudo -i apt install " + line +  " -y")
			print("INSTALLED " + line)
		return(list(User_Specifics.filelist()))
            
	def rep_install():
		f = open(reps, 'r')
		for lines in f:
			os.system(lines)
			print ('installed' + lines)
	def mod_install():
		f = open(modules, 'r')
		for lines in f:
			os.system(lines)
			print ('installed ' + lines)
		return(list(User_Specifics.importlist()))
	@classmethod
	def root_priv_input(cls):
		namelist = []
		print("THESE FILES ARE USED TO STORE DATA ABOUT YOUR OPERATING SYSTEM\n\n")
		confirm1 = input("\n\nDO YOU WANT TO ADD  USERS TO THE PRIVILEDGE LIST?   ")
		while confirm1 == "yes":            
			names = input("TYPE A USERNAME TO GIVE IT ROOT PRIVILEDGES    ")
			namelist.append(names)
			confirm1 = input("\n\nDO YOU WANT TO ADD MORE USERS TO THE PRIVILEDGE LIST?   ")
			if confirm1 != "yes":
				password = input("LASTLY, INPUT YOUR PASSWORD     ")
				confirm = input("\n\nIS THE PASSWORD DISPLAYED, YOUR PASSWORD?    ")
				while confirm != "yes":
					password = input("\n\nINPUT YOUR PASSWORD   ")
					confirm = input("\n\nIS THE PASSWORD DISPLAYED, YOUR PASSWORD?    ")
                    
		return cls(password,namelist)




File_Check.config_filecheck()              
