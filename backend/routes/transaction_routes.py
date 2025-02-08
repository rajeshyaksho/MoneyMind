from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Transaction

# define the blueprint
transaction_routes = Blueprint('transaction_routes', __name__)

# Add Transaction
@transaction_routes.route('/add', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('type') or not data.get('amount') or not data.get('category'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    new_transaction = Transaction(
        user_id=user_id,
        type=data['type'],
        amount=data['amount'],
        category=data['category'],
        description=data.get('description')
    )
    new_transaction.save()

    return jsonify({'message': 'Transaction added successfully'}), 201 

# Get All Transactions from a User
@transaction_routes.route('/all', methods=['GET'])
@jwt_required()
def get_all_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    
    transactions_list = [
        {
            'id':tx.id,
            'type':tx.type,
            'amount':tx.amount,
            'category':tx.category,
            'description':tx.description,
            'date':tx.date
        }
        for tx in transactions
    ]

    return jsonify({'transactions': transactions_list}), 200

# Delete a Transaction
@transaction_routes.route('/delete/<int:transaction_id>', methods=['DELETE'])
@jwt_required()

def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()

    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted successfully'}), 200