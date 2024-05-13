from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date,Time,DateTime , and_, func, case
import datetime
from datetime import datetime, timedelta
app = Flask(__name__)
app.secret_key = 'f33924fea4dd7123a0daa9d2a7213679'
# Replace the following values with your database connection details
db_username = 'crm'
db_password = 'LSciYCtCK7tZXAxL'
db_host = '23.226.8.83'
db_database = 'crm'
db_port = 3306
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # None, Lax, or Strict
app.config['SESSION_COOKIE_SECURE'] = True  # Should be True if using SameSite=None
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['PERMANENT_SESSION_LIFETIME'] =3600*8

# CORS(app, supports_credentials = True)#resources={r"/*": {"origins": "*"}},

# CORS(app, supports_credentials = True)

db = SQLAlchemy(app)
###########SQL Query#############
# INSERT INTO `db_vn168_user` (`username`, `password`, `company_id`, `role`, `team`) VALUES ('shang168', 'admin', 'f0732', 'admin', 'IT');
class User(db.Model):
    __tablename__ = 'db_vn168_user'
    username =  db.Column(db.String(255), primary_key = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    company_name = db.Column(db.String(255), nullable = False)
    company_id = db.Column(db.String(255), nullable = False, unique = True)
    role = db.Column(db.String(255), nullable = False)
    team = db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return f'<User {self.username}>'
###################################################################################
#######################Data model for dropdown list display as an option for data fill-in
#List BO code    
class BO(db.Model):
    __tablename__ = 'db_vn168_crm_bo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bo_code = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.bo_code
#List category
class Category(db.Model):
    __tablename__ = 'db_vn168_crm_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.category
#List contact node
class Contact_Note(db.Model):
    __tablename__ = 'db_vn168_crm_contact_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_note = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.note
#List of call note
class Call_Note(db.Model):
    __tablename__ = 'db_vn168_crm_call_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    call_note = db.Column(db.String(255), primary_key = True,unique = True, nullable = False)
    def __repr__(self):
        return self.call_note
#########
class Zalo_Note(db.Model):
    __tablename__ = 'db_vn168_crm_zalo_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zalo_note= db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.zalo_note
class Tele_Note(db.Model):
    __tablename__ = 'db_vn168_crm_tele_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tele_note= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.tele_note
class SMS_Note(db.Model):
    __tablename__ = 'db_vn168_crm_sms_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sms_note= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.sms_note
class Social_Note(db.Model):
    __tablename__ = 'db_vn168_crm_social_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_note= db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.social_note
class Interaction_Content(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168_interaction_content'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.interaction_content
class Interaction_Result(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168_crm_interaction_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.result 
class Customers(db.Model):
    __tablename__ = 'db_vn168_crm_customer'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    note = db.Column(db.String(255), nullable = True)
    code_origin = db.Column(db.String(255), nullable = True)
    username = db.Column(db.String(255), nullable = False)
    phone_number = db.Column(db.String(128), nullable = True)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = True)
    contact_note = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = True)
    zalo_note = db.Column(db.String(255), nullable = True)
    tele_note = db.Column(db.String(255),nullable = True)
    sms_note = db.Column(db.String(255),nullable = True)
    social_note = db.Column(db.String(255),nullable = True)
    interaction_content = db.Column(db.String(255), nullable = True)
    interaction_result = db.Column(db.String(255), nullable = True)
    person_in_charge = db.Column(db.String(255), nullable = False)
    filled_date = db.Column(DateTime, nullable = False)
    assistant = db.Column(db.String(255),nullable = True)
    creator =  db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return self.code
class Customer_Record_History(db.Model):
    __tablename__ = 'db_vn168_crm_record_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filled_date = db.Column(DateTime, nullable = False)
    created_at = db.Column(DateTime,  nullable=False)
    code = db.Column(db.String(255),  nullable = False)
    username = db.Column(db.String(255), nullable = False)
    phone_number = db.Column(db.String(128), nullable = True)
    note = db.Column(db.String(255), nullable = True)
    code_origin = db.Column(db.String(255), nullable = True)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    contact_note = db.Column(db.String(255), nullable = True)
    call_note = db.Column(db.String(255), nullable = True)
    zalo_note = db.Column(db.String(255), nullable = True)
    tele_note = db.Column(db.String(255),nullable = True)
    sms_note = db.Column(db.String(255),nullable = True)
    social_note = db.Column(db.String(255),nullable = True)
    interaction_content = db.Column(db.String(255), nullable = True)
    interaction_result = db.Column(db.String(255), nullable = True)
    person_in_charge = db.Column(db.String(255), nullable = False)
    assistant = db.Column(db.String(255), nullable = True)
    creator = db.Column(db.String(255),nullable = False)
    editor =  db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return self.created_at
class Tool_Category(db.Model):
    __tablename__ = 'db_vn168_crm_tool_category'
    id = db.Column(db.Integer, primary_key=True, unique = True, autoincrement=True)
    tool_category = db.Column(db.String(255), unique = True, nullable = False)
    type = db.Column(db.String(255),  nullable=False)
########################################################################
################Devices Management######################################
#############################################################################SIM########
class Sim_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_sim_mgt'
    sim_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    number = db.Column(db.String(255), nullable = False)
    provider = db.Column(db.String(255))
    status = db.Column(db.String(255)) #Trạng thái
    package = db.Column(db.String(255))
    zalo_status = db.Column(db.String(255))
    tele_status = db.Column(db.String(255))
    social_status = db.Column(db.String(255))
    sms_status = db.Column(db.String(255))
    storage_location = db.Column(db.String(255))
    sim_note = db.Column(db.String(255))
    def __repr__(self):
        return self.sim_code
#####IP###############
class IP_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_ip_mgt'
    ip_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    ip_info = db.Column(db.String(255), nullable = False)
    expired_date = db.Column(Date)
    country = db.Column(db.String(255))
    provider = db.Column(db.String(255))
    status = db.Column(db.String(255))
    day_until_expiration = db.Column(db.String(255))
    zalo_note = db.Column(db.String(255))
    ip_note = db.Column(db.String(255))
#######Phone##################
class Phone_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_phone_mgt'
    device_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    device_info  = db.Column(db.String(255),unique = True, nullable = False)
    online = db.Column(db.String(255))
    online_cls = db.Column(db.String(255))
    online_nkb = db.Column(db.String(255))
    online_agency = db.Column(db.String(255))
    number1 = db.Column(db.String(255))
    number2 = db.Column(db.String(255))
    phone_note = db.Column(db.String(255))
######Email###################
class Email_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_email_mgt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    recovery_email = db.Column(db.String(255), nullable = True)
    number_verification = db.Column(db.String(255), nullable = True)
    person_in_charge = db.Column(db.String(255), nullable = True)
    email_status = db.Column(db.String(255), nullable = False)
    email_password = db.Column(db.String(255), nullable = False)
    note = db.Column(db.String(255), nullable = True)
    def __repr__(self):
        return self.email    
#######Data model for all contact method including zalo, tele, faceboook , tiktok
######Tool######################################################################
###Zalo
class Zalo_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_zalo_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True)
    tool_category = db.Column(db.String(255))
    creation_device = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    zalo_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    acc_status = db.Column(db.String(255))
    note = db.Column(db.String(255))
###Tele
class Tele_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_tele_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True)
    type = db.Column(db.String(255))
    tool_category = db.Column(db.String(255))
    creation_device = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    tele_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    acc_status = db.Column(db.String(255))
    note = db.Column(db.String(255))
###Facebook
class Social_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_social_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True)
    tool_category = db.Column(db.String(255))
    creation_device = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    social_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    acc_status = db.Column(db.String(255))    
    note = db.Column(db.String(255))

####Employee session management table#########################
class Session_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_session_mgt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    login_ip = db.Column(db.String(255),nullable = True)
    # ip_addr ==
    checkin_time = db.Column(DateTime , nullable = False)
    checkout_time = db.Column(db.String(255), nullable = False)