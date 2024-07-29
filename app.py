from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from models import db, WellLog, SeismicData
from integration import integrate_datasets
from parser import parse_seismic_data, parse_well_log, convert_to_common_format
import psycopg2
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/yourdatabase'


# Initialising the configuration of the database: SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
# app.config["SQLALCHEMY_BINDS"] = {
#     'registration': 'sqlite:///valentina_new_student.db',
#     'web_content':'sqlite:///web_contents.db',
#     'SignUp' : 'sqlite:///SignUp.db'
# }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "K0lade001."
db.init_app(app)




@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Process file (translate to common format)
    if filename.endswith('.las'):
        data = parse_well_log(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        common_format_data = convert_to_common_format(data)
        well_log = WellLog(data=common_format_data)
        db.session.add(well_log)
        db.session.commit()
    elif filename.endswith('.segy'):
        data = parse_seismic_data(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        common_format_data = convert_to_common_format(data)
        seismic_data = SeismicData(data=common_format_data)
        db.session.add(seismic_data)
        db.session.commit()
    return jsonify({"message": "File uploaded and processed successfully"}), 200

@app.route('/api/integrated-data', methods=['GET'])
def get_integrated_data():
    well_logs = WellLog.query.all()
    seismic_data = SeismicData.query.all()
    # Example integration logic
    integrated_data = integrate_datasets([wl.data for wl in well_logs], [sd.data for sd in seismic_data])
    return jsonify(integrated_data)

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory('template', 'index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
