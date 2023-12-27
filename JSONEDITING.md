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

  

  These options choose how 
