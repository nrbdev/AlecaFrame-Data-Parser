# AlecaFrame Inventory Parser

### Step 1.

Navigate to the folder where the script is installed using `cd <folder_path>`

### Step 2.

Use the `pip install -r requirements.txt` command to install required dependencies

### Step 3.

Copy `lastData.dat` from `%LOCALAPPDATA%\AlecaFrame` into the folder where the script is installed OR let the script do it automatically

Alternatively you can pass in the `lastData.dat` path through the command line

### Step 4.

Run the script with python: `python AlecaFrameDataDecompiler.py`

### Step 5.

All your parsed AlecaFrame data is saved into the `output` directory.

`output\lastData.json` is your parsed AlecaFrame inventory.

You can ignore `output\lastData_patched.json`
