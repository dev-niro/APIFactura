from flask import Flask,jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

orders = []

class BE(Resource):
    def post(self):
        body = request.get_json()
        response = requests.get("http://localhost:27776/api/cliente/%s" % body['client'])
        cliente = response.json()
        productos = []
        total = 0
        for x in body['products']:
            response = requests.get("http://localhost:27776/api/producto/%s" % x['id'])
            product = response.json()
            product['quantity'] = int(x['quantity'])
            total += (product['price']*int(x['quantity']))
            productos.append(product)
        data = {
            'cliente': cliente,
            'productos': productos,
            'total': total
        }
        return jsonify(data)

api.add_resource(BE, '/api/BE')

# if __name__ == '__main__':
app.run(debug=True)