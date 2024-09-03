from flask import jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from market import app, db
from market.models import User, Item

@app.route("/",methods=["GET"])
def home():
    return (
        {'name':'sagar make this homepage beautiful',
         'salary': '2 rupay dunga iss kaam ke'}
    )


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully', 'user': user.to_dict()}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/logout')
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/market')
@login_required
def api_market():
    items = Item.query.filter_by(owner=None).all()
    return jsonify({'items': [item.to_dict() for item in items]}), 200

@app.route('/api/purchase', methods=['POST'])
@login_required
def api_purchase():
    data = request.get_json()
    item = Item.query.get(data['item_id'])
    if item and item.owner is None and current_user.budget >= item.price:
        item.owner = current_user.id
        current_user.budget -= item.price
        db.session.commit()
        return jsonify({'message': 'Item purchased successfully', 'user': current_user.to_dict()}), 200
    return jsonify({'message': 'Purchase failed'}), 400

@app.route('/api/sell', methods=['POST'])
@login_required
def api_sell():
    data = request.get_json()
    item = Item.query.get(data['item_id'])
    if item and item.owner == current_user.id:
        item.owner = None
        current_user.budget += item.price
        db.session.commit()
        return jsonify({'message': 'Item sold successfully', 'user': current_user.to_dict()}), 200
    return jsonify({'message': 'Sale failed'}), 400

@app.route('/api/user')
@login_required
def api_user():
    return jsonify(current_user.to_dict()), 200