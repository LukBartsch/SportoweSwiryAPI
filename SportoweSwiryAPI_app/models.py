import jwt

from flask import abort, current_app
from datetime import datetime, timedelta
from SportoweSwiryAPI_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
import hashlib
import binascii

class User(db.Model):
    __tableName__ = 'usersAPI'
    id = db.Column(db.String(50), unique=True, nullable=False , primary_key=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=True)
    is_added_by_google = db.Column(db.Boolean, default=False)
    is_added_by_fb = db.Column(db.Boolean, default=False)

    event_admin = db.relationship('Event', backref='admin', lazy='dynamic')
    events = db.relationship('Participation', backref='user', lazy='dynamic')
    activities = db.relationship('Activities', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.name} {self.last_name}'


    @staticmethod
    def generate_ID(name: str, last_name: str) -> str:

        sufix = 0

        id = name[0:3] + last_name[0:3] + str(sufix)
        user=User.query.filter(User.id == id).first()

        while user != None:
            sufix +=1
            print(sufix)
            id = name[0:3] + last_name[0:3] + str(sufix)
            user=User.query.filter(User.id == id).first()

        return id

    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        #os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii') 

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),
        salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def remove_accents(self):
        strange='ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
        ascii_replacements='UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
        translator=str.maketrans(strange,ascii_replacements)
        return self.id.translate(translator)

    def generate_jwt(self) -> str:
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(minutes=current_app.config.get('JWT_EXPIRED_MINUTES', 30))
        }
        return jwt.encode(payload, current_app.config.get('SECRET_KEY'))

    @staticmethod
    def all_events(user_id):
        participations = Participation.query.filter(Participation.user_id==user_id).all()
        user_events_ids=[]

        for participation in participations:
            user_events_ids.append(participation.event_id)

        user_events = Event.query.filter(Event.id.in_(user_events_ids))
        return user_events


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    last_name = fields.String(required=True, validate=validate.Length(max=50))
    mail = fields.String(required=True, validate=validate.Length(max=50))
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))
    is_admin = fields.Boolean(dump_default=False)
    confirmed = fields.Boolean(dump_default=True)
    is_added_by_google = fields.Boolean(dump_default=False)
    is_added_by_fb = fields.Boolean(dump_defaultt=False)


class LoginUserSchema(Schema):
    mail = fields.String(required=True, validate=validate.Length(max=50))
    password = fields.String(load_only=True, required=True, validate=validate.Length(max=500))


class UpdatePasswordUserSchema(Schema):
    current_password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))
    new_password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    default_coefficient = db.Column(db.Float, nullable = False, default = 0)
    default_is_constant = db.Column(db.Boolean, nullable = False, default = False)
    category = db.Column(db.String(50), nullable = False, default = 'Other')
    activities = db.relationship('Activities', backref='activity_type', lazy='dynamic')
    events = db.relationship('CoefficientsList', backref='sport', lazy='dynamic')

    @staticmethod
    def all_sports_list():
        sports = Sport.query.all()
        sport_types = [sport.name for sport in sports]
        return sport_types

    @staticmethod
    def give_sport_id(sport_name):
        sport = Sport.query.filter(Sport.name == sport_name).first()
        sport_id = sport.id
        return sport_id

    @staticmethod
    def give_sport_name(sport_id):
        sport = Sport.query.filter(Sport.id == sport_id).first()
        sport_name = sport.name
        return sport_name

class SportSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    default_coefficient = fields.Decimal(required=True)
    default_is_constant = fields.Boolean(required=True)
    category = fields.String(required=True)


class Activities(db.Model):
    __tableName__ = 'activitiesAPI'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    time = db.Column(db.Integer, nullable=False, default=0)
    strava_id = db.Column(db.BigInteger)


class ActivitySchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(dump_only=True)
    activity_type_id = fields.Integer(required=True)
    activity_name = fields.String(load_only=True)
    date = fields.Date('%d-%m-%Y', required=True)
    distance = fields.Decimal(required=True)
    time = fields.Integer()
    strava_id = fields.Integer()

    @validates('date')
    def validate_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f'Birth date must be lower than {datetime.now().date()}')


class ActivitySchemaAdd(ActivitySchema):
    activity_type_id = fields.Integer()
    activity_name = fields.String(required=True)
    time = fields.Time('%H:%M:%S')

    @validates('activity_name')
    def validate_activity_exist(self, value):
        available_activity_types = Sport.all_sports_list()
        if value not in available_activity_types:
            raise ValidationError(f'This type of activity ({value}) is not available in the application.')


class Event(db.Model):
    __tableName__ = 'eventsAPI'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start = db.Column(db.Date, nullable=False)
    length_weeks = db.Column(db.Integer,nullable=False)
    admin_id = db.Column(db.String(50), db.ForeignKey('user.id')) 
    status = db.Column(db.String(50), nullable=False)
    is_private = db.Column(db.Boolean, nullable=False)
    is_secret = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(50))
    max_user_amount = db.Column(db.Integer, nullable=False)

    participants = db.relationship('Participation', backref='event', lazy='dynamic')
    # distance_set = db.relationship('DistancesTable', backref='event', lazy='dynamic')
    coefficients_list = db.relationship('CoefficientsList', backref='event', lazy='dynamic')

    @staticmethod
    def give_event_id(event_name):
        event = Event.query.filter(Event.name == event_name).first()
        if event:
            event_id = event.id
        else:
            abort(404, description=f'Event ({event_name}) not found')
        return event_id

class Participation(db.Model):
    __tableName__ = 'participationAPI'
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)


class CoefficientsList(db.Model):
    __tableName__ = 'coefficients_list_API'
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('sport.id'), primary_key=True)
    value = db.Column(db.Float, nullable = False, default = 0)
    is_constant = db.Column(db.Boolean, nullable = False, default = False)


class EventSchema(Schema):
    id = fields.Integer(dumpl_only=True)
    name = fields.String(required=True)
    start = fields.Date('%d-%m-%Y', required=True)
    length_weeks = fields.Integer(required=True)
    admin_id = fields.String(required=True) 
    status = fields.String(required=True)
    is_private = fields.Boolean(required=True)
    is_secret = fields.Boolean(required=True)
    password = fields.String()
    max_user_amount = fields.Integer(required=True)


class EventStatusSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    status = fields.String(required=True)

    @validates('status')
    def validate_status_exist(self, value):
        available_event_statuses = ['Zapisy otwarte', 'W trakcie', 'Zakończone']
        if value not in available_event_statuses:
            raise ValidationError(f'This status ({value}) is not available in the application.')


user_schema = UserSchema()
update_password_user_schema = UpdatePasswordUserSchema()
activity_schema = ActivitySchemaAdd()
event_schema = EventSchema()
event_status_schema = EventStatusSchema()