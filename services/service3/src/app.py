import qrcode
from flask import Flask, send_file, jsonify

app = Flask(__name__)


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route('/api/qr/<string:unique_ref>')
def generate_qrcode(unique_ref):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(unique_ref)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.jpg")

    return send_file("qrcode.jpg", mimetype='image/jpg')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
