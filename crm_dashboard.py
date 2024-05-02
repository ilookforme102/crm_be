from flask import Blueprint
crm_stats = Blueprint('crm_stats', __name__, url_prefix='/crm_stats')
@crm_stats.route('/test')
def show_dashboard():
    return {'message':'helloworld'}