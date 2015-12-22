import os
current_dir = os.path.dirname(os.path.realpath("__file__"))
os.chdir(current_dir)

execfile("database.py")
remove_all()

os.chdir(current_dir + "/../dumps")
execfile("init_db.py")

os.chdir(current_dir)
execfile("vote.py")
