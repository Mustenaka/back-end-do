import sys
import os

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

print(projectPath)

from flask import Flask
from flask import session
from control.Msession import MySessionInterface

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.session_interface = MySessionInterface()


@app.route('/login.html', methods=['GET', "POST"])
def login():
    print(session)
    session['user1'] = 'alex'
    session['user2'] = 'alex'
    del session['user2']

    return "内容"


if __name__ == '__main__':
    app.run()