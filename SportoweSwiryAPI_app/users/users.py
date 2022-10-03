from flask import jsonify, abort
from webargs.flaskparser import use_args
from SportoweSwiryAPI_app import db
from SportoweSwiryAPI_app.models import User, UserSchema, user_schema, update_password_user_schema
from SportoweSwiryAPI_app.utilities import validate_json_content_type, get_schema_args, apply_order, apply_filter, get_pagination, token_required
from SportoweSwiryAPI_app.users import users_bp

@users_bp.route('/users', methods=['GET'])
def getUsers():
    
    query = User.query
    schema_args = get_schema_args(User)
    query = apply_order(User, query)
    query = apply_filter(User, query)
    items, pagination = get_pagination(query, 'users.getUsers')
    users=UserSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': users,
        'number_of_records': len(users),
        'pagination': pagination
    })

@users_bp.route('/users/admins', methods=['GET'])
def getAdmins():
    admins=User.query.filter(User.isAdmin == True).all()
    admins_schema=UserSchema(many=True)

    return jsonify({
        'success': True,
        'data': admins_schema.dump(admins),
        'number_of_records': len(admins)
    })

@users_bp.route('/users/<string:author_id>', methods=['GET'])
def getSingleUser(user_id: str):
    user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@users_bp.route('/users', methods=['POST'])
@validate_json_content_type
@use_args(user_schema, error_status_code=400)
def createUser(args: dict):
    if User.query.filter(User.mail == args['mail']).first():
        abort(409, description=f'User with email {args["mail"]} already exist')

    new_id=User.generate_ID(args['name'], args['lastName'])
    newUser=User(id=new_id, name=args['name'], lastName=args['lastName'], mail=args['mail'], 
                password=args['password'])

    newUser.id = newUser.removeAccents()
    newUser.password=newUser.hash_password()

    db.session.add(newUser)
    db.session.commit()

    token = newUser.generate_jwt()

    return jsonify({
        'success': True,
        'data': user_schema.dump(newUser),
        'token': token
    }), 201
    

@users_bp.route('/login', methods=['POST'])
@validate_json_content_type
@use_args(UserSchema(only=['mail', 'password']), error_status_code=400)
def loginUser(args: dict):
    user=User.query.filter(User.mail == args['mail']).first()
    if not user:
        abort(401, description=f'Invalid credentials')

    if not User.verify_password(user.password, args['password']):
        abort(401, description=f'Invalid credentials')

    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'name': user.name,
        'last_name': user.lastName,
        'mail': user.mail,
        'token': token
    }), 201

@users_bp.route('/me', methods=['GET'])
@token_required
def getCurrentUser(user_id: str):
    user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')

    return jsonify({
        'success': True,
        'name': user.name,
        'last_name': user.lastName,
        'mail': user.mail,
    })


@users_bp.route('/update/password', methods=['PUT'])
@token_required
@validate_json_content_type
@use_args(update_password_user_schema, error_status_code=400)
def updatePassword(user_id: str, args: dict):
    user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')

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
@use_args(UserSchema(only=['name', 'lastName', 'mail']), error_status_code=400)
def updateUserData(user_id: str, args: dict):
    if User.query.filter(User.mail == args['mail']).first():
        abort(409, description=f'User with email {args["mail"]} already exist')

    user=User.query.get_or_404(user_id, description=f'Author with id (username): {user_id}  not found')

    user.name=args['name']
    user.lastName=args['lastName']
    user.mail=args['mail']
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })
