from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from sqlalchemy.sql.expression import literal

from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy.sql import select

from sqlalchemy import Date,Time,DateTime , and_, func, case,distinct, text
import datetime
from datetime import datetime, timedelta
from models.db_schema import Customers,Category
from models.db_schema import app, db
crm_stats = Blueprint('crm_stats', __name__, url_prefix='/crm/stats')
######################################################################################################
########################################Reports#######################################################
######################################################################################################
#Total number of contacted customer (number of rows in the database)
#Total number of customers who have deposited into their betting account (depositors) : Number
#Conversion rate (depositos/customers) of SEO data and Non-SEO data : 

@crm_stats.route('/metrics/key_metrics')
def key_metrics():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    if start_date and end_date:
        query = query.filter(and_(
            func.date(Customers.filled_date) >= datetime.strptime(start_date, '%Y-%m-%d'),
            func.date(Customers.filled_date) <= datetime.strptime(end_date, '%Y-%m-%d')
        ))
    customers = query.count()
    seo_customers = query.filter(Customers.category == 'SEO Data').count()
    crm_customers  = query.filter(Customers.category != 'SEO Data').count()
    seo_depositors = query.filter(Customers.interaction_result == ['Khách SEO Tự Nạp Tiền']).count()
    crm_depositors = query.filter(Customers.interaction_result == ['Khách CRM Nạp Tiền']).count()
    depositors = query.filter(Customers.interaction_result.in_(['Khách SEO Tự Nạp Tiền','Khách CRM Nạp Tiền'])).count()
    try:
        conversion_rate =  100*depositors/customers
    except ZeroDivisionError:
        conversion_rate = 0
    try:
        seo_conversion_rate =  100*seo_depositors/seo_customers
    except ZeroDivisionError:
        seo_conversion_rate = 0
    try:
        crm_conversion_rate =  100*crm_depositors/crm_customers
    except ZeroDivisionError:
        crm_conversion_rate = 0 
    # return {
    #         'customers':customers,
    #         'conversion_rate':conversion_rate,
    #         'customers': seo_customers,
    #         'conversion_rate':seo_conversion_rate,

    #     }
    return jsonify({
        'vn168':{
            'customers':customers,
            'depositor':depositors,
            'conversion_rate':conversion_rate
        },
        'seo':{
            'customers': seo_customers,
            'depositor':seo_depositors,
            'conversion_rate':seo_conversion_rate
        },
        'crm': {
            'customers': crm_customers,
            'depositor':crm_depositors,
            'conversion_rate': crm_conversion_rate
        }
    })
###############################################
#The pie chart to see the ingredient of depositor with 2 class: Khach SEO Tu Nap Tien and Khach CRM Nap Tien
def calculate_percentage(data):
    # Calculate the total count
    total_count = sum(item['count'] for item in data)
    
    # Calculate the percentage for each category
    percentages = [
        {'category': item['category'], 'percentage': (item['count'] / total_count) * 100}
        for item in data
    ]
    
    return percentages

@crm_stats.route('/charts/depositor_result')
def get_depositor_result():
    data  =  request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    results =  query.with_entities(
        Customers.interaction_result,
        func.count(Customers.interaction_result).label('count')
        ).filter(and_(
            Customers.interaction_result.in_(['Khách SEO Tự Nạp Tiền','Khách CRM Nạp Tiền']),
           func.date(Customers.filled_date) >= start_date,
            func.date(Customers.filled_date) <= end_date)).group_by(
            Customers.interaction_result
        ).all()
    result_dict = [{'category': result.interaction_result,'count': result.count} for result in results]
    percentages = calculate_percentage(result_dict)
    return jsonify(percentages)#jsonify([{'value': result.count} for result in results])
