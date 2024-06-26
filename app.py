from flask import Flask, jsonify, request, session, make_response,redirect, url_for, Blueprint
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date,Time,DateTime , and_, func, case
import datetime
from datetime import datetime, timedelta,timezone
from controller.crm_dashboard import crm_stats
from controller.crm_manage import crm_bp, get_auto_code,get_auto_any_code
from models.db_schema import User, BO, Category,Contact_Note,Call_Note,Zalo_Note,Tele_Note,SMS_Note,Social_Note,Interaction_Content,Interaction_Result,Customers,Customer_Record_History,Tool_Category,Sim_Mgt,IP_Mgt,Phone_Mgt,Email_Mgt,Zalo_Mgt,Tele_Mgt,Social_Mgt,Session_Mgt
from models.db_schema import app, db 
from flask_cors import CORS,cross_origin

CORS(app, supports_credentials = True)
###############################Preset Function#######################
def get_ip_addr():
    header = request.headers
    if 'X-Forwarded-For' in header:
        user_ip = header['X-Forwarded-For'].split(',')[0].strip()  # Take the first IP in the list
    else:
        user_ip = request.remote_addr  # Fallback to the direct connection IP

    return user_ip
##################################################
##Create all tables that defined above
@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all() 
    return 'All tables are created successfully'
###############################################################################################
# #############################################################################################
# #################### Middleware to check if the user is authenticated########################
# #############################################################################################
@app.before_request
def check_authentication():
    #skip authorization for the optiohns method bcz it doesnt has cookie
    if request.method != "OPTIONS":
        
        session_cookie = request.cookies.get('session') 
        if request.endpoint != 'login' and 'username' not in session and session_cookie != True:
            return jsonify({'error': 'unauthenticated'}), 401#redirect(url_for('login'))
    else: 
        headers = {
            'Access-Control-Allow-Origin': '*',  # Replace with your frontend domain
            'Access-Control-Allow-Methods': 'PUT, DELETE',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',  # Cache preflight response for 1 hour
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)
###############################################################################################
#############Log-in/ Log-out###################################################################
###############################################################################################
# Login endpoint

@app.route('/login', methods=['POST'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)
    user_data = User.query.all()
    users = {user.username: {'password': user.password} for user in user_data}

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['checkin_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            session['checkout_time'] = 'chưa check out bạn eey!'#'not yet checked out'
            role = User.query.get(session['username']).role
            team = User.query.get(session['username']).team
            if team == 'crm' or role == 'admin':
                company_name = User.query.get(session['username']).company_name
                session['role'] = role
                login_ip = get_ip_addr()
                new_working_session = Session_Mgt(username=username,checkin_time = session['checkin_time'],login_ip = login_ip,checkout_time = session['checkout_time'])
                db.session.add(new_working_session)
                db.session.commit()
                return jsonify({'message': 'Welcome, {},you are logging in as {}!'.format(session['username'],session['role']),'role': session['role'],'username':session['username'],'company_name': company_name})#session['username']
            else: 
                return jsonify({'error': 'unauthenticated login'}), 401
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    return  jsonify({'error': 'unauthenticated login'}), 401
# Logout endpoint
@app.route('/logout')
def logout():
    current_working_session = Session_Mgt.query.filter(and_(Session_Mgt.checkin_time == datetime.strptime(session['checkin_time'], '%Y-%m-%d %H:%M:%S'),Session_Mgt.username == session["username"])).first()
    check_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_working_session.checkout_time = check_out_time
    db.session.commit()
    session.clear()
    # # session.pop('username', None)
    return jsonify({'message': current_working_session.checkout_time })
    # return {'checkin':session['checkin_time'],'username':session['username']}
# Index page
# @app.route('/loggedin')
# def loggedin():
#     # role = User.query.get.filter(User.role == session['username'])
#     return jsonify({'message': 'Welcome, {},you are logging in as {}!'.format(session['username'],session['role'])})#session['username']

# def get_user_info():
#     headers_dict = {key: value for key, value in request.headers.items()}
@app.route('/test')
def test():
    return request.cookies.get('session') 
@crm_bp.route('/test')
def test():
    # Define the timezone GMT+8
    # tz = pytz.timezone('Asia/Singapore')  # Example of a city in GMT+8 zone

    # Get current date in the specified timezone
    # today_tz = datetime.now().date()
    
    # max_date_data = [{'date': i.date.strftime('%y-%m-%d'),'code':i.code} for i in max_date]
    # # Combine today's date with midnight time, keeping it timezone-aware
    # midnight_today_tz = datetime.combine(datetime.today(), time.min)
    # today_str = midnight_today_tz.strftime('%y%m%d')
    # count = Customers.query.filter(Customers.filled_date >= midnight_today_tz).count() 
    # index_ = count + 1
    # code = today_str+'-'+str(index_)

    code = get_auto_any_code(Sim_Mgt, attr = 'sim_code')
    return [code]# {'haha':today_max_code}
    # headers_dict = [{key: value} for key, value in addr.items()]
    # # ip_addr = headers_dict.get()
    # return headers_dict  # Return headers as a JSON response
    # data = request.form
    # date_string  = data.get('date')
    # date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    # customers = Customers.query.filter(Customers.username == 'shangđasdasđsd')
    # test_list = [{'username': customer.username, 'datre': customer.filled_date >= date_obj} for customer in customers]
    # # return {'str':date_obj}
    # contact_note = Contact_Note.query.filter(Contact_Note.note == 'sda')
    # notes =  [{'note': note.note} for note in contact_note]
    # username = session['username']
    # life_time = app.config['PERMANENT_SESSION_LIFETIME']
    # return addr
    # date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # return date_str
app.register_blueprint(crm_stats)
app.register_blueprint(crm_bp)
# app.register_blueprint(social_bp)
# app.register_blueprint(dev_bp)
# app.register_blueprint(seo_bp)
if __name__ == '__main__':
    app.run(port=3005, debug=True)