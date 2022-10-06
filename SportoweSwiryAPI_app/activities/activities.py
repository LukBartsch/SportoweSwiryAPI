from flask import jsonify
from SportoweSwiryAPI_app.models import User, Activities, ActivitySchema
from SportoweSwiryAPI_app.utilities import get_schema_args, apply_order, apply_filter,get_pagination, token_required
from SportoweSwiryAPI_app.activities import activities_bp

@activities_bp.route('/activities', methods=['GET'])
@token_required
def get_activities(user_id: str):

    user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')
    
    query = Activities.query.filter(Activities.userName==user_id)

    schema_args = get_schema_args(Activities)
    query = apply_order(Activities, query)
    query = apply_filter(Activities, query)
    items, pagination = get_pagination(query, 'activities.get_activities')
    activities=ActivitySchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': activities,
        'number_of_records': len(activities),
        'pagination': pagination
    })