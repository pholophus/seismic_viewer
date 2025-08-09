from flask import Flask, jsonify, send_from_directory, request, Response
from flask_cors import CORS
from seismic_viewer import get_seismic_data, get_ebcdic_header, get_file_metadata, get_file_path_from_api
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/get_file_path_from_api', methods=['GET'])
def serve_file_path_from_api():
    start_time = time.time()
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    result = get_file_path_from_api(geofile_id, jwt_token)
    
    if 'error' in result:
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/get_seismic_data', methods=['GET'])
def serve_seismic_data():
    start_time = time.time()
    start_trace = int(request.args.get('start_trace', 0))
    end_trace = request.args.get('end_trace', None)
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)

    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400

    if end_trace is not None:
        end_trace = int(end_trace)
    
    result = get_seismic_data(geofile_id=geofile_id, start_trace=start_trace, end_trace=end_trace, jwt_token=jwt_token)
    
    if 'error' in result:
        return jsonify(result), 500
    
    # Extract binary data and metadata
    binary_data = result['data']
    metadata = {k: v for k, v in result.items() if k != 'data'}
    
    # Create response with binary data and JSON metadata in headers
    response = Response(binary_data, mimetype='application/octet-stream')
    response.headers['X-Metadata'] = json.dumps(metadata)
    response.headers['Access-Control-Expose-Headers'] = 'X-Metadata'
    
    return response

@app.route('/get_ebcdic_header', methods=['GET'])
def serve_ebcdic_header():
    start_time = time.time()
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    result = get_ebcdic_header(geofile_id=geofile_id, jwt_token=jwt_token)
    
    if result['error']:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/get_file_metadata', methods=['GET'])
def serve_file_metadata():
    start_time = time.time()
    geofile_id = request.args.get('geofile_id', None)
    jwt_token = request.args.get('jwt_token', None)
    
    if not geofile_id:
        return jsonify({'error': 'geofile_id parameter is required'}), 400
    
    result = get_file_metadata(geofile_id=geofile_id, jwt_token=jwt_token)
    
    if result['error']:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/metrics')
def get_metrics():
    """Performance metrics endpoint"""
    import psutil
    import os
    
    # Get system metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get process metrics
    process = psutil.Process(os.getpid())
    process_memory = process.memory_info()
    
    metrics = {
        'system': {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_free_gb': round(disk.free / (1024**3), 2)
        },
        'process': {
            'memory_mb': round(process_memory.rss / (1024**2), 2),
            'cpu_percent': process.cpu_percent(),
            'threads': process.num_threads()
        },
        'application': {
            'status': 'running',
            'uptime_seconds': time.time() - process.create_time()
        }
    }
    
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)