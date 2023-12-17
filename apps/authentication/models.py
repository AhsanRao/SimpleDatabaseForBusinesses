from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from datetime import datetime

from apps import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from apps.authentication.util import hash_pass

db = SQLAlchemy()
class AuctionItem(db.Model):
    __tablename__ = 'auction_items'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(512), nullable=False)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    ends = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    current = db.Column(db.Float, nullable=False)
    open = db.Column(db.Float, nullable=False)
    reserve = db.Column(db.String(100), nullable=False)
    bids = db.Column(db.Integer, nullable=False)
    business = db.Column(db.String(255), nullable=False)
    updated = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'title': self.title,
            'url': self.url,
            'status': self.status,
            'ends': self.ends,
            'description': self.description,
            'current': self.current,
            'open': self.open,
            'reserve': self.reserve,
            'bids': self.bids,
            'business': self.business,
            'updated': self.updated
        }

class Person(db.Model):
    __tablename__ = 'persons'

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)

    # Relationships
    addresses = db.relationship('Address', backref='person', lazy=True)
    phone_numbers = db.relationship('PhoneNumber', backref='person', lazy=True)
    contracts = db.relationship('Contract', backref='person', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'email': self.email,
            'role': self.role
        }

class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    zipcode = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'country': self.country,
            'person_id': self.person_id
        }

class PhoneNumber(db.Model):
    __tablename__ = 'phone_numbers'

    phone_id = db.Column(db.Integer, primary_key=True)
    home_phone_number = db.Column(db.String(255))
    business_phone_number = db.Column(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'home_phone_number': self.home_phone_number,
            'business_phone_number': self.business_phone_number,
            'person_id': self.person_id
        }

class Contract(db.Model):
    __tablename__ = 'contracts'

    contract_id = db.Column(db.Integer, primary_key=True)
    installation_date = db.Column(db.Date, nullable=False)
    monthly_charges = db.Column(db.Numeric(10, 2), nullable=False)
    billing_date = db.Column(db.Date, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'), nullable=False)
    role = db.Column(db.String(255), nullable=False)

    # Relationships
    contract_equipments = db.relationship('ContractEquipment', backref='contract', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'installation_date': self.installation_date.isoformat() if self.installation_date else None,
            'monthly_charges': str(self.monthly_charges),
            'billing_date': self.billing_date.isoformat() if self.billing_date else None,
            'renewal_date': self.renewal_date.isoformat() if self.renewal_date else None,
            'person_id': self.person_id,
            'role': self.role
        }

class Equipment(db.Model):
    __tablename__ = 'equipments'

    equipment_id = db.Column(db.Integer, primary_key=True)
    asset_tag_number = db.Column(db.String(255), unique=True, nullable=False)
    equipment_name = db.Column(db.String(255), nullable=False)
    serial_number = db.Column(db.String(255), unique=True, nullable=False)
    install_date = db.Column(db.Date, nullable=False)

    # Relationships
    contract_equipments = db.relationship('ContractEquipment', backref='equipment', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_tag_number': self.asset_tag_number,
            'equipment_name': self.equipment_name,
            'serial_number': self.serial_number,
            'install_date': self.install_date.isoformat() if self.install_date else None
        }

class ContractEquipment(db.Model):
    __tablename__ = 'contract_equipments'

    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.contract_id'), primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.equipment_id'), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.person_id'))

    def to_dict(self):
        return {
            'contract_id': self.contract_id,
            'equipment_id': self.equipment_id,
            'person_id': self.person_id
        }

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)
    first_name    = db.Column(db.String)
    last_name     = db.Column(db.String)
    address       = db.Column(db.Text)
    about         = db.Column(db.Text)

    oauth_github  = db.Column(db.String(100), nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username: str) -> "Users":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "Users":
        return cls.query.filter_by(id=_id).first()
   
    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
          
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
    
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(Users)
