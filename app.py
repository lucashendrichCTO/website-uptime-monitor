from flask import Flask, render_template, request, jsonify
import requests
import time
from datetime import datetime
import threading
import queue

app = Flask(__name__)

# Store monitoring results
monitoring_results = {}
detailed_results = {}  # Store detailed check results for charts

def check_website(url, duration, frequency, result_queue):
    """Monitor website for specified duration and calculate uptime"""
    start_time = time.time()
    end_time = start_time + (duration * 60)  # Convert minutes to seconds
    successful_checks = 0
    total_checks = 0
    check_results = []  # Store individual check results
    
    while time.time() < end_time:
        check_time = time.time()
        try:
            response = requests.get(url, timeout=0.1)  # 100ms timeout
            is_success = response.status_code == 200
            if is_success:
                successful_checks += 1
            total_checks += 1
        except:
            is_success = False
            total_checks += 1
        
        # Store check result with timestamp
        check_results.append({
            'timestamp': datetime.fromtimestamp(check_time).strftime('%H:%M:%S'),
            'success': is_success
        })
        
        time.sleep(frequency / 1000)  # Convert milliseconds to seconds
    
    uptime_percentage = (successful_checks / total_checks) * 100 if total_checks > 0 else 0
    result = {
        'url': url,
        'uptime': uptime_percentage,
        'total_checks': total_checks,
        'successful_checks': successful_checks,
        'duration': duration,
        'frequency': frequency,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Store the results
    monitoring_results[url] = result
    detailed_results[url] = check_results
    result_queue.put(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor', methods=['POST'])
def monitor():
    url = request.form.get('url')
    duration = request.form.get('duration', type=int)
    frequency = request.form.get('frequency', type=int)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not duration or duration < 1 or duration > 60:
        return jsonify({'error': 'Duration must be between 1 and 60 minutes'}), 400
    
    if not frequency or frequency < 10 or frequency > 10000:
        return jsonify({'error': 'Frequency must be between 10 and 10000 milliseconds'}), 400
    
    # Add http:// if not present
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Create a queue for the monitoring result
    result_queue = queue.Queue()
    
    # Start monitoring in a separate thread
    thread = threading.Thread(target=check_website, args=(url, duration, frequency, result_queue))
    thread.start()
    
    return jsonify({'message': 'Monitoring started', 'url': url, 'duration': duration, 'frequency': frequency})

@app.route('/results')
def get_results():
    url = request.args.get('url')
    if url:
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return jsonify(monitoring_results.get(url, {}))
    return jsonify(monitoring_results)

@app.route('/detailed_results')
def get_detailed_results():
    url = request.args.get('url')
    if url:
        # Add http:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return jsonify(detailed_results.get(url, []))
    return jsonify(detailed_results)

if __name__ == '__main__':
    app.run(debug=True) 