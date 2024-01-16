# Dependencies: #

import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog, CTk, CTkLabel

from PIL import Image
from io import BytesIO

import os
import zipfile
import requests
import shutil

from googleapiclient.http import MediaIoBaseDownload
import googleapiclient.discovery
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.request
from urllib.request import urlopen
import json

# JSON Loading: #

dataurl = "https://raw.githubusercontent.com/anonymous-editor/BRMM/main/public_mod_data.json"
response = urllib.request.urlopen(dataurl)
data = json.loads(response.read().decode('utf-8'))

# App Frame Code: #

class MyApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Brick Rigs Mod Manager")
        self.geometry("1920x1080")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self)
        self.scrollable_frame.grid(row=0, column=0, sticky='nsew', rowspan=7, columnspan=4)

app = MyApp()
scrollable_frame = app.scrollable_frame

# Global Theming: #

try:
    with open('theme.txt', 'r') as file:
        theme = file.read().strip()
except (FileNotFoundError, ValueError):
    theme = "dark-blue"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(theme)

# Path Variables: #

def W4():
    save_window = CTk()
    save_window.title("Initial Setup Status")
    save_window.geometry("550x165")

    message = CTkLabel(save_window, text="\nBRMM has saved your Brick Rigs install paths in your BRMM folder!\n\nFrom now on, you don't have to manually select the two folders.\n\nPlease restart BRMM for full functionality.\n", font=("Segoe UI", 16))
    message.pack()

    save_window.mainloop()
    
if not os.path.isfile('modpath.txt') and not os.path.isfile('pakspath.txt'):
    modpath = filedialog.askdirectory(title="Select your 'Mods' folder to continue.")
    with open('modpath.txt', 'w') as f:
        f.write(modpath)
    
    pakspath = filedialog.askdirectory(title="Select your 'Paks' folder to continue.")
    with open('pakspath.txt', 'w') as e:
        e.write(pakspath)
    
    W4()

else:
    with open('modpath.txt', 'r') as f:
        modpath = f.read()

    with open('pakspath.txt', 'r') as e:
        pakspath = e.read()

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Settings")       
        self.bind("<Destroy>", self.apply_changes)
        print("OptionsWindow initialized")


        self.modspath_var = tk.StringVar()
        self.pakspath_var = tk.StringVar()

        # Mechanism to display the current mod/pak folder paths: #

        with open('modpath.txt', 'r') as f:
            self.modspath_var.set(f.read())
        with open('pakspath.txt', 'r') as e:
            self.pakspath_var.set(e.read())

        # UI Organization: #

        tab_view = ctk.CTkTabview(self)
        tab_view.pack(fill='both', expand=True)
        tab1 = tab_view.add("UI")
        tab2 = tab_view.add("Paths")

        frame1 = ctk.CTkFrame(tab1)
        frame1.pack(fill='both', expand=True)
        frame2 = ctk.CTkFrame(tab2)
        frame2.pack(fill='both', expand=True)
        frame3 = ctk.CTkFrame(tab2)
        frame3.pack(fill='both', expand=True)

    # Tab 1 Widgets: #

        # Column changer widget: #

        try:
            with open('columns_value.txt', 'r') as file:
                current_value = int(file.read().strip())
        except (FileNotFoundError, ValueError):
            current_value = 2

        dropdown_label = ctk.CTkLabel(frame1, text="DISCLAIMER: Any changes you make here will only apply when you restart BRMM.\n\nNumber of columns:", font=("Segoe UI", 16), wraplength=250)
        dropdown_label.pack(pady=5)
        self.dropdown_options = ["2", "3", "4", "5"]
        self.selected_option = tk.StringVar()
        self.dropdown_menu = ctk.CTkComboBox(frame1, values=self.dropdown_options)
        self.dropdown_menu.pack()
        self.dropdown_menu.set(str(current_value))
        self.dropdown_menu.bind("<FocusOut>", self.destroy)
        apply_button = ctk.CTkButton(frame1, text="Apply", command=self.apply_changes, font=("Segoe UI", 14))
        apply_button.pack(pady=10, ipady=5)
        
        # Theme changer widget: #

        theme_label = ctk.CTkLabel(frame1, text="Select theme:", font=("Segoe UI", 16))
        theme_label.pack(pady=(15, 5))
        self.theme_options = ["dark-blue", "blue", "green"]
        self.selected_theme = tk.StringVar()
        self.theme_menu = ctk.CTkComboBox(frame1, values=self.theme_options)
        self.theme_menu.pack()
       
        try:
            with open('theme.txt', 'r') as file:
                current_theme = file.read().strip()
        except (FileNotFoundError, ValueError):
            current_theme = "dark-blue"

        self.theme_menu.set(current_theme)
        self.selected_theme.set(current_theme)

        apply_theme_button = ctk.CTkButton(frame1, text="(Apply Theme", command=self.apply_theme_changes, font=("Segoe UI", 14))
        dropdown_label.pack(pady=5)
        apply_theme_button.pack(pady=10, ipady=5)
    
    # Tab 2 Widgets: #
           
        modpath_label = ctk.CTkLabel(frame2, text="DISCLAIMER: Any changes you make here will only apply when you restart BRMM.\n\nMods folder path:", font=("Segoe UI", 16), wraplength=250)
        modpath_label.pack(pady=5)
        modpath_entry = ctk.CTkEntry(frame2, textvariable=self.modspath_var, width=250)
        modpath_entry.pack()
        modpath_button = ctk.CTkButton(frame2, text="Browse", command=self.browse_modpath, font=("Segoe UI", 14))
        modpath_button.pack(pady=10, ipady=5)

        pakspath_label = ctk.CTkLabel(frame3, text="Paks folder path:", font=("Segoe UI", 16))
        pakspath_label.pack(pady=(15,5))
        pakspath_entry = ctk.CTkEntry(frame3, textvariable=self.pakspath_var, width=250)
        pakspath_entry.pack()
        pakspath_button = ctk.CTkButton(frame3, text="Browse", command=self.browse_pakspath, font=("Segoe UI", 14))
        pakspath_button.pack(pady=10, ipady=5)
    
    # File Operations: #

    def browse_modpath(self):
        path = filedialog.askdirectory(title="Select your 'Mods' folder.")
        self.modspath_var.set(path)
        with open('modpath.txt', 'w') as f:
            f.write(path)

    def browse_pakspath(self):
        path = filedialog.askdirectory(title="Select your 'Paks' folder.")
        self.pakspath_var.set(path)
        with open('pakspath.txt', 'w') as e:
            e.write(path)

    def apply_changes(self, event=None):
        selected_option = self.dropdown_menu.get()
        with open('columns_value.txt', 'w') as file:
            file.write(str(int(selected_option)))

    def apply_theme_changes(self):
        selected_theme = self.theme_menu.get()
        with open('theme.txt', 'w') as file:
            file.write(selected_theme)
    
    # Window Launcher: #

    def open_options_window(parent):
        OptionsWindow(parent)

