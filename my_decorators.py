from datetime import datetime
import json
from xml.etree.ElementTree import Comment
from flask import Response, request
from views import can_view_post
from models import Bookmark
from models import Comment
from models import Following
from models import Post
from models import LikePost

def handle_db_insert_error(endpoint_function):
    def outer_function(self, *args, **kwargs):
        print('handle_db_insert_error')
        try:
            # try to execute the query:
            return endpoint_function(self, *args, **kwargs)
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            print(db_message)                   # logs it to the console
            message = 'DECORATOR! Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json()
            # post_data['user_id'] = self.current_user.id
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return outer_function


def is_valid_int(endpoint_function):
    def outer_function_with_security_checks(self):
        try:
            body = request.get_json()
            post_id = body.get('post_id')
            post_id = int(post_id)
        except:
            response_obj = {
                'message': 'Invalid post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self)
    return outer_function_with_security_checks

def secure_bookmark(endpoint_function):
    def outer_function_with_security_checks(self):
        print('secure_bookmark')
        body = request.get_json()
        post_id = body.get('post_id')
        print(post_id)
        print(can_view_post(post_id, self.current_user))
        if can_view_post(post_id, self.current_user):
            return endpoint_function(self)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks


def check_ownership_of_bookmark(endpoint_function):
    def outer_function_with_security_checks(self, id):
        print(id)
        bookmark = Bookmark.query.get(id)
        if bookmark.user_id == self.current_user.id:
            return endpoint_function(self, id)
        else:
            response_obj = {
                'message': 'You did not create bookmark id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks

def valid_id_format(endpoint_function):
    def outer_function_with_security_checks(self, id):
        try:
            bookmark_id = id
            bookmark_id = int(bookmark_id)
        except:
            response_obj = {
                'message': 'Invalid bookmark id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, id)
    return outer_function_with_security_checks

def id_exists_or_not(endpoint_function):
    def outer_function_with_security_checks(self, id):
        bookmark = Bookmark.query.get(id)
        if bool(bookmark) == False:
            response_obj = {
                'message': 'ID does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, id)
    return outer_function_with_security_checks


########################################## COMMENTS ########################################################

def id_exists_or_not_comments(endpoint_function):
    def outer_function_with_security_checks(self, id):
        comment = Comment.query.get(id)
        if bool(comment) == False:
            response_obj = {
                'message': 'Comment ID does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, id)
    return outer_function_with_security_checks

def comment_valid_id_format(endpoint_function):
    def outer_function_with_security_checks(self, id):
        try:
            comment_id = id
            comment_id = int(comment_id)
        except:
            response_obj = {
                'message': 'Invalid comment id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, id)
    return outer_function_with_security_checks

def check_ownership_of_comment(endpoint_function):
    def outer_function_with_security_checks(self, id):
        print(id)
        comment = Comment.query.get(id)
        if comment.user_id == self.current_user.id:
            return endpoint_function(self, id)
        else:
            response_obj = {
                'message': 'You did not create comment id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks

def is_valid_int_comments(endpoint_function):
    def outer_function_with_security_checks(self):
        try:
            body = request.get_json()
            post_id = body.get('post_id')
            post_id = int(post_id)
        except:
            response_obj = {
                'message': 'Invalid post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self)
    return outer_function_with_security_checks

def handle_db_insert_error_comments(endpoint_function):
    def outer_function(self, *args, **kwargs):
        print('handle_db_insert_error')
        try:
            # try to execute the query:
            return endpoint_function(self, *args, **kwargs)
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            print(db_message)                   # logs it to the console
            message = 'DECORATOR! Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json()
            post_data['user_id'] = self.current_user.id
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_function

def secure_comment(endpoint_function):
    def outer_function_with_security_checks(self):
        print('secure_comment')
        body = request.get_json()
        post_id = body.get('post_id')
        print(post_id)
        print(can_view_post(post_id, self.current_user))
        if can_view_post(post_id, self.current_user):
            return endpoint_function(self)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks

######################################### FOLLOWING ####################################################

def handle_db_insert_error_following(endpoint_function):
    def outer_function(self, *args, **kwargs):
        print('handle_db_insert_error')
        try:
            # try to execute the query:
            return endpoint_function(self, *args, **kwargs)
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            print(db_message)                   # logs it to the console
            message = 'DECORATOR! Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json()
            # post_data['user_id'] = self.current_user.id
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_function

def is_valid_int_following(endpoint_function):
    def outer_function_with_security_checks(self):
        try:
            body = request.get_json()
            following_id = body.get('user_id')
            following_id = int(following_id)
        except:
            response_obj = {
                'message': 'Invalid following id={0}'.format(following_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self)
    return outer_function_with_security_checks

def following_valid_id_format(endpoint_function):
    def outer_function_with_security_checks(self, id):
        try:
            following_id = id
            following_id = int(following_id)
        except:
            response_obj = {
                'message': 'Invalid following id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, id)
    return outer_function_with_security_checks

def id_exists_or_not_following(endpoint_function):
    def outer_function_with_security_checks(self, id):
        following = Following.query.get(id)
        if bool(following) == False:
            response_obj = {
                'message': 'Person does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, id)
    return outer_function_with_security_checks

def check_ownership_of_following(endpoint_function):
    def outer_function_with_security_checks(self, id):
        following = Following.query.get(id)
        if following.user_id == self.current_user.id:
            return endpoint_function(self, id)
        else:
            response_obj = {
                'message': 'You did not create this following record'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks

######################################### LIKE POSTS ####################################################

def valid_postid_format(endpoint_function):
    def outer_function_with_security_checks(self, post_id):
        try:
            id_post = post_id
            id_post = int(id_post)
        except:
            response_obj = {
                'message': 'Invalid following id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, post_id)
    return outer_function_with_security_checks

def post_id_exists(endpoint_function):
    def outer_function_with_security_checks(self, post_id):
        post = Post.query.get(post_id)
        if bool(post) == False:
            response_obj = {
                'message': 'Post does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, post_id)
    return outer_function_with_security_checks

def secure_like(endpoint_function):
    def outer_function_with_security_checks(self, post_id):
        if can_view_post(post_id, self.current_user):
            return endpoint_function(self, post_id)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_function_with_security_checks

def like_valid_id_format(endpoint_function):
    def outer_function_with_security_checks(self, post_id, id):
        try:
            id_post = post_id
            id_post = int(id_post)
            like_id = id
            id = int(id)
        except:
            response_obj = {
                'message': 'Invalid post id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, post_id, id)
    return outer_function_with_security_checks

def like_post_id_exists(endpoint_function):
    def outer_function_with_security_checks(self, post_id, id):
        post = Post.query.get(post_id)
        like = LikePost.query.get(id)
        if bool(post) == False or bool(like) == False:
            response_obj = {
                'message': 'Post does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, post_id, id)
    return outer_function_with_security_checks

def check_ownership_of_like(endpoint_function):
    def outer_function_with_security_checks(self, post_id, id):
        like = LikePost.query.get(id)
        if like.user_id == self.current_user.id:
            return endpoint_function(self, post_id, id)
        else:
            response_obj = {
                'message': 'You did not create this like'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
            
    return outer_function_with_security_checks

######################################### POSTS ####################################################

def valid_id_format_post(endpoint_function):
    def outer_function_with_security_checks(self, id):
        try:
            post_id = id
            post_id = int(post_id)
        except:
            response_obj = {
                'message': 'Invalid post id format'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_function(self, id)
    return outer_function_with_security_checks

def id_exists_posts(endpoint_function):
    def outer_function_with_security_checks(self, id):
        post = Post.query.get(id)
        if bool(post) == False:
            response_obj = {
                'message': 'Post does not exist'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        else:
            return endpoint_function(self, id)
    return outer_function_with_security_checks

def secure_post(endpoint_function):
    def outer_function_with_security_checks(self, post_id):
        if can_view_post(post_id, self.current_user):
            return endpoint_function(self, post_id)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_function_with_security_checks