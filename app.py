
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQLdb
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, DateTimeField, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime

app = Flask(__name__)


# config Mysql
app.config['JSON_SORT_KEYS'] = False
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sajilo_yatra'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = '3306'
conn = MySQLdb.connect('127.0.0.1', user='root', password='')
cur = conn.cursor()
cur.execute('use sajilo_yatra')

# index
@app.route('/')
def home():
    return render_template("home.html")

# about
@app.route('/about')
def about():
    return render_template("about.html")


# register form class
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    location = StringField(
        'Location', [validators.Length(min=4, max=50)], default='NULL')
    type = SelectField('Type', choices=[
                       ('mentor', 'Mentor'), ('user', 'User')])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')


class RegisterForm1(Form):

    festival = StringField(
        'Festival', [validators.Length(min=0, max=200)])
    food = StringField(
        'Food', [validators.Length(min=0, max=200)])
    events = StringField(
        'Events', [validators.Length(min=0, max=200)])
    timing = StringField(
        'Event Time', [validators.Length(min=4, max=200), validators.DataRequired()])
    date = DateTimeField(
        'Date and Time(YYYY-MM-DD HH:MM:SS)', [validators.DataRequired()], format='%Y-%m-%d %H:%M:%S')
    duration = IntegerField('Duration in hours', [validators.DataRequired()])
    description = StringField(
        'Description', [validators.Length(min=4, max=1000), validators.DataRequired()])


# user login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get form fields
        username = request.form['username']
        password_candiate = request.form['password']
        # get user by username
        result = cur.execute(
            "select * from register_table where user_name=%s", [username])
        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data[2]
            type = data[3]
            location = data[4]
            userid = data[0]

            # compare password
            if sha256_crypt.verify(password_candiate, password):
                # passed
                session['logged_in'] = True
                session['user_name'] = username
                session['location'] = location
                session['user_id'] = userid
                if type == 'mentor':
                    flash('You are now logged in Mentor', 'success')
                    return redirect(url_for('mentor', user_id=userid))
                else:
                    flash('You are now logged in User', 'success')
                    return redirect(url_for('user', user_id=userid))
            else:
                error = "Invalid login"
                return render_template('login.html', error=error)

            error = "Username not found"
            return render_template('login.html', error=error)

    return render_template('login.html')

# user register
@app.route('/mentor/<user_id>', methods=['GET', 'POST'])
def mentor(user_id):
    form = RegisterForm1(request.form)
    if request.method == 'POST' and form.validate():
        cur = conn.cursor()
        cur.execute('use sajilo_yatra')
        result = cur.execute(
            "select * from register_table where user_id=%s", [user_id])
        data = cur.fetchone()
        location = data[4]
        festival = form.festival.data
        food = form.food.data
        events = form.events.data
        timing = form.timing.data
        date = form.date.data
        duration = form.duration.data
        description = form.description.data
        userid = user_id
        cur.execute("insert into local_table(location,festival,food,events,user_id,timing,date,duration,description) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (location, festival, food, events, user_id, timing, date, duration, description))
        conn.commit()


        flash("Your description about the place has been inserted!Thank you fro your contribution!!", "success")
        return redirect(url_for('mentor', user_id=userid))
    return render_template('mentor.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        location = form.location.data
        type = form.type.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        cur.execute("insert into register_table(user_name,pw,user_type,location) values(%s,%s,%s,%s)",
                    (username, password, type, location))
        conn.commit()
        flash("You are now registered and can log in", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


class Userdata(Form):
    destination = StringField(
        'Destination', [validators.Length(min=4, max=25)])
    month = SelectField(
        'Month', choices=[('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')])


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = Userdata(request.form)
    if request.method == 'POST' and form.validate():
        destination = form.destination.data
        month = form.month.data
        return redirect(url_for('plans', d=destination, m=month))
    return render_template('user.html', form=form)


@app.route('/plans/<d>/<m>', methods=['GET', 'POST'])
def plans(d, m):
    def sortkey(val):
        return val[1]

    recomendedplan = []
    a = datetime.strptime('0001-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
    b = datetime.strptime('9999-01-31 23:59:59','%Y-%m-%d %H:%M:%S')
    cur = conn.cursor()
    cur.execute('use sajilo_yatra')
    result = cur.execute(
        "select * from local_table where location=%s and date between %s and %s", [d,a,b])
    allplan=list(cur.fetchall())
    for record in cur:
        id = record[0]
        cur1 = conn.cursor()
        cur1.execute('use sajilo_yatra')
        cur1.execute("select * from review_table where id=%s", [id])
        all = list(cur1.fetchone())
        recomendedplan.append(all)
    recomendedplan.sort(key=sortkey,reverse=True)
    allp=recomendedplan[:3]
    idarr=[]
    for i in range(3):
        idarr.append(allp[i][0])
    cur2 = conn.cursor()
    cur2.execute('use sajilo_yatra')
    recoplan=[]
    for x in idarr:
        result = cur2.execute(
            "select * from local_table where id=%s", [x])
        y=list(cur2.fetchone())
        recoplan.append(y)
    session['planlists']=recoplan
    session['allplanlists']=allplan
    return render_template('plans.html', recoplans=recoplan,allplans=allplan)

@app.route('/plans/addtoplanr', methods=['GET', 'POST'])
def addtoplanr():
    planlist=[]
    for item in session.pop('planlists', []):
        planlist.append(item)
    idarr=[]
    for plan in planlist:
        idarr.append(plan[0])
    user_id=session['user_id']
    cur3 = conn.cursor()
    cur3.execute('use sajilo_yatra')
    for x in idarr:
        cur3.execute("insert into alltrip_table(user_id,id) values (%s,%s)",(user_id,x))
    conn.commit()
    return redirect(url_for('pplans', user_id=user_id))

@app.route('/plans/addtoplanc', methods=['GET', 'POST'])
def addtoplanc():
    planlist=[]
    for item in session.pop('allplanlists', []):
        planlist.append(item)

    idarr=[]
    for plan in planlist:
        idarr.append(plan[0])
    user_id=session['user_id']
    cur4 = conn.cursor()
    cur4.execute('use sajilo_yatra')
    for x in idarr:
        cur4.execute("insert into alltrip_table(user_id,id) values (%s,%s)",(user_id,x))
    conn.commit()
    return redirect(url_for('pplans', user_id=user_id))

@app.route('/pplans/<user_id>', methods=['GET', 'POST'])
@app.route('/pplans', methods=['GET', 'POST'])
def pplans(user_id):
    allplan = []
    uid = session['user_id']
    cur = conn.cursor()
    cur.execute('use sajilo_yatra')
    result = cur.execute(
        "select * from alltrip_table where user_id=%s", [uid])
    for record in cur:
        id = record[1]
        cur1 = conn.cursor()
        cur1.execute('use sajilo_yatra')
        cur1.execute("select * from local_table where id=%s", [id])
        all = list(cur1.fetchone())
        allplan.append(all)
    return render_template('pplans.html', allplans=allplan)

# Check if user logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# logout
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("You  are now logged out", 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(port=3000, debug=True)
