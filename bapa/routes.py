from bapa import app, controllers
from flask import g, session, request
from flask import redirect, render_template, url_for, flash

@app.before_request
def before_request():
    # stay logged in with a cookie
    user_id = session.get('user_id')
    if not controllers.record_user_activity(user_id):
        logout(None)


@app.route("/")
def home():
    return render_template('home/home.html', session=session)



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register the user."""
    if session.get('user_id'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        error = controllers.signup(
            request.form['ushpa'],
            request.form['email'],
            request.form['password'],
            request.form['password2'],
            request.form['firstname'],
            request.form['lastname']
        )
        if not error:    
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('auth/register.html', error=error)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if session.get('user_id'):
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        user = controllers.authenticate_user(request.form['ushpa'], request.form['password'])
        if user:
            flash('Welcome back, %s' % user['firstname'])
            session['user_id'] = str(user['_id'])
            session['user_ushpa'] = user['ushpa']
            session['firstname'] = user['firstname']
            session['lastname'] = user['lastname']
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
    return render_template('auth/login.html', error=error, session=session)



@app.route('/logout')
def logout(msg='You were logged out'):
    """Logs the user out."""
    flash(msg)
    session.pop('user_id', None)
    return redirect(url_for('home'))




@app.route('/account', methods=['GET'])
def account():
    """View BAPA membership account."""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        account = controllers.get_last_payment(session['user_id'])
        if not account:
            return redirect(url_for('pay'))
    return render_template('account/account.html', account=account)


@app.route('/pay_dues', methods=['GET', 'POST'])
def pay():
    """Pay club dues"""
    if not session.get('user_id'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':

        error = controllers.make_payment(
            session['user_ushpa'],
            request.form['password'],
            request.form['amount']
        )
        if not error:
            return redirect(url_for('account'))
    return render_template('account/pay.html', error=error, session=session)
