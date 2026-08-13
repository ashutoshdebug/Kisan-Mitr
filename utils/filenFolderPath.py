import os
from pathlib import Path
from datetime import datetime
from database.db_handler import dbHandler

class fileFolderPath:
    def __init__(self):
        self.formatted_string = None
        self.folder_path = None
        self.path = None

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
                    dbHandler.addFolderPath(username = self.sanitize_name, path = self.path)
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