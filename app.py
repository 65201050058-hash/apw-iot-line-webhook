from flask import Flask, request

app = Flask(__name__)


# หน้าแรกสำหรับทดสอบ Render
@app.route("/", methods=["GET"])
def home():
    return "APW IoT LINE Webhook OK", 200


# LINE Webhook
@app.route("/callback", methods=["POST"])
def callback():
    try:
        # รับข้อมูลจาก LINE
        data = request.get_json(silent=True)

        print("LINE Webhook received:")
        print(data)

        # ตอบกลับ HTTP 200 ให้ LINE
        return "OK", 200

    except Exception as e:
        print("Error:", e)
        return "OK", 200


# สำหรับรันบน Render
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
