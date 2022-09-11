from urllib import request
from flask import Flask, json, request,jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['LOCAL_FOLDER'] = 'C:/Users/amita/Desktop/FTP'

@app.route('/', methods=['GET'])
def main():
    return "HTTP Files Transfer"

@app.route('/upload', methods=['POST'])
def upload_new_file():
    if 'file' not in request.files:
        res = jsonify({'message': 'No files to upload'})
        res.status_code = 400
        return res
    
    file = request.files['file']
    filename = secure_filename(file.filename)

    for f in list_files():
        if f == filename:
            res = jsonify({'message': 'There is a file with the same name'})
            res.status_code = 400
            return res

    file.save(os.path.join(app.config['LOCAL_FOLDER'], filename))
    res = jsonify({'message': 'File successfully uploaded'})
    res.status_code = 200
    return res

@app.route('/update', methods = ['PUT'])
def update_file():
    if 'file' not in request.files:
        res = jsonify({'message': 'No files to upload'})
        res.status_code = 400
        return res
    
    file = request.files['file']
    filename = secure_filename(file.filename)

    file.save(os.path.join(app.config['LOCAL_FOLDER'], filename))
    res = jsonify({'message': 'File successfully uploaded'})
    res.status_code = 200
    return res

@app.route('/all', methods=['GET'])
def list_all_files():
    return list_files()


@app.route('/getfile/<name>', methods = ['GET'])
def get_file(name):
    try:
        return send_from_directory(app.config["LOCAL_FOLDER"], path=name, as_attachment=True)
    except:
        res = jsonify({'message': 'File Not Found',
                        'Suggestion': "Try list all files with HTTP GET /all route"})
        res.status_code = 404
        return res


@app.route('/remove/<name>', methods=['DELETE'])
def delete_file(name):
    if name not in list_files():
        res = jsonify({'message': 'File Not Found',
                        'Suggestion': "Try list all files with HTTP GET /all route"})
        res.status_code = 404
        return res
    file_path = os.path.join(app.config['LOCAL_FOLDER'], name)
    os.remove(file_path)
    res = jsonify({'message': 'File deleted uploaded'})
    res.status_code = 200
    return res
    



def list_files():
    return os.listdir(app.config['LOCAL_FOLDER'])

if __name__ == "__main__":
    app.run(debug=True)