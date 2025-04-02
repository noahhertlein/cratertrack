from backend.app import db
from datetime import datetime
from sqlalchemy import Enum

class Lead(db.Model):
    """
    Lead model representing potential customers in the CRM.
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(
        Enum('NEW', 'SENT', 'REPLIED', 'BOOKED', name='lead_status'),
        default='NEW',
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New fields
    address = db.Column(db.String(255))
    zip = db.Column(db.String(10))
    resort = db.Column(db.String(100))
    mortgaged = db.Column(db.Boolean, default=False)
    last_text_sent = db.Column(db.DateTime)
    last_text_content = db.Column(db.Text)
    last_response = db.Column(db.Text)
    response_timestamp = db.Column(db.DateTime)

    # Phone fields
    phone_1 = db.Column(db.String(20))
    phone_2 = db.Column(db.String(20))
    phone_3 = db.Column(db.String(20))
    phone_4 = db.Column(db.String(20))

    # Relationship with notes
    notes = db.relationship('Note', backref='lead', lazy=True, cascade="all, delete-orphan")
    tags = db.relationship('Tag', secondary='lead_tag', backref=db.backref('leads', lazy='dynamic'))
    
    def to_dict(self):
        result = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'address': self.address,
            'zip': self.zip,
            'resort': self.resort,
            'mortgaged': self.mortgaged,
            'phone_1': self.phone_1,
            'phone_2': self.phone_2,
            'phone_3': self.phone_3,
            'phone_4': self.phone_4,
            'last_text_sent': self.last_text_sent.isoformat() if self.last_text_sent else None,
            'last_text_content': self.last_text_content,
            'last_response': self.last_response,
            'response_timestamp': self.response_timestamp.isoformat() if self.response_timestamp else None,
            'notes': [note.to_dict() for note in self.notes],
            'tags': [tag.to_dict() for tag in self.tags]
        }
        return result


class Note(db.Model):
    """
    Note model for storing internal notes related to leads.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'lead_id': self.lead_id
        }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class LeadTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
