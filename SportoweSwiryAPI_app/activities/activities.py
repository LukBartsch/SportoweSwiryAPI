from flask import jsonify
from webargs.flaskparser import use_args
import datetime
from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import User, Activities, ActivitySchema, CoefficientsList, CoefficientsListSchema, activity_schema
from SportoweSwiryAPI_app.utilities import get_schema_args, apply_order, apply_filter,get_pagination, token_required, validate_json_content_type
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

@activities_bp.route('/activities/types', methods=['GET'])
@token_required
def get_types_of_activities(user_id: str):
	
    # user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')

    set_name = "Podstawowy zestaw współczynników"

    query = CoefficientsList.query.filter(CoefficientsList.setName==set_name)
    schema_args = get_schema_args(CoefficientsList)
    query = apply_order(CoefficientsList, query)
    query = apply_filter(CoefficientsList, query)
    items, pagination = get_pagination(query, 'activities.get_types_of_activities')

    types_of_activities = CoefficientsListSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': types_of_activities,
        'number_of_records': len(types_of_activities),
        'pagination': pagination
    })


@activities_bp.route('/activities', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(activity_schema, error_status_code=400)
def add_activity(user_id: str, args: dict):

        
    new_activity=Activities(date=args['date'], activity=args['activity'], distance=args['distance'], userName=user_id)

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': activity_schema.dump(new_activity),
    }), 201