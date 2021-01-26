from flask import jsonify, request, url_for, abort, flash, redirect
from flask_babel import _
from app import db
from app.api import bp
from app.models import Post
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())

@bp.route('/posts', methods=['GET'])
@token_auth.login_required
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    data = request.get_json() or {}
    data['user_id'] = token_auth.current_user().id
    if 'body' not in data:
        return bad_request('Must include body field')
    
    post = Post()
    post.from_dict(data, new_post=True)
    db.session.add(post)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response

@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    post = Post.query.get_or_404(id)

    if token_auth.current_user().id != post.user_id:
        abort(403)

    data = request.get_json() or {}
    if 'body' not in data:
        return bad_request('Must include body field')

    post.from_dict(data, new_post=False)
    db.session.commit()
    return jsonify(post.to_dict())
