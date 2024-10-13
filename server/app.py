from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  # Set to False for pretty JSON output

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Route to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()  # Fetch all messages from the database
    return jsonify([message.to_dict() for message in messages])  # Return as a JSON list

# Route to get a specific message by ID
@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    message = Message.query.get_or_404(id)  # Fetch the message or return 404 if not found
    return jsonify(message.to_dict())  # Return the message as a JSON object

# Route to create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()  # Get JSON data from request
    body = data.get('body')
    username = data.get('username')

    if not body or not username:
        return jsonify({'error': 'Body and username are required!'}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at
    }), 201

# Route to update an existing message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)  # Fetch the message or return 404 if not found
    data = request.get_json()  # Get the JSON data sent from the client
    message.body = data.get('body', message.body)  # Update the message body if provided
    db.session.commit()  # Commit the changes to the database
    return jsonify(message.to_dict())  # Return the updated message

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)  # Fetch the message or return 404 if not found
    db.session.delete(message)  # Delete the message
    db.session.commit()  # Commit the deletion
    return '', 204  # Return no content, indicating successful deletion

if __name__ == '__main__':
    app.run(port=5555)
