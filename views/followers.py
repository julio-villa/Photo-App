from flask import Response, request
from flask_restful import Resource
from models import Following
import json
from models import User
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        followers = Following.query.filter_by(
            following_id = self.current_user.id).order_by('id').all()
        followers_list_of_dictionaries = [
            follower.to_dict_follower() for follower in followers
        ]

        return Response(json.dumps(followers_list_of_dictionaries), mimetype="application/json", status=200)

#follower_id=self.current_user.id.order_by('id').all()
def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
