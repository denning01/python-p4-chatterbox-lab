from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Setting up custom naming conventions for database constraints
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initializing the database with custom metadata
db = SQLAlchemy(metadata=metadata)

# Message model
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)  # Message ID
    body = db.Column(db.String, nullable=False)    # Message content
    username = db.Column(db.String, nullable=False)  # Username field
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp when message is created

    # Serialize specific fields
    serialize_only = ('id', 'body', 'username', 'created_at')  # Include username for serialization

    def __repr__(self):
        return f'<Message {self.body}>'

    def serialize(self):
        """Serialize the message instance."""
        return {field: getattr(self, field) for field in self.serialize_only}

    @classmethod
    def create(cls, body, username):
        """Create a new message."""
        message = cls(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return message

    @classmethod
    def update(cls, message_id, body):
        """Update an existing message by ID."""
        message = cls.query.get(message_id)
        if message:
            message.body = body
            db.session.commit()
            return message
        return None

    @classmethod
    def delete(cls, message_id):
        """Delete a message by ID."""
        message = cls.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return message  # Returning the deleted message
        return None

    @classmethod
    def get_all_messages(cls):
        """Get all messages."""
        return cls.query.all()
