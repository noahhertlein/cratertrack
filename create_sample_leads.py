#!/usr/bin/env python3
"""
Script to create sample leads in the database.
Run this script directly to add sample leads to the database.
"""

import os
import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Set up the Flask app and database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import models after setting up the app
with app.app_context():
    from backend.models import Lead, Tag, LeadTag

def create_sample_leads():
    """Create sample leads in the database."""
    print("Creating sample leads...")
    
    # First, make sure the database tables exist
    db.create_all()
    
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
