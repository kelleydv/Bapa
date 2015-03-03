from . import controllers
from flask import session, render_template, redirect, url_for, request, flash
from flask import Blueprint

acct_bp = Blueprint('account', __name__, template_folder='templates')


@acct_bp.route('/view', methods=['GET'])
def view():
    """View BAPA membership account."""
    if not session.get('user_id'):
        return redirect(url_for('home.login'))
    if request.method == 'GET':
        account = controllers.get_last_payment(session['user_id'])
        if not account:
            return redirect(url_for('account.pay'))
    return render_template('account.html', account=account)


@acct_bp.route('/pay', methods=['GET', 'POST'])
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
            return redirect(url_for('account.view'))
    return render_template('pay.html', error=error, session=session)
