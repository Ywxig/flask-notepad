import logging
from flask import Flask, request, render_template
import os
import json
import utils
import markdown

app = Flask(__name__, static_folder='static')


MUSIC_FOLDER = os.path.join('static', 'music_lib')
DOCUMENTS_FOLDER = os.path.join("documents")

# Disable request logging
app.logger.setLevel(logging.ERROR)

@app.route("/")
def main():
    CONFIG = open("config.json", "r").read()
    ABOUT = json.loads(CONFIG)
    return render_template("index.html", name_app=ABOUT["name"], version=ABOUT["version"], title=ABOUT["name"])

@app.route("/docs", methods=['GET', 'POST'])
def docs():
    #This function for use server as data storage with online connect
    # read all files in DOCUMENTS_FOLDER
    files = os.listdir(DOCUMENTS_FOLDER)

    filtered = []
    for file in files:
        if file.endswith(('.txt')):
            filtered.append(file)

    files = filtered

    if request.method == 'POST':
        button = request.form['file-control']
        filename = button.split("|")[0]
        action = button.split("|")[1]
        if action == "view":
            text = utils.File.read(filename=filename,
                                   doc_folder=DOCUMENTS_FOLDER)
            return render_template("view.html", filename=filename, text=markdown.markdown(text), title=f"View - {filename}")
        else:
            text = utils.File.read(filename=filename,
                                   doc_folder=DOCUMENTS_FOLDER)
            return render_template("editor.html", filename=filename, text=text, title=f"Edit - {filename}")        

    return render_template("docs.html", files=files, title="Documents")



@app.route("/docs/edit", methods=['GET', 'POST'])
def edit():
    #This function for use server as data storage with online connect

    if request.method == 'POST':
        text = request.form['text']
        title = request.form['title']
        button = request.form['button']
        if button == "save":
            utils.File.write(
                filename = title,
                ctx = text.replace("\r", ""),
                doc_folder = DOCUMENTS_FOLDER)

            return render_template("view.html", filename=title, text=markdown.markdown(text), title=f"View - {title}")
        else:
            return render_template("editor.html", filename=title, text=text, title=f"Edit - {title}")

    return render_template("editor.html", filename="New file.txt", text="# New file", title=f"Edit - New file.txt")

@app.route("/music")
def music():
    # read all file in music_lib
    tracks = os.listdir(MUSIC_FOLDER)
    # filtered fils

    filtered = []
    for track in tracks:
        if track.endswith(('.mp3', '.m4a', '.wav')):
            filtered.append(track)

    tracks = filtered

    return render_template('music.html', tracks=tracks, title=f"Music")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)