from flask import Flask, request

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.json
    print("\n🔔 ALERT RECEIVED:")
    print(data)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
