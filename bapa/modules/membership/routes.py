from . import controllers
from bapa import app
from bapa.decorators.auth import redirect_authenticated, require_auth
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint

bp = Blueprint('membership', __name__, template_folder='templates')


@bp.route('/profile')
@bp.route('/profile/<user_id>')
@require_auth
def profile(user_id=None):
    """View a user profile"""
    own_profile = False
    if not user_id or user_id == session['user']['id']:
        own_profile = True #user is viewing their own profile
    if request.args.get('public'):
        own_profile = False

    user_id = user_id or session['user']['id']
    profile_user_data, profile = controllers.get_user_profile(int(user_id))

    if not (profile_user_data and profile):
        return redirect(url_for('membership.profile'))

    if profile.private:
        if session['user']['id'] == profile.user_id and request.args.get('public'):
            flash('Your profile is set to private')
            return redirect(url_for('membership.profile'))
        if not session['user']['id'] == profile.user_id and not session['user'].get('officer'):
            return redirect(url_for('membership.profile'))

    return render_template('profile.html', session=session, own_profile=own_profile, profile=profile, profile_user_data=profile_user_data, paypal=app.config['PAYPAL'])

@bp.route('/profile/edit', methods=['GET', 'POST'])
@require_auth
def edit_profile():
    """Make changes to profile data"""
    if request.method == 'POST':
        controllers.update_user_profile(session['user']['id'], request.form)
        flash('Your profile has been updated')
        return(redirect(url_for('membership.profile')))

    _, profile = controllers.get_user_profile(session['user']['id'])
    return render_template('edit_profile.html', user=session['user'], profile=profile)

@bp.route('/profile/picture', methods=['POST'])
@require_auth
def profile_picture():
    """Upload a profile picture"""
    if request.method == 'POST':
        controllers.upload_profile_picture(session['user']['id'], request.files.get('picture'))
        flash('Your profile picture has been updated')
    return(redirect(url_for('membership.profile')))

@bp.route('/ipnlistener', methods=['POST'])
def listener():
    """IPN listener for paypal payments"""
    ipn = request.form
    error = controllers.record_payment(ipn)
    return ''
