import segyio
import numpy as np

def get_seismic_data(file_path, start_trace=0, end_trace=None):
    try:
        with segyio.open(file_path, 'r', ignore_geometry=True) as segyfile:
            n_traces = segyfile.tracecount
            n_samples = len(segyfile.samples)
            sample_rate = segyfile.samples[1] - segyfile.samples[0]
            # Limit end_trace to the total number of traces
            end_trace = min(end_trace, n_traces) if end_trace else n_traces
            # Ensure start_trace and end_trace are valid
            start_trace = max(0, start_trace)
            if start_trace >= n_traces or end_trace <= start_trace:
                return {'error': 'Invalid trace range'}
            # Read only the specified range of traces
            data = np.zeros((n_samples, end_trace - start_trace))
            for i, trace_idx in enumerate(range(start_trace, end_trace)):
                data[:, i] = segyfile.trace[trace_idx]
            return {
                'data': data.tolist(),
                'sample_rate': float(sample_rate),
                'n_traces': end_trace - start_trace,
                'n_samples': n_samples,
                'start_trace': start_trace,
                'total_traces': n_traces
            }
    except Exception as e:
        return {'error': str(e)}
    
def get_ebcdic_header(file_path):
    try:
        with segyio.open(file_path, 'r', ignore_geometry=True) as segyfile:
            header = segyfile.text[0]
            lines = [header[i:i+80].decode('ascii') for i in range(0, len(header), 80)]
            return {
                'header': lines,
                'error': None
            }
    except Exception as e:
        return {
            'header': None,
            'error': str(e)
        }
    
def get_file_metadata(file_path):
    try:
        with segyio.open(file_path, 'r', ignore_geometry=True) as segyfile:
            sample_interval_us = segyfile.bin[segyio.BinField.Interval] # In microseconds
            sample_interval_ms = sample_interval_us / 1000 if sample_interval_us else None

            #Trace headers:
            ffids = []
            sps = []
            cdps = []

            for trace_idx, trace in enumerate(segyfile.trace):
                trace_header = segyfile.header[trace_idx] # Access header for current trace
                ffid = trace_header.get(segyio.TraceField.TRACE_SEQUENCE_FILE, None)
                sp = trace_header.get(segyio.TraceField.FieldRecord, None)
                cdp = trace_header.get(segyio.TraceField.CDP, None)
                if ffid is not None:
                    ffids.append(ffid)
                if sp is not None:
                    sps.append(sp)
                if cdp is not None:
                    cdps.append(cdp)

            ffid_range = f"{min(ffids)} to {max(ffids)}" if ffids else "N/A"
            sp_range = f"{min(sps)} to {max(sps)}" if sps else "N/A"
            cdp_range = f"{min(cdps)} to {max(cdps)}" if cdps else "N/A"
            sample_rate = f"{sample_interval_ms} ms" if sample_interval_ms else "N/A"

            return {
                'ffid_range': ffid_range,
                'sp_range': sp_range,
                'cdp_range': cdp_range,
                'sample_rate': sample_rate,
                'error': None
            }
    except Exception as e:
        return {
            'ffid_range': 'N/A',
            'sp_range': 'N/A',
            'cdp_range': 'N/A',
            'sample_rate': 'N/A',
            'error': str(e)
        }