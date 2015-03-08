from . import controllers
from flask import session, render_template, redirect, url_for, request, flash
from flask import Blueprint

memb_bp = Blueprint('membership', __name__, template_folder='templates')


@memb_bp.route('/status', methods=['GET'])
def status():
    """View BAPA membership status"""
    if not session.get('user_id'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        payment = controllers.get_last_payment(session['user_id'])
        if not payment:
            return redirect(url_for('membership.pay'))
    return render_template('status.html', payment=payment)


@memb_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    """Pay club dues"""
    if not session.get('user_id'):
        return redirect(url_for('home.login'))
    error = None
    if request.method == 'POST':

        error = controllers.make_payment(
            session['user_ushpa'],
            request.form['password'],
            request.form['amount']
        )
        if not error:
            return redirect(url_for('membership.status'))
    return render_template('pay.html', error=error, session=session)
