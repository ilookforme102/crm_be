from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date,Time,DateTime , and_, func, case
import datetime
from datetime import datetime, timedelta
from db_schema import Customers
crm_stats = Blueprint('crm_stats', __name__, url_prefix='/crm/stats')
######################################################################################################
########################################Reports#######################################################
######################################################################################################
#Total number of contacted customer (number of rows in the database)
#Total number of customers who have deposited into their betting account (depositors) : Number
#Conversion rate (depositos/customers) of SEO data and Non-SEO data : Number
@crm_stats.route('/metrics/key_metrics', methods = ['POST','OPTIONS'])
def key_metrics():
    data = request.form
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    query = Customers.query
    query = query.filter(and_(
        Customers.filled_date >= datetime.strptime(start_date, '%Y-%m-%d'),
        Customers.filled_date <= datetime.strptime(end_date, '%Y-%m-%d')
    ))
    customers = query.count()
    seo_customers = query.filter(Customers.category == 'SEO Data').count()
    crm_customers  = query.filter(Customers.category != 'SEO Data').count()
    seo_depositors = query.filter(Customers.interaction_result == ['Khách SEO Nạp Tiền']).count()
    crm_depositors = query.filter(Customers.interaction_result == ['Khách CRM Nạp Tiền']).count()
    depositors = query.filter(Customers.interaction_result.in_(['Khách SEO Nạp Tiền','Khách CRM Nạp Tiền'])).count()
    conversion_rate =  100*depositors/customers
    seo_conversion_rate =  100*seo_depositors/seo_customers
    crm_conversion_rate =  100*crm_depositors/crm_customers
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
#crm/stats/charts
#Time serrie data for total customers 
#Heatmap data for category data and its result
#Time serries data for total number of customers for each CRM team member
#Detail of customers by result category for each CRM team 
#Total depositors for each CRM team member
#Time Serrie data for total depositors comparison between CRM customers and SEO customers
@crm_stats.route('/charts/customers_per_member')
def get_customer_per_member():
    data = request.args
    start_date = data.get('start_date')
    end_date = data.get('end_date')
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
            results  = results1.filter(and_(
                Customers.person_in_charge == pic,
                Customers.filled_date >= start_date,
                Customers.filled_date <= end_date
            )).all()
            data = [
                {
                    'date': result.date.isoformat() if result.date else None,
                    'customer_by_date': result.customer_by_date,
                    'person_in_charge': result.person_in_charge,
                } for result in results
            ]

            return jsonify(data)
        if pic == 'all':
            results  = results1.filter(and_(
                Customers.filled_date >= start_date,
                Customers.filled_date <= end_date
            )).all()
            data = [
                {
                    'date': result.date.isoformat() if result.date else None,
                    'customer_by_date': result.customer_by_date,
                    'person_in_charge': result.person_in_charge,
                } for result in results
            ]

            return jsonify(data)
    else:
        results  = results1.filter(and_(
            Customers.filled_date >= start_date,
            Customers.filled_date <= end_date
        )).all()
        data = [
            {
                'date': result.date.isoformat() if result.date else None,
                'customer_by_date': result.customer_by_date,
                'person_in_charge': result.person_in_charge,
            } for result in results
        ]

        return jsonify(data)
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
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    query = Customers.query
    results = query.with_entities(
        func.count(Customers.code).label('Depositor'),
        Customers.person_in_charge,
    ).filter(and_(
        Customers.interaction_result.in_(['Khách SEO Nạp Tiền','Khách CRM Nạp Tiền']),
        Customers.filled_date >= start_date,
        Customers.filled_date <= end_date
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
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    query = Customers.query
    results = query.with_entities(
        case(
            (Customers.category == 'SEO Data', 'SEO Data')
        , else_='CRM Data').label('new_category'),
        Customers.interaction_result,
        func.count(Customers.interaction_result).label('result_count')
    ).filter(and_(
        Customers.filled_date >= start_date,
        Customers.filled_date <= end_date
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
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    query = Customers.query
    results = query.with_entities(
        Customers.person_in_charge,
        Customers.interaction_result,
        func.count(Customers.code).label('result_count')
    ).filter(
        and_(
            Customers.filled_date <= end_date,
            Customers.filled_date >= start_date
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
@crm_stats.route('/test')
def show_dashboard():
    return {'message':'helloworld'}