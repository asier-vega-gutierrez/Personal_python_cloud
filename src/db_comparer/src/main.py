from config.config import ApplicationConfiguration
from sqlite.sqlite import Sqlite
import pandas as pd
import json
import os
from flask import Flask, jsonify, request


UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
config = ApplicationConfiguration('asier')


@app.route('/upload_local', methods=['POST'])
def upload():

    if request.method == 'POST':

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "asier_local.db"))

        return f"File {file.filename} uploaded successfully \n", 200


@app.route('/upload_cloud', methods=['POST'])
def upload():

    if request.method == 'POST':

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "asier_cloud.db"))

        return f"File {file.filename} uploaded successfully \n", 200

# Call this method to compare the two actual dbs (must be uploaded firts)
@app.route('/compare', methods=['GET'])
def compare():

    if request.method == 'GET':
        
        # Read the bd information
        local_db = Sqlite(config.APP_RECEIVED_DB_PATH)
        cloud_db = Sqlite(config.APP_STORED_DB_PATH)

        # Compare the ids to find diferences
        ids_to_uploada = pd.DataFrame(data = (set(local_db.data[0].values) - set(cloud_db.data[0].values)) ) 
        #print(ids_to_uploada)

        # Save the response
        with open("output/ids.json", "w+") as json_file:
            json.dump(ids_to_uploada.to_json(), json_file)
        
        # Send the respose back
        return jsonify(ids_to_uploada.to_json()), 200


    
# Test GET request
#curl -X GET http://localhost:5000/compare

# Test POST request with file
#curl -X POST -F "file=@/home/asier/Personal_cloud/src/local_sync_client/db/tracker.db" http://localhost:5000/upload


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)