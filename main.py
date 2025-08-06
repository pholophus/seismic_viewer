from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from seismic_viewer import get_seismic_data, get_ebcdic_header, get_file_metadata
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Configuration - single source of truth for file path
SEISMIC_FILE_PATH = '../data/MYS1993P20152DM01PMOREGION/MYS1993P20152DM01PMOREGION_RC93-002_UNFILT_SCAL_MIGR_flatten.sgy'

@app.route('/get_seismic_data', methods=['GET'])
def serve_seismic_data():
    start_trace = int(request.args.get('start_trace', 0))
    end_trace = request.args.get('end_trace', None)

    if end_trace is not None:
        end_trace = int(end_trace)
    app.logger.debug(f"Reading traces {start_trace} to {end_trace} from {SEISMIC_FILE_PATH}")
    result = get_seismic_data(SEISMIC_FILE_PATH, start_trace, end_trace)
    if 'error' in result:
        app.logger.error(f"Error in get_seismic_data: {result['error']}")
        return jsonify(result), 500
    app.logger.debug("Successfully processed SEG-Y data")
    return jsonify(result)

@app.route('/get_ebcdic_header', methods=['GET'])
def serve_ebcdic_header():
    app.logger.debug(f"Reading EBCDIC header from {SEISMIC_FILE_PATH}")
    result = get_ebcdic_header(SEISMIC_FILE_PATH)
    if result['error']:
        app.logger.error(f"Error in get ebcdic_header: {result['error']}")
        return jsonify(result), 500
    app.logger.debug("Successfully retrieved EBCDIC header")
    return jsonify(result)

@app.route('/get_file_metadata', methods=['GET'])
def serve_file_metadata():
    app.logger.debug(f"Reading file metadata from {SEISMIC_FILE_PATH}")
    result = get_file_metadata(SEISMIC_FILE_PATH)
    if result['error']:
        app.logger.error(f"Error in get_file_metadata: {result['error']}")
        return jsonify(result), 500
    app.logger.debug("Successfully retrieved file metadata")
    return jsonify(result)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)