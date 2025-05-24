# HalfSword Savior

A simple Python script (`HalfSword_savior.py`) to manage your HalfSword game saves, allowing you to create multiple backups and load them easily.

---

## Features

* **Create New Saves:** Back up your current game progress with an automatic timestamped name or a custom name.
* **Load Existing Saves:** Replace your current game save with any of your created backups.
* **List Saves:** View all your available backup saves.
* **Delete Saves:** Remove unwanted backup saves.
* **Auto-load Latest:** Quickly load your most recent backup directly from the main menu.

---

## Setup

1.  **Download:** Save the `HalfSword_savior.py` file to a convenient location on your computer.
2.  **Configuration:** Open the `HalfSword_savior.py` file with a text editor (like Notepad, VS Code, Sublime Text).
    * Ensure the `SAVE_FOLDER_PATH` variable is correctly set to your HalfSword save game directory. The default path is usually:
        ```python
        SAVE_FOLDER_PATH = os.path.join(os.path.expanduser("~"), r"AppData\Local\HalfSwordUE5\Saved\SaveGames")
        ```
        You typically won't need to change this unless your game saves are in a non-standard location.
    * Confirm `ORIGINAL_SAVE_FILENAME` is set to `"SG Gauntlet Progress.sav"`.
    * You can change `SAVE_SUBFOLDER_NAME` if you prefer a different name for your backup folder (default is `"GauntletSaves"`).

---

## How to Use

1.  **Run the Script:** Double-click `HalfSword_savior.py` or run it from your terminal: `python HalfSword_savior.py`
2.  **Main Menu:**
    * **1. Create new save:** This will copy your current `SG Gauntlet Progress.sav` into the `GauntletSaves` subfolder. You can provide a custom name (e.g., "MyEpicRun") or leave it blank for an automatic timestamp (e.g., "auto\_2023-10-27\_14:30.sav").
    * **2. Load existing save:** This will show you a numbered list of all your backup saves. Enter the number corresponding to the save you wish to load. This will **delete your current `SG Gauntlet Progress.sav`** and replace it with the selected backup.
    * **3. Show list of saves:** Displays all the `.sav` files found in your `GauntletSaves` subfolder.
    * **4. Delete saves:** Allows you to select one or more saves by number to delete them from your backup folder.
    * **5. Exit:** Closes the script.
    * **Press Enter (no input):** This shortcut will automatically load the *latest* save file from your `GauntletSaves` folder.
