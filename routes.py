from . import bp as api
from flask import jsonify, request
from app.models import Post

@api.route('/')
def index():
    return 'Hello World'

#Create new user.
@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['email', 'user', 'password']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    # Add new post to database with request body info
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201


#Get an existing user.
@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=['POST'])
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # Add new post to database with request body info
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201


@api.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    post_to_edit.update(**request.json)
    return jsonify(post_to_edit.to_dict())

@api.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    post_to_delete.delete()
    return jsonify({'message': 'You have successfully deleted the post'})
