import os
import shutil
import datetime

# --- SETTINGS ---
# Path to the folder where game saves are located (where ORIGINAL_SAVE_FILENAME resides)
# Example: r"C:\Users\Username\AppData\Local\HalfSwordUE5\Saved\SaveGames"
# The '{os.path.expanduser("~")}' part will automatically be replaced by the current user's home directory (e.g., C:\Users\Username)
SAVE_FOLDER_PATH = os.path.join(os.path.expanduser("~"), r"AppData\Local\HalfSwordUE5\Saved\SaveGames")

# Name of the main game save file (without path, just the name with extension)
ORIGINAL_SAVE_FILENAME = "SG Gauntlet Progress.sav" 

# Name of the subfolder to store our backup saves
SAVE_SUBFOLDER_NAME = "GauntletSaves" 

def get_original_save_path():
    return os.path.join(SAVE_FOLDER_PATH, ORIGINAL_SAVE_FILENAME)

def get_backup_folder_path():
    backup_path = os.path.join(SAVE_FOLDER_PATH, SAVE_SUBFOLDER_NAME)

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
        print(f"Created save backup folder: {backup_path}")
    return backup_path

def get_backup_save_path(filename):
    return os.path.join(get_backup_folder_path(), filename)

def generate_unique_save_name():
    now = datetime.datetime.now()
    return now.strftime("auto_%Y-%m-%d_%H:%M.sav")

