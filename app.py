from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello! My DevOps App is running and my name is Sakshi, and i am working as devops engineer and working in TCS!",
        "status": "healthy",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)