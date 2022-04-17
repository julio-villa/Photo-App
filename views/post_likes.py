from flask import Response
from flask_restful import Resource
from models import LikePost, db
import json
from . import can_view_post
from my_decorators import valid_id_format, valid_postid_format, post_id_exists, secure_like, like_valid_id_format, \
    like_post_id_exists, check_ownership_of_like
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @valid_postid_format
    @post_id_exists
    @secure_like
    def post(self, post_id):
        id_post = post_id

        list_likes = LikePost.query.filter_by(
            user_id = self.current_user.id, post_id = id_post).order_by('id').all()
        likes_dictionary = [
            like.to_dict() for like in list_likes
        ]

        if len(likes_dictionary) > 0:
            response_obj = {
                'message': 'Error! Duplicate'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        else:
            like = LikePost(self.current_user.id, post_id)
            db.session.add(like)
            db.session.commit()
            return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @like_valid_id_format
    @like_post_id_exists
    @check_ownership_of_like
    def delete(self, post_id, id):
        LikePost.query.filter_by(id=id, post_id = post_id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Like {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps((serialized_data)), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