options_window = OptionsWindow.open_options_window

try:
    with open('columns_value.txt', 'r') as file:
        number = int(file.read().strip())
except (FileNotFoundError, ValueError):
    number = 2

# Download Controllers: #

def create_message_window(message_text):
    window = CTk()
    window.title("Mod Status")
    window.geometry("450x110")

    message = CTkLabel(window, text=message_text, font=("Segoe UI", 16))
    message.pack()
        
    window.mainloop()

def handle_existing_file(destination):
    if os.path.exists(destination):
        create_message_window("\nThe mod is already installed into your copy of Brick Rigs.\n\nYou can close this window now.\n")
        return app

def download_file(url, destination, download_func):
    handle_existing_file(destination)

    download_func(url, destination, quiet=False)
    
    if zipfile.is_zipfile(destination):
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(destination))

    create_message_window("\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n")

    return app

def download_googledrive_file(file_id, destination):
    handle_existing_file(destination)

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_721310632565-2i4qb11ui3lsgv7c2541cmeom0c51dai.apps.googleusercontent.com.json', ['https://www.googleapis.com/auth/drive.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = googleapiclient.discovery.build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = open(destination, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.close()

    if zipfile.is_zipfile(destination):
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(destination))

    create_message_window("\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n")

    return app

def download_discord_file(url, filename):  
    download_file(url, filename, lambda url, destination, quiet: open(destination, 'wb').write(requests.get(url).content))

def download_github_zipfile(url, destination):
    handle_existing_file(destination)

    response = requests.get(url)

    with open(destination, 'wb') as out_file:
        out_file.write(response.content)

    if zipfile.is_zipfile(destination):
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(os.path.splitext(destination)[0])

    create_message_window("\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n")

    return app

# Frame GUI Formatting: #

class ContentFormatting:
    FRAME_PADDING = {"padx": 30, "pady": 30, "sticky": 'nsew'}
    MOD_TITLE_FONT = {"font": ("Segoe UI Semibold", 28)}
    MOD_CONTENT_FONT = {"font": ("Segoe UI Semibold", 28)}
    INSTALL_BUTTON = {"text": "Install", "font": ("Segoe UI", 18)}
    REMOVE_BUTTON = {"text": "Remove", "font": ("Segoe UI Semibold", 18), "fg_color": "#b3322e"}
    INSTALL_BUTTON_PACKING = {"anchor": "center", "ipady": 5, "pady": 15}
    REMOVE_BUTTON_PACKING = {"anchor": "center", "ipady": 5, "pady": (0,8)}
    IMAGE_LABEL = {"text": ""}

    @staticmethod
    def create_frame(parent, **kwargs):
        frame = tk.Frame(parent, bg="#003459", padx=10, pady=10, **kwargs)
        return frame

    @staticmethod
    def create_image_label(photo):
        label = ContentFormatting.IMAGE_LABEL.copy()
        label["image"] = photo
        return label

    @staticmethod
    def create_image_label_packing(is_centered):
        return {"anchor": is_centered, "padx": 30, "pady": 15}

mod_title_font = ContentFormatting.MOD_TITLE_FONT
mod_content_font = ContentFormatting.MOD_CONTENT_FONT
install_button = ContentFormatting.INSTALL_BUTTON
install_button_packing = ContentFormatting.INSTALL_BUTTON_PACKING
remove_button = ContentFormatting.REMOVE_BUTTON
remove_button_packing = ContentFormatting.REMOVE_BUTTON_PACKING
create_image_label = ContentFormatting.create_image_label
create_image_label_packing = ContentFormatting.create_image_label_packing

# Uninstaller: #

def create_message_window1(message_text):
    window = CTk()
    window.title("Mod Status")
    window.geometry("350x110")
    
    message = CTkLabel(window, text=message_text, font=("Segoe UI", 16))
    message.pack()
      
    window.mainloop()

def usuccessmessage():
    create_message_window1("\nThe mod has been removed from Brick Rigs!\n\nYou can close this window now.\n")

def notexists():
    create_message_window1("\nThe mod is not installed into Brick Rigs.\n\nYou can close this window now.\n")

# Main Window GUI: #

title = ctk.CTkLabel(scrollable_frame, text="Available Mods:", font=("Segoe UI Semibold", 48), anchor="nw")
title.grid(row=0, column=0, padx=15, pady=15)

for i in range(len(data["mods"])):
    mod = data["mods"][i]
    frame_10 = ContentFormatting.create_frame(scrollable_frame)
    frame_10.grid(row=2+int(i/number), column=i%number, **ContentFormatting.FRAME_PADDING)

    textbox_16 = ctk.CTkLabel(frame_10, text=mod["name"], **ContentFormatting.MOD_TITLE_FONT)
    textbox_16.pack(anchor="center", padx=10, pady=10)

    # Options Button: #

    top_frame = ctk.CTkFrame(scrollable_frame)
    top_frame.grid(row=0, column=(number)-1)

    options_button = ctk.CTkButton(top_frame, text="Settings", command=lambda: OptionsWindow(top_frame), font=("Segoe UI", 18))
    options_button.pack(ipady=5)

    # Image Loading: #

    response = requests.get(mod["image"])
    image = Image.open(BytesIO(response.content))
    image.thumbnail((480, 270))

    ctk_image = ctk.CTkImage(image, size=(480, 270))

    label = ctk.CTkLabel(frame_10, image=ctk_image, text="")
    label.pack(**create_image_label_packing('center'))

    textbox_17 = ctk.CTkLabel(frame_10, font=("Segoe UI", 16), text=mod["description"]+"\n\nSize: "+mod["size"]+"\nAuthor: "+mod["author"], wraplength=500)
    textbox_17.pack(anchor="center", padx=30, pady=15)

    # Download Handlers: #
    
    if mod["installType"] == "gd": # gd = Google Drive
        destination = os.path.join(modpath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda file_id=mod["install"], destination=f'{modpath}{mod["installpath"]}': download_googledrive_file(file_id, destination), **install_button)
        button.pack(**install_button_packing)

    elif mod["installType"] == "gdpak":
        destination = os.path.join(pakspath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda url=mod["install"], destination=f'{pakspath}{mod["installpath"]}': download_googledrive_file(url, destination), **install_button)
        button.pack(**install_button_packing)
    
    elif mod["installType"] == "d": # d = Discord
        destination = os.path.join(modpath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda url=mod["install"], destination=f'{modpath}{mod["installpath"]}': download_discord_file(url, destination), **install_button)
        button.pack(**install_button_packing)

    elif mod["installType"] == "dpak":
        destination = os.path.join(pakspath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda file_id=mod["install"], destination=f'{pakspath}{mod["installpath"]}': download_discord_file(file_id, destination), **install_button)
        button.pack(**install_button_packing)

    elif mod["installType"] == "github":
        destination = os.path.join(modpath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda url=mod["install"], destination=f'{modpath}{mod["installpath"]}': download_github_zipfile(url, destination), **install_button)
        button.pack(**install_button_packing)

    # File Removal Managers: #
    
    def command_func():
        remove_file(file_path1, folder_path1)
    
    if mod["deinstallType"] == "zip":
        def remove_file(file_path1, folder_path1):
            if not os.path.exists(file_path1):
                notexists()
                return app
            os.remove(file_path1)
            shutil.rmtree(folder_path1)
            usuccessmessage()
            return app

        file_path1 = f'{modpath}{mod["installpath"]}'
        folder_path1 = f'{modpath}{mod["deinstallpath"]}'
        button = ctk.CTkButton(frame_10, command=lambda file_path1=file_path1, folder_path1=folder_path1: remove_file(file_path1, folder_path1), **remove_button)
        button.pack(**remove_button_packing)

    elif mod["deinstallType"] == "pak":
        def removepakfile(file_path2):
            if not os.path.exists(file_path2):
                notexists()
                return app
            os.remove(file_path2)
            usuccessmessage()
            return app

        file_path2 = f'{pakspath}{mod["installpath"]}'
        button = ctk.CTkButton(frame_10, command=lambda file_path2=file_path2: removepakfile(file_path2), **remove_button)
        button.pack(**remove_button_packing)

app.mainloop()
