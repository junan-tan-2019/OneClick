import os
import json
import requests
from flask import Flask, request, jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
if os.environ.get('db_conn'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'db_conn') + '/collection'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = None

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}
db = SQLAlchemy(app)
CORS(app)

service0_url_update = os.environ.get('service_0_url') + '/update'
service2_url = os.environ.get('lambda_url')


class Collection(db.Model):
    __tablename__ = 'item_collection'

    unique_ref = db.Column(db.String(255), primary_key=True, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)

    def __init__(self, unique_ref, location, phone_number) -> None:
        self.unique_ref = unique_ref
        self.location = location
        self.phone_number = phone_number

    def to_dict(self):
        return {
            "unique_ref": self.unique_ref,
            "location": self.location,
            "phone_number": self.phone_number
        }


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/vending_machine/collection", methods=["GET", "POST"])
def main_menu():
    if request.method == "POST":
        unique_ref = request.form.get("unique_ref")
        data = Collection.query.filter_by(unique_ref=unique_ref).first()

        if not data:
            return render_template("failure.html")

        collection_data = data.to_dict()
        payload = {'location': collection_data['location']}
        headers = {'content-type': 'application/json'}
        # notify service 0 that item has been collected by user
        response = requests.patch(service0_url_update, data=json.dumps(
            payload), headers=headers)

        print(response)

        # sms message to remind user that item is collected
        payload_sms = {"collected": True,
                       "phone_number": collection_data['phone_number']}
        headers_sms = {'content-type': 'application/json',
                       'x-api-key': os.environ.get('api_key')}
        response_sms = requests.post(service2_url, data=json.dumps(
            payload_sms), headers=headers_sms)

        print(response_sms)
        # delete the collection data once the person has collected his/her item
        try:
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500
        # return a success html page to indicate the transaction is succesful.
        return render_template("success.html")

    return render_template("collection_point.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
