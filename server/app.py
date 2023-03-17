from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


# @app.route('/')
# def index():
#     response = make_response(
#         {
#             "message": "Hello Campers!"
#         },
#         200
#     )
#     return response

class Index(Resource):
    def get(self):
        response = make_response(
            {"message": "Hello Campers!"},
            200
        )
        return response

api.add_resource(Index, '/')

class Campers(Resource):
    def get(self):
        # import ipdb; ipdb.set_trace()
        response_dict_list = [each.to_dict() for each in Camper.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        try:
            new_camper = Camper(
                name=request.form['name'],
                age=request.form['age']
            )
            db.session.add(new_camper)
            db.session.commit()
        except Exception as e:
            # import ipdb; ipdb.set_trace()
            response = make_response({"error":e.__str__()}, 422)
            return response
        response_dict = new_camper.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Campers, '/campers')

class CampersByID(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if camper:
            camper_dict = camper.to_dict()
            response = make_response(camper_dict, 200)
            return response
        else:
            response = make_response({"message":"Camper not found"}, 404)
            return response
api.add_resource(CampersByID, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        response_dict_list = [each.to_dict() for each in Activity.query.all()]
        response = make_response(response_dict_list, 200)
        return response
api.add_resource(Activities, '/activities')
    
class ActivitiesByID(Resource):
    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if activity:
            db.session.delete(activity)
            db.session.commit()
            response = make_response({"message": "Activity deleted"}, 200)
            return response
        else:
            response = make_response({"message":"Activity not found"}, 404)
            return response
api.add_resource(ActivitiesByID, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        try:
            new_signup = Signup(
                time=request.form['time'],
                camper_id=request.form['camper_id'],
                activity_id=request.form['activity_id']
            )
            db.session.add(new_signup)
            db.session.commit()
        except Exception as e:
            response = make_response({"error":e.__str__()}, 422)
            return response
        response_dict = new_signup.to_dict()
        response = make_response(response_dict, 201)
        return response
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
