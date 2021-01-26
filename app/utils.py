from guess_language import guess_language
from flask import flash, redirect, url_for
from flask_login import current_user
from flask_babel import _
from app import db
from app.models import Post

def create_post(body):
    language = guess_language(body)
    if language == 'UNKNOWN' or len(language) > 5:
        language = ''
    post = Post(body=body, author=current_user,
                language=language)
    db.session.add(post)
    db.session.commit()
    flash(_('Your post is now live!'), 'success')
