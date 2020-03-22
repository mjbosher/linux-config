import os
import getpass
user = getpass.getuser()
pathname = '/home/{0}/.cache/tilda/'.format(user)
print(pathname)
if os.path.exists(pathname):
	os.system('rm -r -f ' + pathname)
