from app import db
from datetime import datetime
from sqlalchemy import Enum

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Owner 1 information
    owner1_first_name = db.Column(db.String(100), nullable=False)
    owner1_last_name = db.Column(db.String(100), nullable=False)
    
    # Owner 2 information
    owner2_first_name = db.Column(db.String(100))
    owner2_last_name = db.Column(db.String(100))
    
    # Contact information
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Up to 4 phone numbers
    phone1 = db.Column(db.String(20), nullable=False)
    phone2 = db.Column(db.String(20))
    phone3 = db.Column(db.String(20))
    phone4 = db.Column(db.String(20))
    
    # Address information
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    
    # Additional information
    developer_name = db.Column(db.String(200))
    purchase_date = db.Column(db.Date)
    deed_type = db.Column(db.String(100))
    
    # Lead status
    status = db.Column(
        Enum('NEW', 'SENT', 'REPLIED', 'BOOKED', name='lead_status'),
        default='NEW',
        nullable=False
    )
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with notes
    notes = db.relationship('Note', backref='lead', lazy=True, cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'owner1_first_name': self.owner1_first_name,
            'owner1_last_name': self.owner1_last_name,
            'owner1_full_name': f"{self.owner1_first_name} {self.owner1_last_name}",
            'owner2_first_name': self.owner2_first_name,
            'owner2_last_name': self.owner2_last_name,
            'owner2_full_name': f"{self.owner2_first_name} {self.owner2_last_name}" if self.owner2_first_name and self.owner2_last_name else None,
            'email': self.email,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'phone3': self.phone3,
            'phone4': self.phone4,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'developer_name': self.developer_name,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'deed_type': self.deed_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': [note.to_dict() for note in self.notes]
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'lead_id': self.lead_id
        }
