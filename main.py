from flask import Flask, jsonify, send_from_directory, request, Response
from flask_cors import CORS
from seismic_viewer import get_seismic_data, get_ebcdic_header, get_file_metadata
import logging
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Configuration - single source of truth for file path
SEISMIC_FILE_PATH = '/Users/afedsetup/Documents/afed_documents/2D Seismic/2D MALAY BASIN/MYS19892DM2PM-5_8/MYS19892DM2PM-5_8_P89A231_FILT_SCAL_MIGR.sgy'
SEISMIC_FILE_PATH = '../data/MYS1993P20152DM01PMOREGION/MYS1993P20152DM01PMOREGION_RC93-002_UNFILT_SCAL_MIGR_flatten.sgy'
# SEISMIC_FILE_PATH = '/mnt/skkmigassfs/West Bangkanai/2013_AFE 13-0004_2D Seismic Reprocessing (West Bangkanai Teweh 2D)/WEST_BANGKANAI TEWEH 2D/4. FINAL_PSTM_STACK/FINAL_PSTM_STACK_KT85_02.sgy'
# SEISMIC_FILE_PATH = '/Volumes/homes/public/SKKMigas_WestBangkanai/Seismic/2013_AFE 13-0004_2D_seismic_Repro_WestBangkanai_Teweh_2D/West_Bangkanai_Teweh_2D/4. FINAL_PSTM_STACK/FINAL_PSTM_STACK_KT85_02.sgy'
# SEISMIC_FILE_PATH = '/root/seismic_data/2d/FINAL_PSTM_STACK_KT85_02.sgy'

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
    
    # Extract binary data and metadata
    binary_data = result['data']
    metadata = {k: v for k, v in result.items() if k != 'data'}
    
    # Create response with binary data and JSON metadata in headers
    response = Response(binary_data, mimetype='application/octet-stream')
    response.headers['X-Metadata'] = json.dumps(metadata)
    response.headers['Access-Control-Expose-Headers'] = 'X-Metadata'
    
    app.logger.debug("Successfully processed SEG-Y data")
    return response

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
    app.run(debug=False, host='0.0.0.0', port=5001)