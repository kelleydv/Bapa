from . import controllers
from flask import render_template, redirect, url_for
from flask import session, request
from flask import Blueprint

bp = Blueprint('membership', __name__, template_folder='templates')


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
