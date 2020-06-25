from flask import *
#from mongo import user_exist, username_taken, get_data, put_confirmation_token, get_confirmation_token, user_create,\
#    get_session, init_session, modify_session, delete_session, get_items
#from mailer import send_join_mail
from pprint import pprint
from time import sleep
import secrets


app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    :param
    active: ["dashboard", "dynamics", "sales", "analysis", "mp_purchases", "losses", "map", "traffic", "competitiors", "facilities", "settings"]
    :return:
    """
    if "uid" not in session:
        session["uid"] = secrets.token_urlsafe()
        return redirect("/login")
    '''mongosession = get_session(session["uid"])
    if mongosession is None or len(mongosession["order"]) == 0:
        return redirect("/login")
    #pprint(session)
    cur_pos, active = request.args.get("u", "-no-such-"), request.args.get("page", "-no-such-")
    if cur_pos == "-no-such-" and "cur_pos" not in mongosession:
        mongosession["cur_pos"] = 1
    if active == "-no-such-" and "active" not in mongosession:
        mongosession["active"] = "dashboard"
    if cur_pos != "-no-such-" and str(cur_pos).isdigit() and int(cur_pos) <= len(mongosession["order"]):
        mongosession["cur_pos"] = int(cur_pos)
    if active != "-no-such-" and active in {"dashboard", "dynamics", "sales", "analysis", "mp_purchases", "losses",
                                            "map", "traffic", "competitiors", "facilities", "settings"}:
        mongosession["active"] = active
    data = None
    if mongosession["active"] == "dashboard":
        tab = request.args.get("tab", "-no-such-")
        if tab == "-no-such-" and "tab" not in mongosession:
            mongosession["tab"] = "visible"
        if tab != "-no-such-" and tab in {"visible", "invisible", "ready_to_supply", "state_failed", "all",
                                          "awaiting_packaging", "awaiting_deliver", "arbitration",
                                          "delivering", "delivered", "cancelled_user", "cancelled_deliver"}:
            mongosession["tab"] = tab
        print(mongosession["tab"])
        if mongosession["tab"] == "visible":
            print(1)
            user = mongosession["users"][mongosession["order"][mongosession["cur_pos"] - 1]]
            data = get_items(user["ozon_apikey"], user["client_id"], tab)["data"]
            pprint(data)
    print(mongosession)
    modify_session(session["uid"], mongosession)
    pprint(mongosession)'''
    return render_template("accounts-12.html", data=[], accounts=["ivanpush27@gmail.com", "hbr.tip@gmail.com"], cur_pos=1, active="dashboard", tab="visible")


@app.route('/confirm', methods=['GET', 'POST'])
def confirm_join():
    token = request.args.get("token", "")
    if token:
        response, message = get_confirmation_token(token)
        print(response, message)
        if response:
            username, password = message
            response, data = user_create(username, password)
            if response:
                if "uid" not in session:
                    session["uid"] = secrets.token_urlsafe()
                mongosession = get_session(session["uid"])
                if mongosession is None:
                    init_session(session["uid"])
                    mongosession = get_session(session["uid"])
                mongosession["users"][username] = data
                mongosession["order"] = mongosession.get("order", []) + [username]
                modify_session(session["uid"], mongosession)
                return redirect("/")
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    delete_session(session.get("uid", "-"))
    session.pop("uid", None)
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("got it")
        username, password = request.form.get("username", ""), request.form.get("password", "")
        '''
        print(username, password)
        if username and password:
            print("there")
            response = user_exist(username, password)
            if response[0]:
                data = response[1]
                if "uid" not in session:
                    session["uid"] = secrets.token_urlsafe()
                mongosession = get_session(session["uid"])
                if mongosession is None:
                    init_session(session["uid"])
                    mongosession = get_session(session["uid"])
                mongosession["users"][username] = data
                mongosession["order"] = mongosession.get("order", []) + [username]
                modify_session(session["uid"], mongosession)
                return redirect("/")
            else:
                print("nope")
                return render_template("login.html", attempt=True)'''
        return redirect("/")
    return render_template("login.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        print("got it register")
        email, password = request.form.get("email", ""), request.form.get("password", "")
        print(email, password)
        if email and password:
            print("lol rly")
            if not username_taken(email):
                print("rendering success")
                token = put_confirmation_token(email, password)
                send_join_mail(email, token)
                return render_template("join_success.html")
            else:
                print("oops")
                return render_template("registration.html", attempt=True)
    return render_template("registration.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', threaded=True)
    app.app_context().push()
