from flask import Flask, request
import hmac
import hashlib
import base64
import os
import json

app = Flask(__name__)

# ดึง Channel Secret จาก Environment Variable
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")


# ==============================
# หน้าแรก
# ==============================
@app.route("/", methods=["GET"])
def home():
    return "APW IoT LINE Webhook OK", 200


# ==============================
# LINE WEBHOOK
# ==============================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_data(as_text=True)

    # รับลายเซ็นจาก LINE
    signature = request.headers.get("X-Line-Signature", "")

    # ตรวจสอบ Channel Secret
    if not CHANNEL_SECRET:
        print("ERROR: CHANNEL_SECRET ยังไม่ได้ตั้งค่า")
        return "Server configuration error", 500

    hash_value = hmac.new(
        CHANNEL_SECRET.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256
    ).digest()

    expected_signature = base64.b64encode(hash_value).decode("utf-8")

    # ตรวจสอบว่าเป็นข้อความจาก LINE จริงหรือไม่
    if not hmac.compare_digest(signature, expected_signature):
        print("Invalid signature")
        return "Invalid signature", 400

    # แปลงข้อมูล JSON
    try:
        data = json.loads(body)
    except Exception:
        return "Invalid JSON", 400

    print("==============================")
    print("LINE WEBHOOK")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("==============================")


    # ==============================
    # อ่าน Event
    # ==============================
    for event in data.get("events", []):

        event_type = event.get("type")

        print("Event Type:", event_type)


        # ==============================
        # เมื่อมีข้อความเข้ามา
        # ==============================
        if event_type == "message":

            source = event.get("source", {})

            # User ID
            user_id = source.get("userId")

            print("USER ID =", user_id)


            # ==============================
            # ถ้าเป็นข้อความตัวหนังสือ
            # ==============================
            message = event.get("message", {})

            if message.get("type") == "text":

                text = message.get("text", "")

                print("ข้อความจาก LINE =", text)


                # ==============================
                # คำสั่งทดสอบ
                # ==============================

                if text == "ทดสอบ":
                    print("ได้รับคำสั่งทดสอบแล้ว")

                elif text == "สถานะ":
                    print("ได้รับคำสั่งขอสถานะ")

                elif text == "เริ่ม":
                    print("ได้รับคำสั่งเริ่ม")

                elif text == "หยุด":
                    print("ได้รับคำสั่งหยุด")


    # ต้องตอบ LINE เป็น HTTP 200
    return "OK", 200


# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
