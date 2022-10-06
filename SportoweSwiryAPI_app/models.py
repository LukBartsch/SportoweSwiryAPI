from email.policy import default
from importlib.metadata import requires
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
    lastName = db.Column(db.String(50))
    mail = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=True)
    isAddedByGoogle = db.Column(db.Boolean, default=False)
    isAddedByFb = db.Column(db.Boolean, default=False)

    activities = db.relationship('Activities', backref='user', lazy='dynamic')

    # event_admin = db.relationship('Event', backref='admin', lazy='dynamic')
    # events = db.relationship('Participation', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.name} {self.lastName}'


    @staticmethod
    def generate_ID(name: str, lastName: str) -> str:

        sufix = 0

        id = name[0:3] + lastName[0:3] + str(sufix)
        user=User.query.filter(User.id == id).first()

        while user != None:
            sufix +=1
            print(sufix)
            id = name[0:3] + lastName[0:3] + str(sufix)
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

    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),
        salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def removeAccents(self):
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


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(max=50))
    lastName = fields.String(required=True, validate=validate.Length(max=50))
    mail = fields.String(required=True, validate=validate.Length(max=50))
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))
    isAdmin = fields.Boolean(dump_default=False)
    confirmed = fields.Boolean(dump_default=True)
    isAddedByGoogle = fields.Boolean(dump_default=False)
    isAddedByFb = fields.Boolean(dump_defaultt=False)

class UpdatePasswordUserSchema(Schema):
    current_password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))
    new_password = fields.String(load_only=True, required=True, validate=validate.Length(min=8, max=500))


class Activities(db.Model):
    __tableName__ = 'activitiesAPI'
    # id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    # activity = db.Column(db.String(50), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    # distance = db.Column(db.Float, nullable=False)
    # time = db.Column(db.Time)
    # strava_id = db.Column(db.BigInteger)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    activity = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    time = db.Column(db.Time, default=datetime.utcnow())
    userName = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    stravaID = db.Column(db.BigInteger)

class CoefficientsList(db.Model):
    __tableName__ = 'coefficientsListAPI'
    id = db.Column(db.Integer, primary_key=True)
    setName = db.Column(db.String(50))
    activityName = db.Column(db.String(50))
    value = db.Column(db.Float)
    constant = db.Column(db.Boolean)


class ActivitySchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date('%d-%m-%Y', required=True)
    activity = fields.String(required=True)
    distance = fields.Decimal(required=True)
    time = fields.Time('%H:%M:%S')
    userName = fields.String(dump_only=True)
    stravaID = fields.Integer()

    @validates('date')
    def validate_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f'Birth date must be lower than {datetime.now().date()}')

    @validates('activity')
    def validate_activity_exist(self, value):
        available_activity_types = CoefficientsList.query.all()
        available_activity_types = [(a.activityName) for a in available_activity_types]
        available_activity_types = list(dict.fromkeys(available_activity_types))

        if value not in available_activity_types:
            raise ValidationError(f'This type of activity ({value}) is not available in the application.')


class CoefficientsListSchema(Schema):
    id = fields.Integer(dumpl_only=True, load_only=True)
    setName = fields.String()
    activityName = fields.String(required=True)
    value = fields.Decimal(required=True)
    constant = fields.Boolean(required=True)

user_schema = UserSchema()
update_password_user_schema = UpdatePasswordUserSchema()
activity_schema = ActivitySchema()