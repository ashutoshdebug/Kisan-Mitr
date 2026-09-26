import os
import json
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
from database.db_handler import dbHandler
import shutil

databaseHandler = dbHandler()

class fileFolderPath:
    def __init__(self):
        self.formatted_string = None
        self.folder_path = None
        self.path = None
        self.image_folder = None
        self.result_folder = None
        self.user_profile_pfp_folder = None
        self.pfp_default = None
        self.pfp_custom = None
        self.result_file = None
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
            self.image_folder = self.path / "image"
            self.result_folder = self.path / "result"
            self.user_profile_pfp_folder = self.path / "pfp_folder"
            self.pfp_default = self.user_profile_pfp_folder / "pfp_default"
            self.pfp_custom = self.user_profile_pfp_folder / "pfp_custom"
    
            try:
                print("Create folder username:", self.sanitize_name)
    
                if self.path.exists():
                    if self.image_folder.exists() and self.result_folder.exists() and self.user_profile_pfp_folder.exists() and self.pfp_custom.exists() and self.pfp_default.exists():
                        self.addDefaultPFP("static/uploads/frontend/default-profile.svg")
                        databaseHandler.addFolderPath(username = self.sanitize_name, path = str(self.path))
                    else:
                        self.image_folder.mkdir(parents=True, exist_ok = True)
                        self.result_folder.mkdir(parents=True, exist_ok=True)
                        self.user_profile_pfp_folder.mkdir(parents=True, exist_ok=True)
                        self.pfp_default.mkdir(parents=True, exist_ok=True)
                        self.pfp_custom.mkdir(parents=True, exist_ok=True)
                        self.addDefaultPFP("static/uploads/frontend/default-profile.svg")
                        
                        
                    # self.addFolderPath(self.sanitize_name, str(self.path))
                    # exist = True
                    # print("Folder exist:", exist)
    
                else:
                    self.path.mkdir(parents=True, exist_ok=True)
                    self.image_folder.mkdir(parents=True, exist_ok = True)
                    self.result_folder.mkdir(parents=True, exist_ok=True)
                    self.user_profile_pfp_folder.mkdir(parents=True, exist_ok=True)
                    self.pfp_default.mkdir(parents=True, exist_ok=True)
                    self.pfp_custom.mkdir(parents=True, exist_ok=True)
                    self.addDefaultPFP("static/uploads/frontend/default-profile.svg")
                    # print(str(path))
                    databaseHandler.addFolderPath(username = self.sanitize_name, path = str(self.path))
                    print("Folder path called")
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

    def fileSave(self, file):
        print("fileSave path:",self.image_folder)
        fileSavePath = Path(self.image_folder)
        for item in fileSavePath.iterdir():
            # fileSavePath.unlink(missing_ok = True)
            if item.is_file():
                print("File exists")
                item.unlink()
                
        filename = secure_filename(file.filename)
        name, extension = os.path.splitext(filename)
        self.new_name = (f"{name}_{self.dateTimeStamp()}{extension}")
        file_path = os.path.join(self.image_folder, self.new_name)
        file.save(file_path)
        print("File name:", file)
        # databaseHandler.addImageName(databaseHandler.username_folder, new_name)

    def saveJsonFile(self, result):
        folder = Path(self.result_folder) / "result.json"
        try:
            self.result_file = "result.json"
            with open(folder, "w") as file:
                json.dump(result, file, indent=4)
                return True

        except (OSError, TypeError) as err:
            print("JSON save error:", err)
            return False


    def addDefaultPFP(self, fileDIR):
        # print("addDefaultPFP Function called")
        try:
            fileDIR = Path(fileDIR)
            # filename = os.path.basename(fileDIR)
            shutil.copy(fileDIR, Path(self.pfp_default))            
            # print(fileDIR)
            # print(filename)
        except OSError as err:
            print("Error:", err)