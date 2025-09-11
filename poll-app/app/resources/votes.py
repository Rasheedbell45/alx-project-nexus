from flask_restx import Namespace, Resource, fields
from flask import request
from ..extensions import db
from ..models import Poll, PollOption, Vote, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from datetime import datetime

votes_ns = Namespace("votes", description="Voting endpoints")

vote_model = votes_ns.model("Vote", {
    "poll_id": fields.Integer(required=True),
    "option_id": fields.Integer(required=True)
})

@votes_ns.route("/")
class CastVote(Resource):
    @votes_ns.expect(vote_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        poll_id = data.get("poll_id")
        option_id = data.get("option_id")

        # Input validation
        poll = Poll.query.get_or_404(poll_id)
        # check expiry
        if poll.expires_at and poll.expires_at < datetime.utcnow():
            return {"message": "Poll has expired"}, 400

        option = PollOption.query.filter_by(id=option_id, poll_id=poll_id).first()
        if not option:
            return {"message": "Invalid option for this poll"}, 400

        # Prevent duplicate vote - DB unique constraint + check
        existing = Vote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
        if existing:
            return {"message": "User has already voted in this poll"}, 400

        # Create vote and increment option.votes_count atomically
        try:
            vote = Vote(user_id=user_id, poll_id=poll_id, option_id=option_id)
            db.session.add(vote)
            # Atomic increment using SQL expression to avoid concurrency issues
            PollOption.query.filter_by(id=option_id).update({PollOption.votes_count: PollOption.votes_count + 1})
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Duplicate vote detected"}, 400
        except Exception as exc:
            db.session.rollback()
            return {"message": f"Vote failed: {str(exc)}"}, 500

        return {"message": "Vote recorded", "option_id": option_id}, 201
