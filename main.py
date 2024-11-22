from flask import Flask, request
from flask_restful import Api, Resource
from routerconfig import RouterConfig

app = Flask(__name__)
api = Api(app)


class Modifyspeed(Resource):
    def post(self):
        data = request.get_json()
        auth = request.authorization
        return RouterConfig.config_router(data, auth)


# Modify Routes
api.add_resource(Modifyspeed, '/api/RouterConfig/modifyspeed/')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=7005)
