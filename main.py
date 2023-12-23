### Developed by TLM ###

# Dependencies #
import tkinter as tk
from tkinter import PhotoImage
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkButton
from PIL import Image
from io import BytesIO
import os
import gdown
import zipfile
import requests
import shutil

path = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods'

if not os.path.exists(path):
    os.mkdir(path)

# Theming #
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Button Controllers #

def W2():
    
    alert_window = CTk()
    alert_window.title("Installation Complete!")
    alert_window.geometry("450x120")
    
    message = CTkLabel(alert_window, text="\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n", font=("Segoe UI", 16))
    message.pack()
      
    alert_window.mainloop()

should_continue = True

def do_nothing():
    
    global should_continue
    should_continue = False

def W3():

    alert1_window = CTk()
    alert1_window.title("Confirmation")
    alert1_window.geometry("550x200")
    
    message = CTkLabel(alert1_window, text="\nAre you sure that you want to remove this mod?", font=("Segoe UI", 16))
    message.pack()
    
    confirm_button = CTkButton(alert1_window, text="Yes", command=alert1_window.destroy, font=("Segoe UI Semibold", 18))
    confirm_button.pack(pady=16)
    
    deny_button = CTkButton(alert1_window, text="No", command=do_nothing, font=("Segoe UI Semibold", 18))
    deny_button.pack(pady=(0,16))
      
    alert1_window.mainloop()

def download_file(file_id, destination):
    
    global should_continue
    
    if os.path.exists(destination):
        
        if not should_continue:
        
            return
        
        W3()
                
        os.remove(destination)
        
        shutil.rmtree(os.path.splitext(destination)[0])
        
        return app

    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False)

    with zipfile.ZipFile(destination, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(destination))
    
    W2()
      
def download_zipfile(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
        
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(filename))
    
    W2()
     
# App Frame Code
app = ctk.CTk()
app.geometry("1790x720")
app.title("Brick Rigs Mod Manager")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

scrollable_frame = ctk.CTkScrollableFrame(master=app)
scrollable_frame.grid(row=0, column=0, sticky='nsew', rowspan=7, columnspan=4)

# Frame UI References #
def create_frame(parent, **kwargs):
   frame = tk.Frame(parent, bg="#003459", padx=10, pady=10, **kwargs)
   return frame

def create_frame_padding():
    return {"padx": 30, "pady": 30, "sticky": 'nsew'}

# Mod Description UI References #
def mod_title_font():
    return {"font": ("Segoe UI Semibold", 28)}

def mod_content_font():
    return {"font": ("Segoe UI Semibold", 28)}

# Button UI References #
def install_button():
    return {"text": "Install/Remove", "font": ("Segoe UI", 18)}

def install_button_packing():
   return {"anchor": "center", "ipady": 5, "pady": 15}

def create_ctk_image(image):
  return {"light_image": image, "size": (480, 270)}

def create_image_label(ctk_image):
    return {"image": ctk_image, "text": ""}

def create_image_label_packing(is_centered):
    return {"anchor": is_centered, "padx": 30, "pady": 15}

# Image References #

urls = ["https://github.com/anonymous-editor/BRMI/blob/main/M1.png", 
       "https://github.com/anonymous-editor/BRMI/blob/main/M2.png",
       "https://github.com/anonymous-editor/BRMI/blob/main/M3.png",
       "https://github.com/anonymous-editor/BRMI/blob/main/M4.png",
       "https://github.com/anonymous-editor/BRMI/blob/main/M5.png",
       "https://github.com/anonymous-editor/BRMI/blob/main/M6.png",
       "https://github.com/anonymous-editor/BRMI/blob/main/M7.png",
]

raw_urls = [url.replace('blob', 'raw') for url in urls]

responses = [requests.get(raw_url) for raw_url in raw_urls]

# UI Stuff #
title = ctk.CTkLabel(scrollable_frame, text="Available Mods:", font=("Segoe UI Semibold", 48), anchor="nw")
title.grid(row=0, column=0, padx=15, pady=15)

# Bricksdale Speedway UI #
frame_3 = create_frame(scrollable_frame)
frame_3.grid(row=2, column=0, **create_frame_padding())

