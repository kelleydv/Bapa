from . import controllers
from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask import Blueprint

bp = Blueprint('membership', __name__, template_folder='templates')


@bp.route('/profile')
@bp.route('/profile/<user_id>')
def profile(user_id=None):
    """View a user profile"""
    if not session.get('user'):
        return redirect(url_for('home.login'))

    if user_id:
        profile_user_data, profile = controllers.get_user_profile(int(user_id))
    else:
        #User is viewing their own profile
        profile_user_data, profile = controllers.get_user_profile(session['user']['id'])

    if not (profile_user_data and profile):
        return redirect(url_for('membership.profile'))

    return render_template('profile.html', user=session['user'], profile=profile, profile_user_data=profile_user_data)

@bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Make changes to profile data"""
    if not session.get('user'):
        return redirect(url_for('home.login'))

    if request.method == 'POST':
        controllers.update_user_profile(session['user']['id'], request.form)
        flash('Your profile has been updated')
        return(redirect(url_for('membership.profile')))

    _, profile = controllers.get_user_profile(session['user']['id'])
    return render_template('edit_profile.html', user=session['user'], profile=profile)

@bp.route('/status', methods=['GET'])
def status():
    """View BAPA membership status"""
    if not session.get('user'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        payment = controllers.get_last_payment(session['user']['id'])
        if not payment:
            return redirect(url_for('membership.pay'))
    return render_template('status.html', payment=payment)


@bp.route('/pay', methods=['GET', 'POST'])
def pay():
    """Pay club dues"""
    if not session.get('user'):
        return redirect(url_for('home.login'))
    error = None
    return render_template('pay.html', error=error, session=session)

@bp.route('/ipnlistener', methods=['POST'])
def listener():
    """IPN listener for paypal payments"""
    ipn = request.form
    controllers.record_payment(ipn)
    return ''
