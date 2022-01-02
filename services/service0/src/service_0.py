from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
if os.environ.get('db_conn'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'db_conn') + '/stocks'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = None

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)


class Stocks(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    stock = db.Column(db.Integer)

    def __init__(self, location, stock, longitude, latitude):
        self.location = location
        self.longitude = longitude
        self.latitude = latitude
        self.stock = stock

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "stock": self.stock
        }


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/stocks")
def get_all():
    stocks_list = Stocks.query.all()
    stklist = {
        "data": {
            "stocks": [stock.to_dict() for stock in stocks_list]
        }
    }
    # if len(stocks_list) != 0:
    return render_template("map.html", stocks_list=stocks_list,
                           stklist=stklist, service1_link=os.environ.get
                           ('service_1_url'))


@app.route("/stocks/update", methods=['PATCH'])
def update_stock():
    data = request.get_json()
    if 'location' in data.keys():
        selected_stock = Stocks.query.filter_by(
            location=data['location']).first()
        print(selected_stock)
        if selected_stock is None:
            return jsonify(
                {
                    "data": {
                        "stock": selected_stock
                    },
                    "message": "Location not found."
                }
            ), 404
        else:
            if selected_stock.stock - 1 >= 0:
                selected_stock.stock = selected_stock.stock - 1
                try:
                    db.session.commit()
                except Exception as e:
                    return jsonify(
                        {
                            "message": "An error occured updating the stocks.",
                            "error": str(e)
                        }
                    ), 500
                return jsonify(
                    {
                        "data": selected_stock.to_dict()
                    }
                ), 200
            else:
                return jsonify(
                    {
                        "message": "There are insufficient stocks " +
                        "in the chosen location.",
                        "error": "Not enough stocks in location."
                    }
                ), 500
    else:
        return jsonify(
            {
                "message": "An error occurred updating the stocks.",
                "error": "The location key is not in the request"
            }
        ), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
