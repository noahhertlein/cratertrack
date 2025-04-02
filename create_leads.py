#!/usr/bin/env python3
"""
Standalone script to create sample leads in a SQLite database.
This script creates its own database connection and doesn't rely on the app structure.
"""

import os
import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship

# Set up the Flask app and database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Define models directly in this script
class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

# Association table for Lead-Tag many-to-many relationship
lead_tag = Table(
    'lead_tag',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('lead_id', Integer, ForeignKey('lead.id'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False)
)

class Lead(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    status = Column(Enum('NEW', 'SENT', 'REPLIED', 'BOOKED', name='lead_status'), default='NEW', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New fields
    address = Column(String(255))
    zip = Column(String(10))
    resort = Column(String(100))
    mortgaged = Column(Boolean, default=False)
    last_text_sent = Column(DateTime)
    last_text_content = Column(Text)
    last_response = Column(Text)
    response_timestamp = Column(DateTime)

    # Phone fields
    phone_1 = Column(String(20))
    phone_2 = Column(String(20))
    phone_3 = Column(String(20))
    phone_4 = Column(String(20))

    # Relationships
    tags = relationship('Tag', secondary=lead_tag, backref=db.backref('leads', lazy='dynamic'))

    def to_dict(self):
        result = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
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
            'tags': [tag.to_dict() for tag in self.tags]
        }
        return result

def create_sample_leads():
    """Create sample leads in the database."""
    print("Creating sample leads...")
    
    # Create a test tag
    test_tag = Tag.query.filter_by(name="test").first()
    if not test_tag:
        test_tag = Tag(name="test")
        db.session.add(test_tag)
        db.session.commit()
        print("Created 'test' tag")
    
    # Create sample leads
    leads = [
        {
            "first_name": "Jason",
            "last_name": "Hemingway",
            "email": "jason@example.com",
            "phone_1": "417-619-1055",
            "status": "NEW",
            "tags": []
        },
        {
            "first_name": "Noah",
            "last_name": "Hertlein",
            "email": "noah@example.com",
            "phone_1": "860-934-3187",
            "status": "NEW",
            "tags": [test_tag]
        }
    ]
    
    for lead_data in leads:
        # Check if lead already exists
        existing_lead = Lead.query.filter_by(
            first_name=lead_data["first_name"],
            last_name=lead_data["last_name"],
            email=lead_data["email"]
        ).first()
        
        if existing_lead:
            print(f"Lead {lead_data['first_name']} {lead_data['last_name']} already exists, skipping.")
            continue
        
        # Create new lead
        tags = lead_data.pop("tags")
        new_lead = Lead(**lead_data)
        
        # Add tags
        for tag in tags:
            new_lead.tags.append(tag)
        
        db.session.add(new_lead)
        print(f"Added lead: {lead_data['first_name']} {lead_data['last_name']}")
    
    # Commit all changes
    db.session.commit()
    print("Sample leads created successfully!")

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        # Create sample leads
        create_sample_leads()
