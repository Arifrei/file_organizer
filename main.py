import os
import shutil
from os import mkdir

FILE_TYPES = {
    "Documents": ['.pdf', '.docx', '.txt', '.xls', '.xlsx', '.pptx'],
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    "Videos": ['.mp4', '.avi', '.mov', '.mkv'],
    "Audio": ['.mp3', '.wav', '.aac'],
    "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
    "Scripts": ['.py', '.js', '.sh', '.bat'],
    "Others": []
}

moved_files = []

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return "others"

def organize_files(filepath):
    if not os.path.isdir(filepath):
        print("Invalid filepath")
        return

    for item in os.listdir(filepath):
        item_path = os.path.join(filepath, item)

        if os.path.isfile(item_path):
            _, ext = os.path.splitext(item)
            category = get_category(ext)
            category_folder = os.path.join(filepath, category)

            if not os.path.exists(category_folder):
                os.mkdir(category_folder)

            dest_path = os.path.join(category_folder, item)
            shutil.move(item_path, dest_path)
            moved_files.append((dest_path, item_path))

def undo_last_move():
    while moved_files:
        moved_to, original = moved_files.pop()
        if os.path.exists(moved_to):
            shutil.move(original, moved_to)
        else:
            print(f"File not found for undo: {moved_to}")

organize_files("C:/Users/Hello/Documents")