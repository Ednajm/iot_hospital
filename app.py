from flask import Flask, render_template, jsonify

# dashboard_server.py


app = Flask(__name__)

@app.route('/')
def index():
    return "IOT Hospital Dashboard Server is running."

@app.route('/api/status')
def status():
    # Example status endpoint
    return jsonify({"status": "ok", "message": "Server is operational"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    