from flask import Flask, session, redirect, url_for, escape, request
from datetime import timedelta
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 设置session到期时间
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1) 
    if request.method == 'POST':
        #session['username'] = request.form['username']
        session['username'] = request.json.get('user_id')
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()