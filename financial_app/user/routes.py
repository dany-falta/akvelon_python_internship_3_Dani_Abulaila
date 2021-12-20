from flask import Flask
from flask_restx import Api, Resource, Namespace
from financial_app import api, db
from financial_app import models
from werkzeug.security import generate_password_hash

api = Namespace('User', description='User related operations')

user_id_parser = api.parser()
user_id_parser.add_argument('user_id', type=int, default='1', required=True)

@api.route('/view_users')
class ViewUsers(Resource):
    user_schema = models.UserSchema()

    @api.doc(id= 'get_users', description="Query all users")
    def get(self):
        """ Return information on all users """

        users = db.session.query(models.User).all()
        return self.user_schema.dump(users, many=True), 200

@api.route('/view_user_by_id')
class ViewUserByID(Resource):
    user_schema = models.UserSchema()

    @api.doc(id= 'get_user_by_id', params={"user_id": "A User ID"} , description="Query user by ID")
    @api.expect(user_id_parser)
    def get(self, user_id_parser=user_id_parser):
        """ Return information on a single user """

        arg = user_id_parser.parse_args()
        user_id = arg['user_id']
        user = db.session.query(models.User).filter_by(user_id=user_id).first()
        if not user:
            return 'User not found.', 404
        return self.user_schema.dump(user), 200

@api.route('/create_user')
class CreateUser(Resource):
    user_schema = models.UserSchema()

    user_parser = api.parser()
    user_parser.add_argument('email', type=str, required=True)
    user_parser.add_argument('password', type=str, required=True)
    user_parser.add_argument('first_name', type=str, required=True)
    user_parser.add_argument('last_name', type=str, required=True)

    @api.doc(id= 'create_user', description="Create a new user")
    @api.expect(user_parser)
    def post(self, user_parser=user_parser):
       """ Create a new user """

       data = user_parser.parse_args()
       email = data['email']
       first_name = data['first_name']
       last_name = data['last_name']
       password = data['password']

       exists = db.session.query(models.User).filter_by(email=email).first()

       if exists:
           return 'User with this email already exists.', 409
       elif len(first_name) < 3 or len(last_name) < 3:
           return 'First and last names need to be longer.', 422
       elif len(password) < 5:
           return 'Password should be longer than 4 characters.', 422
       else:
           data['password'] = generate_password_hash(password, method='sha256')
           user = self.user_schema.load(data)
           db.session.add(user)
           db.session.commit()
           return self.user_schema.dump(user), 200

@api.route('/update_user')
class UpdateUser(Resource):
    user_schema = models.UserSchema()

    user_update_parser = api.parser()
    user_update_parser.add_argument('email', type=str)
    user_update_parser.add_argument('password', type=str)
    user_update_parser.add_argument('first_name', type=str)
    user_update_parser.add_argument('last_name', type=str)

    @api.doc(id= 'update_user', description="Update information on an existing user")
    @api.expect(user_id_parser, user_update_parser)
    def post(self, user_id_parser=user_id_parser, user_update_parser=user_update_parser):
       """ Update information on an existing user """

       arg = user_id_parser.parse_args()
       user_id = arg['user_id']
       user = db.session.query(models.User).filter_by(user_id=user_id).first()
       if not user:
           return 'User not found.', 404

       data = user_update_parser.parse_args()
       email = data['email']
       first_name = data['first_name']
       last_name = data['last_name']
       password = data['password']

       exists = db.session.query(models.User).filter_by(email=email).first()

       if exists:
           return 'User with this email already exists.', 409
       elif first_name and len(first_name) < 3 or last_name and len(last_name) < 3:
           return 'First and last names need to be longer.', 422
       elif password and len(password) < 5:
           return 'Password should be longer than 4 characters.', 422
       else:
           if email:
               user.email = email
           if first_name:
               user.first_name = first_name
           if last_name:
               user.last_name = last_name
           if password:
               user.password = generate_password_hash(password, method='sha256')
           db.session.commit()
           return self.user_schema.dump(user), 200

@api.route('/delete_user')
class DeleteUser(Resource):
    @api.doc(id= 'delete_user', description="Delete an existing user")
    @api.expect(user_id_parser)
    def delete(self,user_id_parser=user_id_parser):
        """ Delete an existing user """

        arg = user_id_parser.parse_args()
        user_id = arg['user_id']
        user = db.session.query(models.User).filter_by(user_id=user_id).first()
        if not user:
            return 'User not found.', 404

        db.session.delete(user)
        db.session.commit()
        return 'User deleted successfully', 200
