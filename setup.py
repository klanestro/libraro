import os

def setup():
	dir = os.path.dirname(os.path.normpath(os.path.join(os.getcwd(), __file__)))
	print ""
	print "Libraro root: " + dir + "/libraro"
	#print "Do you want libraro set up in this directory? y/n"
	if not confirm("Do you want libraro set up in this directory?"):
		return
	os.system("git clone git://github.com/alexeiboronine/libraro.git libraro")
	os.chdir("libraro")
	f = open("local_settings.py", "w")
	f.write('ROOT_FOLDER = "' + dir + '/libraro/"')
	f.write("\n")
	f.close()
	print "Unpacking database and text files"
	os.system("./scripts.py unpack")
	if confirm("Do you want to run the Django server?"):
		os.system("python manage.py runserver")
	else:
		print 'Done. Run "python manage.py runserver" to test'

def confirm(prompt=None, resp=True):
	if prompt is None:
		prompt = 'Confirm'

	if resp:
		prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
	else:
		prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
	while True:
		ans = raw_input(prompt)
		if not ans:
			return resp
		if ans not in ['y', 'Y', 'n', 'N']:
			print 'please enter y or n.'
			continue
		if ans == 'y' or ans == 'Y':
			return True
		if ans == 'n' or ans == 'N':
			return False

if __name__ == "__main__":
	setup()
