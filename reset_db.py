#!/usr/bin/env python3
"""
Script to reset the database and create sample leads.
This will drop all existing tables and create new ones.
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
    __tablename__ = 'tag'
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
    __tablename__ = 'lead'
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

class Note(db.Model):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead_id = Column(Integer, ForeignKey('lead.id'), nullable=False)
    
    # Relationship
    lead = relationship('Lead', backref=db.backref('notes', lazy=True, cascade="all, delete-orphan"))

def reset_database():
    """Drop all tables and recreate them."""
    print("Dropping all tables...")
    db.drop_all()
    print("Creating all tables...")
    db.create_all()
    print("Database reset complete!")

def create_sample_leads():
    """Create sample leads in the database."""
    print("Creating sample leads...")
    
    # Create a test tag
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
        # Reset database
        reset_database()
        # Create sample leads
        create_sample_leads()
