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
    username = db.Column(db.String, nullable=False)  # Add username field
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp when message is created

    # Optional: serialize specific fields
    serialize_only = ('id', 'body', 'username', 'created_at')  # Include username for serialization

    def __repr__(self):
        return f'<Message {self.body}>'
