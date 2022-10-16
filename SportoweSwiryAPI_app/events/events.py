from flask import jsonify, abort
from webargs.flaskparser import use_args

from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import User, Event, Participation, EventSchema, event_status_schema
from SportoweSwiryAPI_app.utilities import get_schema_args, apply_order, apply_filter,get_pagination, token_required, validate_json_content_type
from SportoweSwiryAPI_app.events import events_bp

@events_bp.route('/events', methods=['GET'])
@token_required
def get_my_events(user_id: str):

    query = User.all_events(user_id)
    schema_args = get_schema_args(Event)
    query = apply_order(Event, query)
    query = apply_filter(Event, query)
    items, pagination = get_pagination(query, 'events.get_my_events')
    events=EventSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': events,
        'number_of_records': len(events),
        'pagination': pagination
    })


@events_bp.route('/all_events', methods=['GET'])
@token_required
def get_all_events(user_id: str):

    query = Event.query
    schema_args = get_schema_args(Event)
    query = apply_order(Event, query)
    query = apply_filter(Event, query)
    items, pagination = get_pagination(query, 'events.get_all_events')
    events=EventSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': events,
        'number_of_records': len(events),
        'pagination': pagination
    })


@events_bp.route('/available_events', methods=['GET'])
@token_required
def get_available_events(user_id: str):

    query = Event.query.filter(Event.status == "Zapisy otwarte")
    schema_args = get_schema_args(Event)
    query = apply_order(Event, query)
    query = apply_filter(Event, query)
    items, pagination = get_pagination(query, 'events.get_available_events')
    events=EventSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': events,
        'number_of_records': len(events),
        'pagination': pagination
    })


@events_bp.route("/join_event/<int:event_id>")
@token_required
def join_event(user_id: str, event_id: int):

    event = Event.query.get_or_404(event_id, description=f'Event with id {event_id} not found')

    if event.status == "Zapisy otwarte":
        is_participating = Participation.query.filter(Participation.user_id == user_id).filter(Participation.event_id == event_id).first()
        if is_participating == None:
            participation = Participation(user_id = user_id, event_id = event_id)
            db.session.add(participation)
            db.session.commit()
        else:
            abort(409, description=f'You are already signed up for this event ({event.name}).')
    else:
        abort(403, description=f'Joining for this event ({event.name}) is currently unavailable.')

    return jsonify({
        'success': True,
        'data': f'Congratulations. You signed up for event: {event.name}'
    })


@events_bp.route("/leave_event/<int:event_id>")
@token_required
def leave_event(user_id: str, event_id: int):

    event = Event.query.get_or_404(event_id, description=f'Event with id {event_id} not found')

    is_participating = Participation.query.filter(Participation.user_id == user_id).filter(Participation.event_id == event_id).first()
    if is_participating != None and event.status == "Zapisy otwarte":
        participation = Participation.query.filter(Participation.event_id==event_id).filter(Participation.user_id == user_id).first()
        db.session.delete(participation)
        db.session.commit()

    elif is_participating != None and event.status != "Zapisy otwarte":
        abort(403, description=f'It is no longer possible to leave an event ({event.name}) at this time.')
    elif is_participating == None:
        abort(409, description=f'You are not participating in this event ({event.name}).')

    return jsonify({
        'success': True,
        'data': f'You have been signed out of the event ({event.name})'
    })

@events_bp.route("/change_event_status", methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(event_status_schema, error_status_code=400)
def change_event_status(user_id: str, args: dict):

    event_id = Event.give_event_id(args['name'])
    event = Event.query.get_or_404(event_id, description=f'Event with id {event_id} not found')

    event.status = args['status']
    db.session.commit()

    return jsonify({
        'success': True,
        'data': f'The status of the event ({event.name}) has been set to: {event.status}'
    })
