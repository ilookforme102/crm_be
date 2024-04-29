from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date,Time,DateTime , and_
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

CORS(app, supports_credentials = True)#resources={r"/*": {"origins": "*"}},


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
    username = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    contact_note = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = False)
    zalo_note = db.Column(db.String(255), nullable = False)
    tele_note = db.Column(db.String(255),nullable = False)
    sms_note = db.Column(db.String(255),nullable = False)
    social_note = db.Column(db.String(255),nullable = False)
    interaction_content = db.Column(db.String(255), nullable = False)
    interaction_result = db.Column(db.String(255), nullable = False)
    person_in_charge = db.Column(db.String(255), nullable = False)
    filled_date = db.Column(DateTime, nullable = False)
    assistant = db.Column(db.String(255))
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
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    contact_note = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = False)
    zalo_note = db.Column(db.String(255), nullable = False)
    tele_note = db.Column(db.String(255),nullable = False)
    sms_note = db.Column(db.String(255),nullable = False)
    social_note = db.Column(db.String(255),nullable = False)
    interaction_content = db.Column(db.String(255), nullable = False)
    interaction_result = db.Column(db.String(255), nullable = False)
    person_in_charge = db.Column(db.String(255), nullable = False)
    assistant = db.Column(db.String(255))
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
    num_zalo_acc_created = db.Column(db.String(255))
    num_zalo_acc_active = db.Column(db.String(255))
    num_zalo_acc_active = db.Column(db.String(255))
    online = db.Column(db.String(255))
    online_cls = db.Column(db.String(255))
    online_nkb = db.Column(db.String(255))
    online_agency = db.Column(db.String(255))
    num_sim = db.Column(db.Integer)
    number1 = db.Column(db.String(255))
    number2 = db.Column(db.String(255))
    phone_note = db.Column(db.String(255))
######Email###################
class Email_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_email_mgt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    email_status = db.Column(db.String(255), nullable = False)
    email_password = db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return self.email    
#######Data model for all contact method including zalo, tele, faceboook , tiktok
######Tool######################################################################
###Zalo
class Zalo_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_zalo_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    tool_category = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    zalo_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    note = db.Column(db.String(255))
###Tele
class Tele_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_tele_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    tool_category = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    tele_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    note = db.Column(db.String(255))
###Facebook
class Social_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_social_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    tool_category = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    social_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    note = db.Column(db.String(255))

####Employee session management table#########################
class Session_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_session_mgt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    # ip_addr ==
    checkin_time = db.Column(DateTime , nullable = False)
    checkout_time = db.Column(db.String(255), nullable = False)
#####Using Flask Blueprints to create hierarchical API endpoints#####
#Declare blueprint for CRM team
crm_bp = Blueprint('crm_bp', __name__, url_prefix='/crm')
social_bp = Blueprint('social_bp', __name__, url_prefix='/social')
dev_bp = Blueprint('dev_bp', __name__, url_prefix='/dev')
seo_bp = Blueprint('seo_bp', __name__, url_prefix='/seo')

##################################################
##Create aall tables that defined above
@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all() 
    return 'All tables are created successfully'
#############################################################
@crm_bp.route('/show-record')
def show_records():
    records = Customers.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    dates = [{'filled_date':record.filled_date ,"end date":(datetime.now().date()-timedelta(days=10)),"Start date":datetime.strptime("2024-04-23", '%Y-%m-%d').date()} for record in records]
    return dates    
#Show all record
@crm_bp.route('/record')
def get_records():
    # users = Customers.query.all()
    query = Customers.query
    data = request.args
    page = int(data.get('page','1'))
    per_page = int(data.get('per_page','10'))
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    contact_note = data.get('contact_note')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    sms_note = data.get('sms_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    creator = data.get('creator')
    start_date_str = data.get('start_date_str')
    end_date_str = data.get('end_date_str')
    try:
        # Parse the date string into a date object
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        # end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except TypeError:
        start_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        # end_date = datetime.now().date()+ timedelta(days=10)
    try:
        # Parse the date string into a date object
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except TypeError:
        end_date = datetime.now().date()+ timedelta(days=10)
    # Query the database for customers matching the username and date
    param_mapping = {
            'username': Customers.username.like(f'%{username}%'),
            'category':Customers.category.like(f'%{category}%'),
            'bo_code':Customers.bo_code.like(f'%{bo_code}%'),
            'contact_note':Customers.contact_note.like(f'%{contact_note}%'),
            'call_note':Customers.call_note.like(f'%{call_note}%'),
            'zalo_note':Customers.zalo_note.like(f'%{zalo_note}%'),
            'tele_note':Customers.tele_note.like(f'%{tele_note}%'),
            'sms_note':Customers.sms_note.like(f'%{sms_note}%'),
            'social_note':Customers.social_note.like(f'%{social_note}%'),
            'person_in_charge':Customers.person_in_charge.like(f'%{person_in_charge}%'),
            'interaction_content':Customers.interaction_content.like(f'%{interaction_content}%'),
            'interaction_result':Customers.interaction_result.like(f'%{interaction_result}%'),
            'assistant':Customers.assistant.like(f'%{assistant}%'),
            'creator':Customers.creator.like(f'%{creator}%'),
            'code':Customers.code.like(f'%{code}%'),
            'end_date_str':Customers.filled_date <= end_date,
            'start_date_str':Customers.filled_date >= start_date
    }
    for key, value in param_mapping.items():
        if key in data:
            query = query.filter(value)

    customers =  query.all()
    print(query.statement)
    customer_data = [{'code':customer.code, 'username':customer.username,'category':customer.category,'bo_code':customer.bo_code,'contact_note':customer.contact_note,'call_note':customer.call_note,'zalo_note':customer.zalo_note,'tele_note':customer.tele_note,'sms_note':customer.sms_note,'social_note':customer.social_note,'interaction_content':customer.interaction_content,'interaction_result':customer.interaction_result,'person_in_charge':customer.person_in_charge,'filled_date': customer.filled_date.isoformat(),'assistant':customer.assistant,'creator':customer.creator} for customer in customers]
    paginated_data = customer_data[start_index:end_index]
    paginated_data = customer_data[start_index:end_index]

    return jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(customer_data)})

