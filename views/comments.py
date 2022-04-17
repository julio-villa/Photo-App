from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post
from my_decorators import id_exists_or_not_comments, comment_valid_id_format, check_ownership_of_comment, \
handle_db_insert_error_comments, is_valid_int_comments, secure_comment
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    @is_valid_int_comments
    @secure_comment
    @handle_db_insert_error_comments
    def post(self):
        body = request.get_json()
        text = body.get('text')
        post_id = body.get('post_id')
        if bool(text) == False:
            response_obj = {
                'message': 'No text!'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        else:
            comment = Comment(text, self.current_user.id, post_id)
            db.session.add(comment)
            db.session.commit()
            return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    @comment_valid_id_format
    @id_exists_or_not_comments
    @check_ownership_of_comment
    def delete(self, id):
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Comment {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
