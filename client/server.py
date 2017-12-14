from flask import Flask, request, make_response, jsonify
import stats, config
import jwt, datetime
from functools import wraps
import requests


app = Flask(__name__)

#this decorator checks for the valid auth token
def protected(f):
    wraps(f)
    def decorated(*args, **kwargs):
        print(request.args)
        token = request.args.get("token")
        source = request.args.get("source")
        if source == "internal":
            return f(*args, **kwargs)
        print("token is {}".format(token))
        if not token and token ==" ":
            return jsonify({"message":"Token is missing"}) , 403
        try:
            data = jwt.decode(token,config.SECRET_KEY)
        except Exception as e:
            print(e)
            return jsonify({"message":"token is Invalid..!!!"}),403
        return f(*args, **kwargs)
    return decorated





@app.route('/run/')
@protected
def run_command():
    cmd = request.args.get("cmd")
    if cmd:
        return stats.run_command(cmd)
    else:
        return "No command given"

@protected
@app.route('/stats/')
def get_stats():
    return str(stats.get_system_status())

@protected
@app.route('/processlist/')
def show_process_list():
    count = request.args.get("count")
    sort = request.args.get("sort")
    return stats.get_process_list(sort_by = sort, count = count)



@app.route("/logout/")
def logout():
    #request.authorization = None
    #jwt.InvalidIssuer
    #blacklist the token todo
    return jsonify({"message":"logout Succesfull"})


@app.route("/login/")
def login():
    auth = request.authorization
    if auth and auth.password == "HelloDude":
        token = jwt.encode(
            {
            'user' : auth.username,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},
             config.SECRET_KEY
             )
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})




if __name__ == '__main__':
   app.run(debug = True)
