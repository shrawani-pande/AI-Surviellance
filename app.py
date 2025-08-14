from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', image_url='/static/currentDetection.jpg')

@app.route('/init', methods=['POST'])
def InitLockdown():
    
    try:
        r = requests.get('http://192.168.139.88:8080/InitLockdown')
        print(r.status_code)
    except:
        print("Error Starting Lockdown")    

    return "Lockdown is Triggered Successfully!!"

@app.route('/stop', methods=['POST'])
def StopLockdown():
    
    try:
        r = requests.get('http://192.168.139.88:8080/StopLockdown')
    except:
        print("Error Stopping Lockdown")    

    return "Lockdown is Stopped Successfully"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
