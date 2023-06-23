import os


class new_folder:
    def __init__(self):
        pass
    def make_new_folder():
        folder_dir = 'folder'
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)