#/charts/customers_per_member
#Time serrie data for total customers 
#Heatmap data for category data and its result
#Time serries data for total number of customers for each CRM team member
#Detail of customers by result category for each CRM team 
#Total depositors for each CRM team member
#Time Serrie data for total depositors comparison between CRM customers and SEO customers
@crm_stats.route('/charts/customers_per_member')
def get_customer_per_member():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    pic = data.get('person_in_charge')
    query = Customers.query
    results1 = query.with_entities(
        func.date(Customers.filled_date).label('date'),
        func.count(func.date(Customers.filled_date)).label('customer_by_date'),
        Customers.person_in_charge,
    ).group_by(
        func.date(Customers.filled_date),
        Customers.person_in_charge,
    )
    if pic: # and Customers.query.filter(Customers.person_in_charge == pic):
        if pic != 'all':
            list_pic = [i for i in pic.split(',')] if pic else None
            if list_pic:
                results  = results1.filter(and_(
                    func.date(Customers.filled_date)>= start_date,
                    func.date(Customers.filled_date) <= end_date,
                    Customers.person_in_charge.in_(list_pic)
                )).all()
            else:
                results  = results1.filter(and_(
                    func.date(Customers.filled_date)>= start_date,
                    func.date(Customers.filled_date) <= end_date
                )).all()
            data = [
                {
                    'date': result.date.isoformat() if result.date else None,
                    'customer_by_date': result.customer_by_date,
                    'person_in_charge': result.person_in_charge,
                } for result in results
            ]
            grouped_data = {}
            for entry in data:
                person_in_charge = entry["person_in_charge"].lower()
                if person_in_charge not in grouped_data:
                    grouped_data[person_in_charge] = []
                grouped_data[person_in_charge].append({
                    "customer_by_date": entry["customer_by_date"],
                    "date": entry["date"]
                })

            return jsonify(grouped_data )

        if pic == 'all':
            results  = results1.filter(and_(
                func.date(Customers.filled_date) >= start_date,
                func.date(Customers.filled_date) <= end_date
            )).all()
            data = [
                {
                    'date': result.date.isoformat() if result.date else None,
                    'customer_by_date': result.customer_by_date,
                    'person_in_charge': result.person_in_charge,
                } for result in results
            ]
            grouped_data = {}
            for entry in data:
                person_in_charge = entry["person_in_charge"].lower()
                if person_in_charge not in grouped_data:
                    grouped_data[person_in_charge] = []
                grouped_data[person_in_charge].append({
                    "customer_by_date": entry["customer_by_date"],
                    "date": entry["date"]
                })

            return jsonify(grouped_data )
    else:
        results  = results1.filter(and_(
            func.date(Customers.filled_date) >= start_date,
            func.date(Customers.filled_date) <= end_date
        )).all()
        data = [
            {
                'date': result.date.isoformat() if result.date else None,
                'customer_by_date': result.customer_by_date,
                'person_in_charge': result.person_in_charge,
            } for result in results
        ]

        grouped_data = {}
        for entry in data:
            person_in_charge = entry["person_in_charge"].lower()
            if person_in_charge not in grouped_data:
                grouped_data[person_in_charge] = []
            grouped_data[person_in_charge].append({
                "customer_by_date": entry["customer_by_date"],
                "date": entry["date"]
            })

        return jsonify(grouped_data )
# def get_customer_per_member():
#     data = request.args
#     start_date = data.get('start_date',"2020-01-01")
#     end_date_default = datetime.now().strftime('%Y-%m-%d')
#     end_date = data.get('end_date',end_date_default)
#     pic = data.get('person_in_charge')
#     query = Customers.query
#     results1 = query.with_entities(
#         func.date(Customers.filled_date).label('date'),
#         func.count(func.date(Customers.filled_date)).label('customer_by_date'),
#         Customers.person_in_charge,
#     ).group_by(
#         func.date(Customers.filled_date),
#         Customers.person_in_charge,
#     )
#     if pic: # and Customers.query.filter(Customers.person_in_charge == pic):
#         if pic != 'all':
#             results  = results1.filter(and_(
#                 Customers.person_in_charge == pic,
#                 Customers.filled_date >= start_date,
#                 Customers.filled_date <= end_date
#             )).all()
#             data = [
#                 {
#                     'date': result.date.isoformat() if result.date else None,
#                     'customer_by_date': result.customer_by_date,
#                     'person_in_charge': result.person_in_charge,
#                 } for result in results
#             ]
#             grouped_data = {}
#             for entry in data:
#                 person_in_charge = entry["person_in_charge"].lower()
#                 if person_in_charge not in grouped_data:
#                     grouped_data[person_in_charge] = []
#                 grouped_data[person_in_charge].append({
#                     "customer_by_date": entry["customer_by_date"],
#                     "date": entry["date"]
#                 })

