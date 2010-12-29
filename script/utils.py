import os
import shutil

def clear_folder(folder):
    folder = os.path.realpath(folder)
    for name in os.listdir(folder):
        name = os.path.join(folder, name)
        if os.path.isdir(name):
            shutil.rmtree(name, True)
        else:
            try:
                os.remove(name)
            except OSError:
                pass