################################################
##Save new record of customer to the Customer table
@crm_bp.route('/record', methods=['POST'])
def add_record():
    if not request.form:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.form
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    contact_note = data.get('contact_note')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    sms_note = data.get('sms_note')
    social_note = data.get('social_note')
    person_in_charge = session['username']
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    filled_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assistant = data.get('assistant')
    creator = session['username']
    # Check if the user already exists
    if Customers.query.filter((Customers.code == code)).first():
        return jsonify({"error": "Code is already existed, please try again"}), 409
    new_customer = Customers(code= code, username=username,category=category,bo_code=bo_code,contact_note = contact_note,call_note=call_note,zalo_note=zalo_note,tele_note=tele_note,sms_note = sms_note,social_note=social_note,interaction_content=interaction_content, interaction_result = interaction_result, person_in_charge = person_in_charge,filled_date = filled_date,assistant = assistant, creator = creator)
    db.session.add(new_customer)
    try:
        db.session.commit()
        return jsonify({'message': 'Record added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
#####Edit value for a specific code in Customer table, using POST method instad PUT method
####OPTIONS
# @crm_bp.route('/record/<string:code>', methods=['OPTIONS'])
# def handle_preflight():
#     # Add CORS headers to the response
#     response = jsonify({'message': 'Preflight request processed successfully'})
#     response.headers.add('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
#     response.headers.add('Access-Control-Allow-Methods', 'PUT')  # Allow PUT requests
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
@crm_bp.route('/record/<string:code>',methods = ['PUT','OPTIONS'])
def edit_record(code):
    #######################
    # Get method perform a query filtering on the primary key
    record = Customers.query.get(code)
    
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    data = request.form
    record.username = data.get('username')
    record.category = data.get('category')
    record.bo_code = data.get('bo_code')
    record.contact_note = data.get('contact_note')
    record.call_note = data.get('call_note')
    record.zalo_note = data.get('zalo_note')
    record.tele_note = data.get('tele_note')
    record.sms_note = data.get('sms_note')
    record.social_note = data.get('social_note')
    record.person_in_charge = data.get('person_in_charge')
    record.interaction_content = data.get('interaction_content')
    record.interaction_result = data.get('interaction_result')
    record.assistant = data.get('assistant')
    new_record_history = Customer_Record_History(filled_date = record.filled_date,
                                                  created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                                  code= code, 
                                                  username=record.username,
                                                  category=record.category,
                                                  bo_code=record.bo_code,
                                                  contact_note = record.contact_note,
                                                  call_note=record.call_note,
                                                  zalo_note=record.zalo_note,
                                                  tele_note=record.tele_note,
                                                  sms_note = record.sms_note,
                                                  social_note=record.social_note,
                                                  interaction_content=record.interaction_content, 
                                                  interaction_result = record.interaction_result, 
                                                  person_in_charge = record.person_in_charge,
                                                  assistant = record.assistant,
                                                  creator = record.creator,
                                                   editor = session["username"] )
    db.session.add(new_record_history)
    db.session.commit()
    return jsonify({
        'message': 'New record for {} updated successfully'.format(record.code),
        'record': {
            'code': record.code,
            'username': record.username,
            'category' : record.category,
            'bo_code' : record.bo_code,
            'contact_note':record.contact_note,
            'call_note' : record.call_note,
            'zalo_note' : record.zalo_note,
            'tele_note' : record.tele_note,
            'sms' : record.sms_note,
            'social_note' : record.social_note,
            'person_in_charge' : record.person_in_charge,
            'interaction_content' : record.interaction_content,
            'interaction_result' : record.interaction_result,
            'assistant' : record.assistant,
            'creator': record.creator
        }
    }), 200

#######Delete record#############
@crm_bp.route('/record/<string:code>',methods = ['DELETE', 'OPTIONS'])
def remove_record(code):
    record = Customers.query.get(code)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully'})
    else:
        # If the user does not exist, return a 404 error
        return jsonify({'error': 'Record not found'}), 404
#####################################################
#crm/record_history/<string:code>
@crm_bp.route('/record_history/<string:code>',methods =['GET'])
def get_record_history(code):
    history_records = Customer_Record_History.query.filter(Customer_Record_History.code == code).order_by(Customer_Record_History.created_at.desc()).all()
    history_record_data = [{ 'code':code,
                            'filled_date': history_record.filled_date,
                            'edited_at': history_record.created_at,
                            'username': history_record.username,
                            'category' : history_record.category,
                            'bo_code' : history_record.bo_code,
                            'contact_note':history_record.contact_note,
                            'call_note' : history_record.call_note,
                            'zalo_note' : history_record.zalo_note,
                            'tele_note' : history_record.tele_note,
                            'sms' : history_record.sms_note,
                            'social_note' : history_record.social_note,
                            'person_in_charge' : history_record.person_in_charge,
                            'interaction_content' : history_record.interaction_content,
                            'interaction_result' : history_record.interaction_result,
                            'assistant' : history_record.assistant,
                            'creator': history_record.creator,
                            'editor': history_record.editor
                           } for history_record in history_records]
    return history_record_data
@crm_bp.route('/add_history',methods = ['POST'])
def add_history():
    data = request.form
    filled_date = data.get('filled_date')
    # created_at = data.get('created_at')
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    contact_note = data.get('contact_note')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    sms_note = data.get('sms_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    editor = data.get('editor')
    creator = data.get('creator')
    new_history = Customer_Record_History(filled_date = filled_date,
                                                  created_at =  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                                  code= code, 
                                                  username=username,
                                                  category=category,
                                                  bo_code=bo_code,
                                                  contact_note = contact_note,
                                                  call_note=call_note,
                                                  zalo_note=zalo_note,
                                                  tele_note=tele_note,
                                                  sms_note = sms_note,
                                                  social_note=social_note,
                                                  interaction_content=interaction_content, 
                                                  interaction_result = interaction_result, 
                                                  person_in_charge = person_in_charge,
                                                  assistant = assistant,
                                                  creator = creator,
                                                  editor = editor)
    db.session.add(new_history)
    db.session.commit()
    return jsonify({'message': 'History added successfully'}), 200

#############################################
#################Dropdown List###############
#/crm/bo
#/crm/bo [POST]
#/crm/bo [DELETE]
@crm_bp.route('/bo')
def get_bo():
    query = BO.query
    boes = query.all()
    bo_data = [{'bo_code':bo.bo_code} for bo in boes]
    try:
        data = request.args
        page = int(data.get('page'))
        per_page = int(data.get('per_page'))
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
        paginated_data = bo_data[start_index:end_index]
        return jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(bo_data)})
    except TypeError:
        return jsonify({'items': bo_data, 'page': 1, 'per_page': len(bo_data), 'total_items': len(bo_data)})

#add multiple value to bo code
@crm_bp.route('/bo',methods = ['POST'])
def add_bo():
    try:
        data_form = request.form
        data = [{'bo_code':bo_code} for bo_code in data_form.getlist('bo_code')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'}), 400

        for bo in data:
            # Validate data (e.g., check if bo_code is provided)
            if 'bo_code' not in bo:
                return jsonify({'error': 'bo_code is required for each BO'}), 400
            if BO.query.filter(BO.bo_code ==  bo["bo_code"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(bo['bo_code'])}), 409
            # Create a new BO object and add it to the session
            new_bo = BO(bo_code= bo['bo_code'])
            db.session.add(new_bo)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'Users added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@crm_bp.route('/bo/<string:bo_code>',methods = ['DELETE', 'OPTIONS'])
def remove_bo(bo_code):
    code = BO.query.filter(BO.bo_code == bo_code).first()
    if code:
        db.session.delete(code)
        db.session.commit()
        return jsonify({'message':'bo code removed successfully'})
    else:
        return jsonify({'error':'bo code not found'}),404
#/crm/category
#/crm/category [POST]
#/crm/category [DELETE]
@crm_bp.route('/category')
def show_category():
    categories =  Category.query.all()
    categoy_data =  [{'category': category.category} for category in categories]
    try:
        data = request.args
        page = int(data.get('page'))
        per_page = int(data.get('per_page'))
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data =  categoy_data[start_index:end_index]
        return  jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(categoy_data)})
    except TypeError:
        return  jsonify({'items': categoy_data, 'page': 1, 'per_page': len(categoy_data), 'total_items': len(categoy_data)})

