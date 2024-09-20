from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import sys
import os

app = Flask(__name__)
CORS(app) 
@app.route('/')
def index():
    return send_from_directory('', 'Compiler.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')
    inputs = data.get('inputs', [])

    if not code:
        return jsonify({'output': 'No code provided'}), 400

    filename = 'temp_code.py'
    with open(filename, 'w') as file:
        file.write(code)

    try:
        process = subprocess.Popen(
            [sys.executable, filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(input='\n'.join(inputs), timeout=10)
        output = stdout + stderr
    except subprocess.TimeoutExpired:
        process.kill()
        output = 'Error: Code execution timeout'
    finally:
        os.remove(filename)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
