from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date,Time,DateTime,asc ,nulls_last, and_,text, func, case, Integer, union,desc, or_
import datetime
from datetime import datetime, timedelta, time
from models.db_schema import User, BO, Category,Contact_Note,Call_Note,Zalo_Note,Tele_Note,SMS_Note,Social_Note,Interaction_Content,Interaction_Result,Customers,Customer_Record_History,Tool_Category,Sim_Mgt,IP_Mgt,Phone_Mgt,Email_Mgt,Zalo_Mgt,Tele_Mgt,Social_Mgt,Session_Mgt
from models.db_schema import db 
crm_bp = Blueprint('crm_bp', __name__, url_prefix='/crm')
#############################################################
@crm_bp.route('/show-record')
def show_records():
    records = Customers.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    dates = [{'filled_date':record.filled_date ,"end date":(datetime.now().date()-timedelta(days=10)),"Start date":datetime.strptime("2024-04-23", '%Y-%m-%d').date()} for record in records]
    return dates    
#Show all record
@crm_bp.route('/export_data')
def export_data():
    data = request.args
    fields = data.get('fields')
    if fields:
        # Split the fields by comma to get a list of field names
        field_list = fields.split(',')
        valid_fields = [getattr(Customers, field) for field in field_list if hasattr(Customers, field)]
        
        if not valid_fields:
            return jsonify({'error': 'No valid fields specified'}), 400
        
        # Execute the query with the selected fields
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        data = []

        if not start_date_str or not end_date_str:
            results = db.session.query(*valid_fields).all()
            for result in results:
                user_data = {field: getattr(result, field) for field in field_list}
                data.append(user_data)
            
            return jsonify(data)
        results = db.session.query(*valid_fields).filter(
            and_(
                func.date( func.date_sub(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE"))) >= start_date_str,
                func.date( func.date_sub(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE"))) <= end_date_str
            )
        ).order_by(Customers.filled_date.desc()).all()
        for result in results:
            user_data = {field: getattr(result, field) for field in field_list}
            data.append(user_data)
        
        return jsonify(data)
    else:
        return jsonify({'error': 'No fields specified'}), 400
@crm_bp.route('/record')
def get_records():
    # users = Customers.query.all()
    query = Customers.query
    data = request.args
    is_edited = data.get('is_edited','false')
    page = int(data.get('page','1'))
    per_page = int(data.get('per_page','20'))
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    code = data.get('code')
    username = data.get('username')
    note = data.get('note')
    code_origin = data.get('code_origin')
    phone_number = data.get('phone_number')
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
            'note': Customers.note.like(f'%{note}%'),
            'code_origin': Customers.code_origin.like(f'%{code_origin}%'),
            'category':Customers.category.like(f'%{category}%'),
            'phone_number':Customers.phone_number.like(f'%{phone_number}%'),
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
            'start_date_str':  func.date( func.date_sub(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE"))) >= start_date,
            'end_date_str': func.date( func.date_sub(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE"))) <= end_date
            # 'start_date_str':  func.date_add(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE")) >= func.date(start_date),
            # 'end_date_str': func.date_add(Customers.filled_date, text("INTERVAL '18:10' HOUR_MINUTE")) <= func.date(end_date)

    }
    for key, value in param_mapping.items():
        if key in data:
            query = query.filter(value)
    if is_edited == 'false':
        customers =  query.order_by(Customers.filled_date.desc()).all()
    if is_edited == 'true':
        customers = query.order_by(Customers.recent_changed_at.desc(),Customers.filled_date.desc()).all()
    print(query.statement)
    customer_data = [{'code':customer.code, 'username':customer.username,'note':customer.note,'code_origin':customer.code_origin,'phone_number':customer.phone_number,'category':customer.category,'bo_code':customer.bo_code,'contact_note':customer.contact_note,'call_note':customer.call_note,'zalo_note':customer.zalo_note,'tele_note':customer.tele_note,'sms_note':customer.sms_note,'social_note':customer.social_note,'interaction_content':customer.interaction_content,'interaction_result':customer.interaction_result,'person_in_charge':customer.person_in_charge,'filled_date': customer.filled_date,'recent_changed_at':customer.recent_changed_at,'assistant':customer.assistant,'creator':customer.creator} for customer in customers]
    paginated_data = customer_data[start_index:end_index]
    paginated_data = customer_data[start_index:end_index]
    # data = [{"filled_date":customer.filled_date}    for customer in customers]
    return jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(customer_data)})
    # return jsonify({'items':data,'size':len(data)})
################################################
##Save new record of customer to the Customer table

def get_code():
    midnight_today_tz = datetime.combine(datetime.today(), time.min)
    today_str = midnight_today_tz.strftime('%y%m%d')
    count = Customers.query.filter(Customers.filled_date >= midnight_today_tz).count() 
    index_ = count + 1
    code = today_str+'-'+str(index_)
    return code
def get_auto_code_2(db,**kwargs):
    prefix = kwargs.get('prefix', '')
    today_str = datetime.now().strftime('%y%m%d')
    count = db.query.count() 
    index_ = count + 1
    code = prefix+today_str+'-'+str(index_)
    while db.query.get(code) is not None:
        index_ +=1
        code = prefix+today_str+'-'+str(index_)
    return code
def get_auto_code(db, **kwargs):
    prefix = kwargs.get('prefix', '')
    today_str = datetime.now().strftime('%y%m%d')
    count = db.query.with_entities(func.max(func.cast(func.substring_index(db.code,'-',-1), Integer))).scalar()
    if count:
        count = int(count)
        index_ = count + 1
        if len(str(index_))>=2:
            code = prefix+today_str+'-'+str(index_)
        else:
             code = prefix+today_str+'-'+'0'+str(index_)
    else:
        index_ = '01'
        code = prefix+today_str+'-'+str(index_)
    return code
def get_auto_sim_code(db, **kwargs):
    prefix = kwargs.get('prefix', '')
    today_str = datetime.now().strftime('%y%m%d')
    count = db.query.with_entities(func.max(func.cast(func.substring_index(db.sim_code,'-',-1), Integer))).scalar()
    if count:
        count = int(count)
        index_ = count + 1
        code = prefix+today_str+'-'+str(index_)
    else:
        index_ = 1
        code = prefix+today_str+'-'+str(index_)
    return code
def get_auto_any_code(db,attr, **kwargs):
    prefix = kwargs.get('prefix', '')
    today_str = datetime.now().strftime('%y%m%d')
    count = db.query.with_entities(func.max(func.cast(func.substring_index(db.__dict__[attr],'-',-1), Integer))).scalar()
    if count:
        count = int(count)
        index_ = count + 1
        code = prefix+today_str+'-'+str(index_)
    else:
        index_ = 1
        code = prefix+today_str+'-'+str(index_)
    return code
@crm_bp.route('/record', methods=['POST'])
def add_record():
    if not request.form:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.form
    note = data.get('note')
    code_origin = data.get('code_origin')
    username = data.get('username')
    phone_number = data.get('phone_number')
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
    # assistant = ''
    creator = session['username']
    code = get_code()#data.get('code')
    # Check if the user already exists
    if Customers.query.filter((Customers.code == code)).first():
        return jsonify({"error": "Code is already existed, please try again"}), 409
    new_customer = Customers(code=code, username=username,note = note, code_origin =  code_origin,phone_number=phone_number,category=category,bo_code=bo_code,contact_note = contact_note,call_note=call_note,zalo_note=zalo_note,tele_note=tele_note,sms_note = sms_note,social_note=social_note,interaction_content=interaction_content, interaction_result = interaction_result, person_in_charge = person_in_charge,filled_date = filled_date, creator = creator)
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
    current_record_data = {
        "filled_date": record.filled_date,
        # "recent_changed_at"
        "code": code, 
        "username":record.username,
        "note":record.note,
        "code_origin":record.code_origin,
        "phone_number":record.phone_number,
        "category":record.category,
        "bo_code":record.bo_code,
        "contact_note": record.contact_note,
        "call_note":record.call_note,
        "zalo_note":record.zalo_note,
        "tele_note":record.tele_note,
        "sms_note" : record.sms_note,
        "social_note":record.social_note,
        "interaction_content":record.interaction_content, 
        "interaction_result": record.interaction_result, 
        "person_in_charge" : record.person_in_charge,
        "assistant": record.assistant,
        "creator" :record.creator,
        "editor" :session["username"]
    }
    new_record_history = Customer_Record_History(filled_date = current_record_data["filled_date"],
                                                  created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                                  code= code, 
                                                  username=current_record_data["username"],
                                                  note=current_record_data["note"],
                                                  code_origin=current_record_data["code_origin"],
                                                  phone_number=current_record_data["phone_number"],
                                                  category=current_record_data["category"],
                                                  bo_code=current_record_data["bo_code"],
                                                  contact_note = current_record_data["contact_note"],
                                                  call_note=current_record_data["call_note"],
                                                  zalo_note=current_record_data["zalo_note"],
                                                  tele_note=current_record_data["tele_note"],
                                                  sms_note = current_record_data["sms_note"],
                                                  social_note=current_record_data["social_note"],
                                                  interaction_content=current_record_data["interaction_content"], 
                                                  interaction_result = current_record_data["interaction_result"], 
                                                  person_in_charge = current_record_data["person_in_charge"],
                                                  assistant = current_record_data["assistant"],
                                                  creator = current_record_data["creator"],
                                                  editor = session["username"],
                                                  )
    
    data = request.form
    record.username = data.get('username')
    record.note = data.get('note')
    record.code_origin = data.get('code_origin')
    record.phone_number = data.get('phone_number')
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
    record.recent_changed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # new_record_history.change_log = jsonify({
    # Compare the values of the record object and the new_record_history object
    change_log = {}
    for column in Customers.__table__.columns:
        column_name = column.name
        record_value = getattr(record, column_name)
        try:
            history_value = getattr(new_record_history, column_name)
        except AttributeError:
            continue

        if record_value != history_value:
            # try:
            #     change_log[column_name] = str(history_value + ',' +  record_value
            # except TypeError:
            change_log[column_name] = str(history_value) + ',' +  str(record_value)
        new_record_history.change_log = change_log
    if not change_log:
        return jsonify({'error': 'no change has made'}), 400
    elif change_log:
        db.session.add(new_record_history)
        db.session.commit()
        return jsonify({
        'message': 'New record for {} updated successfully'.format(record.code),
        'record': {
            'code': record.code,
            'username': record.username,
            'note': record.note,
            'code_origin': record.code_origin,
            'phone_number': record.phone_number,
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
    current_record = Customers.query.get(code)
    current_record_data = [{
                            'code':code,
                            'filled_date': current_record.filled_date,
                            'recent_changed_at': current_record.recent_changed_at,
                            'username': current_record.username,
                            'note': current_record.note,
                            'code_origin': current_record.code_origin,
                            'phone_number': current_record.phone_number,
                            'category' : current_record.category,
                            'bo_code' : current_record.bo_code,
                            'contact_note':current_record.contact_note,
                            'call_note' : current_record.call_note,
                            'zalo_note' : current_record.zalo_note,
                            'tele_note' : current_record.tele_note,
                            'sms' : current_record.sms_note,
                            'social_note' : current_record.social_note,
                            'person_in_charge' : current_record.person_in_charge,
                            'interaction_content' : current_record.interaction_content,
                            'interaction_result' : current_record.interaction_result,
                            'assistant' : current_record.assistant,
                            'creator': current_record.creator,
                            }]  
    history_records = Customer_Record_History.query.filter(Customer_Record_History.code == code).order_by(Customer_Record_History.created_at.desc()).all()
    history_record_data = [{ 'code':code,
                            'filled_date': history_record.filled_date,
                            'edited_at': history_record.created_at,
                            'username': history_record.username,
                            'note': history_record.note,
                            'code_origin': history_record.code_origin,
                            'phone_number': history_record.phone_number,
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
                            'editor': history_record.editor,
                            'change_log': history_record.change_log
                           } for history_record in history_records]
    return jsonify({
        'current_record': current_record_data,
        'history_record': history_record_data
    })
    
@crm_bp.route('/add_history',methods = ['POST'])
def add_history():
    data = request.form
    filled_date = data.get('filled_date')
    # created_at = data.get('created_at')
    code = data.get('code')
    username = data.get('username')
    note = data.get('note')
    code_origin = data.get('code_origin')
    phone_number = data.get('phone_number')
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
                                        note=note,
                                        code_origin=code_origin,
                                        phone_number =phone_number,
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
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(contact_note['contact_note'])}), 409
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
    data = request.args
    tool_type = data.get('type')
    if tool_type != None:
        type_data = [i for i in tool_category_data if i['type'] == tool_type]
        return jsonify({'items':type_data,'total_items':len(type_data)})
    else:
        return jsonify({'items':tool_category_data,'total_items':len(tool_category_data)})

        # page = data.get('page')
        # per_page = data.get('per_page',10)
    # data = request.form
    # try:
    #     data = request.args
    #     page = data.get('page')
    #     per_page = data.get('per_page',10)
    #     tool_type = data.get('type')
    #     if tool_type != None:
    #         start_index = (page - 1) * per_page
    #         end_index = start_index + per_page
    #         type_data = [i for i in tool_category_data if i['type'] == tool_type]
    #         paginated_data = type_data[start_index:end_index]
    #         return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(tool_category_data)})
    #     else:
    #         start_index = (page - 1) * per_page
    #         end_index = start_index + per_page
    #         paginated_data = tool_category_data[start_index:end_index]
    #         return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(paginated_data)})
    # except TypeError:
    #     return jsonify({'items':tool_category_data,'page':1,'per_page':len(tool_category_data), 'total_items':len(tool_category_data)})
    # type_data  = data.get('type')
    # return jsonify({'mesage':type_data })

@crm_bp.route('/tool_category', methods = ['POST','OPTIONS'])
def add_tool_category():
    try:
        data = request.json
        tool_category_list = [{'tool_category':category.get('tool_category'), 'type':category.get('type')} for category in data]
        if not tool_category_list or not isinstance(tool_category_list, list):
            return jsonify({'error': 'Invalid JSON data'}), 400

        for category in tool_category_list:
            # Validate data (e.g., check if bo_code is provided)
            if 'tool_category' not in category:
                return jsonify({'error': 'tool_category is required for each BO'}), 400
            if 'type' not in category:
                return jsonify({'error': 'type is required for each BO'}), 400
            if Tool_Category.query.filter(Tool_Category.tool_category ==  category["tool_category"]).first():
                return jsonify({"error": """the value "{}" is already existed, please try again""".format(category["tool_category"])}), 409
            # Create a new BO object and add it to the session
            new_tool_category = Tool_Category(tool_category= category['tool_category'], type = category['type'])
            db.session.add(new_tool_category)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'Tool category successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    # if not request.form:
    #     return jsonify({"error": "Missing FORM in request"}), 400
    # data = request.json
    # tool_category = data.get('tool_category')
    # type = data.get('type')
    # if Tool_Category.query.filter(Tool_Category.tool_category == tool_category).all():
    #     return jsonify({'error':'Tool category is already existed, please try again'}),409
    # new_tool_category = Tool_Category(tool_category = tool_category, type = type)
    # db.session.add(new_tool_category)
    # try:
    #     db.session.commit()
    #     return jsonify({'message': 'Tool category added successfully'}),200
    # except Exception as e:
    #     db.session.rollback()  # Roll back the transaction if an error occurs
    #     return str(e),500
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
    data = request.args
    query = Phone_Mgt.query
    search_str = data.get('search')
    if search_str:
        query = query.filter(
            or_(
                Phone_Mgt.device_code.like(f"%{search_str}%"),
                Phone_Mgt.device_info.like(f"%{search_str}%")
            )
        )
    phones = query.order_by(Phone_Mgt.device_code.desc()).all()
    phone_data = [{'device_code': phone.device_code,
                   'device_info': phone.device_info,
                   'online':phone.online,
                   'online_cls': phone.online_cls,
                   'online_nkb': phone.online_nkb,
                   'online_agency': phone.online_agency,
                   'number1': phone.number1,
                   'number2': phone.number2,
                   'phone_note': phone.phone_note} for phone in phones]
    try:
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
    device_code = get_auto_any_code(Phone_Mgt, attr= 'device_code', prefix = 'PH-')
    device_info = data.get('device_info')
    online = data.get('online') ##### get from zalo note table
    online_cls = data.get('online_cls') ##### get from zalo note table
    online_nkb = data.get('online_nkb') ##### get from zalo note table
    online_agency = data.get('online_agency')
    number1 = data.get('number1')
    number2 = data.get('number2')
    phone_note = data.get('phone_note')
    if Phone_Mgt.query.filter(Phone_Mgt.device_info == device_info).all():
        return jsonify({"error": "Device info is already existed, please try again"}), 409
    new_phone  = Phone_Mgt(
        device_code = device_code,
        device_info = device_info,
        online = online,
        online_cls = online_cls,
        online_nkb = online_nkb,
        online_agency = online_agency,
        number1 = number1,
        number2 = number2,
        phone_note = phone_note
    )
    db.session.add(new_phone)
    try:
        db.session.commit()
        return jsonify({'message': 'Device info added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/device/phone/<string:device_code>', methods =['PUT','OPTIONS'])
def edit_phone(device_code):
    data = request.form
    device = Phone_Mgt.query.get(device_code)
    if not device:
        return jsonify({'error': 'Record not found'}), 404
    device.device_info = data.get('device_info') ##### get from zalo note table
    device.online = data.get('online') ##### get from zalo note table
    device.online_cls = data.get('online_cls') ##### get from zalo note table
    device.online_nkb = data.get('online_nkb') ##### get from zalo note table
    device.online_agency = data.get('online_agency')
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
#####################Phone linked Tele/Zalo/Scoial###############
@crm_bp.route('/device/phone_tools')
# select  ss.device_info, (COUNT(ss.code) OVER (PARTITION BY ss.device_info) ) linked_devices, ss.code
# from (SELECT s.code,d.device_info from (SELECT code, creation_device 
# from `db_vn168_crm_zalo_mgt`
# UNION
# SELECT code, creation_device 
# from `db_vn168_crm_tele_mgt`
# UNION
# SELECT code, creation_device 
# from `db_vn168_crm_social_mgt`) as s 
# LEFT JOIN `db_vn168_crm_phone_mgt` d 
# ON d.device_info = s.creation_device
# UNION
# SELECT s.code,d.device_info from (SELECT code, creation_device 
# from `db_vn168_crm_zalo_mgt`
# UNION
# SELECT code, creation_device 
# from `db_vn168_crm_tele_mgt`
# UNION
# SELECT code, creation_device 
# from `db_vn168_crm_social_mgt`) as s 
# Right JOIN `db_vn168_crm_phone_mgt` d 
# ON d.device_info = s.creation_device) as ss;
def get_list_linked_tool():
    # Create subquery
    union_query = union(
        db.session.query(Zalo_Mgt.code.label('code'), Zalo_Mgt.creation_device.label('creation_device')),
        db.session.query(Tele_Mgt.code.label('code'), Tele_Mgt.creation_device.label('creation_device')),
        db.session.query(Social_Mgt.code.label('code'), Social_Mgt.creation_device.label('creation_device'))
    )
    subquery = union_query.subquery('s')
    # LEFT JOIN Query
    left_join_query = db.session.query(
        subquery.c.code.label('code'), Phone_Mgt.device_info.label('device_info')
        ).select_from(
            subquery
            ).outerjoin(
        Phone_Mgt, Phone_Mgt.device_info == subquery.c.creation_device
    )

    # RIGHT JOIN Query (this can be tricky in SQLAlchemy as it doesn't support right join directly, but you can reverse the order of tables and use outerjoin)
    right_join_query = db.session.query(subquery.c.code.label('code'), Phone_Mgt.device_info.label('device_info')).select_from(Phone_Mgt).outerjoin(
        subquery, Phone_Mgt.device_info == subquery.c.creation_device
    )

    # Final UNION
    raw_data_query = union(
        left_join_query, 
        right_join_query).subquery()
    final_query = db.session.query(raw_data_query.c.device_info, 
                                   raw_data_query.c.code,
                                   func.count(raw_data_query.c.code).over(partition_by=raw_data_query.c.device_info).label('linked_tools')
                                     ).order_by(desc('linked_tools'))
    # Executing the final query
    results = final_query.all()
    data = request.args
    page = int(data.get('page',1))
    per_page = int(data.get('per_page',20))
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    try:
        linked_tools = int(data.get('linked_tools', None))
        if linked_tools or linked_tools == 0:
            result_data = [{'device':result.device_info,'code': result.code,'linked_tools': result.linked_tools} for result in results if result.linked_tools == linked_tools]

            # linked_data = [i for i in result_data if i['linked_tools'] == linked_tools]
            paginated_data = result_data[start_index:end_index]
            return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(result_data)})
        elif linked_tools is None:
            result_data = [{'device':result.device_info,'code': result.code,'linked_tools': result.linked_tools} for result in results]

            paginated_data = result_data[start_index:end_index]
            return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(result_data)})
    except (ValueError,TypeError) :
        result_data = [{'device':result.device_info,'code': result.code,'linked_tools': result.linked_tools} for result in results]

        paginated_data = result_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(result_data)})


###################
###IP Management###
###################
@crm_bp.route('/device/ip')#GET
def show_ip():
    data = request.args
    query = IP_Mgt.query
    search_str = data.get('search')
    if search_str:
        query = query.filter(
            or_(
                IP_Mgt.ip_code.like(f"%{search_str}%"),
                IP_Mgt.ip_info.like(f"%{search_str}%"),
            )
        )
    ips = query.order_by(IP_Mgt.ip_code.desc()).all()
    ip_data = [{'ip_code': ip.ip_code,
                   'ip_info': ip.ip_info,
                   'expired_date': ip.expired_date,
                   'country': ip.country,
                   'provider': ip.provider,
                   'status': ip.status,
                   'day_until_expiration': ip.day_until_expiration,
                   'zalo_note': ip.zalo_note,
                   'ip_note': ip.ip_note} for ip in ips]
    try:
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
    ip_code = get_auto_any_code(IP_Mgt, attr = 'ip_code', prefix = 'IP-')
    ip_info  = data.get('ip_info')
    expired_date = data.get('expired_date')
    country = data.get('country') ##### get from zalo note table
    provider = data.get('provider') ##### get from zalo note table
    status = data.get('status') ##### get from zalo note table
    day_until_expiration = data.get('day_until_expiration')
    zalo_note = data.get('zalo_note')
    ip_note = data.get('ip_note')
    if IP_Mgt.query.filter(IP_Mgt.ip_info == ip_info):
        return jsonify({"error": "Ip Info is already existed, please try again"}), 409
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
    data = request.args
    query = Sim_Mgt.query
    search_str = data.get('search')
    if search_str:
        query = query.filter(
            or_(
                Sim_Mgt.sim_code.like(f"%{search_str}%"),
                Sim_Mgt.number.like(f"%{search_str}%"),
            )
        )
    sims = query.order_by(Sim_Mgt.sim_code.desc()).all()
    sim_data = [{'sim_code': sim.sim_code,
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
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
    sim_code   = get_auto_any_code(Sim_Mgt, attr = 'sim_code', prefix = 'SIM-')
    number = data.get('number')
    if Sim_Mgt.query.filter(Sim_Mgt.number == number):
        return jsonify({"error": "Sim Number is already existed, please try again"}), 409
    new_sim  = Sim_Mgt(
        sim_code = sim_code,
        number = number,
        provider = data.get('provider'),
        status = data.get('status'),
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
    number = data.get('number')
    if not sim:
        return jsonify({'error': 'Sim not found'}), 404
    if Sim_Mgt.query.filter(Sim_Mgt.number == number):
        return jsonify({"error": "Sim Number is already existed, please try again"}), 409
    sim.number = number
    sim.provider = data.get('provider')
    sim.status = data.get('status')
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
    data = request.args
    filter_val = data.get('search')
    query =  Zalo_Mgt.query
    if filter_val:
        query = query.filter(
        or_(
            Zalo_Mgt.code.like(f"%{filter_val}%"),
            Zalo_Mgt.username.like(f"%{filter_val}%")                   
        )
        )
    zalos = query.order_by(Zalo_Mgt.code.desc()).all()
    zalo_data = [{'code': zalo.code,
                'tool_category': zalo.tool_category,
                'creation_device': zalo.creation_device,
                'person_in_charge': zalo.person_in_charge,
                'zalo_note': zalo.zalo_note,
                'username': zalo.username,
                'password': zalo.password,
                'phone_number': zalo.phone_number,
                'email': zalo.email,
                'ip_address': zalo.ip_address,
                'acc_status': zalo.acc_status,
                'note': zalo.note} for zalo in zalos]
    try:
        
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_data = zalo_data[start_index:end_index]
        return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(zalo_data)})
    except Exception as e:
        print(e)
        return jsonify({'items':zalo_data,'page':1,'per_page':len(zalo_data), 'total_items':len(zalo_data)})
@crm_bp.route('/tool/zalo', methods= ['POST']) #POST
def add_zalo():
    if not request.form:
        return jsonify({"error": "Missing FORM in request"}), 400
    data = request.form
    zalo_code   = get_auto_code(Zalo_Mgt, prefix = 'ZL-')
    if Zalo_Mgt.query.get(zalo_code):
        return jsonify({"error": "Zalo code is already existed, please try again"}), 409
    new_zalo  = Zalo_Mgt(
        code = zalo_code,
        tool_category = data.get('tool_category'),
        creation_device = data.get('creation_device'),
        person_in_charge = data.get('person_in_charge'),
        zalo_note = data.get('zalo_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        acc_status = data.get('acc_status'),
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
    zalo.creation_device = data.get('creation_device')
    zalo.person_in_charge = data.get('person_in_charge')
    zalo.zalo_note = data.get('zalo_note'),
    zalo.username = data.get('username')
    zalo.password = data.get('password')
    zalo.phone_number = data.get('phone_number')
    zalo.email = data.get('email')
    zalo.ip_address = data.get('ip_address')
    zalo.acc_status = data.get('acc_status')
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
    data = request.args
    filter_val = data.get('search')
    query =  Tele_Mgt.query
    if filter_val:
        query = query.filter(
        or_(
            Tele_Mgt.code.like(f"%{filter_val}%"),
            Tele_Mgt.username.like(f"%{filter_val}%")                   
        )
        )
    teles = query.order_by(Tele_Mgt.code.desc()).all()
    tele_data = [{'code': tele.code,
                'type': tele.type,
                'tool_category': tele.tool_category,
                'creation_device': tele.creation_device,
                'person_in_charge': tele.person_in_charge,
                'tele_note': tele.tele_note,
                'username': tele.username,
                'password': tele.password,
                'phone_number': tele.phone_number,
                'email': tele.email,
                'ip_address': tele.ip_address,
                'acc_status': tele.acc_status,
                'note': tele.note} for tele in teles]
    try:
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
    tele_code   = get_auto_code(Tele_Mgt, prefix = 'TELE-')
    if Tele_Mgt.query.get(tele_code):
        return jsonify({"error": "Tele code is already existed, please try again"}), 409
    new_tele  = Tele_Mgt(
        code = tele_code,
        type = data.get('type'),
        tool_category = data.get('tool_category'),
        creation_device = data.get('creation_device'),
        person_in_charge = data.get('person_in_charge'),
        tele_note = data.get('tele_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        acc_status = data.get('acc_status'),
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
    tele.type = data.get('type')
    tele.tool_category = data.get('tool_category')
    tele.creation_device = data.get('creation_device')
    tele.person_in_charge = data.get('person_in_charge')
    tele.tele_note = data.get('tele_note'),
    tele.username = data.get('username')
    tele.password = data.get('password')
    tele.phone_number = data.get('phone_number')
    tele.email = data.get('email')
    tele.ip_address = data.get('ip_address')
    tele.acc_status = data.get('acc_status')
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
    data = request.args
    filter_val = data.get('search')
    query =  Social_Mgt.query
    if filter_val:
        query = query.filter(
        or_(
            Social_Mgt.code.like(f"%{filter_val}%"),
            Social_Mgt.username.like(f"%{filter_val}%")                   
        )
        )
    socials = query.order_by(Social_Mgt.code.desc()).all()
    social_data = [{'code': social.code,
                'tool_category': social.tool_category,
                'creation_device': social.creation_device,
                'person_in_charge': social.person_in_charge,
                'social_note': social.social_note,
                'username': social.username,
                'password': social.password,
                'phone_number': social.phone_number,
                'email': social.email,
                'ip_address': social.ip_address,
                'acc_status': social.acc_status,
                'note': social.note} for social in socials]
    try:
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
    code   = get_auto_code(Social_Mgt, prefix= 'SOC-')
    if Social_Mgt.query.get(code) is not None:

        return jsonify({"error": "Social code is already existed, please try again"}), 409
    new_social  = Social_Mgt(
        code = code,
        tool_category = data.get('tool_category'),
        creation_device = data.get('creation_device'),
        person_in_charge = data.get('person_in_charge'),
        social_note = data.get('social_note'),
        username = data.get('username'),
        password = data.get('password'),
        phone_number = data.get('phone_number'),
        email = data.get('email'),
        ip_address = data.get('ip_address'),
        acc_status = data.get('acc_status'),
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
    social.creation_device = data.get('creation_device')
    social.person_in_charge = data.get('person_in_charge')
    social.social_note = data.get('social_note'),
    social.username = data.get('username')
    social.password = data.get('password')
    social.phone_number = data.get('phone_number')
    social.email = data.get('email')
    social.ip_address = data.get('ip_address')
    social.acc_status = data.get('acc_status')
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
    data = request.args
    filter_val = data.get('search')
    query =  Email_Mgt.query
    if filter_val:
        query = query.filter(
        or_(
            Email_Mgt.email.like(f"%{filter_val}%"),
            Email_Mgt.number_verification.like(f"%{filter_val}%")                   
        )
        )
    emails = query.order_by(Email_Mgt.id.desc()).all()
    email_data = [{'id': email.id,
                'email': email.email,
                'recovery_email': email.recovery_email,
                'number_verification': email.number_verification,
                'person_in_charge': email.person_in_charge,
                'email_password': email.email_password,
                'email_status': email.email_status,
                'note': email.note
                } for email in emails]
    try:
        data = request.args
        page = int(data.get('page',1))
        per_page = int(data.get('per_page',10))
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
        return jsonify({"error": "Email is already existed, please try again"}), 409
    new_social  = Email_Mgt(
        email = email,
        recovery_email = data.get('recovery_email'),
        number_verification = data.get('number_verification'),
        person_in_charge = data.get('person_in_charge'),
        email_password = data.get('email_password'),
        note = data.get('note'),
        email_status = data.get('email_status')
    )
    db.session.add(new_social)
    try:
        db.session.commit()
        return jsonify({'message': 'New email added successfully'}),200
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e),500
@crm_bp.route('/tool/email/<string:email>', methods =['PUT','OPTIONS'])
def edit_email(email):
    data = request.form
    email = Email_Mgt.query.filter(Email_Mgt.email == email).first()
    if not email:
        return jsonify({'error': 'Email not found'}), 404
    email.recovery_email = data.get('recovery_email')
    email.number_verification = data.get('number_verification')
    email.person_in_charge = data.get('person_in_charge')
    email.email_password = data.get('note')
    email.note = data.get('email_password')
    email.email_status = data.get('email_status')
   
    db.session.commit()
    return jsonify({'message':'Email info updated successfully'}),200
@crm_bp.route('/tool/email/<string:email>', methods= ['DELETE', 'OPTIONS']) #DELETE
def remove_email(email):
    email = Email_Mgt.query.filter(Email_Mgt.email == email).first()
    if email:
        db.session.delete(email)
        db.session.commit()
        return jsonify({'message': 'Email removed successfully'}),200
    else:
        return jsonify({'error':'Email not found'}),404

#########################################################################################################
###################################User Management#######################################################
#########################################################################################################
#crm/user
#crm/user [POST]
#crm/user [PUT]
#crm/user [DELETE]
@crm_bp.route('/user')
def show_users():
    users = User.query.all()
    # user_data =[]
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    # user_data = {user.username: {'role': user.role,'company_id': user.company_id,'password': user.password,'company_id': user.company_id,'company_name': user.company_name,'team': user.team} for user in users}
    if 'role' in session and session['role']=='member':
        return jsonify({'message': 'lêu lêu'})
    else:
        if session['role'] == "admin":
            user_data = [{'username':user.username ,'role': user.role,'company_id': user.company_id,'password': user.password,'company_id': user.company_id,'company_name': user.company_name,'team': user.team} for user in users]
        if session['role'] == "leader":
            user_data = [{'username':user.username ,'role': user.role,'company_id': user.company_id,'password': user.password,'company_id': user.company_id,'company_name': user.company_name,'team': user.team} for user in users if user.role == 'member' or user.username == session['username']]

        try:
            data = request.args
            page = int(data.get('page',1))
            per_page = int(data.get('per_page',10))
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            paginated_data = user_data[start_index:end_index]
            return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(user_data)})
        except TypeError:
            return jsonify({'items':user_data,'page':1,'per_page':len(user_data), 'total_items':len(user_data)})
@crm_bp.route('/user_list')
def get_all_user():
    users = User.query.all()
    user_names = [user.username for user in users]
    return user_names
#Add user, not register
@crm_bp.route('/user', methods=['POST'])
def add_user():
    if 'role' in session and session['role'] in ['admin','leader']:
        # users  =  get_users()
        if not request.form:
            return jsonify({"error": "Missing JSON in request"}), 400
        data = request.form
        username = data.get('username')
        password = data.get('password')
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
            return jsonify({'message':"User added successfully!"})
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if an error occurs
            return str(e)
    else:
        return jsonify({"error": "unauthenticated"}),401
@crm_bp.route('/user/<string:username>', methods = ['PUT','OPTIONS'])
def edit_user(username):
    if 'role' in session and session['role'] in ['admin','leader']:
        user = User.query.get(username)
        if user:
            data = request.form
            new_password = data.get('password')
            if new_password:
                user.password = new_password
            new_company_name = data.get('company_name')
            if new_company_name:
                user.company_name = new_company_name
            new_company_id = data.get('company_id')
            if new_company_id:
                user.company_id = new_company_id
            new_role = data.get('role')
            if new_role:
                user.role = new_role
            new_team = data.get('team')
            if new_team:
                user.team = new_team
        
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
    working_sessions = Session_Mgt.query.order_by(Session_Mgt.checkin_time.desc()).all()
    working_session_data = [{'username': working_session.username,'login_ip':working_session.login_ip,'checkin_time':working_session.checkin_time,'checkout_time': working_session.checkout_time} for working_session in working_sessions]
    data = request.args
    username = data.get('username')
    if username == None:
        try:
            
            page = data.get('page', type= int)
            per_page = data.get('per_page',type = int)
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            paginated_data = working_session_data[start_index:end_index]
            return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(working_session_data)})
        except TypeError:
            return jsonify({'items':working_session_data,'page':1,'per_page':len(working_session_data), 'total_items':len(working_session_data)})
    else:
        try:
            
            page = data.get('page', type= int)
            per_page = data.get('per_page',type = int)
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            
            data_for_user = [i for i in working_session_data if i['username'] == username]
            paginated_data = data_for_user[start_index:end_index]
            return jsonify({'items':paginated_data,'page':page,'per_page':per_page, 'total_items':len(data_for_user)})
        except TypeError:
            return jsonify({'items':working_session_data,'page':1,'per_page':len(working_session_data), 'total_items':len(working_session_data)})