@crm_bp.route('/category', methods= ['POST'])
def add_category():
    try:
        data_form = request.form
        data = [{'category':category} for category in data_form.getlist('category')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'}),400
        for category in data:
            if 'category'  not in category:
                return jsonify({'error':'category is require for each category table'})
            if Category.query.filter(Category.category == category["category"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(category['category'])}), 409
            else:
                new_category = Category(category = category['category'])
                db.session.add(new_category)
        db.session.commit()
        return jsonify({'message':'Category added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/category/<string:category>', methods= ['DELETE', 'OPTIONS'])
def remove_category(category):
    category_name = Category.query.filter(Category.category == category).first()
    if category_name:
        db.session.delete(category_name)
        db.session.commit()
        return jsonify({'message': 'Category removed successfully'})
    else:
        return jsonify({'error':'category not found'}),404
#/crm/contact_note
#/crm/contact_note [POST]
#/crm/contact_note [DELETE]
@crm_bp.route('/contact_note')
def show_contact_note():
    contact_notes = Contact_Note.query.all()
    contact_note_data = [{'contact_note': contact_note.contact_note} for contact_note in contact_notes]
    try:
        data = request.args
        page = int(data.get('page'))
        per_page = int(data.get('per_page'))
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = contact_note_data[start_index:end_index]
        return  jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(contact_note_data)})
    except TypeError:
        return  jsonify({'items': contact_note_data, 'page': 1, 'per_page': len(contact_note_data), 'total_items': len(contact_note_data)})
