<p align="center">
  <img src="https://github.com/anonymous-editor/BRMM/assets/74514726/a21722a8-dcd3-4c3e-ae69-e05cb3f8d58f" width=50% height=50%>
</p>

## System Requirements:

```
Windows 10/11, 64 bit
Brick Rigs, version 1.6+
```

## What is This?

This is BRMM, an unofficial, 'plug and play' mod management solution for Brick Rigs. It can:
- Load all mod entries in the GUI through the web.
- Choose and remember your Brick Rigs install path.
- Install and/or extract mods to those paths.
- Display prompts about if the mod is installed/not, etc.

## Mod Showcase:

> [!TIP]
> Be sure to open the video in a new tab.

HUGE thanks to Andi_pog for making this vid to showcase BRMM.

<p align="center">
  <a href="https://www.youtube.com/watch?v=N1n8hyOlo_k" target="_blank" rel="noopener noreferrer">
     <img src="https://img.youtube.com/vi/N1n8hyOlo_k/maxresdefault.jpg" alt="Video">
  </a>
</p>

## Install Guide:

> [!IMPORTANT]
> Your antivirus may prevent you from downloading or running this program. This is a false positive, so feel free to make an exception for BRMM in your antivirus. The source code is included for anyone concerned.

> [!TIP]
> When you close the settings app, you **will** get an error that reads:
> ```
> File "c:\Users\%username%\path\to\BRMMxxx.exe", line 195, in apply_changes
>   selected_option = self.dropdown_menu.get()
>                      ^^^^^^^^^^^^^^^^^^^^^^^^
> File "C:\Users\%username%\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\customtkinter\windows\widgets\ctk_combobox.py", line 397, in get
>    return self._entry.get()
>           ^^^^^^^^^^^^^^^^^
> File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.496.0_x64__qbz5n2kfra8p0\Lib\tkinter\__init__.py", line 3124, in get
>   return self.tk.call(self._w, 'get')
>          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> _tkinter.TclError: invalid command name ".!ctkframe.!canvas.!ctkscrollableframe.!ctkframe17.!optionswindow.!ctktabview.!ctkframe.!ctkframe.!ctkcombobox.!entry"
> ```
> This error is **NOT** a bug and only warns you about trying to edit a value that the app is using. If you change anything in the settings menu, you have to restart BRMM for your changes to apply correctly.

BRMM is made entirely in **Python 3.12.1** to handle the file operations and the GUI.

To use BRMM, download `BRMM1xx_x64.zip` through the "Releases" page or from [this link](https://github.com/anonymous-editor/BRMM/releases/tag/1.5.0).

Once BRMM launches, you should see two windows as shown below:

![Screenshot 2023-12-26 202023](https://github.com/anonymous-editor/BRMM/assets/74514726/ed92b550-aba1-4302-8e46-388b5694a7de)

You can use the terminal to check if your download operations are successful or not.

## Contributing to BRMM

### Source Code:

Anyone (who wants to improve BRMM) can make pull requests to `BRMM_latest.py`. Be sure to provide a description of what you want to change however, so that it is more likely to be approved. This is a **semi-community project**, so please don't fork the project into another public repository, unless if it is being used to assist with this project.

You can run BRMM from source by using [these instructions](https://github.com/anonymous-editor/BRMM/blob/main/SOURCECODE.md).

### GUI:

You can add mod entries to BRMM through [this `.md` file](https://github.com/anonymous-editor/BRMM/blob/main/JSONEDITING.md). All instructions are provided in the link.

## Credits:
- [KoT3isGood](https://github.com/KoT3isGood): Created a draft of implementing JSON code into BRMM, along with creating other commits.
- [Iridium-7](https://github.com/Iridium-7): Added some configuration values into the original BRMM source code.
