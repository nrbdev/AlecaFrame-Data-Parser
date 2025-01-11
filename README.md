# AlecaFrame Inventory Parser

### Step 1.

Navigate to the folder where the script is installed using `cd <folder_path>`

### Step 2.

Use the `pip install -r requirements.txt` command to install required dependencies

### Step 3.

Copy `lastData.dat` from `%LOCALAPPDATA%\AlecaFrame` into the folder where the script is installed OR let the script do it automatically

### Step 4.

Run the script with python: `python AlecaFrame_Data_Parser.py`

### Step 5.

All your parsed AlecaFrame data is saved into the `data` directory.

`data\lastData.json` is your unmodified AlecaFrame inventory.

`data\lastData.out.json` is your inventory from AlecaFrame fixed up a lil' so it can be imported into openWF

`data\lastData.ldts.json` is your exported loadout configs for importing into openWF (coming eventually)

##

# Importing to OpenWF

Will add this when I have time