@crm_bp.route('/contact_note', methods= ['POST'])
def add_contact_note():
    try:
        data_form = request.form
        data = [{'contact_note':contact_note} for contact_note in data_form.getlist('contact_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for contact_note in data:
            if 'contact_note'  not in contact_note:
                return jsonify({'error':'contact note is require for each note table'})
            if Contact_Note.query.filter(Contact_Note.contact_note == contact_note["contact_note"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(contact_note['note'])}), 409
            else:
                new_contact_note = Contact_Note(contact_note = contact_note['contact_note'])
                db.session.add(new_contact_note)
        db.session.commit()
        return jsonify({'message':'Note(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/contact_note/<string:contact_note>', methods= ['DELETE', 'OPTIONS'])
def remove_contact_note(contact_note):
    contact_note = Contact_Note.query.filter(Contact_Note.contact_note == contact_note).first()
    if contact_note:
        db.session.delete(contact_note)
        db.session.commit()
        return jsonify({'message': 'contact_note removed successfully'})
    else:
        return jsonify({'error':'contact_note not found'}),404
#/crm/call_note 
#/crm/call_note [POST]
#/crm/call_note [DELETE]
@crm_bp.route("/call_note") #GET
def show_call_note():
    call_notes = Call_Note.query.all()
    call_note_data = [{'call_note': call_note.call_note} for call_note in call_notes]
    try:
        data = request.args
        page = int(data.get('page'))
        per_page = int(data.get('per_page'))
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data =  call_note_data[start_index:end_index]
        return  jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(call_note_data)})
    except TypeError:
        return  jsonify({'items': call_note_data, 'page': 1, 'per_page': len(call_note_data), 'total_items': len(call_note_data)})
#Add new call record
@crm_bp.route('/call_note', methods= ['POST']) #POST
def add_call_note():
    try:
        data_form = request.form
        data = [{'call_note':call_note} for call_note in data_form.getlist('call_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for call_note in data:
            if 'call_note'  not in call_note:
                return jsonify({'error':'call_note is require for each call_note table'})
            if Call_Note.query.filter(Call_Note.call_note == call_note["call_note"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(call_note['call_note'])}), 409
            else:
                new_call_note = Call_Note(call_note = call_note['call_note'])
                db.session.add(new_call_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/call_note/<string:call_note>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_call_note(call_note):
    call_note = Call_Note.query.filter(Call_Note.call_note == call_note).first()
    if call_note:
        db.session.delete(call_note)
        db.session.commit()
        return jsonify({'message': 'call_note removed successfully'})
    else:
        return jsonify({'error':'call_note not found'}),404

#/crm/zalo_note
#/crm/zalo_note [POST]
#/crm/zalo_note [DELETE]

@crm_bp.route("/zalo_note") #GET
def show_zalo_note():
    # data = request.args
    # page = int(data.get('page'),'1')
    # per_page = int(data.get('per_page'),'2')
    # start_index = (page - 1) * per_page
    # end_index = start_index + per_page
    zalo_notes = Zalo_Note.query.all()
    zalo_note_data = [{'zalo_note': zalo_note.zalo_note} for zalo_note in zalo_notes]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = zalo_note_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page,'total_items':len(zalo_note_data)})
    except TypeError:
        return jsonify({'items':zalo_note_data,'page':1,'per_page':len(zalo_note_data),'total_items':len(zalo_note_data)})

@crm_bp.route('/zalo_note', methods= ['POST']) #POST
def add_zalo_note():
    try:
        data_form = request.form
        data = [{'zalo_note':zalo_note} for zalo_note in data_form.getlist('zalo_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for zalo_note in data:
            if 'zalo_note'  not in zalo_note:
                return jsonify({'error':'zalo_note is require for each call_note table'})
            if Zalo_Note.query.filter(Zalo_Note.zalo_note == zalo_note["zalo_note"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(zalo_note['zalo_note'])}), 409
            else:
                new_zalo_note = Zalo_Note(zalo_note = zalo_note['zalo_note'])
                db.session.add(new_zalo_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/zalo_note/<string:zalo_note>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_zalo_note(zalo_note):
    zalo_note = Zalo_Note.query.filter(Zalo_Note.zalo_note == zalo_note).first()
    if zalo_note:
        db.session.delete(zalo_note)
        db.session.commit()
        return jsonify({'message': 'call_note removed successfully'})
    else:
        return jsonify({'error':'call_note not found'}),404
#/crm/tele_note 
#/crm/tele_note [POST]
#/crm/tele_note [DELETE]
@crm_bp.route("/tele_note") #GET
def show_tele_note():
    tele_notes = Tele_Note.query.all()
    tele_note_data = [{'tele_note': tele_note.tele_note} for tele_note in tele_notes]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = tele_note_data[start_index:end_index]
        return jsonify({'items': paginated_data,'page':page,'per_page':per_page,'total_items': len(tele_note_data)})
    except TypeError:
        return jsonify({'items': tele_note_data,'page':1,'per_page':len(tele_note_data),'total_items': len(tele_note_data)})
@crm_bp.route('/tele_note', methods= ['POST']) #POST
def add_tele_note():
    try:
        data_form = request.form
        data = [{'tele_note':tele_note} for tele_note in data_form.getlist('tele_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for tele_note in data:
            if 'tele_note'  not in tele_note:
                return jsonify({'error':'tele_note is require for each tele_note table'})
            if Tele_Note.query.filter(Tele_Note.tele_note == tele_note["tele_note"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(tele_note['tele_note'])}), 409
            else:
                new_tele_note = Tele_Note(tele_note = tele_note['tele_note'])
                db.session.add(new_tele_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/tele_note/<string:tele_note>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_tele_note(tele_note):
    tele_note = Tele_Note.query.filter(Tele_Note.tele_note == tele_note).first()
    if tele_note:
        db.session.delete(tele_note)
        db.session.commit()
        return jsonify({'message': 'tele_note removed successfully'})
    else:
        return jsonify({'error':'tele_note not found'}),404
#/crm/sms_note 
#/crm/sms_note [POST]
#/crm/sms_note [DELETE    
@crm_bp.route("/sms_note") #GET
def show_sms_note():
    sms_notes = SMS_Note.query.all()
    sms_note_data = [{'sms_note': sms_note.sms_note} for sms_note in sms_notes]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = sms_note_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(sms_note_data)})
    except TypeError:
        return jsonify({'items':sms_note_data,'page':1,'per_page':len(sms_note_data), 'total_items':len(sms_note_data)})
@crm_bp.route('/sms_note', methods= ['POST']) #POST
def add_sms_note():
    try:
        data_form = request.form
        data = [{'sms_note':sms_note} for sms_note in data_form.getlist('sms_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for sms_note in data:
            if 'sms_note'  not in sms_note:
                return jsonify({'error':'sms_note is require for each sms_note table'})
            if SMS_Note.query.filter(SMS_Note.sms_note == sms_note["sms_note"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(sms_note['sms_note'])}), 409 
            else:
                new_sms_note = SMS_Note(sms_note = sms_note['sms_note'])
                db.session.add(new_sms_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/sms_note/<string:sms_note>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_sms_note(sms_note):
    sms_note = SMS_Note.query.filter(SMS_Note.sms_note == sms_note).first()
    if sms_note:
        db.session.delete(sms_note)
        db.session.commit()
        return jsonify({'message': 'sms_note removed successfully'})
    else:
        return jsonify({'error':'sms_note not found'}),404

#/crm/social_note 
#/crm/social_note [POST]
#/crm/social_note [DELETE]
@crm_bp.route("/social_note") #GET
def show_social_note():
    social_notes = Social_Note.query.all()
    social_note_data = [{'social_note': social_note.social_note} for social_note in social_notes]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = social_note_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(social_note_data)})
    except TypeError:
        return jsonify({'items':social_note_data,'page':1,'per_page':len(social_note_data), 'total_items':len(social_note_data)})
@crm_bp.route('/social_note', methods= ['POST']) #POST
def add_social_note():
    try:
        data_form = request.form
        data = [{'social_note':social_note} for social_note in data_form.getlist('social_note')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for social_note in data:
            if 'social_note'  not in social_note:
                return jsonify({'error':'social_note is require for each social_note table'})
            if Social_Note.query.filter(Social_Note.social_note == social_note['social_note']).first():
                return jsonify({"error":"""the value "{}" already existed, please try a new value""".format(social_note["social_note"])})
            else:
                new_social_note = Social_Note(social_note = social_note['social_note'])
                db.session.add(new_social_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/social_note/<string:social_note>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_social_note(social_note):
    social_note = Social_Note.query.filter(Social_Note.social_note == social_note).first()
    if social_note:
        db.session.delete(social_note)
        db.session.commit()
        return jsonify({'message': 'social_note removed successfully'})
    else:
        return jsonify({'error':'social_note not found'}),404
#/crm/interaction_content 
#/crm/interaction_content [POST]
#/crm/interaction_content [DELETE]
@crm_bp.route("/interaction_content") #GET
def show_interaction_content():
    contents = Interaction_Content.query.all()
    interaction_content_data = [{'content': content.content} for content in contents]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = interaction_content_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(interaction_content_data)})
    except TypeError:
        return jsonify({'items':interaction_content_data,'page':1,'per_page':len(interaction_content_data), 'total_items':len(interaction_content_data)})
@crm_bp.route('/interaction_content', methods= ['POST']) #POST
def add_interaction_content():
    try:
        data_form = request.form
        data = [{'content':content} for content in data_form.getlist('content')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for content in data:
            if 'content'  not in content:
                return jsonify({'error':'content is require for each content table'})
            if Interaction_Content.query.filter((Interaction_Content.content == content['content'])).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(content['content'])}), 409
            else:
                new_interaction_content = Interaction_Content(content = content['content'])
                db.session.add(new_interaction_content)
        db.session.commit()
        return jsonify({'message':'interaction_content(s) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/interaction_content/<string:content>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_interaction_content(content):
    interaction_content = Interaction_Content.query.filter(Interaction_Content.content == content).first()
    if interaction_content:
        db.session.delete(interaction_content)
        db.session.commit()
        return jsonify({'message': 'content removed successfully'})
    else:
        return jsonify({'error':'content not found'}),404
#/crm/interaction_result 
#/crm/interaction_result [POST]
#/crm/interaction_result [DELETE]
@crm_bp.route("/interaction_result") #GET
def show_interaction_result():
    results = Interaction_Result.query.all()
    interaction_result_data = [{'result': result.result} for result in results]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = interaction_result_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(interaction_result_data)})
    except TypeError:
        return jsonify({'items':interaction_result_data,'page':1,'per_page':len(interaction_result_data), 'total_items':len(interaction_result_data)})
@crm_bp.route('/interaction_result', methods= ['POST']) #POST
def add_interaction_result():
    try:
        data_form = request.form
        data = [{'result':result} for result in data_form.getlist('result')]
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid FORM data'})
        for result in data:
            if 'result'  not in result:
                return jsonify({'error':'result is require for each result table'})
            if Interaction_Result.query.filter((Interaction_Result.result == result['result'])).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(result['result'])}), 409
            else:
                result = Interaction_Result(result = result['result'])
                db.session.add(result)
        db.session.commit()
        return jsonify({'message':'interaction_result(s) added successfully'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/interaction_result/<string:result>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_interaction_result(result):
    result = Interaction_Result.query.filter(Interaction_Result.result == result).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return jsonify({'message': 'result removed successfully'})
    else:
        return jsonify({'error':'result not found'}),404

#/crm/assistant
@crm_bp.route('/assistant')
def get_assistant_crm():
    assistants = User.query.filter(User.team == "crm").all()
    assistant_data=[{"assistant": data.username} for data in assistants]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = assistant_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(assistant_data)})
    except TypeError:
        return jsonify({'items':assistant_data,'page':1,'per_page':len(assistant_data), 'total_items':len(assistant_data)})

#####################################################################################
#crm/person_in_charge
@crm_bp.route('/person_in_charge')
def get_pic_crm():
    person_in_charge = User.query.filter(User.team == "crm")
    pic_data=[{"person_in_charge": data.username} for data in person_in_charge]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = pic_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(pic_data)})
    except TypeError:
        return jsonify({'items':pic_data,'page':1,'per_page':len(pic_data), 'total_items':len(pic_data)})
######################################################################################
#/crm/tool_category
#/crm/tool_category [POST]
#/crm/tool_category [EDIT] 
@crm_bp.route('/tool_category', methods =['GET'])
def show_tool_category():
    tool_categories = Tool_Category.query.all()
    tool_category_data = [{'tool_category': tool_category.tool_category, 'type': tool_category.type} for tool_category in tool_categories]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = tool_category_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(tool_category_data)})
    except TypeError:
        return jsonify({'items':tool_category_data,'page':1,'per_page':len(tool_category_data), 'total_items':len(tool_category_data)})
