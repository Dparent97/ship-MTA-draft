from app import db
from datetime import datetime


class WorkItem(db.Model):
    __tablename__ = 'work_items'

    id = db.Column(db.Integer, primary_key=True)
    item_number = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    ns_equipment = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=False)  # Increased from 500 to 2000
    detail = db.Column(db.Text, nullable=False)
    references = db.Column(db.Text)
    submitter_name = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Submitted')
    
    # Assignment & Revision fields
    assigned_to = db.Column(db.String(100))
    needs_revision = db.Column(db.Boolean, default=False)
    revision_notes = db.Column(db.Text)
    original_submitter = db.Column(db.String(100))
    last_modified_by = db.Column(db.String(100))
    last_modified_at = db.Column(db.DateTime)

    # Admin Notes (internal only)
    admin_notes = db.Column(db.Text)
    admin_notes_updated_at = db.Column(db.DateTime)

    # Relationships
    photos = db.relationship('Photo', backref='work_item', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='work_item', lazy=True, cascade='all, delete-orphan')
    history = db.relationship('StatusHistory', backref='work_item', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<WorkItem {self.item_number}>'


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(500), nullable=False)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'), nullable=False)

    def __repr__(self):
        return f'<Photo {self.filename}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Comment by {self.author_name}>'


class StatusHistory(db.Model):
    __tablename__ = 'status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'), nullable=False)
    old_status = db.Column(db.String(20))
    new_status = db.Column(db.String(20), nullable=False)
    changed_by = db.Column(db.String(100), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<StatusHistory {self.work_item_id}: {self.new_status}>'
