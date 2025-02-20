# AlecaFrame Inventory Parser

### Step 1.

Navigate to the folder where the script is installed using `cd <folder_path>`

### Step 2.

Use the `pip install -r requirements.txt` command to install required dependencies

### Step 3.

Copy `lastData.dat` from `%LOCALAPPDATA%\AlecaFrame` into the script folder. The script can also do this automatically if there is no file in the current directory.

Alternatively you can pass in the `lastData.dat` path through the command line using parameter `-p` or `--path`. Go to step 4 for how to run the script.

### Step 4.

Run the script with python: `python AlecaFrame-Inventory-Parser.py`

### Step 5.

You AlecaFrame inventory data will be saved to the `\output\lastData.json` file.