@crm_bp.route('/tool_category', methods = ['POST','OPTIONS'])
def add_tool_category():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    tool_category = data.get('tool_category')
    type = data.get('type')
    if Tool_Category.query.filter(Tool_Category.tool_category == tool_category).all():
        return jsonify({'error':'Tool category is already existed, please try again'}),409
    new_tool_category = Tool_Category(tool_category = tool_category, type = type)
    db.session.add(new_tool_category)
    try:
        db.session.commit()
        return jsonify({'message': 'Tool category added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool_category/<string:tool_category>', methods = ['DELETE','OPTIONS'])
def delete_tool_category(tool_category):
    tool_category = Tool_Category.query.filter(Tool_Category.tool_category == tool_category).first()
    if tool_category:
        db.session.delete(tool_category)
        db.session.commit()
        return jsonify({'message': 'Tool category removed successfully'}),200
    else:
        return jsonify({'error':'Tool category not found'}),404
##################################################################################
#######################Devices Management#########################################
##################################################################################
###Phone###
@crm_bp.route('/device/phone')#GET
def show_phone():
    phones = Phone_Mgt.query.all()
    phone_data = [{'device_code': phone.device_code,
                   'num_zalo_acc_created': phone.num_zalo_acc_created,
                   'num_zalo_acc_active': phone.num_zalo_acc_active,
                   'online': phone.num_zalo_acc_active,
                   'online_cls': phone.online_cls,
                   'online_nkb': phone.online_nkb,
                   'online_agency': phone.online_agency,
                   'num_sim': phone.num_sim,
                   'number1': phone.number1,
                   'number2	': phone.number2,
                   'phone_note': phone.phone_note} for phone in phones]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = phone_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(phone_data)})
    except TypeError:
        return jsonify({'items':phone_data,'page':1,'per_page':len(phone_data), 'total_items':len(phone_data)})

@crm_bp.route('/device/phone', methods= ['POST']) #POST
def add_phone():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    device_code = data.get('device_code')
    num_zalo_acc_created = data.get('num_zalo_acc_created')
    num_zalo_acc_active = data.get('num_zalo_acc_active')
    online = data.get('online') ##### get from zalo note table
    online_cls = data.get('online_cls') ##### get from zalo note table
    online_nkb = data.get('online_nkb') ##### get from zalo note table
    online_agency = data.get('online_agency')
    num_sim = data.get('num_sim')
    number1 = data.get('number1')
    number2 = data.get('number2')
    phone_note = data.get('phone_note')
    if Phone_Mgt.query.get(device_code):
        return jsonify({"error": "Device Code is already existed, please try again"}), 409
    new_phone  = Phone_Mgt(
        device_code = device_code,
        num_zalo_acc_created = num_zalo_acc_created,
        num_zalo_acc_active = num_zalo_acc_active,
        online = online,
        online_cls = online_cls,
        online_nkb = online_nkb,
        online_agency = online_agency,
        num_sim = num_sim,
        number1 = number1,
        number2 = number2,
        phone_note = phone_note
    )
    db.session.add(new_phone)
    try:
        db.session.commit()
        return jsonify({'message': 'Device code added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/device/phone/<string:device_code>', methods =['PUT','OPTIONS'])
def edit_phone(device_code):
    data = request.form
    device = Phone_Mgt.query.get(device_code)
    if not device:
        return jsonify({'error': 'Record not found'}), 404
    device.num_zalo_acc_created = data.get('num_zalo_acc_created')
    device.num_zalo_acc_active = data.get('num_zalo_acc_active')
    device.online = data.get('online') ##### get from zalo note table
    device.online_cls = data.get('online_cls') ##### get from zalo note table
    device.online_nkb = data.get('online_nkb') ##### get from zalo note table
    device.online_agency = data.get('online_agency')
    device.num_sim = data.get('num_sim')
    device.number1 = data.get('number1')
    device.number2 = data.get('number2')
    device.phone_note = data.get('phone_note')
    db.session.commit()
    return jsonify({'message':'New device updated successfully'}),200
@crm_bp.route('/device/phone/<string:device_code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_phone(device_code):
    device = Phone_Mgt.query.get(device_code)
    if device:
        db.session.delete(device)
        db.session.commit()
        return jsonify({'message': 'device removed successfully'}),200
    else:
        return jsonify({'error':'device not found'}),404
###################
###IP Management###
###################
@crm_bp.route('/device/ip')#GET
def show_ip():
    ips = IP_Mgt.query.all()
    ip_data = [{'ip_code ': ip.ip_code,
                   'ip_info': ip.ip_info,
                   'expired_date': ip.expired_date,
                   'country': ip.country,
                   'provider': ip.provider,
                   'status': ip.status,
                   'day_until_expiration': ip.day_until_expiration,
                   'zalo_note': ip.zalo_note,
                   'ip_note': ip.ip_note} for ip in ips]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = ip_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(ip_data)})
    except TypeError:
        return jsonify({'items':ip_data,'page':1,'per_page':len(ip_data), 'total_items':len(ip_data)})
@crm_bp.route('/device/ip', methods= ['POST']) #POST
def add_ip():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    ip_code   = data.get('ip_code')
    ip_info  = data.get('ip_info')
    expired_date = data.get('expired_date')
    country = data.get('country') ##### get from zalo note table
    provider = data.get('provider') ##### get from zalo note table
    status = data.get('status') ##### get from zalo note table
    day_until_expiration = data.get('day_until_expiration')
    zalo_note = data.get('zalo_note')
    ip_note = data.get('ip_note')
    if IP_Mgt.query.get(ip_code):
        return jsonify({"error": "Ip code is already existed, please try again"}), 409
    new_phone  = IP_Mgt(
        ip_code = ip_code,
        ip_info = ip_info,
        expired_date = expired_date,
        country = country,
        provider = provider,
        status = status,
        day_until_expiration = day_until_expiration,
        zalo_note = zalo_note,
        ip_note = ip_note
    )
    db.session.add(new_phone)
    try:
        db.session.commit()
        return jsonify({'message': 'IP added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/device/ip/<string:ip_code>', methods =['PUT','OPTIONS'])
def edit_ip(ip_code):
    data = request.form
    ip = IP_Mgt.query.get(ip_code)
    if not ip:
        return jsonify({'error': 'IP not found'}), 404
    ip.ip_info = data.get('ip_info')
    ip.expired_date = data.get('expired_date')
    ip.country = data.get('country') ##### get from zalo note table
    ip.provider = data.get('provider') ##### get from zalo note table
    ip.status = data.get('status') ##### get from zalo note table
    ip.day_until_expiration = data.get('day_until_expiration')
    ip.zalo_note = data.get('zalo_note')
    ip.ip_note = data.get('ip_note')
    db.session.commit()
    return jsonify({'message':'New device updated successfully'}),200
@crm_bp.route('/device/ip/<string:ip_code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_ip(ip_code):
    device = IP_Mgt.query.get(ip_code)
    if device:
        db.session.delete(device)
        db.session.commit()
        return jsonify({'message': 'IP removed successfully'}),200
    else:
        return jsonify({'error':'IP not found'}),404
#######################    
###Sim Management######
#######################
@crm_bp.route('/device/sim')#GET
def show_sim():
    sims = Sim_Mgt.query.all()
    sim_data = [{'sim_code  ': sim.sim_code,
                'number': sim.number,
                'provider': sim.provider,
                'status': sim.status,
                'package': sim.package,
                'zalo_status': sim.zalo_status,
                'tele_status': sim.tele_status,
                'social_status': sim.social_status,
                'sms_status': sim.sms_status,
                'storage_location': sim.storage_location,
                'sim_note': sim.sim_note} for sim in sims]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = sim_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(sim_data)})
    except TypeError:
        return jsonify({'items':sim_data,'page':1,'per_page':len(sim_data), 'total_items':len(sim_data)})
@crm_bp.route('/device/sim', methods= ['POST']) #POST
def add_sim():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    sim_code   = data.get('sim_code')
    if Sim_Mgt.query.get(sim_code):
        return jsonify({"error": "Sim code is already existed, please try again"}), 409
    new_sim  = Sim_Mgt(
        sim_code = sim_code,
        number = data.get('number'),
        provider = data.get('provider'),
        package = data.get('package'),
        zalo_status = data.get('zalo_status'),
        tele_status = data.get('tele_status'),
        social_status = data.get('social_status'),
        sms_status = data.get('sms_status'),
        storage_location = data.get('storage_location'),
        sim_note = data.get('sim_note')
    )
    db.session.add(new_sim)
    try:
        db.session.commit()
        return jsonify({'message': 'New sim added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/device/sim/<string:sim_code>', methods =['PUT','OPTIONS'])
def edit_sim(sim_code):
    data = request.form
    sim = Sim_Mgt.query.get(sim_code)
    if not sim:
        return jsonify({'error': 'Sim not found'}), 404
    sim.number = data.get('number')
    sim.provider = data.get('provider')
    sim.package = data.get('package')
    sim.zalo_status = data.get('zalo_status')
    sim.tele_status = data.get('tele_status')
    sim.social_status = data.get('social_status')
    sim.sms_status = data.get('sms_status')
    sim.storage_location = data.get('storage_location')
    sim.sim_note = data.get('sim_note')
    db.session.commit()
    return jsonify({'message':'Sim info updated successfully'}),200
@crm_bp.route('/device/sim/<string:sim_code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_sim(sim_code):
    sim = Sim_Mgt.query.get(sim_code)
    if sim:
        db.session.delete(sim)
        db.session.commit()
        return jsonify({'message': 'Sim removed successfully'}),200
    else:
        return jsonify({'error':'Sim not found'}),404
#######################################################################################################
###################################Tool Management#####################################################
#######################################################################################################
##########################
#######Zalo Manage########
##########################
@crm_bp.route('/tool/zalo')
def get_zalo():
    zalos = Zalo_Mgt.query.all()
    zalo_data = [{'code': zalo.code,
                'tool_category': zalo.tool_category,
                'person_in_charge': zalo.person_in_charge,
                'zalo_note': zalo.zalo_note,
                'username': zalo.username,
                'password': zalo.password,
                'phone_number': zalo.phone_number,
                'email': zalo.email,
                'ip_address': zalo.ip_address,
                'note': zalo.note} for zalo in zalos]
    try:
        data = request.args
        page = data.get('page',1)
        per_page = data.get('per_page',10)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = zalo_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(zalo_data)})
    except Exception:
        return jsonify({'items':zalo_data,'page':1,'per_page':len(zalo_data), 'total_items':len(zalo_data)})
