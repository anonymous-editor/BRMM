### Developed by TLM ###

# Dependencies #
import tkinter as tk

import customtkinter as ctk
from customtkinter import filedialog, CTk, CTkLabel
from PIL import Image, ImageTk
from io import BytesIO
import os
import gdown
import zipfile
import requests
import subprocess

root = tk.Tk()
root.withdraw()

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

# Image References #

urls = ["https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG", 
       "https://github.com/anonymous-editor/BRMM/raw/main/M2.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M3.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M4.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M5.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M6.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M7.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M8.png",
       "https://github.com/anonymous-editor/BRMM/raw/main/M9.png"
]

responses = [requests.get(url) for url in urls]

# UI Stuff #
title = ctk.CTkLabel(scrollable_frame, text="Available Mods:", font=("Segoe UI Semibold", 48), anchor="nw")
title.grid(row=0, column=0, padx=15, pady=15)

# Bricksdale Speedway UI #
frame_3 = create_frame(scrollable_frame)
frame_3.grid(row=2, column=0, **create_frame_padding())

textbox_1 = ctk.CTkLabel(frame_3, text="Bricksdale Speedway", **mod_title_font())
textbox_1.pack(anchor="center", padx=10, pady=10)

def prevent_go():
    
    label.image_ref = photo

image_path = Image.open(BytesIO(responses[0].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_3, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

app.bind("<Configure>", lambda e: prevent_go())

textbox_3 = ctk.CTkLabel(frame_3, font=("Segoe UI", 16), text="This map brings the world of American motorsports into Brick Rigs, with realistic props, lighting, Arizonian landscaping, and track layouts. There are many types of motorsports events here, ranging from demolition derbies to oval racing.\n\nSize: 167 MB\nAuthor: batt", wraplength=500)
textbox_3.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_3, command=lambda: download_googledrive_zipfile('1D6vJSi0rz6ix2oPLwFk9S2Bai2xOTGiS', f'{modpath}\\Mods\\BricksdaleSpeedway.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_3, command=lambda: remove_file(f"{modpath}\\Mods\\BricksdaleSpeedway.zip", f"{modpath}\\Mods\\BricksdaleSpeedway"), **remove_button())
button.pack(**remove_button_packing())

# Batt's Showroom UI #
frame_4 = create_frame(scrollable_frame)
frame_4.grid(row=2, column=1, **create_frame_padding())

textbox_4 = ctk.CTkLabel(frame_4, text="Batt's Showroom", **mod_title_font())
textbox_4.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[1].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_4, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_5 = ctk.CTkLabel(frame_4, font=("Segoe UI", 16), text="This map is designed with excellent lighting conditions in mind and comes with a suite of post-processing options. It's intended for you to take pictures of items to the Steam Workshop. Make sure to crank up your settings up when you do.\n\nSize: 6.94 MB\nAuthor: batt", wraplength=500)
textbox_5.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_4, command=lambda: download_googledrive_zipfile('1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy', f'{modpath}\\Mods\\batt_showroom.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_4, command=lambda: remove_file(f"{modpath}\\Mods\\batt_showroom.zip", f"{modpath}\\Mods\\batt_showroom"), **remove_button())
button.pack(**remove_button_packing())

# FNAF Map UI #

frame_5 = create_frame(scrollable_frame)
frame_5.grid(row=2, column=2, **create_frame_padding())

textbox_6 = ctk.CTkLabel(frame_5, text="FNAF Map/Mod", **mod_title_font())
textbox_6.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[2].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_5, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_7 = ctk.CTkLabel(frame_5, font=("Segoe UI", 16), text="This map is a replica of 'Five Nights At Freddy's,' a classic horror game. In Brick Rigs, the map has it's own custom gamemode to suit the map. There's even a way to cook and eat pizzas from within the map, along with many other high-quality details.\n\nSize: 56.7 MB\nAuthor: lord_bondrewd", wraplength=500)
textbox_7.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_5, command=lambda: download_googledrive_zipfile('1z9TrMazaFOLkTJ8r4h5lWJ1lkLq6QzLr', f'{modpath}\\Mods\\FNAF1.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_5, command=lambda: remove_file(f"{modpath}\\Mods\\FNAF1.zip", f"{modpath}\\Mods\\FNAF1"), **remove_button())
button.pack(**remove_button_packing())

# Vanilla Content Expansion UI #

frame_6 = create_frame(scrollable_frame)
frame_6.grid(row=3, column=0, **create_frame_padding())

textbox_8 = ctk.CTkLabel(frame_6, text="Vanilla Content Expansion", **mod_title_font())
textbox_8.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[3].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_6, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_9 = ctk.CTkLabel(frame_6, font=("Segoe UI", 16), text="This mod features over 10 new, develepor-quality weapons, weapon paints, and even a new 'Awooga Car Horn.' The ten weapons encompass primary, secondary, and special weapon types. However, be careful about joining multiplayer servers without this mod.\n\nSize: 98.4 MB\nAuthor: kvthetank", wraplength=500)
textbox_9.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_6, command=lambda: download_googledrive_zipfile('1RnQKGILY8f-v8Cq8Hpp-acye_bRsTE0v', f'{modpath}\\Mods\\VanillaContentExpansion.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_6, command=lambda: remove_file(f"{modpath}\\Mods\\VanillaContentExpansion.zip", f"{modpath}\\Mods\\VanillaContentExpansion"), **remove_button())
button.pack(**remove_button_packing())

# Black Theme #

frame_7 = create_frame(scrollable_frame)
frame_7.grid(row=3, column=1, **create_frame_padding())

textbox_10 = ctk.CTkLabel(frame_7, text="Black Theme", **mod_title_font())
textbox_10.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[4].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_7, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_11 = ctk.CTkLabel(frame_7, font=("Segoe UI", 16), text="This is the first Brick Rigs mod to add a new color scheme to the user interface. It is 'simple,' according to the publisher himself. Not much else can be said about this mod, besides it's minimal size of only ~530 KB.\n\nSize: 526.07 KB\nAuthor: Redacted_xd", wraplength=500)
textbox_11.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_7, command=lambda: download_discord_zipfile('https://cdn.discordapp.com/attachments/751767065970475093/1181849071930060831/BlackTheme.zip?', f'{modpath}\\Mods\\BlackTheme.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_7, command=lambda: remove_file(f"{modpath}\\Mods\\BlackTheme.zip", f"{modpath}\\Mods\\BlackTheme"), **remove_button())
button.pack(**remove_button_packing())

# Airstrike #

frame_8 = create_frame(scrollable_frame)
frame_8.grid(row=3, column=2, **create_frame_padding())

textbox_12 = ctk.CTkLabel(frame_8, text="Airstrike Mod", **mod_title_font())
textbox_12.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[5].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_8, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_13 = ctk.CTkLabel(frame_8, font=("Segoe UI", 16), text="Another first for Brick Rigs are nukes, not the ones that kids use to troll in public servers, but instead, ones that can be spawned in by players for a less laggy experience. These explosives are classified as 'weapons' in their selection menu, which have some quirks to them.\n\nSize: 47.8 MB\nAuthor: lord_bondrewd", wraplength=500)
textbox_13.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_8, command=lambda: download_googledrive_zipfile('1QvqNwaJJvweAr1eKNzNpVWseFEsj36iq', f'{modpath}\\Mods\\Airstrike.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_8, command=lambda: remove_file(f"{modpath}\\Mods\\Airstrike.zip", f"{modpath}\\Mods\\Airstrike"), **remove_button())
button.pack(**remove_button_packing())

# Knife Mod #

frame_9 = create_frame(scrollable_frame)
frame_9.grid(row=4, column=0, **create_frame_padding())

textbox_14 = ctk.CTkLabel(frame_9, text="Knife", **mod_title_font())
textbox_14.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[6].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_9, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_15 = ctk.CTkLabel(frame_9, font=("Segoe UI", 16), text="This mod features knives, which are paintable. They have the same 'brick-built' aesthetic found in other high-quality mods. The knife itself works by 'shooting' a weak bullet at a target when triggered with the right key.\n\nSize: 1.38 MB\nAuthor: batt", wraplength=500)
textbox_15.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_9, command=lambda: download_googledrive_zipfile('1y5QEsYv1HCeNGna2O9RYtDmuNlTNdnzc', f'{modpath}\\Mods\\batt_knife.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_9, command=lambda: remove_file(f"{modpath}\\Mods\\batt_knife.zip", f"{modpath}\\Mods\\batt_knife"), **remove_button())
button.pack(**remove_button_packing())

# Clouds Mod #

frame_10 = create_frame(scrollable_frame)
frame_10.grid(row=4, column=1, **create_frame_padding())

textbox_16 = ctk.CTkLabel(frame_10, text="Remastered Skies", **mod_title_font())
textbox_16.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[7].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_10, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_17 = ctk.CTkLabel(frame_10, font=("Segoe UI", 16), text="This mod replaces the in-game weather system with a realistic alternative. It also changes the Sun's size to be more life-like, and even comes with a moon phase and a space background. It's also very customizable.\n\nSize: 241 MB\nAuthor: andi_pog", wraplength=500)
textbox_17.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_10, command=lambda: download_googledrive_pakfile('1SRmDYR2DLU2YQbCzs2ExBz_huj1GkLQv', f'{modpath}\\Content\\Paks\\APRS-WindowsNoEditor_P.pak'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_10, command=lambda: removepakfile(f"{modpath}\\Content\\Paks\\APRS-WindowsNoEditor_P.pak"), **remove_button())
button.pack(**remove_button_packing())

# Advanced Sights #

frame_11 = create_frame(scrollable_frame)
frame_11.grid(row=4, column=2, **create_frame_padding())

textbox_16 = ctk.CTkLabel(frame_11, text="Advanced Sights", **mod_title_font())
textbox_16.pack(anchor="center", padx=10, pady=10)

image_path = Image.open(BytesIO(responses[8].content))
image_path = image_path.resize((480, 270))

photo = ImageTk.PhotoImage(image_path, master=app)

label = ctk.CTkLabel(frame_11, image=photo, text="")
label.image = photo  # keep a reference!
label.pack(**create_image_label_packing('center'))

textbox_17 = ctk.CTkLabel(frame_11, font=("Segoe UI", 16), text="This 'simple' mod adds a scope with cool night visibility and several custom features. You're able to control the scope through various mouse controls. There's also a way to control the scope mode. More features to this mod are coming soon!\n\nSize: 8.94 MB\nAuthor: Redacted_xd", wraplength=500)
textbox_17.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_11, command=lambda: download_discord_zipfile('https://cdn.discordapp.com/attachments/751767065970475093/1188166613237772488/AdvancedScopes_RD_BOOSTY.zip?', f'{modpath}\\Mods\\AdvancedScopes.zip'), **install_button())
button.pack(**install_button_packing())

button = ctk.CTkButton(frame_11, command=lambda: remove_file(f"{modpath}\\Mods\\AdvancedScopes.zip", f"{modpath}\\Mods\\AdvancedScopes"), **remove_button())
button.pack(**remove_button_packing())

app.mainloop()
