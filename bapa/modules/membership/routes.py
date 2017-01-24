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
    if user_id:
        profile_user_data, profile = controllers.get_user_profile(int(user_id))
    else:
        #User is viewing their own profile
        profile_user_data, profile = controllers.get_user_profile(session['user']['id'])

    if not (profile_user_data and profile):
        return redirect(url_for('membership.profile'))

    return render_template('profile.html', user=session['user'], profile=profile, profile_user_data=profile_user_data)

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

@bp.route('/status', methods=['GET'])
@require_auth
def status():
    """View BAPA membership status"""
    if request.method == 'GET':
        payment = controllers.get_last_payment(session['user']['id'])
    return render_template('status.html', payment=payment, session=session)


@bp.route('/pay', methods=['GET', 'POST'])
@require_auth
def pay():
    """Pay club dues"""
    error = None
    return render_template('pay.html', paypal=app.config['PAYPAL'], error=error, session=session)

@bp.route('/ipnlistener', methods=['POST'])
def listener():
    """IPN listener for paypal payments"""
    ipn = request.form
    error = controllers.record_payment(ipn)
    return ''
