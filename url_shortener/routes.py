from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db
from .models import Link

from .auth import require_auth

shortener = Blueprint('shortener', __name__)

@shortener.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.views = link.views + 1
    db.session.commit()
    return redirect(link.original_url)

@shortener.route('/create_link', methods=['POST'])
def create_link():
    original_url = request.form['original_url']
    parts = original_url.split('?', 1)
    if len(parts) > 1:
        parsed_url = '?'.join([parts[0], '&'.join(sorted(parts[1].split('&')))])
    else:
        parsed_url = original_url

    res = db.session.query(Link).filter_by(original_url=parsed_url).all()
    if len(res) != 0:
        link = res[0]
    else:
        link = Link(original_url=parsed_url)
        db.session.add(link)
        db.session.commit()

    return render_template('link_success.html', new_url=link.short_url, original_url=original_url)

@shortener.route('/')
def index():
    return render_template('index.html')

@shortener.route('/analytics')
@require_auth
def analytics():
    links = Link.query.all()

    return render_template('analytics.html', links=links)

@shortener.errorhandler(404)
def page_not_found(e):
    return '<h1>Page Not Found 404</h1>', 404

@shortener.route("/clear")
def clear():
    Link.query.delete()
    db.session.commit()
    return redirect("/analytics")