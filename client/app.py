import json
import os
import datetime
import requests
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
app = Flask(__name__)
UPLOAD_FOLDER = str(Path(__file__).parents[1]) + "/api/data_input"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=('GET', 'POST'))
def get_data_from_user():
    """Get data from user and send it to the api."""
    if request.method == 'POST':
        url = 'http://127.0.0.1:5000/api/transformation/itrf'
        data = json.loads(json.dumps(dict(request.form)))
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename = os.path.splitext(filename)[0] + "_" + str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + ".xlsx"))
        file_path = app.config['UPLOAD_FOLDER'] + "/" + filename + ".xlsx"
        data_json={'file': file_path,
                   'filename': filename,
                   'itrf_begin': 2008,
                   'epoch_begin': float(data['epoch_begin'][0]),
                   'itrf_final': 1994,
                   'epoch_final': float(data['epoch_final'][0]),
                   'email': data['email'][0],
                   'velocity': data['velocity'][0],
                   'date': str(datetime.datetime.now())
                   }
        send = requests.post(url, json=data_json)
        res = send.status_code
        if res == 200:
            return render_template('index.html', arguments={'error': False, 'email':data['email'][0]})
        else:
            return render_template('index.html', arguments={'error': True})
    return render_template('index.html', arguments={'error': None})



if __name__ == '__main__':
    app.run()