@crm_bp.route('/tool/zalo', methods= ['POST']) #POST
def add_zalo():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    zalo_code   = data.get('code')
    if Zalo_Mgt.query.get(zalo_code):
        return jsonify({"error": "Zalo code is already existed, please try again"}), 409
    new_zalo  = Zalo_Mgt(
        code = zalo_code,
        tool_category = data.get('tool_category'),
        person_in_charge = data.get('person_in_charge'),
        zalo_note = data.get('zalo_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        note = data.get('note'),
    )
    db.session.add(new_zalo)
    try:
        db.session.commit()
        return jsonify({'message': 'New zalo added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool/zalo/<string:code>', methods =['PUT','OPTIONS'])
def edit_zalo(code):
    data = request.form
    zalo = Zalo_Mgt.query.get(code)
    if not zalo:
        return jsonify({'error': 'Zalo not found'}), 404
    zalo.tool_category = data.get('tool_category')
    zalo.person_in_charge = data.get('person_in_charge')
    zalo.zalo_note = data.get('zalo_note'),
    zalo.username = data.get('username')
    zalo.password = data.get('password')
    zalo.phone_number = data.get('phone_number')
    zalo.email = data.get('email')
    zalo.ip_address = data.get('ip_address')
    zalo.note = data.get('note')
    db.session.commit()
    return jsonify({'message':'Zalo info updated successfully'}),200
@crm_bp.route('/tool/zalo/<string:code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_zalo(code):
    code = Zalo_Mgt.query.get(code)
    if code:
        db.session.delete(code)
        db.session.commit()
        return jsonify({'message': 'Code removed successfully'}),200
    else:
        return jsonify({'error':'Code not found'}),404
##########################
#######Tele Manage########
##########################
@crm_bp.route('/tool/tele')
def get_tele():
    teles = Tele_Mgt.query.all()
    tele_data = [{'code': tele.code,
                'tool_category': tele.tool_category,
                'person_in_charge': tele.person_in_charge,
                'tele_note': tele.tele_note,
                'username': tele.username,
                'password': tele.password,
                'phone_number': tele.phone_number,
                'email': tele.email,
                'ip_address': tele.ip_address,
                'note': tele.note} for tele in teles]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = tele_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(tele_data)})
    except TypeError:
        return jsonify({'items':tele_data,'page':1,'per_page':len(tele_data), 'total_items':len(tele_data)})
@crm_bp.route('/tool/tele', methods= ['POST']) #POST
def add_tele():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    tele_code   = data.get('code')
    if Tele_Mgt.query.get(tele_code):
        return jsonify({"error": "Tele code is already existed, please try again"}), 409
    new_tele  = Tele_Mgt(
        code = tele_code,
        tool_category = data.get('tool_category'),
        person_in_charge = data.get('person_in_charge'),
        tele_note = data.get('tele_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        note = data.get('note'),
    )
    db.session.add(new_tele)
    try:
        db.session.commit()
        return jsonify({'message': 'New tele added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool/tele/<string:code>', methods =['PUT','OPTIONS'])
def edit_tele(code):
    data = request.form
    tele = Tele_Mgt.query.get(code)
    if not tele:
        return jsonify({'error': 'Tele not found'}), 404
    tele.tool_category = data.get('tool_category')
    tele.person_in_charge = data.get('person_in_charge')
    tele.tele_note = data.get('tele_note'),
    tele.username = data.get('username')
    tele.password = data.get('password')
    tele.phone_number = data.get('phone_number')
    tele.email = data.get('email')
    tele.ip_address = data.get('ip_address')
    tele.note = data.get('note')
    db.session.commit()
    return jsonify({'message':'Tele info updated successfully'}),200
@crm_bp.route('/tool/tele/<string:code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_tele(code):
    code = Tele_Mgt.query.get(code)
    if code:
        db.session.delete(code)
        db.session.commit()
        return jsonify({'message': 'Code removed successfully'}),200
    else:
        return jsonify({'error':'Code not found'}),404
##########################
#######Social Manage########
##########################
@crm_bp.route('/tool/social')
def get_social():
    socials = Social_Mgt.query.all()
    social_data = [{'code': social.code,
                'tool_category': social.tool_category,
                'person_in_charge': social.person_in_charge,
                'social_note': social.social_note,
                'username': social.username,
                'password': social.password,
                'phone_number': social.phone_number,
                'email': social.email,
                'ip_address': social.ip_address,
                'note': social.note} for social in socials]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = social_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(social_data)})
    except TypeError:
        return jsonify({'items':social_data,'page':1,'per_page':len(social_data), 'total_items':len(social_data)})
@crm_bp.route('/tool/social', methods= ['POST']) #POST
def add_social():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    social_code   = data.get('code')
    if Social_Mgt.query.get(social_code):
        return jsonify({"error": "Social code is already existed, please try again"}), 409
    new_social  = Social_Mgt(
        code = social_code,
        tool_category = data.get('tool_category'),
        person_in_charge = data.get('person_in_charge'),
        social_note = data.get('social_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        note = data.get('note'),
    )
    db.session.add(new_social)
    try:
        db.session.commit()
        return jsonify({'message': 'New social added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool/social/<string:code>', methods =['PUT','OPTIONS'])
def edit_social(code):
    data = request.form
    social = Social_Mgt.query.get(code)
    if not social:
        return jsonify({'error': 'Social not found'}), 404
    social.tool_category = data.get('tool_category')
    social.person_in_charge = data.get('person_in_charge')
    social.social_note = data.get('social_note'),
    social.username = data.get('username')
    social.password = data.get('password')
    social.phone_number = data.get('phone_number')
    social.email = data.get('email')
    social.ip_address = data.get('ip_address')
    social.note = data.get('note')
    db.session.commit()
    return jsonify({'message':'Social info updated successfully'}),200
@crm_bp.route('/tool/social/<string:code>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_social(code):
    code = Social_Mgt.query.get(code)
    if code:
        db.session.delete(code)
        db.session.commit()
        return jsonify({'message': 'Social code removed successfully'}),200
    else:
        return jsonify({'error':'Social code not found'}),404
##########################
#######Email Manage########
##########################
@crm_bp.route('/tool/email')
def get_email():
    emails = Email_Mgt.query.all()
    email_data = [{'email': email.code,
                'email_password': email.tool_category,
                'email_status': email.person_in_charge} for email in emails]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = email_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(email_data)})
    except TypeError:
        return jsonify({'items':email_data,'page':1,'per_page':len(email_data), 'total_items':len(email_data)})
@crm_bp.route('/tool/email', methods= ['POST']) #POST
def add_email():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    email   = data.get('email')
    if Email_Mgt.query.filter(Email_Mgt.email == email).first():
        return jsonify({"error": "Social code is already existed, please try again"}), 409
    new_social  = Email_Mgt(
        email = email,
        email_password = data.get('email_password'),
        email_status = data.get('email_status')
    )
    db.session.add(new_social)
    try:
        db.session.commit()
        return jsonify({'message': 'New social added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool/email/<string:email>', methods =['PUT','OPTIONS'])
def edit_email(email):
    data = request.form
    email = Email_Mgt.query.filter(Email_Mgt.email == email)
    if not email:
        return jsonify({'error': 'Email not found'}), 404
    email.email_password = data.get('email_password')
    email.email_status = data.get('email_status')
   
    db.session.commit()
    return jsonify({'message':'Email info updated successfully'}),200
@crm_bp.route('/tool/email/<string:email>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_email(email):
    email = Email_Mgt.query.get(email)
    if email:
        db.session.delete(email)
        db.session.commit()
        return jsonify({'message': 'Social code removed successfully'}),200
    else:
        return jsonify({'error':'Social code not found'}),404
######################################################################################################
########################################Reports#######################################################
######################################################################################################
@crm_bp.route('/stats/metrics/total_customers')
def count_customer():
    query = Customers.query
    customers = query.count()
    depositors = query.filter(Customers.interaction_result in ['Khách SEO Nạp Tiền','Khách CRM Nạp Tiền']).count()
    return jsonify({'total_customer':customers})
######################################################################################################
################################User Management#######################################################
######################################################################################################
#crm/user
#crm/user [POST]
#crm/user [PUT]
#crm/user [DELETE]
@crm_bp.route('/user')
def show_users():
    users = User.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    user_data = {user.username: {'role': user.role,'company_id': user.company_id,'password': user.password,'company_id': user.company_id,'company_name': user.company_name,'team': user.team} for user in users}
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = user_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(user_data)})
    except TypeError:
        return jsonify({'items':user_data,'page':1,'per_page':len(user_data), 'total_items':len(user_data)})
#Add user, not register
@crm_bp.route('/user', methods=['POST'])
def add_user():
    if 'role' in session and session['role'] in ['admin','leader']:
        # users  =  get_users()
        if not request.form:
            return jsonify({"error": "Missing JSON in request"}), 400
        data = request.form
        username = data.get('username')
        password = data.get('username')
        company_name = data.get('company_name')
        company_id = data.get('company_id')
        role = data.get('role')
        team = data.get('team')
        # Check if the user already exists
        if User.query.filter((User.username == username)).first():
            return jsonify({"error": "User is already existed, please try again"}), 409
        new_user = User(username=username,password=password,company_name=company_name,company_id=company_id,role=role,team=team)
        db.session.add(new_user)
        try:
            db.session.commit()
            return "User added successfully!"
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if an error occurs
            return str(e)
    else:
        return jsonify({"error": "unauthenticated"}),401
@crm_bp.route('/user/<string:username>', methods = ['POST','OPTIONS'])
def edit_user(username):
    if 'role' in session and session['role'] in ['admin','leader']:
        user = User.query.get(username)
        data = request.form
        current_password =  user.password
        new_password = data.get('password')
        
        if user:
            if new_password == current_password:
                return jsonify({'error': 'new password should be different from old password'}), 400
            else:
                db.session.commit()
                return jsonify({'message': 'User data editted successfully'})
        else:
            # If the user does not exist, return a 404 error
            return jsonify({'error': 'Record not found'}), 404
    else:
        return  jsonify({'error': 'unauthenticated login'}), 401
@crm_bp.route('/user/<string:username>', methods = ['DELETE', 'OPTIONS'])
def remove_user(username):
    if 'role' in session and session['role'] in ['admin','leader']:
        user = User.query.get(username)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            # If the user does not exist, return a 404 error
            return jsonify({'error': 'Record not found'}), 404
    else:
        return  jsonify({'error': 'unauthenticated login'}), 401
#############################################################################################
####################User Session Managemenet#################################################
#############################################################################################
##/crm/user_session##
@crm_bp.route('/user_session')
def show_user_working_session():
    working_sessions = Session_Mgt.query.all()
    working_session_data = [{'username': working_session.username,'checkin_time':working_session.checkin_time,'checkout_time': working_session.checkout_time} for working_session in working_sessions]
    try:
        data = request.args
        page = data.get('page')
        per_page = data.get('per_page')
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = working_session_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(working_session_data)})
    except TypeError:
        return jsonify({'items':working_session_data,'page':1,'per_page':len(working_session_data), 'total_items':len(working_session_data)})

#############################################################################################
#################### Middleware to check if the user is authenticated########################
#############################################################################################
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)
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
            company_name = User.query.get(session['username']).company_name
            session['role'] = role
            new_working_session = Session_Mgt(username=username,checkin_time = session['checkin_time'],checkout_time = session['checkout_time'])
            db.session.add(new_working_session)
            db.session.commit()
            return jsonify({'message': 'Welcome, {},you are logging in as {}!'.format(session['username'],session['role']),'role': session['role'],'username':session['username'],'company_name': company_name})#session['username']
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

def get_user_info():
    headers_dict = {key: value for key, value in request.headers.items()}

@crm_bp.route('/test')
def test():
    # addr = request.headers
    # headers_dict = {key: value for key, value in request.headers.items()}
    # ip_addr = headers_dict.get()
    # return jsonify(headers_dict)  # Return headers as a JSON response
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
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return date_str
app.register_blueprint(crm_bp)
app.register_blueprint(social_bp)
app.register_blueprint(dev_bp)
app.register_blueprint(seo_bp)
if __name__ == '__main__':
    app.run(port=5001, debug=True)