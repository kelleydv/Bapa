from bapa import app
from bapa.views import bef_req, Home, Register, Login, Logout, Account, Pay

app.before_request(bef_req)

app.add_url_rule('/', view_func=Home.as_view('home'))
app.add_url_rule('/register', view_func=Register.as_view('register'))
app.add_url_rule('/login', view_func=Login.as_view('login'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/account', view_func=Account.as_view('account'))
app.add_url_rule('/pay_dues', view_func=Pay.as_view('pay'))
