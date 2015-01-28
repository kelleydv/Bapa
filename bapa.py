import hashlib, datetime, os
from flask import Flask, g, request, session, render_template, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = os.environ['bapa_session_secret']


def init_db(db='bapa'):
    g.db = MongoClient()[db] #lazily

def get_db():
    if not hasattr(g, 'db'):
        init_db()
    return g.db

def sha1(m):
    return hashlib.sha1(m.encode('utf-8')).hexdigest()

def timestamp():
    return str(datetime.datetime.utcnow())



@app.before_request
def before_request():
    # stay logged in with a cookie
    g.user = None
    if 'user_id' in session:
        g.user = get_db().users.find_one( {'_id':ObjectId(session['user_id'])} )
        # record time of last activity on website
        if g.user:
            get_db().users.update(
                {'_id':g.user['_id']}, {
                    "$set":{'last_activity':timestamp()}
                }
            )
        else:
            # user_id invalid
            session.pop('user_id', None)


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if g.user:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        password = request.form['password']
        print('here')
        user = get_db().users.find_one({"ushpa":request.form['ushpa']})
        print('there')
        if user is None:
            error = 'Invalid username'
        elif not sha1(password) == user['password']:
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = str(user['_id']) # keep user logged in between requests
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register the user."""
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
        elif get_db().users.find_one({"ushpa": request.form['ushpa']}):
            error = 'This USHPA pilot number is already in use by a current BAPA member'
        else:
            # Insert user into database.  
            userRecord = {
                'ushpa': request.form['ushpa'], # pilot number
                'email': request.form['email'],
                'password': sha1(request.form['password']),
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],
                'last_activity': timestamp(),
                'active': False,    # Is the user's membership active?
                'current': False,   # Has user paid membership dues?
                'officer': False,   # Is the user a BAPA officer?
                'admin': False,     # Does the user have admin priveleges?
            }
            get_db().users.insert(userRecord)
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))




@app.route('/account', methods=['GET', 'POST'])
def account():
    """View BAPA membership account."""
    if not g.user:
        return redirect(url_for('login'))
    error = None
    if request.method == 'GET':
        g.account = get_db().accounts.find_one({'user_id': g.user['_id']}) #todo: sort for most recent
        if not g.account:
            return redirect(url_for('pay'))
    return render_template('account.html', error=error)


@app.route('/pay_dues', methods=['GET', 'POST'])
def pay():
    """Pay club dues"""
    if not g.user:
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        if not request.form['ushpa'] == g.user['ushpa']:
            error = "You are currently logged in with pilot number %s" % g.user['ushpa']
        elif not request.form['ushpa']:
            error = "You must enter a valid USHPA number."
        elif not sha1(request.form['password']) == g.user['password']:
            error = "Invalid password."

        request.form['amount']

        accountRecord = {
            'user_id': g.user['_id'],
            'date': timestamp(),
            'amount': request.form['amount']
        }
        get_db().accounts.insert(accountRecord)
        return redirect(url_for('account'))
    return render_template('pay.html')




if __name__ == "__main__":
    app.debug = True
    app.run()

