# 2D Seismic Viewer - Flask Version

A web-based 2D seismic data viewer built with Flask that allows you to visualize SEG-Y seismic data files through an interactive web interface.

## Features

- **Interactive 2D Seismic Visualization**: View seismic data using Plotly.js
- **SEG-Y File Support**: Read and process SEG-Y format seismic files
- **EBCDIC Header Display**: View file header information
- **File Metadata**: Display trace ranges, sample rates, and other metadata
- **Trace Loading**: Load seismic traces in chunks for better performance
- **Web-based Interface**: Access through any modern web browser

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### 1. Clone or Download the Project

Make sure you have the project files in your local directory.

### 2. Install Required Dependencies

Install all required Python packages using the requirements.txt file:

```bash
pip3 install -r requirements.txt
```

Or install packages individually:

```bash
pip3 install flask==3.0.0
pip3 install flask-cors==4.0.0
pip3 install segyio==1.9.13
pip3 install numpy==1.24.3
```

## Configuration

### Seismic File Path

The application is configured to read from a specific SEG-Y file. To change the file path, edit the `SEISMIC_FILE_PATH` variable in `main.py`:

```python
SEISMIC_FILE_PATH = '../data/MYS1993P20152DM01PMOREGION/MYS1993P20152DM01PMOREGION_RC93-002_UNFILT_SCAL_MIGR_flatten.sgy'
```

### Port Configuration

The default port is 5010. To change it, modify the last line in `main.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5010)
```

## Running the Application

### 1. Start the Flask Server

```bash
python3 main.py
```

### 2. Access the Application

Open your web browser and navigate to:

```
http://localhost:5010
```

**Important**: Do not open the `index.html` file directly from your file system. Always access the application through the Flask web server.

## API Endpoints

The application provides the following REST API endpoints:

- **`GET /`** - Serves the main HTML interface
- **`GET /get_seismic_data?start_trace=X&end_trace=Y`** - Returns seismic data for specified trace range
- **`GET /get_ebcdic_header`** - Returns the EBCDIC header information
- **`GET /get_file_metadata`** - Returns file metadata (FFID ranges, SP ranges, etc.)

## Usage

1. **Load Initial Data**: The application automatically loads the first 1000 traces when you open it
2. **Load More Traces**: Click the "Load More Traces" button to load additional traces
3. **View Headers**: The EBCDIC header is displayed below the seismic plot
4. **View Metadata**: File metadata is shown in a card below the header

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'flask'"**
   - Solution: Install the required packages using `pip3 install -r requirements.txt`

2. **"Failed to fetch" errors in browser**
   - Solution: Make sure you're accessing `http://localhost:5010` and not opening the HTML file directly

3. **CORS errors**
   - Solution: The application includes CORS support. Make sure you're accessing through the web server

4. **File not found errors**
   - Solution: Check that the `SEISMIC_FILE_PATH` in `main.py` points to a valid SEG-Y file

### Port Already in Use

If port 5010 is already in use, change the port in `main.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # or any other available port
```

## File Structure

```
flask/
├── main.py              # Flask application server
├── seismic_viewer.py    # SEG-Y data processing functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── static/
    └── index.html      # Web interface
```

## Dependencies

- **Flask**: Web framework for the API server
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **segyio**: SEG-Y file reading and processing
- **numpy**: Numerical operations on seismic data

## Development

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development
python3 main.py
```

The application will automatically reload when you make changes to the Python files.

## License

This project is for educational and research purposes. 