#             return jsonify(grouped_data )
#         if pic == 'all':
#             results  = results1.filter(and_(
#                 Customers.filled_date >= start_date,
#                 Customers.filled_date <= end_date
#             )).all()
#             data = [
#                 {
#                     'date': result.date.isoformat() if result.date else None,
#                     'customer_by_date': result.customer_by_date,
#                     'person_in_charge': result.person_in_charge,
#                 } for result in results
#             ]
#             grouped_data = {}
#             for entry in data:
#                 person_in_charge = entry["person_in_charge"].lower()
#                 if person_in_charge not in grouped_data:
#                     grouped_data[person_in_charge] = []
#                 grouped_data[person_in_charge].append({
#                     "customer_by_date": entry["customer_by_date"],
#                     "date": entry["date"]
#                 })

#             return jsonify(grouped_data )
#     else:
#         results  = results1.filter(and_(
#             Customers.filled_date >= start_date,
#             Customers.filled_date <= end_date
#         )).all()
#         data = [
#             {
#                 'date': result.date.isoformat() if result.date else None,
#                 'customer_by_date': result.customer_by_date,
#                 'person_in_charge': result.person_in_charge,
#             } for result in results
#         ]

#         grouped_data = {}
#         for entry in data:
#             person_in_charge = entry["person_in_charge"].lower()
#             if person_in_charge not in grouped_data:
#                 grouped_data[person_in_charge] = []
#             grouped_data[person_in_charge].append({
#                 "customer_by_date": entry["customer_by_date"],
#                 "date": entry["date"]
#             })

#         return jsonify(grouped_data )
@crm_stats.route('/charts/pic_time')
#SELECT COUNT(`code`),person_in_charge FROM `db_vn168_crm_customer` WHERE `interaction_result` 
#in ('Khách SEO Nạp Tiền','Khách CRM Nạp Tiền') 
#AND filled_date <= '2024-04-30' 
#AND filled_date >= '2024-04-20' 
#GROUP BY person_in_charge;

def get_depositor_each():
    # #data format :
    # # {
    # #"team A": {data for team A},
    # # "team B": {data for team B}
    # # }
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    results = query.with_entities(
        func.count(Customers.code).label('Depositor'),
        Customers.person_in_charge,
    ).filter(and_(
        Customers.interaction_result.in_(['Khách SEO Tự Nạp Tiền','Khách CRM Nạp Tiền']),
        func.date(Customers.filled_date) >= start_date,
        func.date(Customers.filled_date) <= end_date
                  )).group_by(
        Customers.person_in_charge).all()
    query_data = [
        {
            'pic': result.person_in_charge,
            'count':result.Depositor
        } for result in results
    ]
    return jsonify(query_data)
# SELECT 
# (CASE WHEN category = 'SEO Data' THEN 'SEO Data' ELSE 'CRM Data' END) 
# AS new_categor,interaction_result,COUNT(interaction_result) 
# FROM `db_vn168_crm_customer` 
# GROUP BY new_categor,interaction_result;
# The difference of behavious of customer from SEO and CRM data based on interaction result


@crm_stats.route('/charts/category_result')
def active_customer_for_category():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    results = query.with_entities(
        case(
            (Customers.category == 'SEO Data', 'SEO Data')
        , else_='CRM Data').label('new_category'),
        Customers.interaction_result,
        func.count(Customers.interaction_result).label('result_count')
    ).filter(and_(
        func.date(Customers.filled_date) >= start_date,
        func.date(Customers.filled_date) <= end_date
                  )).group_by(
        'new_category',
        Customers.interaction_result
    ).all()

    query_data = [
        {
            'new_category': result.new_category,
            'interaction_result': result.interaction_result,
            'customer_count': result.result_count
        } for result in results
    ]
    return query_data
###SELECT `person_in_charge`, interaction_result , COUNT(code) as result_count 
#FROM `db_vn168_crm_customer` 
#GROUP BY person_in_charge,interaction_result;

