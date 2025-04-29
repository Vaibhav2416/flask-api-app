from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SECRET_KEY"] = "welcome"


db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


# UserModel to handle user data and authentication
class UserModel(db.Model):
    __tablename__ = "users"
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password_hash = db.Column(db.String(300))
    role = db.Column(db.String(200), default="user")


    def generate_pw(self, password):
        self.password_hash = generate_password_hash(password)


    def check_pw(self, password):
        return check_password_hash(self.password_hash, password)


# Resource for user registration
class RegisterResource(Resource):
    def post(self):
        user_data = request.get_json()
        if UserModel.query.filter_by(email=user_data.get("email")).first():
            return {"msg": "User already exists"}
       
        newUser = UserModel(email=user_data.get("email"), role=user_data.get("role"))
        newUser.generate_pw(user_data.get("password"))
        db.session.add(newUser)
        db.session.commit()
        return {"msg": "User Registered Successfully"}


# Resource for user login
class LoginResource(Resource):
    def post(self):
        user_data = request.get_json()
        user = UserModel.query.filter_by(email=user_data.get("email")).first()
        if user and user.check_pw(user_data.get("password")):
            access_token = create_access_token(identity=user.role)
            return {"msg": "User Logged in successfully", "access_token": access_token}
        else:
            return {"msg": "User not found"}


# ProductModel to handle product data
class ProductModel(db.Model):
    __tablename__ = "products_table"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    category = db.Column(db.String(300))
    price = db.Column(db.Integer)


    def to_dict(self):
        return {"product_id": self.product_id, "name": self.name,
                "category": self.category, "price": self.price}


# Resource for managing products
class Product(Resource):
    @jwt_required()
    def get(self, product_id=None):
        if product_id:
            single_product = ProductModel.query.get(product_id)
            if not single_product:
                return {"msg": "Product not found"}
            return jsonify(single_product.to_dict())
        else:
            data = ProductModel.query.all()
            return jsonify([item.to_dict() for item in data])


    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data.get("name") or not data.get("category") or not data.get("price"):
            return {"msg": "Please fill valid data"}, 404


        product = ProductModel(name=data.get("name"), category=data.get("category"),
                               price=data.get("price"))
        db.session.add(product)
        db.session.commit()
        return {"msg": "Product added successfully"}


    @jwt_required()
    def put(self, product_id):
        data = request.get_json()
        find_product = ProductModel.query.get(product_id)
        if find_product:
            find_product.name = data.get("name", find_product.name)
            find_product.category = data.get("category", find_product.category)
            find_product.price = data.get("price", find_product.price)
            db.session.commit()
            return {"msg": "Product Updated Successfully"}
        else:
            return {"msg": "Product Not found"}


    @jwt_required()
    def delete(self, product_id):
        product = ProductModel.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {"msg": "Product deleted successfully"}
        else:
            return {"msg": "Product not found"}


# API endpoints
api.add_resource(Product, "/products", "/products/<int:product_id>")
api.add_resource(RegisterResource, "/register")
api.add_resource(LoginResource, "/login")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
