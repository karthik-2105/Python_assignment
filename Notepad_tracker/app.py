from flask import Flask, request
from git import Repo
import os
from datetime import datetime

app = Flask(__name__)

NOTES_DIR = "notes"
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

# Initialize Git repository
if not os.path.exists(os.path.join(NOTES_DIR, ".git")):
    repo = Repo.init(NOTES_DIR)
else:
    repo = Repo(NOTES_DIR)


@app.route('/')
def home():
    return '''
        <h2>📝 Notepad Tracker</h2>
        <form action="/save" method="POST">
            <label>Enter filename (with .txt):</label><br>
            <input type="text" name="filename" required><br><br>
            <label>Write your note:</label><br>
            <textarea name="content" rows="10" cols="60"></textarea><br><br>
            <label>Save to directory (default: notes/):</label><br>
            <input type="text" name="directory" placeholder="notes"><br><br>
            <button type="submit">Save Note</button>
        </form>
    '''

@app.route('/save', methods=['POST'])
def save_note():
    filename = request.form['filename']
    content = request.form['content']
    directory = request.form.get('directory', 'notes').strip() or 'notes'

    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    # Save file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Git commit — use relative path
    if not os.path.exists(os.path.join(directory, ".git")):
        repo = Repo.init(directory)
    else:
        repo = Repo(directory)

    # ✅ Convert to relative path (important!)
    relative_path = os.path.relpath(file_path, start=repo.working_tree_dir)

    repo.index.add([relative_path])
    repo.index.commit(f"Auto-save {filename} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return f"<h3>✅ Note '{filename}' saved and committed successfully!</h3><a href='/'>Back</a>"


if __name__ == '__main__':
    app.run(debug=True)
