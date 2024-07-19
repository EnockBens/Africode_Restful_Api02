from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource , abort , marshal_with , fields, reqparse

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///block.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.username
    


    
users_args = reqparse.RequestParser()
users_args.add_argument('username', type=str, required=True, help='Username is required')
users_args.add_argument('email', type=str, required=True, help='Email is required')

userfields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(userfields)
    def get(self):
        users = UserModel.query.all()
        return users,200
    
    @marshal_with(userfields)
    def post(self):
        args = users_args.parse_args()
        username = args['username']
        email = args['email']
        new_user = UserModel(username=username ,email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

api.add_resource(Users, "/users/")

class User(Resource):
    @marshal_with(userfields)
    def get(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, message=f"User with id {id} not found")
        else:
            return user, 200
        


    @marshal_with(userfields)
    def patch(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, message=f"User with id {id} not found")
        args = users_args.parse_args()
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user, 200
    
    @marshal_with(userfields)
    def delete(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, message=f"User with id {id} not found")
        db.session.delete(user)
        db.session.commit()
        
        return '', 204
        



api.add_resource(User, "/users/<int:id>")

@app.route('/')
def home():
    return 'Hello World'



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    
    app.run(debug=True)
