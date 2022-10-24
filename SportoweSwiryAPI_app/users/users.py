from flask import jsonify, abort
from webargs.flaskparser import use_args
from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import User, UserSchema, LoginUserSchema, user_schema, update_password_user_schema
from SportoweSwiryAPI_app.utilities import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination, token_required, checking_admin
from SportoweSwiryAPI_app.users import users_bp

@users_bp.route('/users', methods=['GET'])
@token_required
@checking_admin
def get_users(user_id: str):
    
    query = User.query
    schema_args = get_schema_args(User)
    query = apply_order(User, query)
    query = apply_filter(User, query)
    items, pagination = get_pagination(query, 'users.get_users')
    users=UserSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': users,
        'number_of_records': len(users),
        'pagination': pagination
    })

@users_bp.route('/users/admins', methods=['GET'])
def get_admins():
    admins=User.query.filter(User.is_admin == True).all()
    admins_schema=UserSchema(many=True)

    return jsonify({
        'success': True,
        'data': admins_schema.dump(admins),
        'number_of_records': len(admins)
    })

@users_bp.route('/users/<string:user_id>', methods=['GET'])
def get_single_user(user_id: str):
    user=User.query.get_or_404(user_id, description=f'User with id (username): {user_id}  not found')

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@users_bp.route('/users', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def create_user(args: dict):
    if User.query.filter(User.mail == args['mail']).first():
        abort(409, description=f'User with email {args["mail"]} already exist')

    new_id=User.generate_ID(args['name'], args['last_name'])
    new_user=User(id=new_id, name=args['name'], last_name=args['last_name'], mail=args['mail'], 
                password=args['password'])

    new_user.id = new_user.remove_accents()
    new_user.password=new_user.hash_password()

    db.session.add(new_user)
    db.session.commit()

    token = new_user.generate_jwt()

    return jsonify({
        'success': True,
        'data': user_schema.dump(new_user),
        'token': token
    }), 201
    

@users_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(LoginUserSchema, error_status_code=400)
def login_user(args: dict):
    user=User.query.filter(User.mail == args['mail']).first()
    if not user:
        abort(401, description=f'Invalid credentials')

    if not User.verify_password(user.password, args['password']):
        abort(401, description=f'Invalid credentials')

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'name': user.name,
        'last_name': user.last_name,
        'mail': user.mail,
        'token': token
    }), 201

@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id: str):
    user=User.query.get_or_404(user_id, description=f'User with id (username): {user_id}  not found')

    return jsonify({
        'success': True,
        'name': user.name,
        'last_name': user.last_name,
        'mail': user.mail,
    })


@users_bp.route('/update/password', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(update_password_user_schema, error_status_code=400)
def update_password(user_id: str, args: dict):
    user=User.query.get_or_404(user_id, description=f'User with id (username): {user_id}  not found')

    if not User.verify_password(user.password, args['current_password']):
        abort(401, description=f'Invalid credentials')

    user.password=args['new_password']
    user.password=user.hash_password()
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@users_bp.route('/update/data', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(UserSchema(only=['name', 'last_name', 'mail']), error_status_code=400)
def update_user_data(user_id: str, args: dict):
    if User.query.filter(User.mail == args['mail']).first():
        abort(409, description=f'User with email {args["mail"]} already exist')

    user=User.query.get_or_404(user_id, description=f'User with id (username): {user_id}  not found')

    user.name=args['name']
    user.last_name=args['last_name']
    user.mail=args['mail']
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })
