# Standard library imports
import os
import re
import shutil
import zipfile
import json

# Third-party library imports
import configparser
import requests
import urllib
from urllib.request import urlopen
from PIL import Image
import webbrowser

# Custom library imports
import customtkinter as ctk
from customtkinter import filedialog, CTk, CTkLabel
import gdown

# Tkinter imports
import tkinter as tk

# JSON Loading: #

dataurl = "https://raw.githubusercontent.com/anonymous-editor/BRMM/main/Resources/JSON/content.json"
response = urllib.request.urlopen(dataurl)
data = json.loads(response.read().decode('utf-8'))

# Define 'is_updating' at the global scope
is_updating = False

# App Frame Code: #

class MyApp(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Brick Rigs Mod Manager")
        self.geometry("1920x1080")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.iconbitmap('BRMM_ico.ico')
        
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self)
        self.scrollable_frame.grid(row=0, column=0, sticky='nsew', rowspan=2, columnspan=1)

app = MyApp()
scrollable_frame = app.scrollable_frame

# Function Definitions: #

def create_message_window(message_text, title):
    window = CTk()
    window.title(title)
    window.iconbitmap('BRMM_ico.ico')
    
    message = CTkLabel(window, text=message_text, font=("Segoe UI",  16), padx=50)
    message.pack()
        
    window.mainloop()

def check_if_exist(destination):
    if os.path.exists(destination):
        return True
    else:
        return False

# Download Controllers: #

def handle_existing_file(destination):
    if os.path.exists(destination):
        create_message_window("\nThe mod is already installed into your copy of Brick Rigs.\n\nYou can close this window now.\n", "Update Manager")
        return app

def download_and_extract(url, destination, download_func, title):
    handle_existing_file(destination)
    download_func(url, destination, quiet=False)
    
    if zipfile.is_zipfile(destination):
        directory_name = os.path.splitext(destination)[0]
        os.makedirs(directory_name, exist_ok=True)
        
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(directory_name)
    
    create_message_window("\nThe mod has successfully been installed into Brick Rigs!\n\nYou can close this window now.\n", title)
    return app

def download_file(url, destination, download_func):
    return download_and_extract(url, destination, download_func, "Mod Status")

def download_googledrive_file(file_id, destination):
    download_url = f'https://drive.google.com/uc?id={file_id}&export=download&confirm=t'
    try:
        return download_and_extract(download_url, destination, gdown.download, "Server Status")
    except Exception as e:
        create_message_window("\nThe server is currently busy right now, please try again in a few minutes.\n\nA link will now open in your default web browser to redirect you to the mod's Google Drive page.\n\nYou can close this window now.\n", "Server Status")
        print(f"For the techies: '{e}' -Copper")  
        webbrowser.open(download_url)
        return app

def download_discord_file(url, filename):   
    download_file(url, filename, lambda url, destination, quiet: open(destination, 'wb').write(requests.get(url).content))

def download_github_zipfile(url, destination):
    download_file(url, destination, lambda url, destination, quiet: open(destination, 'wb').write(requests.get(url).content))


# Autoupdater: #

update_dataurl = "https://raw.githubusercontent.com/anonymous-editor/BRMM/main/Resources/JSON/update_helper.json"
update_response = urllib.request.urlopen(update_dataurl)
update_data = json.loads(update_response.read().decode('utf-8'))
version_string = update_data["infomation"][0]["latest_version"]
download_link = update_data["infomation"][0]["direct_download_link"]
current_version = 300

def update_brmm():
    global is_updating
    is_updating = True

    local_path = ""

    if version_string == str(current_version):
        create_message_window("\nYou are already on the latest version of BRMM.\n", "Update Handler")
        return

    download_github_zipfile(download_link, os.path.join(local_path, f"BRMM{version_string}.zip"))

    with zipfile.ZipFile(os.path.join(local_path, f"BRMM{version_string}.zip"), 'r') as zip_ref:
        zip_ref.extractall(local_path)

    create_message_window("\nThe latest version of BRMM has been placed alongside this version of BRMM.\n", "Update Handler")

    is_updating = False

    return app

# INI Config: #

config = configparser.ConfigParser()
config.read('settings.ini')

if not os.path.isfile('settings.ini'): 
    modpath = filedialog.askdirectory(title="Select your 'Mods' folder to continue.")
    pakspath = filedialog.askdirectory(title="Select your 'Paks' folder to continue.")
    
    config['PATHS'] = {'modpath': modpath, 'pakspath': pakspath}
    config['UI'] = {'columns': 3, 'theme': "dark-blue"}

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

    create_message_window("\nBRMM has saved your Brick Rigs install paths in your BRMM folder!\n\nFrom now on, you don't have to manually select the two folders.\n\nPlease restart BRMM for full functionality.\n", "Initial Setup")

else:
    modpath = config['PATHS']['modpath']
    pakspath = config['PATHS']['pakspath']
    theme = config['UI']['theme']
    number = config['UI']['columns']

# Global Theming: #

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(theme)

# Settings Windows: #

current_version_with_periods = re.sub(r'(\d)', r'\1.', str(current_version))
version_string_with_periods = re.sub(r'(\d)', r'\1.', str(version_string))

def reset_brmm():
    shutil.rmtree('image_cache', ignore_errors=True)
    if os.path.exists('settings.ini'):
        os.remove('settings.ini')
    create_message_window("\nBRMM has been reset.\n", "Reset Handler")

def copy_to_clipboard():
    # The static text you want to copy to the clipboard
    static_text = f"My current version of BRMM is {current_version_with_periods}\n\nThe lastest version of BRMM is {version_string_with_periods}\n\nI set my Mods and Paks folders to '{modpath}' and '{pakspath}' repectively.\n\nI have {number} columns and the {theme} theme applied in the UI."
    app.clipboard_clear()
    app.clipboard_append(f"```{static_text}```")

class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("Settings")       
        self.bind("<Destroy>", self.apply_changes)
        self.iconbitmap('BRMM_ico.ico')

        self.modspath_var = ctk.StringVar()
        self.pakspath_var = ctk.StringVar()

        # Mechanism to display the current mod/pak folder paths: #

        self.modspath_var.set(config['PATHS']['modpath'])
        self.pakspath_var.set(config['PATHS']['pakspath'])

        # UI Organization: #

        tab_view = ctk.CTkTabview(self)
        tab_view.pack(fill='both', expand=True)

        tab1 = tab_view.add("UI")
        tab2 = tab_view.add("Paths")
        tab3 = tab_view.add("Updates")
        tab4 = tab_view.add("Troubleshooting")

        frame1 = ctk.CTkFrame(tab1)
        frame1.pack(fill='both', expand=True)
        frame2 = ctk.CTkFrame(tab2)
        frame2.pack(fill='both', expand=True)
        frame3 = ctk.CTkFrame(tab2)
        frame3.pack(fill='both', expand=True)
        frame4 = ctk.CTkFrame(tab3)
        frame4.pack(fill='both', expand=True)
        frame5 = ctk.CTkFrame(tab4) 
        frame5.pack(fill='both', expand=True)

    # Tab 1 Widgets: #

        # Column changer widget: #

        current_value = int(config['UI']['columns'])

        dropdown_label = ctk.CTkLabel(frame1, text="DISCLAIMER: Any changes you make here will only apply when you restart BRMM.\n\nNumber of columns:", font=("Segoe UI", 16), wraplength=250)
        dropdown_label.pack(pady=5)
        self.dropdown_options = ["2", "3", "4", "5"]
        self.selected_option = ctk.StringVar()
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
        self.selected_theme = ctk.StringVar()
        self.theme_menu = ctk.CTkComboBox(frame1, values=self.theme_options)
        self.theme_menu.pack()

        self.theme_menu.set(theme)
        self.selected_theme.set(theme)

        apply_theme_button = ctk.CTkButton(frame1, text="Apply Theme", command=self.apply_theme_changes, font=("Segoe UI", 14))
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
    
    # Tab 3 Widgets: #

        updater_label = ctk.CTkLabel(frame4, text=f"You are currently running BRMM, version {current_version_with_periods}\n\nUse the button provided below to manually check for an update.\n\nCopy and paste your 'settings.ini' into your updated BRMM directory for a seamless transition.", font=("Segoe UI",  16), wraplength=250)
        updater_label.pack(pady=5)
        updater_button = ctk.CTkButton(frame4, text="Update", command=update_brmm, font=("Segoe UI",  14))
        updater_button.pack(pady=10, ipady=5)

    # Tab 4 Widgets: #
        
        help_label = ctk.CTkLabel(frame5, text=f"If you are having any problems with BRMM, please use the button below to copy and paste some diagnostic information into Markdown format.", font=("Segoe UI",  16), wraplength=250)
        help_label.pack(pady=5)
        help_button = ctk.CTkButton(frame5, text="Copy Text", command=copy_to_clipboard, font=("Segoe UI", 14))
        help_button.pack(pady=10, ipady=5)

        reset_label = ctk.CTkLabel(frame5, text=f"As an alternative, you can also reset BRMM using the button below. Restart BRMM as soon as it resets and do not initiate any more downloads until BRMM is reopened.", font=("Segoe UI",  16), wraplength=250)
        reset_label.pack(pady=(15,5))
        reset_button = ctk.CTkButton(frame5, text="Reset BRMM", command=reset_brmm, font=("Segoe UI", 14))
        reset_button.pack(pady=10, ipady=5)
            
    # File Operations: #

    def browse_modpath(self):
        path = filedialog.askdirectory(title="Select your 'Mods' folder.")
        self.modspath_var.set(path)
        config['PATHS']['modpath'] = path
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def browse_pakspath(self):
        path = filedialog.askdirectory(title="Select your 'Paks' folder.")
        self.pakspath_var.set(path)
        config['PATHS']['pakspath'] = path
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def apply_changes(self, event=None):
        selected_option = self.dropdown_menu.get()
        config['UI']['columns'] = str(int(selected_option))
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

    def apply_theme_changes(self):
        selected_theme = self.theme_menu.get()
        config['UI']['theme'] = selected_theme
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
            
    # Window Launcher: #

    def open_options_window(parent):
        OptionsWindow(parent)

options_window = OptionsWindow.open_options_window

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
    
    @staticmethod
    def get_install_button_config(file_path, file_path_2 = "copper"):
        if check_if_exist(file_path) or check_if_exist(file_path_2):
            return {"text": "Install", "font": ("Segoe UI", 18), "fg_color": "#154483"}
        else:
            return {"text": "Install", "font": ("Segoe UI",  18)}
    
    @staticmethod
    def get_remove_button_config(file_path):
        if check_if_exist(file_path):
            return {"text": "Remove", "font": ("Segoe UI Semibold", 18), "fg_color": "#b3322e"}
        else:
            return {"text": "Remove", "font": ("Segoe UI Semibold", 18), "fg_color": "#951410"}

mod_title_font = ContentFormatting.MOD_TITLE_FONT
mod_content_font = ContentFormatting.MOD_CONTENT_FONT
install_button = ContentFormatting.INSTALL_BUTTON
install_button_packing = ContentFormatting.INSTALL_BUTTON_PACKING
remove_button = ContentFormatting.REMOVE_BUTTON
remove_button_packing = ContentFormatting.REMOVE_BUTTON_PACKING
create_image_label = ContentFormatting.create_image_label
create_image_label_packing = ContentFormatting.create_image_label_packing

# Uninstaller: #

def usuccessmessage():
    create_message_window("\nThe mod has been removed from Brick Rigs!\n\nYou can close this window now.\n", "Mod Status")

def notexists():
    create_message_window("\nThe mod is not installed into Brick Rigs.\n\nYou can close this window now.\n", "Mod Status")

# Main Window GUI: #

frame = ctk.CTkFrame(scrollable_frame)
frame.grid(row=0, column=0, rowspan=1, columnspan=2, sticky='nsew')

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

title = ctk.CTkLabel(frame, text="Available Mods:", font=("Segoe UI Semibold", 48), anchor="nw")
title.grid(row=0, column=0, padx=15, pady=15)

def open_options(frame):
        frame.options_window = OptionsWindow(frame)
        frame.options_window.mainloop()

options_button = ctk.CTkButton(frame, text="Settings", command=lambda: open_options(frame), font=("Segoe UI", 18))
options_button.grid(row=0, column=1, ipady=5)

# Define the order of the types: #

tab_view = ctk.CTkTabview(scrollable_frame)
tab_view.grid(row=1, column=0, sticky='nsew')
types_order = ['Maps', 'Visual', 'Gameplay', 'Items']

tabs = {}
for type in types_order:
    if type not in tabs:
        tabs[type] = tab_view.add(type)

tab_view._segmented_button.grid(sticky="W")

current_positions = {type: {'row': 0, 'col': 0} for type in types_order}

# Populate the tabs with mods: #

CACHE_DIR = 'image_cache'

def download_image(url, cache_dir=CACHE_DIR):
    os.makedirs(cache_dir, exist_ok=True)

    filename = os.path.join(cache_dir, url.split('/')[-1])
    
    if os.path.exists(filename):
        return Image.open(filename)
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
                
    return Image.open(filename)

for mod in data["mods"]:
    position = current_positions[mod["type"]]

    frame_10 = ContentFormatting.create_frame(tabs[mod["type"]])
    frame_10.grid(row=position['row'], column=position['col'], **ContentFormatting.FRAME_PADDING)

    position['col'] += 1

    if position['col'] >= int(number):
        position['col'] = 0
        position['row'] += 1

    textbox_16 = ctk.CTkLabel(frame_10, text=mod["name"], **ContentFormatting.MOD_TITLE_FONT)
    textbox_16.pack(anchor="center", padx=10, pady=10)

    # Image Loading: #

    image = download_image(mod["image"])
    image.thumbnail((480,  270))
    
    ctk_image = ctk.CTkImage(image, size=(480,  270))
    
    label = ctk.CTkLabel(frame_10, image=ctk_image, text="")
    label.pack(**create_image_label_packing('center'))

    textbox_17 = ctk.CTkLabel(frame_10, font=("Segoe UI", 16), text=mod["description"]+"\n\nSize: "+mod["size"]+"\nAuthor: "+mod["author"], wraplength=500)
    textbox_17.pack(anchor="center", padx=30, pady=15)
        
    # Download Handlers: #
    
    google_paths = {"gd": modpath, "gdpak": pakspath}
    discord_paths = {"d": modpath, "dpak": pakspath}

    if mod["installType"] in google_paths:
        destination = os.path.join(google_paths[mod["installType"]], mod["installpath"])
        destination2 = os.path.join(google_paths[mod["installType"]], mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda file_id=mod["install"], destination=f'{google_paths[mod["installType"]]}{mod["installpath"]}': download_googledrive_file(file_id, destination), **ContentFormatting.get_install_button_config(f"{modpath}{mod['installpath']}", f"{pakspath}{mod['installpath']}"))
        button.pack(**install_button_packing)

    elif mod["installType"] in discord_paths:
        destination = os.path.join(discord_paths[mod["installType"]], mod["installpath"])
        destination2 = os.path.join(discord_paths[mod["installType"]], mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda url=mod["install"], destination=f'{discord_paths[mod["installType"]]}{mod["installpath"]}': download_discord_file(url, destination), **ContentFormatting.get_install_button_config(f"{modpath}{mod['installpath']}", f"{pakspath}{mod['installpath']}"))
        button.pack(**install_button_packing)

    elif mod["installType"] == "github":
        destination = os.path.join(modpath, mod["installpath"])
        destination2 = os.path.join(modpath, mod["installpath"])
        button = ctk.CTkButton(frame_10, command=lambda url=mod["install"], destination=f'{modpath}{mod["installpath"]}': download_github_zipfile(url, destination), **ContentFormatting.get_install_button_config(f"{modpath}{mod['installpath']}", f"{pakspath}{mod['installpath']}")) #install_button
        button.pack(**install_button_packing)

    # File Removal Managers: #
    
    def remove_file(file_path, folder_path=None):
        if not os.path.exists(file_path):
            notexists()
            return app
        os.remove(file_path)
        if folder_path and os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        usuccessmessage()
        return app

    def command_func():
        remove_file(file_path, folder_path)
    
    paths = {"zip": modpath, "pak": pakspath}

    if mod["deinstallType"] == "zip":
        file_path = f'{paths[mod["deinstallType"]]}{mod["installpath"]}'
        folder_path = f'{paths[mod["deinstallType"]]}{mod["deinstallpath"]}'
        button = ctk.CTkButton(frame_10, command=lambda file_path=file_path, folder_path=folder_path: remove_file(file_path, folder_path), **ContentFormatting.get_remove_button_config(f"{modpath}{mod['installpath']}")) #remove_button
        button.pack(**remove_button_packing)


    elif mod["deinstallType"] == "pak":
        file_path = f'{paths[mod["deinstallType"]]}{mod["installpath"]}'
        button = ctk.CTkButton(frame_10, command=lambda file_path=file_path: remove_file(file_path), **ContentFormatting.get_remove_button_config(f"{pakspath}{mod['installpath']}")) #remove_button
        button.pack(**remove_button_packing)

app.mainloop()
