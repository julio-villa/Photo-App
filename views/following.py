from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from my_decorators import handle_db_insert_error_following, is_valid_int_following, \
    following_valid_id_format, id_exists_or_not_following, check_ownership_of_following
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        following_list = Following.query.filter_by(
            user_id = self.current_user.id).order_by('id').all()
        following_list_of_dictionaries = [
            following.to_dict_following() for following in following_list
        ]
        return Response(json.dumps(following_list_of_dictionaries), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    @is_valid_int_following
    @handle_db_insert_error_following
    def post(self):
        body = request.get_json()
        follow_id = body.get('user_id')

        following_list = Following.query.filter_by(
            user_id = self.current_user.id, following_id = follow_id).order_by('id').all()
        following_list_dictionary = [
            following.to_dict_following() for following in following_list
        ]

        if len(following_list_dictionary)>0:
            response_obj = {
                'message': 'Error! Duplicate'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)

        else:
            follow = Following(self.current_user.id, follow_id)
            db.session.add(follow)
            db.session.commit()
            return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    @following_valid_id_format
    @id_exists_or_not_following
    @check_ownership_of_following
    def delete(self, id):
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Following id {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