@crm_stats.route('/charts/customer_pic_result')
def get_customer_pic_result():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    results = query.with_entities(
        Customers.person_in_charge,
        Customers.interaction_result,
        func.count(Customers.code).label('result_count')
    ).filter(
        and_(
            func.date(Customers.filled_date) <= end_date,
            func.date(Customers.filled_date) >= start_date
        )
    ).group_by(
        Customers.person_in_charge,
        Customers.interaction_result
    ).all()
    query_data = [
        {
            'pic': result.person_in_charge,
            'interaction_result': result.interaction_result,
            'customer_count': result.result_count
        } for result in results
    ]
    return jsonify(query_data)
#SELECT DATE(`filled_date`) date, COUNT(*) customer FROM `db_vn168_crm_customer` GROUP BY DATE(`filled_date`);
@crm_stats.route('/charts/customer_date')
def get_customer_date():
    data  = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    query = Customers.query
    results = query.with_entities(
        func.date(Customers.filled_date).label('date'),
        func.count(Customers.filled_date).label('customer')

    ).filter(
        and_(
            func.date(Customers.filled_date) <= end_date,
            func.date(Customers.filled_date) >=  start_date
        )
    ).group_by(
        func.date(Customers.filled_date)
    ).all()
    query_data =[{'date': data.date.isoformat() , 'customer':data.customer } for data in results]
    return jsonify(query_data)
#SELECT person_in_charge, interaction_result result, COUNT(code) customer FROM `db_vn168_crm_customer` GROUP BY person_in_charge, interaction_result;
@crm_stats.route('/charts/pic_result_customer')
def get_pic_result():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    pic = data.get('person_in_charge', None)
    list_pic = [i for i in pic.split(',')] if pic else None

    query = Customers.query
    query = query.with_entities(
        Customers.person_in_charge.label('pic'),
        Customers.interaction_result.label('result'),
        func.count(Customers.code).label('total_customers')
    )
    if list_pic:
        query =  query.filter(
            and_(
                func.date(Customers.filled_date) <= end_date,
                func.date(Customers.filled_date) >=  start_date,
                Customers.person_in_charge.in_(list_pic)
            )
        )
    else:
        query =  query.filter(
            and_(
                func.date(Customers.filled_date) <= end_date,
                func.date(Customers.filled_date) >=  start_date,
            )
        )
    results = query.group_by(
        Customers.person_in_charge,
        Customers.interaction_result
    ).all()
    query_data =[{'pic': data.pic , 'result':data.result,'total customer': data.total_customers } for data in results]
    return jsonify(query_data)
####################################################
#####Satistics for category of customer records#####
####################################################
#SELECT DATE(filled_date), category, COUNT(category) FROM `db_vn168_crm_customer` GROUP BY DATE(filled_date), category;
@crm_stats.route('/charts/property_date_stats')
def get_property_date_stats():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    attr = data.get('property')
    query  = Customers.query
    results = query.with_entities(
        func.date(Customers.__dict__['filled_date']).label('date'),
        Customers.__dict__[attr].label('property'),
        func.count(Customers.__dict__[attr]).label('count')
    ).filter(
        and_(
            func.date(Customers.filled_date) <= end_date,
            func.date(Customers.filled_date) >= start_date,
        )
    ).group_by(
            func.date(Customers.filled_date),
            Customers.__dict__[attr]
        ).all()
    data = [{'date': result.date, attr: result.property, 'count': result.count} for result in results]    
    return data
##Aggregation stats for number of records group by category 1, categry 2
@crm_stats.route('/charts/sub_query')
def get_category_date_stats():
    data = request.args
    start_date = data.get('start_date',"2020-01-01")
    end_date_default = datetime.now().strftime('%Y-%m-%d')
    end_date = data.get('end_date',end_date_default)
    attr1 = data.get('attr1', None)
    attr2 = data.get('attr2', None)
    attr2_sub = data.get('attr2_sub', None)
    pic = data.get('person_in_charge', None)
    list_pic = [i for i in pic.split(',')] if pic else None
    query = Customers.query
    if list_pic:
        query  = query.with_entities(
            # func.date(Customers.__dict__['filled_date']).label('date'),
            Customers.__dict__[attr1].label('property'),
            Customers.__dict__[attr2].label('property2'),
            func.count(Customers.__dict__[attr1]).label('count')
        ).filter(
            and_(
                func.date(Customers.filled_date) <= end_date,
                func.date(Customers.filled_date) >= start_date,
                Customers.person_in_charge.in_(list_pic)
            ))
    else:
        query  = query.with_entities(
            # func.date(Customers.__dict__['filled_date']).label('date'),
            Customers.__dict__[attr1].label('property'),
            Customers.__dict__[attr2].label('property2'),
            func.count(Customers.__dict__[attr1]).label('count')
        ).filter(
            and_(
                Customers.filled_date <= end_date,
                Customers.filled_date >= start_date,
            ))
    if attr2 and attr2_sub:
        query = query.filter( Customers.__dict__[attr2] == attr2_sub)
    results =  query.group_by(
            # func.date(Customers.filled_date),
            Customers.__dict__[attr1],
            Customers.__dict__[attr2]
        ).all()
    data = [{ attr1: result.property,attr2: result.property2, 'count': result.count} for result in results]    
    return data
