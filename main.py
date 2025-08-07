from flask import Flask, jsonify, send_from_directory, request, Response
from flask_cors import CORS
from seismic_viewer import get_seismic_data, get_ebcdic_header, get_file_metadata, get_file_path_from_api
import logging
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

@app.route('/get_file_path_from_api', methods=['GET'])
def serve_file_path_from_api():
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    app.logger.debug(f"Calling get_file_path_from_api with geofile_id: {geofile_id}")
    result = get_file_path_from_api(geofile_id, jwt_token)
    
    if 'error' in result:
        app.logger.error(f"Error in get_file_path_from_api: {result['error']}")
        return jsonify(result), 500
    
    app.logger.debug("Successfully retrieved file path from API")
    return jsonify(result)

@app.route('/get_seismic_data', methods=['GET'])
def serve_seismic_data():
    start_trace = int(request.args.get('start_trace', 0))
    end_trace = request.args.get('end_trace', None)
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)

    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400

    if end_trace is not None:
        end_trace = int(end_trace)
    
    app.logger.debug(f"Reading traces {start_trace} to {end_trace} using geofile_id: {geofile_id}")
    result = get_seismic_data(geofile_id=geofile_id, start_trace=start_trace, end_trace=end_trace, jwt_token=jwt_token)
    
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
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    app.logger.debug(f"Reading EBCDIC header using geofile_id: {geofile_id}")
    result = get_ebcdic_header(geofile_id=geofile_id, jwt_token=jwt_token)
    
    if result['error']:
        app.logger.error(f"Error in get ebcdic_header: {result['error']}")
        return jsonify(result), 500
    app.logger.debug("Successfully retrieved EBCDIC header")
    return jsonify(result)

@app.route('/get_file_metadata', methods=['GET'])
def serve_file_metadata():
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    app.logger.debug(f"Reading file metadata using geofile_id: {geofile_id}")
    result = get_file_metadata(geofile_id=geofile_id, jwt_token=jwt_token)
    
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