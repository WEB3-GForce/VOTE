import os
import imp, importlib
import inspect

this_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print this_dir
src_dir = os.path.dirname(this_dir)
print src_dir

for (dirpath, dirnames, filenames) in os.walk(src_dir):
    print dirpath
    if dirpath == this_dir:
        continue

    if "__init__.py" not in filenames:
        continue

    print dirpath
    for filename in filenames:
        if filename.endswith(".py"):
            k = dirpath.rfind("/") + 1
            global_name = dirpath[k:] + "_" + filename[:-3]
            print global_name
            globals()[global_name] = imp.load_source(filename[:-3], dirpath + "/" + filename)