# SELECT c.date date, ca.category category,COUNT(cu.code) customer  FROM  (SELECT  DISTINCT(DATE(c.filled_date)) date FROM `db_vn168_crm_customer` c) c
# CROSS JOIN  `db_vn168_crm_category` ca
# LEFT JOIN `db_vn168_crm_customer` cu
# ON c.date = date( cu.filled_date) and cu.category = ca.category
# GROUp BY  c.date, ca.category
# ORDER BY c.date, ca.category;
@crm_stats.route('/charts/daily_tracking_category') # Bang theo do so lieu moi ngay category/date
def get_daily_customer():
    data = request.args
    first_day_this_month = datetime.now().replace(day =1).strftime('%Y-%m-%d')
    current_date = datetime.now()
    if current_date.month == 12:
        first_day_next_month = datetime(current_date.year + 1, 1,1)
    else:
        first_day_next_month = datetime(current_date.year, current_date.month +1,1)
    last_day_this_month = (first_day_next_month - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = data.get('start_date', first_day_this_month)
    end_date =  data.get('end_date', last_day_this_month)
    # cross_join_query = db.session.query(Category, DateTable).join(DateTable, isouter=True)
    sub_query = db.session.query(func.date(Customers.filled_date).label('date')).filter(
        and_(
            func.date(Customers.filled_date) >= start_date,
            func.date(Customers.filled_date) <= end_date
        )
    ).distinct().subquery()
    # sub_query2 = db.session.query (func.count(Category.category).label('count')).subquery()
    # cross_join_category_date = db.session.query(sub_query.c.date, Category.category).select_from(Category).join(sub_query, isouter=True).all()
    final_query = db.session.query(
        sub_query.c.date.label('date'),
        Category.category,
        func.count(Customers.code).label('customer')
    ).select_from(
        sub_query
        ).outerjoin(
            Category,literal(True)
        ).outerjoin(
            Customers,
            and_(
               func.date(Customers.filled_date) == sub_query.c.date,
                Customers.category == Category.category 
            )
        ).group_by(
            sub_query.c.date, Category.category
        )
    final_data = final_query.all()
    # test_query = db.session.query(sub_query2.c.count).select_from(sub_query2
    print(final_query.statement)
    data = [{'count':i.date,'category':i.category,'customer':i.customer} for i in    final_data ]
    return data
#Comparing number of SEO/CRM depositor monthly
@crm_stats.route('/charts/monthly_depositor_seo_vs_crm')
def get_monthly_depositor_crm_seo():
    # sql =  text(f'''
    # SELECT interaction_result, MONTH(filled_date),COUNT( MONTH(filled_date)) FROM `db_vn168_crm_customer`
    # WHERE interaction_result in ("Khách CRM Nạp Tiền", "Khách SEO Tự Nạp Tiền")
    # GROUP BY interaction_result,MONTH(filled_date);
    # ''')
    # results = db.session.execute(sql)
    # data = [{'value1': result[0]} for result in results]
    # return jsonify(data)
    results =  db.session.query(
        Customers.interaction_result.label('result'),
        func.date(Customers.filled_date).label('date'),
        func.count(func.date(Customers.filled_date)).label('number_depositor')
    ).filter(
        Customers.interaction_result.in_(["Khách CRM Nạp Tiền", "Khách SEO Tự Nạp Tiền"])
    ).group_by(
        Customers.interaction_result.label('result'),
        func.date(Customers.filled_date).label('date')
    ).all()
# query_data1 = [{'result':result.result, 'date':result.date.strftime('%Y-%m-%d') if result.date else 'N/A','number_depositor': result.number_depositor } for result in results if result.result == 'Khách CRM Nạp Tiền']
    # query_data2 = [{'result':result.result, 'date':result.date.strftime('%Y-%m-%d') if result.date else 'N/A','number_depositor': result.number_depositor } for result in results if result.result == 'Khách SEO Tự Nạp Tiền']
    
    query_data1 = [{'result':result.result, 'date':result.date.strftime('%Y-%m-%d') if result.date else 'N/A','number_depositor': result.number_depositor } for result in results if result.result == 'Khách CRM Nạp Tiền']
    query_data2 = [{'result':result.result, 'date':result.date.strftime('%Y-%m-%d') if result.date else 'N/A','number_depositor': result.number_depositor } for result in results if result.result == 'Khách SEO Tự Nạp Tiền']
    query_data = {'CRM': query_data1,'SEO': query_data2}
    return jsonify(query_data)
######################################
### tracking category/bo_code/date######
@crm_stats.route('/charts/flexattr')
def get_data():
    data = request.args
    condition = ''
    condition = data.get('category',None)
    if condition:
        condition_str = f'''where `db_vn168_crm_customer`.category = "{condition}"'''
    sql = text(f'''select ss.date, ss.bo,COUNT(cuu.code) customer from (select DISTINCT date(cu.filled_date) date, b.bo_code bo FROM `db_vn168_crm_customer` cu CROSS join `db_vn168_crm_bo` b ) ss left join (select * from `db_vn168_crm_customer` {condition_str})cuu ON cuu.bo_code = ss.bo and date(cuu.filled_date) = ss.date GROUP by ss.date, ss.bo order by ss.date, ss.bo;''')
    result = db.session.execute(sql)
    users = [{'date':row[0], 'bo_code': row[1], 'customer': row[2]} for row in result]
    return jsonify(users)

###############################################
###### tracking interaction_result/cateogry/date#########
@crm_stats.route('/charts/get_anything')
def get_dataa():
    data = request.args
    condition = ''
    condition = data.get('category',None)
    if condition:
        condition_str = f'''where `db_vn168_crm_customer`.category = "{condition}"'''
    sql = text(f'''select ss.date, ss.bo,COUNT(cuu.code) customer from (select DISTINCT date(cu.filled_date) date, b.bo_code bo FROM `db_vn168_crm_customer` cu CROSS join `db_vn168_crm_bo` b ) ss left join (select * from `db_vn168_crm_customer` {condition_str})cuu ON cuu.bo_code = ss.bo and date(cuu.filled_date) = ss.date GROUP by ss.date, ss.bo order by ss.date, ss.bo;''')
    result = db.session.execute(sql)
    users = [{'date':row[0], 'bo_code': row[1], 'customer': row[2]} for row in result]
    return jsonify(users)
@crm_stats.route('/charts/customer_pic_heatmap')
def get_customer_by_username():
    person_in_charge = session['username']
    data = request.args
    current_year = data.get('year',str(datetime.now().year) )
    results = db.session.query(
        Customers.person_in_charge.label('pic'),
        func.date(Customers.filled_date).label('date'),
        func.count(func.date(Customers.filled_date)).label('count')
    ).filter(
        and_(
            func.year(Customers.filled_date)== current_year,
            Customers.person_in_charge == person_in_charge
        )
    ).group_by(
        Customers.person_in_charge,
        func.date(Customers.filled_date)
    ).order_by(Customers.filled_date).all()
    data = [{'date': result.date.strftime('%Y-%m-%d'),'count':result.count} for result in results]
    return jsonify(data)
@crm_stats.route('/year_list')
def get_year():
    person_in_charge = session['username']
    results = db.session.query(
        func.year(Customers.filled_date).distinct().label('year')
    ).filter(
        Customers.person_in_charge == person_in_charge
    ).order_by(
        func.year(Customers.filled_date).desc()
    ).all()
    data = [result.year for result in results]
    return jsonify(data)
@crm_stats.route('/test')
def show_dashboard():
    return {'message':'helloworld'}