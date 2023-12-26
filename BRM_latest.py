### Developed by TLM ###

# Dependencies #
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import filedialog, CTk, CTkLabel
from PIL import Image, ImageTk
from io import BytesIO
import os
import gdown
import zipfile
import requests
import subprocess

from urllib.request import urlopen # load file from github
import json # fetch file

root = tk.Tk()
root.withdraw()




# Fetch data from url
# TODO Fill this data

#url = ""
#response1 = urlopen(url)
#text = response1.read()

# Test Data (TO BE REMOVED)
testdata = """
{
    "mods": [{
    "name": "123",
    "installType": "gd",
    "install": "h1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "description": "YOUR DESCRIPTION",
    "size":"1234 MB",
    "author":"me",
    "installpath":"Mods/BricksdaleSpeedway.zip",
    "deinstallpath":"Mods/BricksdaleSpeedway"
    },{
    "name": "456",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "installType": "d",
    "install": "h1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy",
    "description": "YOUR DESCRIPTION",
    "size":"1234 MB",
    "author":"me",
    "installpath":"Mods/BricksdaleSpeedway.zip",
    "deinstallpath":"Mods/BricksdaleSpeedway"
    },{
    "name": "456",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "installType": "d",
    "install": "h1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy",
    "description": "YOUR DESCRIPTION",
    "size":"1234 MB",
    "author":"me",
    "installpath":"Mods/BricksdaleSpeedway.zip",
    "deinstallpath":"Mods/BricksdaleSpeedway"
    },{
    "name": "456",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "installType": "d",
    "install": "h1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy",
    "description": "YOUR DESCRIPTION",
    "size":"1234 MB",
    "author":"me",
    "installpath":"Mods/BricksdaleSpeedway.zip",
    "deinstallpath":"Mods/BricksdaleSpeedway"
    },{
    "name": "456",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "installType": "d",
    "install": "h1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy",
    "description": "YOUR DESCRIPTION",
    "size":"1234 MB",
    "author":"me",
    "installpath":"Mods/BricksdaleSpeedway.zip",
    "deinstallpath":"Mods/BricksdaleSpeedway"
    }]
}
"""

# JSON loading
data = json.loads(testdata)









# App Frame Code

class MyApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Brick Rigs Mod Manager")
        self.geometry("1920x1080")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

app = MyApp()

scrollable_frame = ctk.CTkScrollableFrame(master=app)
scrollable_frame.grid(row=0, column=0, sticky='nsew', rowspan=7, columnspan=4)


# Theming #
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Path variables #

def W4():
    
    save_window = CTk()
    save_window.title("Initial Setup Status")
    save_window.geometry("550x165")

    message = CTkLabel(save_window, text="\nBRMM has saved your Brick Rigs install path in your user folder!\n\nFrom now on, you don't have to manually select your 'BrickRigs' folder.\n\nPlease restart BRMM for full functionality.\n", font=("Segoe UI", 16))
    message.pack()

    save_window.mainloop()
    
if not os.path.isfile('modpath.txt'):
    
    modpath = filedialog.askdirectory(title="Select your 'BrickRigs' folder to continue.")
    with open('modpath.txt', 'w') as f:
        
        f.write(modpath)

    W4()
        
else:
    
    with open('modpath.txt', 'r') as f:
        
        modpath = f.read()
        
# Button Controllers #

def alreadyexists():
    
    awindow = CTk()
    awindow.title("Mod Status")
    awindow.geometry("350x110")
    
    message = CTkLabel(awindow, text="\nThe mod is already installed into Brick Rigs.\n\nYou can close this window now.\n", font=("Segoe UI", 16))
    message.pack()
      
    awindow.mainloop()

def W2():
    
    alert_window = CTk()
    alert_window.title("Mod Status")
    alert_window.geometry("450x110")
    
    message = CTkLabel(alert_window, text="\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n", font=("Segoe UI", 16))
    message.pack()
      
    alert_window.mainloop()

def download_googledrive_zipfile(file_id, destination):

    if os.path.exists(destination):
            
            alreadyexists()

            return app
    
    url = f"https://drive.google.com/uc?id={file_id}"
    
    gdown.download(url, destination, quiet=False)

    with zipfile.ZipFile(destination, 'r') as zip_ref:
        
        zip_ref.extractall(os.path.dirname(destination))

    W2()

def download_googledrive_pakfile(file_id, destination):
    
    if os.path.exists(destination):
            
            alreadyexists()

            return app
    
    url = f"https://drive.google.com/uc?id={file_id}"
    
    gdown.download(url, destination, quiet=False)

    W2()

def download_discord_zipfile(url, filename):
    
    if os.path.exists(filename):
            
            alreadyexists()

            return app
    
    response = requests.get(url)
    
    with open(filename, 'wb') as file:
        
        file.write(response.content)

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        
        zip_ref.extractall(os.path.dirname(filename))

    W2()

def download_discord_pakfile(url, filename):

    if os.path.exists(filename):
            
            alreadyexists()

            return app
    
    response = requests.get(url)

    with open(filename, 'wb') as file:
        file.write(response.content)

    W2()

    return app

