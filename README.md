# flask-thridy
flask的一个插件。 功能只有三个，微信，QQ，微博的第三方登录

Installation
-----
```
pip install flask-thridy
```
Requires
-----

```
* requests
* Flask
```
### QQ开放平台使用示例：
``` python
from flask_thridy import Thridy
from flask import Flask,request,jsonify

app = Flask(__name__)
app.config['THRIDY_AUTH_TYPE'] = 'QQ'
app.config['THRIDY_AUTH_QQ_ID'] = 'your qq_id'
app.config['THRIDY_AUTH_QQ_KEY'] = 'your qq_key'
app.config['THRIDY_AUTH_QQ_REDIRECT'] = 'http://www.example.com/qq_login/authorized'

app.config['SECRET_KEY'] = 'test'

@app.route('/')
def index():
    return thridy.qq_authorize()


@app.route('/qq_login/authorized')
def authorized():
    resp = thridy.qq_authorize_response()
    data = {"access_token":resp['access_token']}
    resp = thridy.qq_get_user_info(data)
    return jsonify(resp)


if __name__ == '__main__':
    thridy = Thridy()
    thridy.init_app(app)
    app.run(port=80,host='0.0.0.0',use_reloader=True,threaded=True)
```

#### 觉得有用，可以点一下star哦（也欢迎转发）