def delete_saves():
    available_saves = list_saves()
    if not available_saves:
        return

    while True:
        choice = input("Enter the numbers of saves to delete (e.g., '1,3,5') or 'q' to cancel: ").strip()
        if choice.lower() == 'q':
            print("Deletion cancelled.")
            return
        
        try:
            choices = [int(num.strip()) for num in choice.split(',')]
            valid_choices = []
            for num in choices:
                if 1 <= num <= len(available_saves):
                    valid_choices.append(num)
                else:
                    print(f"Warning: Save number {num} is invalid and will be skipped.")
            
            if not valid_choices:
                print("No valid save numbers entered. Please try again.")
                continue

            saves_to_delete = sorted(list(set(valid_choices)), reverse=True)
            
            confirm = input(f"Are you sure you want to delete these saves: {', '.join([available_saves[i-1] for i in saves_to_delete])}? (yes/no): ").lower()
            if confirm == 'yes':
                deleted_count = 0
                for index in saves_to_delete:
                    save_name = available_saves[index - 1]
                    save_full_path = get_backup_save_path(save_name)
                    try:
                        os.remove(save_full_path)
                        print(f"Deleted save: '{save_name}'.")
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting '{save_name}': {e}")
                print(f"Successfully deleted {deleted_count} save(s).")
                break
            elif confirm == 'no':
                print("Deletion cancelled.")
                break
            else:
                print("Invalid confirmation. Please type 'yes' or 'no'.")
        except ValueError:
            print("Invalid input format. Please enter numbers separated by commas, or 'q'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def create_new_save(custom_name=None):
    original_full_path = get_original_save_path()
    backup_folder = get_backup_folder_path()

    if not os.path.exists(original_full_path):
        print(f"Error: Original save file '{original_full_path}' not found.")
        print("Please ensure the game has saved at least once and the path is configured correctly.")
        return

    if custom_name:
        if not custom_name.endswith(".sav"):
            save_name = f"{custom_name}.sav"
        else:
            save_name = custom_name
    else:
        save_name = generate_unique_save_name()

    new_save_full_path = get_backup_save_path(save_name)

    try:
        shutil.copy2(original_full_path, new_save_full_path)
        print(f"New save '{save_name}' successfully created in '{SAVE_SUBFOLDER_NAME}' folder.")
    except Exception as e:
        print(f"Error creating new save: {e}")

def get_sorted_saves_by_modification_time():
    backup_folder = get_backup_folder_path()
    saves = [f for f in os.listdir(backup_folder) if f.endswith(".sav")]
    
    saves_with_time = []
    for s in saves:
        try:
            full_path = get_backup_save_path(s)
            mod_time = os.path.getmtime(full_path)
            saves_with_time.append((mod_time, s))
        except OSError:
            continue

    return [s[1] for s in sorted(saves_with_time)]


def list_saves():
    sorted_saves = get_sorted_saves_by_modification_time()

    if not sorted_saves:
        print(f"No additional saves found in '{SAVE_SUBFOLDER_NAME}' folder.")
        return []
    
    print(f"\nAvailable saves in '{SAVE_SUBFOLDER_NAME}':")
    for i, save in enumerate(sorted_saves):
        print(f"{i+1}. {save}")
    return sorted_saves

def load_save(selected_save_name=None, auto_load_latest=False):
    available_saves = get_sorted_saves_by_modification_time()
    if not available_saves:
        print("No saves to load.")
        return

    if auto_load_latest and not selected_save_name:
        selected_save_name = available_saves[-1] 
        print(f"Auto-load: selected the latest save '{selected_save_name}'.")
    elif not selected_save_name:
        list_saves()
        while True:
            try:
                choice = input("Enter the number of the save you want to load (or 'q' to cancel): ")
                if choice.lower() == 'q':
                    print("Save loading cancelled.")
                    return

                choice_index = int(choice) - 1
                if 0 <= choice_index < len(available_saves):
                    selected_save_name = available_saves[choice_index]
                    break
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")
    
    if not selected_save_name:
        return

    original_full_path = get_original_save_path()
    selected_save_full_path = get_backup_save_path(selected_save_name)

    if not os.path.exists(selected_save_full_path):
        print(f"Error: Save file '{selected_save_name}' not found in '{SAVE_SUBFOLDER_NAME}' folder.")
        return

    try:
        if os.path.exists(original_full_path):
            os.remove(original_full_path)
            print(f"Current save file '{ORIGINAL_SAVE_FILENAME}' deleted.")
        else:
            print(f"Current save file '{ORIGINAL_SAVE_FILENAME}' not found. Continuing...")

        shutil.copy2(selected_save_full_path, original_full_path)
        print(f"Save '{selected_save_name}' successfully loaded (replaced '{ORIGINAL_SAVE_FILENAME}').")
        print("You can now launch the game. It will load the last save.")

    except Exception as e:
        print(f"Error loading save: {e}")

def delete_saves():
    """Deletes one or more selected saves from the subfolder."""
    available_saves = list_saves()
    if not available_saves:
        return

    while True:
        try:
            choice = input("Enter the numbers of the saves you want to delete, separated by commas (e.g., '1,3,5') or 'q' to cancel: ")
            if choice.lower() == 'q':
                print("Save deletion cancelled.")
                return
            
            selected_indices = []
            for item in choice.split(','):
                item = item.strip()
                if not item:
                    continue
                index = int(item) - 1
                if 0 <= index < len(available_saves):
                    selected_indices.append(index)
                else:
                    print(f"Invalid number '{item}'. Please try again.")
                    selected_indices = []
                    break
            
            if selected_indices:
                break
            elif choice.strip():
                print("No valid save numbers entered. Please try again.")

        except ValueError:
            print("Invalid input. Please enter numbers separated by commas or 'q'.")
    
    deleted_count = 0
    for index in sorted(list(set(selected_indices)), reverse=True):
        save_to_delete_name = available_saves[index]
        save_to_delete_full_path = get_backup_save_path(save_to_delete_name)
        
        try:
            os.remove(save_to_delete_full_path)
            print(f"Successfully deleted save: '{save_to_delete_name}'.")
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting save '{save_to_delete_name}': {e}")
            
    if deleted_count > 0:
        print(f"Total {deleted_count} save(s) deleted.")
    else:
        print("No saves were deleted.")


def main_menu():
    """Main menu for user interaction."""
    while True:
        print("\n--- Game Save Manager ---")
        print("1. Create new save")
        print("2. Load existing save")
        print("3. Show list of saves")
        print("4. Delete saves")
        print("5. Exit")

        choice = input("Select an action (or just press Enter to load the latest save): ").strip()

        if choice == '1':
            custom_name_input = input("Enter a name for the new save (leave blank for automatic name): ")
            create_new_save(custom_name_input.strip() if custom_name_input.strip() else None)
        elif choice == '2':
            load_save(auto_load_latest=False)
        elif choice == '3':
            list_saves()
        elif choice == '4':
            delete_saves()
        elif choice == '5':
            print("Thank you for using the Save Manager!")
            break
        elif not choice:
            print("No selection made. Auto-loading the latest save...")
            load_save(auto_load_latest=True)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if not os.path.exists(SAVE_FOLDER_PATH):
        print(f"Error: Save folder '{SAVE_FOLDER_PATH}' not found.")
        print("Please create this folder or specify the correct path in the SAVE_FOLDER_PATH variable.")
    else:
        get_backup_folder_path() 
        main_menu()