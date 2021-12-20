from . import db, ma
from sqlalchemy.sql import func
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from datetime import date

class User(db.Model):
    """User entity."""
    #table name is created automatically with the snake_case

    user_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    email = db.Column(db.String(255), unique=True, nullable=False) #field size is set to match the maximum size of an email
    password = db.Column(db.String(150), nullable=False)  #field size is set to match the hashing method

    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)


    def get_id(self):
        return self.user_id

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = User
        load_instance = True
        include_fk = True  #include ForeignKey is set to False by default
        include_relationships = True
    finance = Nested('TransactionSchema', many=True, exclude=('user',))


class Transaction(db.Model):
    """Transaction entity."""
    #table name is created automatically with the snake_case

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    tr_amount = db.Column(db.Float(150), nullable=False)
    tr_date = db.Column(db.Date, default=date.today())

    def get_id(self):
        return self.transaction_id


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta(ma.SQLAlchemyAutoSchema.Meta):
        model = Transaction
        load_instance = True
        include_fk = True  #include ForeignKey is set to False by default
    finance = Nested('UserSchema', many=True, exclude=('transaction',))

db.create_all()
db.session.commit()
