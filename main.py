import logging
from flask import Flask, request, render_template, jsonify
import os
import json
import utils


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
            utils.File.file_architecture_check(filename=file, doc_folder=DOCUMENTS_FOLDER)
            

            file_type = utils.File.get_type_from_file(filename=file,
            doc_folder=DOCUMENTS_FOLDER)

            filtered.append({"filename" : file, "type" : file_type})

    files = filtered

    if request.method == 'POST':
        button = request.form['file-control']
        filename = button.split("|")[0]
        action = button.split("|")[1]
        if action == "view":
            text = utils.File.read( filename=filename,
                                    doc_folder=DOCUMENTS_FOLDER,
                                    type= "markdown")
            
            return render_template("view.html", filename=filename, text=text, title=f"View - {filename}")
        
        if action == "edit":
            text = utils.File.read( filename=filename,
                                    doc_folder=DOCUMENTS_FOLDER,
                                    type= "text")
            

            
            return render_template("editor.html", filename=filename, text=text, title=f"Edit - {filename}")      

        if action == "del":
            os.remove(f"{DOCUMENTS_FOLDER}/{filename}")

            files = os.listdir(DOCUMENTS_FOLDER)
        
            filtered = []
            for file in files:
                if file.endswith(('.txt')):
                    utils.File.file_architecture_check(filename=file, doc_folder=DOCUMENTS_FOLDER)
                    filtered.append(file)
        
            files = filtered


            return render_template("docs.html", files=files, title="Documents")

    return render_template("docs.html", files=files, title="Documents")



@app.route("/docs/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        # Пытаемся взять JSON
        data = request.get_json(silent=True)
        
        if data["action"] == "markdown-save":  # if we need to save file 
            text = data.get('text', '') # get content
            filename = data.get('filename', '')# get filename
            utils.File.write( # write data in file
                filename = filename,
                ctx = text.replace("    ", ""),
                doc_folder = DOCUMENTS_FOLDER,
                type="markdown")
            return render_template("editor.html", filename=filename, text=text, title=f"Edit - {filename}")  
        
        elif data["action"] == "markdown-view": # if we need to view file 
            text = data.get('text', '') # get content
            filename = data.get('filename', '') # get filename

            utils.File.write( # write data in file
                filename = filename,
                ctx = text.replace("    ", ""),
                doc_folder = DOCUMENTS_FOLDER,
                type="markdown")

            ctx = utils.File.read(filename=filename,
                       doc_folder=DOCUMENTS_FOLDER,
                       type= "markdown")
            
            return jsonify({"filename": filename, "text": ctx, "markdown": text}) # send data to show on page
        
    return render_template("editor.html", filename="New file.txt", text="# New file", title="Edit - New file.txt")

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


@app.route("/console",  methods=['GET', 'POST'])
def console():
    if request.method == 'POST':
        button = request.form['button']

        if button == "shutdown":
            os.system("shutdown")
    return render_template('console.html',  title=f"Console")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, use_reloader=True)