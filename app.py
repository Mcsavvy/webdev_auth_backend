from flask import Flask, request, jsonify
import config
from models.user import User
from extensions.database import db
from extensions.auth import jwt
from extensions.cors import cors
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET
db.init_app(app)
jwt.init_app(app)
cors.init_app(app)


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]
    if db.session.query(User).filter(User.email == email).first():
        return jsonify({"msg": "User already exists"}), 400
    hashed_password = generate_password_hash(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    user = db.session.query(User).filter(User.email == email).first()
    if user is None:
        return jsonify({"msg": "Invalid email"}), 401
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})


@app.route("/me")
@jwt_required() # Protect this route with JWT
def me():
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    })


if __name__ == "__main__":
    app.run()
