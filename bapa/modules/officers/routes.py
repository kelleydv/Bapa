from . import controllers
from bapa.decorators.auth import require_auth, require_officer
from flask import render_template, redirect, url_for, flash, g
from flask import session, request
from flask import Blueprint

from oauth2client import client

import json
import os
import httplib2



bp = Blueprint('officers', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
@require_officer
def index():
    """Display Officer's Dashboard"""
    users = controllers.get_users()
    officers = controllers.get_officers()
    return render_template('dashboard.html', users=users, officers=officers)

@bp.route('/news/post', methods=['POST'])
@require_officer
def post_news():
    """Post to news feed"""
    if request.method == 'POST':
        controllers.news_update(
            request.form['subject'],
            request.form['body'],
            session['user']['id'],
            request.form.get('news_id')
        )
        return redirect(url_for('home.news'))

@bp.route('/news/delete', methods=['POST'])
@require_officer
def delete_news():
    """Delete a news post"""
    if request.method == 'POST':
        controllers.delete_news(request.form['post_id'])
        return redirect(url_for('home.news'))

@bp.route('/googlegroup/update', methods=['POST'])
@require_officer
def update_google_group():
    #http://localhost:5000/officers/googlegroup/update
    """Update google group membership"""
    if not session.get('google_oauth'):
        return redirect(url_for('officers.oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['google_oauth'])
    if credentials.access_token_expired:
        return redirect(url_for('officers.oauth2callback'))
    else:
        #https://developers.google.com/api-client-library/python/start/get_started#build
        #https://developers.google.com/admin-sdk/directory/v1/guides/manage-group-members
        http_auth = credentials.authorize(httplib2.Http())
        controllers.update_google_group(http_auth)
        flash('Google Group Features Not Yet Implemented')
        return redirect(url_for('home.news'))
    return redirect(url_for('home.index'))


@bp.route('/oauth2callback')
def oauth2callback():

    with open('client_secrets.json', 'w') as f:
        f.write(json.dumps(
            {
                "web": {
                    "client_id": os.environ['GOOGLE_CLIENT_ID'],
                    "client_secret": os.environ['GOOGLE_CLIENT_SECRET'],
                    "redirect_uris": [url_for('officers.oauth2callback', _external=True)],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://accounts.google.com/o/oauth2/token"
                }
            }
        ))

    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/admin.directory.group',
        redirect_uri=url_for('officers.oauth2callback', _external=True)
    )
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args['code']
        credentials = flow.step2_exchange(auth_code)
        session['google_oauth'] = credentials.to_json()
        return redirect(url_for('officers.update_google_group'))




@bp.route('/news/edit', methods=['GET'])
@require_officer
def edit_news():
    """Edit a news post"""
    news_id = request.args.get('news_id')
    news_subject, news_body = controllers.get_news(news_id)
    users = controllers.get_users()
    return render_template('dashboard.html',
        users=users, news_subject=news_subject, news_body=news_body, news_id=news_id)

@bp.route('/appoint/', methods=['POST'])
@bp.route('/appoint/<key>', methods=['GET'])
@require_auth
def appoint(key=None):
    """Appoint an officer, or unappoint if get parameter "un" is marked"""

    message = None

    #decide if appointing or unappointing
    appointer_id = int(session['user']['id'])
    user_id = request.form.get('user_id')
    if key and not user_id:
        #self-appointment
        user_id = appointer_id
    user_id = int(user_id)
    if request.form.get('un'):
        message = controllers.unappoint(user_id, appointer_id, key)
    else:
        message = controllers.appoint(user_id, appointer_id, request.form.get('office'), key)

    #in the case of self-appointment
    if user_id == appointer_id and 'added' in message:
        session['user']['officer'] = True
    flash(message)
    return redirect(url_for('membership.profile', user_id=user_id))

@bp.route('/permissions/normalize', methods=['GET'])
@require_officer
def view_as_normal():
    """
    Remove officer permissions, temporarily. Useful for exploring the interface
    as a normal user.
    """
    session['user']['officer'] = False
    flash('You are no longer viewing as an officer.')
    return redirect(url_for('home.index'))

@bp.route('/permissions/restore', methods=['GET'])
def restore_permission():
    """
    Restore officer permissions
    """
    if session['user'].get('officer') is not None:
        session['user']['officer'] = True
        flash('You are again viewing as an officer.')
    return redirect(url_for('home.index'))
