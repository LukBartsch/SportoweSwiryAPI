from flask import jsonify
from webargs.flaskparser import use_args
import datetime as dt

from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import Activities, ActivitySchema, Sport, SportSchema, User, SelectUserSchema, activity_schema
from SportoweSwiryAPI_app.utilities import get_schema_args, apply_order, apply_filter,get_pagination, token_required, validate_json_content_type
from SportoweSwiryAPI_app.activities import activities_bp

@activities_bp.route('/activities', methods=['GET'])
@token_required
def get_activities(user_id: str):

    query = Activities.query.filter(Activities.user_id==user_id)
    schema_args = get_schema_args(Activities)
    query = apply_order(Activities, query)
    query = apply_filter(Activities, query)
    items, pagination = get_pagination(query, 'activities.get_activities')
    activities=ActivitySchema(**schema_args).dump(items)

    for activity in activities:
        activity['time'] = str(dt.timedelta(seconds = activity['time']))
        activity['activity_name'] = Sport.give_sport_name(activity['activity_type_id'])

    return jsonify({
        'success': True,
        'data': activities,
        'number_of_records': len(activities),
        'pagination': pagination
    })

@activities_bp.route('/activities/types', methods=['GET'])
@token_required
def get_types_of_activities(user_id: str):
	
    query = Sport.query
    schema_args = get_schema_args(Sport)
    query = apply_order(Sport, query)
    query = apply_filter(Sport, query)
    items, pagination = get_pagination(query, 'activities.get_types_of_activities')

    types_of_activities = SportSchema(**schema_args).dump(items)

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
        time=(dt.datetime.strptime(str(args['time']), '%H:%M:%S'))
        time_in_seconds = (time.hour * 60 + time.minute) * 60 + time.second
    except:
        time=dt.time()
        time_in_seconds = (time.hour * 60 + time.minute) * 60 + time.second

    new_activity=Activities(user_id=user_id, activity_type_id = Sport.give_sport_id(args['activity_name']), 
                    date=args['date'], distance=args['distance'], time=time_in_seconds)

    db.session.add(new_activity)
    db.session.commit()

    schema_args = {'many': False}
    activity=ActivitySchema(**schema_args).dump(new_activity)
    activity['time'] = str(dt.timedelta(seconds = activity['time']))
    activity['activity_name'] = args['activity_name']

    return jsonify({
        'success': True,
        'data': activity,
    }), 201


@activities_bp.route('/activities/<int:activity_id>', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(activity_schema, error_status_code=400)
def update_activity(user_id: str, args: dict, activity_id: int):

    activity = Activities.query.get_or_404(activity_id, description=f'Activity with id {activity_id} not found')

    try:
        time=(dt.datetime.strptime(str(args['time']), '%H:%M:%S'))
        time_in_seconds = (time.hour * 60 + time.minute) * 60 + time.second
    except:
        time=dt.time()
        time_in_seconds = (time.hour * 60 + time.minute) * 60 + time.second

    activity.activity_type_id = Sport.give_sport_id(args['activity_name'])
    activity.date=args['date']
    activity.distance=args['distance']
    activity.time=time_in_seconds

    db.session.commit()

    schema_args = {'many': False}
    activity=ActivitySchema(**schema_args).dump(activity)
    activity['time'] = str(dt.timedelta(seconds = activity['time']))
    activity['activity_name'] = args['activity_name']

    return jsonify({
        'success': True,
        'data': activity,
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



@activities_bp.route('/user_activities', methods=['POST'])
@token_required
@validate_json_content_type
@use_args(SelectUserSchema(only=['id', 'name', 'last_name']), error_status_code=400)
def get_user_activities(user_id: str, args: dict):

    selected_user_id = args['id']
    user=User.query.get_or_404(selected_user_id, description=f'User with id (username): {selected_user_id}  not found')

    query = Activities.query.filter(Activities.user_id==selected_user_id)
    schema_args = get_schema_args(Activities)
    query = apply_order(Activities, query)
    query = apply_filter(Activities, query)
    items, pagination = get_pagination(query, 'activities.get_user_activities')
    activities=ActivitySchema(**schema_args).dump(items)

    for activity in activities:
        activity['time'] = str(dt.timedelta(seconds = activity['time']))
        activity['activity_name'] = Sport.give_sport_name(activity['activity_type_id'])

    return jsonify({
        'success': True,
        'data': activities,
        'number_of_records': len(activities),
        'pagination': pagination
    })