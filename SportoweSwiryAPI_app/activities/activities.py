from flask import jsonify
from webargs.flaskparser import use_args
import datetime
from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import User, Activities, ActivitySchema, CoefficientsList, CoefficientsListSchema, Event, EventSchema, Participation, activity_schema
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

    try:  
        time=datetime.datetime.strptime(str(args['time']), '%H:%M:%S')
    except:
        time=datetime.time()

    new_activity=Activities(date=args['date'], activity=args['activity'], distance=args['distance'], 
                        time=time, userName=user_id)

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': activity_schema.dump(new_activity),
    }), 201


@activities_bp.route('/activities/<int:activity_id>', methods=['DELETE'])
@token_required
def delete_activity(user_id: int, activity_id: int):
    activity = Activities.query.get_or_404(activity_id, description=f'Activity with id {activity_id} not found')

    db.session.delete(activity)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'Activity with id {activity_id} has been deleted'
    })


@activities_bp.route('/events', methods=['GET'])
@token_required
def get_my_events(user_id: str):


    participations = Participation.query.filter(Participation.user_name==user_id).all()

    
    query = Event.query
    schema_args = get_schema_args(Event)
    query = apply_order(Event, query)
    query = apply_filter(Event, query)
    items, pagination = get_pagination(query, 'activities.get_my_events')
    events=EventSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': events,
        'number_of_records': len(events),
        'pagination': pagination
    })