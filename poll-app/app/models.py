from .extensions import db
from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, func

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Poll(db.Model):
    __tablename__ = "polls"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=True, index=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by = db.relationship("User", backref="created_polls")

    def __repr__(self):
        return f"<Poll {self.id}: {self.question[:20]}>"

class PollOption(db.Model):
    __tablename__ = "poll_options"
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"), nullable=False, index=True)
    poll = db.relationship("Poll", backref=db.backref("options", cascade="all, delete-orphan"))
    label = db.Column(db.String(255), nullable=False)
    # denormalized counter for fast reads (kept consistent in transaction)
    votes_count = db.Column(db.Integer, nullable=False, default=0, index=True)

    __table_args__ = (Index("ix_poll_option_poll_label", "poll_id", "label"),)

    def __repr__(self):
        return f"<Option {self.id} ({self.label})>"

class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    user = db.relationship("User", backref="votes")
    poll_id = db.Column(db.Integer, db.ForeignKey("polls.id"), nullable=False, index=True)
    option_id = db.Column(db.Integer, db.ForeignKey("poll_options.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Prevent duplicate voting by same user on same poll
    __table_args__ = (UniqueConstraint('user_id', 'poll_id', name='uq_user_poll_vote'),)
