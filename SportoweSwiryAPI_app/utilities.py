import jwt

from flask import request, url_for, current_app, abort
from flask_sqlalchemy import DefaultMeta, BaseQuery
from typing import Tuple
from werkzeug.exceptions import UnsupportedMediaType
from functools import wraps

def validate_json_content_type(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)
        if data is None:
            raise UnsupportedMediaType('Content type must be application/json')
        return func(*args, **kwargs)
    return wrapper

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        auth = request.headers.get('Authorization')
        if auth:
            token = auth.split(' ')[1]
        if token is None:
            abort(401, description=f'Missing token. Please login to get new token')

        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            abort(401, description=f'Expired token. Please login or register')
        except jwt.InvalidTokenError:
            abort(401, description=f'Invalid. Please login or register')
        else:
            return func(payload['user_id'], *args, **kwargs)
    return wrapper

def get_schema_args(model: DefaultMeta) -> dict:
    schema_args = {'many': True}
    fields = request.args.get('fields')
    if fields:
        schema_args['only'] = [field for field in fields.split(',') if field in model.__table__.columns]
    return schema_args

def apply_order(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    sort_keys = request.args.get('sort')
    if sort_keys:
        for key in sort_keys.split(','):
            descending = False
            if key.startswith('-'):
                key = key[1:]
                descending = True
            column_attribute = getattr(model, key, None)
            if column_attribute is not None:
                query = query.order_by(column_attribute.desc()) if descending else query.order_by(column_attribute)
    return query

def apply_filter(model: DefaultMeta, query: BaseQuery) -> BaseQuery:
    for param, value in request.args.items():
        if param not in {'fields', 'sort', 'page', 'limit'}:
            column_attribute = getattr(model, param, None)
            if column_attribute is not None:
                query = query.filter(column_attribute == value)
    return query

def filter_user_events(model_participation: DefaultMeta, model_event: DefaultMeta, query: BaseQuery, user_id: str) -> BaseQuery:
    participations = model_participation.query.filter(model_participation.user_name==user_id).all()
    for participation in participations:
        query = query.filter(model_event.id == participation.event_id)
    return query

def get_pagination(query: BaseQuery, func_name: str) -> Tuple[list, dict]:
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config.get('PER_PAGE', 5), type=int)
    params = {key: value for key, value in request.args.items() if key != 'page'}
    pagination_object = query.paginate(page, limit, False)
    pagination = {
        'total_pages': pagination_object.pages,
        'total_records': pagination_object.total,
        'current_page': url_for(func_name, page=page, **params),
        'current_page (number)': pagination_object.page
    }
    if pagination_object.has_next:
        pagination['next_page'] = url_for(func_name, page=page+1, **params)
    if pagination_object.has_prev:
        pagination['previous_page'] = url_for(func_name, page=page-1, **params)
    
    return pagination_object.items, pagination