textbox_1 = ctk.CTkLabel(frame_3, text="Bricksdale Speedway", **mod_title_font())
textbox_1.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[0].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_3, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_3 = ctk.CTkLabel(frame_3, font=("Segoe UI", 16), text="This map brings the world of American motorsports into Brick Rigs, with realistic props, lighting, Arizonian landscaping, and track layouts. There are many types of motorsports events here, ranging from demolition derbies to oval racing.\n\nSize: 167 MB\nAuthor: batt", wraplength=500)
textbox_3.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_3, command=lambda: download_file('1D6vJSi0rz6ix2oPLwFk9S2Bai2xOTGiS', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\BricksdaleSpeedway.zip'), **install_button())
button.pack(**install_button_packing())

# Batt's Showroom UI #
frame_4 = create_frame(scrollable_frame)
frame_4.grid(row=2, column=1, **create_frame_padding())

textbox_4 = ctk.CTkLabel(frame_4, text="Batt's Showroom", **mod_title_font())
textbox_4.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[1].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_4, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_5 = ctk.CTkLabel(frame_4, font=("Segoe UI", 16), text="This map is designed with excellent lighting conditions in mind and comes with a suite of post-processing options. It's intended for you to take pictures of items to the Steam Workshop. Make sure to crank up your settings up when you do.\n\nSize: 6.94 MB\nAuthor: batt", wraplength=500)
textbox_5.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_4, command=lambda: download_file('1q8GpP2iiuEkmNDHihcQnn-K7Y0HP_pUy', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\batt_showroom.zip'), **install_button())
button.pack(**install_button_packing())

# FNAF Map UI #

frame_5 = create_frame(scrollable_frame)
frame_5.grid(row=2, column=2, **create_frame_padding())

textbox_6 = ctk.CTkLabel(frame_5, text="FNAF Map/Mod", **mod_title_font())
textbox_6.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[2].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_5, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_7 = ctk.CTkLabel(frame_5, font=("Segoe UI", 16), text="This map is a replica of 'Five Nights At Freddy's,' a classic horror game. In Brick Rigs, the map has it's own custom gamemode to suit the map. There's even a way to cook and eat pizzas from within the map, along with many other high-quality details.\n\nSize: 56.7 MB\nAuthor: lord_bondrewd", wraplength=500)
textbox_7.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_5, command=lambda: download_file('1z9TrMazaFOLkTJ8r4h5lWJ1lkLq6QzLr', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\FNAF1.zip'), **install_button())
button.pack(**install_button_packing())

# Vanilla Content Expansion UI #

frame_6 = create_frame(scrollable_frame)
frame_6.grid(row=3, column=0, **create_frame_padding())

textbox_8 = ctk.CTkLabel(frame_6, text="Vanilla Content Expansion", **mod_title_font())
textbox_8.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[3].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_6, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_9 = ctk.CTkLabel(frame_6, font=("Segoe UI", 16), text="This mod features over 10 new, develepor-quality weapons, weapon paints, and even a new 'Awooga Car Horn.' The ten weapons encompass primary, secondary, and special weapon types. However, be careful about joining multiplayer servers without this mod.\n\nSize: 98.4 MB\nAuthor: kvthetank", wraplength=500)
textbox_9.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_6, command=lambda: download_file('1RnQKGILY8f-v8Cq8Hpp-acye_bRsTE0v', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\VanillaContentExpansion.zip'), **install_button())
button.pack(**install_button_packing())

# Black Theme #

frame_7 = create_frame(scrollable_frame)
frame_7.grid(row=3, column=1, **create_frame_padding())

textbox_10 = ctk.CTkLabel(frame_7, text="Black Theme", **mod_title_font())
textbox_10.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[4].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_7, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_11 = ctk.CTkLabel(frame_7, font=("Segoe UI", 16), text="This is the first Brick Rigs mod to add a new color scheme to the user interface. It is 'simple,' according to the publisher himself. Not much else can be said about this mod, besides it's minimal size of only ~530 KB.\n\nSize: 526.07 KB\nAuthor: Redacted_xd", wraplength=500)
textbox_11.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_7, command=lambda: download_zipfile('https://cdn.discordapp.com/attachments/751767065970475093/1181849071930060831/BlackTheme.zip?', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\BlackTheme.zip'), **install_button())
button.pack(**install_button_packing())

# Airstrike #

frame_8 = create_frame(scrollable_frame)
frame_8.grid(row=3, column=2, **create_frame_padding())

textbox_12 = ctk.CTkLabel(frame_8, text="Airstrike Mod", **mod_title_font())
textbox_12.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[5].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_8, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_13 = ctk.CTkLabel(frame_8, font=("Segoe UI", 16), text="Another first for Brick Rigs are nukes, not the ones that kids use to troll in public servers, but instead, ones that can be spawned in by players for a less laggy experience. These explosives are classified as 'weapons' in their selection menu, which have some quirks to them.\n\nSize: 47.8 MB\nAuthor: lord_bondrewd", wraplength=500)
textbox_13.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_8, command=lambda: download_file('1QvqNwaJJvweAr1eKNzNpVWseFEsj36iq', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\Airstrike.zip'), **install_button())
button.pack(**install_button_packing())
# Knife Mod #

frame_9 = create_frame(scrollable_frame)
frame_9.grid(row=4, column=0, **create_frame_padding())

textbox_14 = ctk.CTkLabel(frame_9, text="Knife", **mod_title_font())
textbox_14.pack(anchor="center", padx=10, pady=10)

image = Image.open(BytesIO(responses[6].content))
ctk_image = ctk.CTkImage(**create_ctk_image(image))
image_label = ctk.CTkLabel(frame_9, image=ctk_image, text="")
image_label.pack(**create_image_label_packing('center'))

textbox_15 = ctk.CTkLabel(frame_9, font=("Segoe UI", 16), text="This mod features knives, which are paintable. They have the same 'brick-built' aesthetic found in other high-quality mods. The knife itself works by 'shooting' a weak bullet at a target when triggered with the right key.\n\nSize: 1.38 MB\nAuthor: batt", wraplength=500)
textbox_15.pack(anchor="center", padx=30, pady=15)

button = ctk.CTkButton(frame_9, command=lambda: download_file('1y5QEsYv1HCeNGna2O9RYtDmuNlTNdnzc', 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Brick Rigs\\BrickRigs\\Mods\\batt_knife.zip'), **install_button())
button.pack(**install_button_packing())

app.mainloop()
