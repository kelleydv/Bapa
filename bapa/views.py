import bapa.models as models
from bapa.utils import timestamp, get_hash
from flask import g, session, request
from flask import redirect, render_template, url_for, flash
from flask.views import View

def bef_req():
    # stay logged in with a cookie
    g.user = None
    if 'user_id' in session:
        g.user = models.User().from_id( session['user_id'] )
        # record time of last activity on website
        if g.user:
            models.User().update(
                session['user_id'],
                "last_activity",
                timestamp()
            )
        else:
            # user_id invalid
            session.pop('user_id', None)


class Home(View):
    """Render Home Page"""

    methods = ['GET']

    def dispatch_request(self):
        return render_template('home/home.html')


class Register(View):
    """Register the user"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        if g.user:
            return redirect(url_for('login'))
        error = None
        if request.method == 'POST':
            if not request.form['ushpa'] or len(request.form['ushpa']) != 5:
                error = 'You have to enter a valid ushpa number'
            elif not request.form['email'] or '@' not in request.form['email']:
                error = 'You have to enter a valid email address'
            elif not request.form['password']:
                error = 'You have to enter a password'
            elif request.form['password'] != request.form['password2']:
                error = 'The two passwords do not match'
            elif models.User().match('ushpa',request.form['ushpa']):
                error = 'This USHPA pilot number is already in use by a current BAPA member'
            else:
                # Insert user into database.
                # See models.User for full schema
                models.User().create(
                    request.form['ushpa'], # pilot number
                    request.form['email'],
                    request.form['password'],
                    request.form['firstname'],
                    request.form['lastname']
                )
                flash('You were successfully registered and can login now')
                return redirect(url_for('login'))
        return render_template('auth/register.html', error=error)


class Login(View):
    """User login"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        if g.user:
            return redirect(url_for('home'))
        error = None
        if request.method == 'POST':

            user = models.User().auth(request.form['ushpa'], request.form['password'])

            if user is None:
                error = 'Invalid username or password'
            else:
                flash('You were logged in')
                session['user_id'] = str(user['_id'])
                session['user_ushpa'] = user['ushpa']
                session['firstname'] = user['firstname']
                session['lastname'] = user['lastname']
                return redirect(url_for('home'))
        return render_template('auth/login.html', error=error)

class Logout(View):
    """Log user out"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        flash('You were logged out')
        session.pop('user_id', None)
        return redirect(url_for('home'))



class Account(View):
    """View BAPA membership account"""

    methods = ['GET']

    def dispatch_request(self):
        if not g.user:
            return redirect(url_for('login'))
        error = None
        if request.method == 'GET':
            g.account = models.Account().match('user_id', g.user['_id']) #todo: sort for most recent
            if not g.account:
                return redirect(url_for('pay'))
        return render_template('account/account.html', error=error)


class Pay(View):
    """Pay club dues"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        if not g.user:
            return redirect(url_for('login'))
        error = None
        if request.method == 'POST':
            if not (request.form['ushpa'] == g.user['ushpa']):
                error = "You are currently logged in with pilot number %s" % g.user['ushpa']
            elif not(request.form['ushpa'] and get_hash(request.form['password'], g.user['salt']) == g.user['password']):
                error = "Invalid USHPA number or password."
            else:
                models.Account().create(g.user['_id'], request.form['amount'])
                return redirect(url_for('account'))
        return render_template('account/pay.html', error=error)

