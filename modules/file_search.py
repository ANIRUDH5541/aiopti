import os
import platform
import subprocess
import psutil  # To handle file closing
import spacy

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def get_user_folder():
    """Returns the path to the user's home directory."""
    return os.path.expanduser("~")

def map_folder_name(folder_name):
    """
    Map spoken folder names to system folder paths.
    """
    user_folder = get_user_folder()
    folders = {
        "downloads": os.path.join(user_folder, "Downloads"),
        "documents": os.path.join(user_folder, "Documents"),
        "desktop": os.path.join(user_folder, "Desktop"),
        "pictures": os.path.join(user_folder, "Pictures"),
        "videos": os.path.join(user_folder, "Videos"),
        "music": os.path.join(user_folder, "Music"),
    }
    return folders.get(folder_name.lower(), None)

def extract_file_and_folder(command):
    """
    Use NLP to extract the file name and folder name from a spoken command.
    """
    doc = nlp(command)
    file_keywords = []
    folder_name = None

    for token in doc:
        # File names (with extensions)
        if token.text.lower().endswith(('.txt', '.pdf', '.docx', '.xlsx', '.png', '.jpg', '.mp4')):
            file_keywords.append(token.text.lower())

        # Folder names
        if token.text.lower() in ["downloads", "documents", "desktop", "pictures", "videos", "music"]:
            folder_name = token.text.lower()

    # Return file name as a joined keyword string if found
    file_name = " ".join(file_keywords) if file_keywords else None
    return file_name, folder_name

def search_files(root_directory, file_keywords):
    """
    Search for files matching keywords in the specified directory.

    Args:
        root_directory (str): Directory to search.
        file_keywords (str): Keywords extracted from the file name.

    Returns:
        list: List of matched file paths.
    """
    matched_files = []

    # Walk through the file system
    for root, _, files in os.walk(root_directory):
        for file in files:
            if all(keyword in file.lower() for keyword in file_keywords.split()):
                matched_files.append(os.path.join(root, file))
    return matched_files

def choose_file_to_open(matched_files):
    """
    Displays multiple files for the user to choose from.

    Args:
        matched_files (list): List of matched file paths.

    Returns:
        str: The selected file path.
    """
    print("Multiple files found:")
    for i, file in enumerate(matched_files):
        print(f"{i + 1}. {file}")

    while True:
        try:
            choice = int(input("Enter the number of the file to open: "))
            if 1 <= choice <= len(matched_files):
                return matched_files[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def open_file(file_path):
    """
    Opens the specified file.

    Args:
        file_path (str): Path of the file to open.
    """
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(["open", file_path])
    else:  # Linux
        subprocess.call(["xdg-open", file_path])

def close_file(file_name):
    """
    Closes a file/application by its name.

    Args:
        file_name (str): Name or partial name of the file to close.
    """
    closed = False
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            # Check if the process name or command line contains the file name
            if file_name.lower() in " ".join(proc.info['cmdline']).lower():
                proc.terminate()  # Attempt to close the process
                closed = True
                print(f"Closed: {file_name}")
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not closed:
        print(f"No open process found for: {file_name}")

def handle_file_search_command(command):
    """
    Process a spoken command to search and open a file.
    """
    file_keywords, folder_name = extract_file_and_folder(command)

    if not file_keywords:
        return "I couldn't identify the file name. Please try again."

    if folder_name:
        folder_path = map_folder_name(folder_name)
        if not folder_path:
            return f"I couldn't locate the {folder_name} folder."
    else:
        folder_path = get_user_folder()  # Search root directory if no folder specified

    # Search for files
    matched_files = search_files(folder_path, file_keywords)

    if not matched_files:
        return "File not found."

    if len(matched_files) > 1:
        file_to_open = choose_file_to_open(matched_files)
    else:
        file_to_open = matched_files[0]

    # Open the chosen file
    open_file(file_to_open)
    return f"Opening file: {file_to_open}"
