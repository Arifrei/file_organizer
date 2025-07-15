import os
import shutil
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')

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
    return "Others"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/organize", methods=["GET", "POST"])
def organize_files():
    message = ""
    filepath = request.form.get("folder")
    if not os.path.isdir(filepath):
        message = "Invalid filepath"
        return render_template("index.html", status=message)

    file_found = False
    for item in os.listdir(filepath):
        item_path = os.path.join(filepath, item)

        if os.path.isfile(item_path):
            file_found = True
            _, ext = os.path.splitext(item)
            category = get_category(ext)
            category_folder = os.path.join(filepath, category)

            if not os.path.exists(category_folder):
                os.mkdir(category_folder)

            dest_path = os.path.join(category_folder, item)
            shutil.move(item_path, dest_path)
            moved_files.append((dest_path, item_path))
            message = "Files organized"
    if not file_found:
        message = "No files to organize"
    return render_template("index.html", status=message)

@app.route("/undo")
def undo():
    message = ""
    if moved_files:
        while moved_files:
            moved_to, original = moved_files.pop()
            if os.path.exists(moved_to):
                shutil.move(moved_to, original)
                message= "Undo successful"
            else:
                message = f"File not found for undo: {moved_to}"
    else:
        message = "No files to move back"
    return render_template("index.html", status=message)

if __name__ == "__main__":
    app.run(debug=True)