class ContentFormatting:
    @staticmethod
    def create_frame(parent, **kwargs):
        frame = tk.Frame(parent, bg="#003459", padx=10, pady=10, **kwargs)
        return frame

    @staticmethod
    def create_frame_padding():
        return {"padx": 30, "pady": 30, "sticky": 'nsew'}

    @staticmethod
    def mod_title_font():
        return {"font": ("Segoe UI Semibold", 28)}

    @staticmethod
    def mod_content_font():
        return {"font": ("Segoe UI Semibold", 28)}

    @staticmethod
    def install_button():
        return {"text": "Install", "font": ("Segoe UI", 18)}

    @staticmethod
    def remove_button():
        return {"text": "Remove", "font": ("Segoe UI", 18)}

    @staticmethod
    def install_button_packing():
        return {"anchor": "center", "ipady": 5, "pady": 15}

    @staticmethod
    def remove_button_packing():
        return {"anchor": "center", "ipady": 5, "pady": (0,8)}

    @staticmethod
    def create_image_label(photo):
        return {"image": photo, "text": ""}

    @staticmethod
    def create_image_label_packing(is_centered):
        return {"anchor": is_centered, "padx": 30, "pady": 15}

create_frame = ContentFormatting.create_frame
create_frame_padding = ContentFormatting.create_frame_padding
mod_title_font = ContentFormatting.mod_title_font
mod_content_font = ContentFormatting.mod_content_font
install_button = ContentFormatting.install_button
install_button_packing = ContentFormatting.install_button_packing
remove_button = ContentFormatting.remove_button
remove_button_packing = ContentFormatting.remove_button_packing
create_image_label = ContentFormatting.create_image_label
create_image_label_packing = ContentFormatting.create_image_label_packing

# Uninstaller #

def usuccessmessage():
    
    success_window = CTk()
    success_window.title("Mod Status")
    success_window.geometry("350x110")
    
    message = CTkLabel(success_window, text="\nThe mod has been removed from Brick Rigs!\n\nYou can close this window now.\n", font=("Segoe UI", 16))
    message.pack()
      
    success_window.mainloop()
    
def notexists():
    
    awindow = CTk()
    awindow.title("Mod Status")
    awindow.geometry("350x110")
    
    message = CTkLabel(awindow, text="\nThe mod is not installed into Brick Rigs.\n\nYou can close this window now.\n", font=("Segoe UI", 16))
    message.pack()
      
    awindow.mainloop()

def remove_file(file_path, folder_path):
        
        if not os.path.exists(file_path):
            
            notexists()

            return app
            
        subprocess.run(["del", file_path], shell=True, check=True)
        subprocess.run(["rmdir", "/S", "/Q", folder_path], shell=True, check=True)

        usuccessmessage()
        
        return app

def removepakfile(file_path):
        
        if not os.path.exists(file_path):
            
            notexists()

            return app
            
        subprocess.run(["del", file_path], shell=True, check=True)

        usuccessmessage()
        
        return app

# UI Stuff #
title = ctk.CTkLabel(scrollable_frame, text="Available Mods:", font=("Segoe UI Semibold", 48), anchor="nw")
title.grid(row=0, column=0, padx=15, pady=15)

for i in range(len(data["mods"])):
    mod = data["mods"][i]
    frame_10 = create_frame(scrollable_frame)
    frame_10.grid(row=2+int(i/3), column=i%3, **create_frame_padding())

    textbox_16 = ctk.CTkLabel(frame_10, text=mod["name"], **mod_title_font())
    textbox_16.pack(anchor="center", padx=10, pady=10)

    # TODO: replace with better solution
    response = requests.get(mod["image"]) # too slow
    image_path = Image.open(BytesIO(response.content))
    image_path = image_path.resize((480, 270))

    photo = ImageTk.PhotoImage(image_path, master=app)

    label = ctk.CTkLabel(frame_10, image=photo, text="")
    label.image = photo  # keep a reference!
    label.pack(**create_image_label_packing('center'))

    textbox_17 = ctk.CTkLabel(frame_10, font=("Segoe UI", 16), text=mod["description"]+"\n\nSize: "+mod["size"]+"\nAuthor: "+mod["author"], wraplength=500)
    textbox_17.pack(anchor="center", padx=30, pady=15)

    if mod["installType"] == "gd": # gd = Google Drive
        # TODO replace string with mod[...]
        button = ctk.CTkButton(frame_10, command=lambda: download_googledrive_pakfile('1SRmDYR2DLU2YQbCzs2ExBz_huj1GkLQv', f'{modpath}\\Content\\Paks\\APRS-WindowsNoEditor_P.pak'), **install_button())
        button.pack(**install_button_packing())
    if mod["installType"] == "d": # d = Discord
        # TODO replace string with mod[...]
        button = ctk.CTkButton(frame_10, command=lambda: download_discord_zipfile('https://cdn.discordapp.com/attachments/751767065970475093/1188166613237772488/AdvancedScopes_RD_BOOSTY.zip?', f'{modpath}\\Mods\\AdvancedScopes.zip'), **install_button())
        button.pack(**install_button_packing())
    # TODO replace string with mod[...]
    button = ctk.CTkButton(frame_10, command=lambda: removepakfile(f"{modpath}\\Content\\Paks\\APRS-WindowsNoEditor_P.pak"), **remove_button())
    button.pack(**remove_button_packing())
app.mainloop()