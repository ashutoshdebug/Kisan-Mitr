import os
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from database.db_handler import dbHandler

databaseHandler = dbHandler()

class fileFolderPath:
    def __init__(self):
        self.formatted_string = None
        self.folder_path = None
        self.path = None
        self.new_name = None

    def createFolder(self, username):
            self.folder_path = None
            # exist = False
            if not username:
                print("Folder creation failed: No username supplied")
                return False
            
            folder_name = username
            self.sanitize_name = os.path.basename(folder_name)
            BASE_DIR = Path(__file__).resolve().parent.parent
            # print("Base dir:", BASE_DIR)
            self.path = BASE_DIR/ "static" / "uploads" / "database" / self.sanitize_name
    
            try:
                print("Create folder username:", self.sanitize_name)
    
                if self.path.exists():
                    pass
                    # self.addFolderPath(self.sanitize_name, str(self.path))
                    # exist = True
                    # print("Folder exist:", exist)
    
                else:
                    self.path.mkdir(parents=True, exist_ok=True)
                    # print(str(path))
                    databaseHandler.addFolderPath(username = self.sanitize_name, path = str(self.path))
                    return True
                    # exist = False
                    # print("Folder doesn't exist:", exist)
            
            except OSError as err:
                print("Create folder filesystem error:", err)
    
            except Exception as err:
                print("Unexpected error:", err)

    def dateTimeStamp(self):
        now = datetime.now()
        self.formatted_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        return self.formatted_string

    def filSave(self, file):
        fileSavePath = Path(self.path)
        for item in fileSavePath.iterdir():
            # fileSavePath.unlink(missing_ok = True)
            if item.is_file():
                print("File exists")
                item.unlink()
                
        filename = secure_filename(file.filename)
        name, extension = os.path.splitext(filename)
        self.new_name = (f"{name}_{self.dateTimeStamp()}{extension}")
        file_path = os.path.join(self.path, self.new_name)
        file.save(file_path)
        print("File name:", file)
        # databaseHandler.addImageName(databaseHandler.username_folder, new_name)