from flask import request, jsonify
from app import app, db
from models import Lead, Note
import logging
from datetime import datetime

# Get all leads
@app.route('/leads', methods=['GET'])
def get_leads():
    try:
        status_filter = request.args.get('status')
        query = Lead.query
        
        if status_filter and status_filter.upper() in ["NEW", "SENT", "REPLIED", "BOOKED"]:
            query = query.filter(Lead.status == status_filter.upper())
        
        leads = query.all()
        return jsonify({'leads': [lead.to_dict() for lead in leads]})
    except Exception as e:
        logging.error(f"Error getting leads: {e}")
        return jsonify({'error': str(e)}), 500

# Create a new lead
@app.route('/leads', methods=['POST'])
def create_lead():
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('owner1_first_name') or not data.get('owner1_last_name') or not data.get('email') or not data.get('phone1'):
            return jsonify({'error': 'Owner 1 first name, Owner 1 last name, email, and primary phone are required'}), 400
        
        # Create new lead with all possible fields
        new_lead = Lead(
            # Owner information
            owner1_first_name=data.get('owner1_first_name'),
            owner1_last_name=data.get('owner1_last_name'),
            owner2_first_name=data.get('owner2_first_name'),
            owner2_last_name=data.get('owner2_last_name'),
            
            # Contact information
            email=data.get('email'),
            phone1=data.get('phone1'),
            phone2=data.get('phone2'),
            phone3=data.get('phone3'),
            phone4=data.get('phone4'),
            
            # Address information
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            
            # Additional information
            developer_name=data.get('developer_name'),
            purchase_date=datetime.strptime(data.get('purchase_date'), '%Y-%m-%d').date() if data.get('purchase_date') else None,
            deed_type=data.get('deed_type'),
            
            # Status
            status=data.get('status', 'NEW').upper()
        )
        
        db.session.add(new_lead)
        db.session.commit()
        
        return jsonify({'lead': new_lead.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating lead: {e}")
        return jsonify({'error': str(e)}), 500

# Update lead status and information
@app.route('/leads/<int:lead_id>', methods=['PATCH'])
def update_lead(lead_id):
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.json
        
        # Update all fields if provided
        # Owner information
        if data.get('owner1_first_name'):
            lead.owner1_first_name = data.get('owner1_first_name')
        if data.get('owner1_last_name'):
            lead.owner1_last_name = data.get('owner1_last_name')
        if 'owner2_first_name' in data:
            lead.owner2_first_name = data.get('owner2_first_name')
        if 'owner2_last_name' in data:
            lead.owner2_last_name = data.get('owner2_last_name')
            
        # Contact information
        if 'email' in data:
            lead.email = data.get('email')
        if data.get('phone1'):
            lead.phone1 = data.get('phone1')
        if 'phone2' in data:
            lead.phone2 = data.get('phone2')
        if 'phone3' in data:
            lead.phone3 = data.get('phone3')
        if 'phone4' in data:
            lead.phone4 = data.get('phone4')
            
        # Address information
        if 'city' in data:
            lead.city = data.get('city')
        if 'state' in data:
            lead.state = data.get('state')
        if 'zip_code' in data:
            lead.zip_code = data.get('zip_code')
            
        # Additional information
        if 'developer_name' in data:
            lead.developer_name = data.get('developer_name')
        if data.get('purchase_date'):
            lead.purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d').date()
        if 'deed_type' in data:
            lead.deed_type = data.get('deed_type')
            
        # Status
        if data.get('status'):
            lead.status = data.get('status').upper()
        
        db.session.commit()
        
        return jsonify({'lead': lead.to_dict()})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating lead: {e}")
        return jsonify({'error': str(e)}), 500

# Add a note to a lead
@app.route('/notes/<int:lead_id>', methods=['POST'])
def add_note(lead_id):
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.json
        
        if not data.get('content'):
            return jsonify({'error': 'Note content is required'}), 400
        
        new_note = Note(
            content=data.get('content'),
            lead_id=lead_id
        )
        
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({'note': new_note.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error adding note: {e}")
        return jsonify({'error': str(e)}), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})
