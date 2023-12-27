# Contributing to BRMM's GUI

BRMM requires that you edit `publicmoddata.json` to add another mod to BRMM. Here's an overview of the format used in BRMM's GUI:

## Raw JSON Format:
```
{
    "name": "Bricksdale Speedway",
    "installType": "gd",
    "deinstallType": "zip",
    "install": "1D6vJSi0rz6ix2oPLwFk9S2Bai2xOTGiS",
    "image": "https://github.com/anonymous-editor/BRMM/raw/main/M1.PNG",
    "description": "This map brings the world of American motorsports into Brick Rigs, with realistic props, lighting, Arizonian landscaping, and track layouts. There are many types of motorsports events here, ranging from demolition derbies to oval racing.",
    "size":"167 MB",
    "author":"batt",
    "installpath":"/BricksdaleSpeedway.zip",
    "deinstallpath":"/BricksdaleSpeedway"
    }
```

Let's group each category into two parts: `frontend`, and `backend`.

> [!IMPORTANT]
> `frontend` refers to code that changes aesthetics, while `backend` refers to code that changes the installation/removal method, per mod.

## Backend JSON Code:

### installType/deinstallType:
The first option is `installType`, which has 4 total options. This assigns an ID to the mod that lets the script download the mod correctly.
- `gd` (Google Drive download, `.zip ` format).
- `gdpak` (Google Drive download, `.pak` format).
- `d` (Direct Discord download, `.zip` format).
- `dpak` (Direct Discord download, `.pak` format).

The next option is `deinstallType`, which lets the script remove the mod correctly. There are two options here, which are both pretty self explanatory.
- `zip`
- `pak`

### install

After the two options is `install`, which provides the URL for downloading the mod. This depends on if the mod is being downloaded through Discord, or through Google Drive.

- Google Drive: Provide the file ID, after `/file/d/` in the URL. An example is provided below.
      ![image](https://github.com/anonymous-editor/BRMM/assets/74514726/b7355507-a2c7-4a20-a6d6-5237a09087c6)

- Discord: Provide everything in the file attachment's url up to and including the `?` symbol. Another example is provided below.
    * Original URL: `https://cdn.discordapp.com/attachments/751767065970475093/1188166613237772488/AdvancedScopes_RD_BOOSTY.zip?ex=65998963&is=65871463&hm=797a20e50d5b7d1ba18e31048b97484174ede19056c0142bd659361d72d0fda1&`
    * Modified URL: `https://cdn.discordapp.com/attachments/751767065970475093/1188166613237772488/AdvancedScopes_RD_BOOSTY.zip?`
      
