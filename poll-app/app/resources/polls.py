from flask_restx import Namespace, Resource, fields
from flask import request
from ..extensions import db
from ..models import Poll, PollOption
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

polls_ns = Namespace("polls", description="Poll management")

option_model = polls_ns.model("Option", {
    "label": fields.String(required=True)
})

create_poll_model = polls_ns.model("CreatePoll", {
    "question": fields.String(required=True),
    "options": fields.List(fields.Nested(option_model), required=True),
    "expires_at": fields.DateTime(required=False, description="ISO8601 datetime")
})

poll_response_model = polls_ns.model("PollResponse", {
    "id": fields.Integer(),
    "question": fields.String(),
    "expires_at": fields.DateTime(),
    "options": fields.List(fields.Nested(polls_ns.model("OptionResponse", {
        "id": fields.Integer(),
        "label": fields.String(),
        "votes_count": fields.Integer()
    })))
})

@polls_ns.route("/")
class PollList(Resource):
    @polls_ns.marshal_list_with(poll_response_model)
    def get(self):
        polls = Poll.query.order_by(Poll.created_at.desc()).all()
        return polls

    @polls_ns.expect(create_poll_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        question = data['question']
        options = data['options']
        expires_at = data.get('expires_at')
        if len(options) < 2:
            return {"message": "At least two options required"}, 400

        user_id = get_jwt_identity()
        poll = Poll(question=question, created_by_id=user_id)
        if expires_at:
            try:
                poll.expires_at = datetime.fromisoformat(expires_at)
            except Exception:
                return {"message": "Invalid expires_at format, use ISO8601"}, 400

        db.session.add(poll)
        db.session.flush()  # get poll.id

        for opt in options:
            popt = PollOption(poll_id=poll.id, label=opt['label'])
            db.session.add(popt)

        db.session.commit()
        return {"id": poll.id, "message": "Poll created"}, 201

@polls_ns.route("/<int:poll_id>")
class PollDetail(Resource):
    @polls_ns.marshal_with(poll_response_model)
    def get(self, poll_id):
        poll = Poll.query.get_or_404(poll_id)
        return poll

    @jwt_required()
    def delete(self, poll_id):
        user_id = get_jwt_identity()
        poll = Poll.query.get_or_404(poll_id)
        # only creator or admin can delete - extend with admin check if needed
        if poll.created_by_id != user_id:
            return {"message": "Not authorized"}, 403
        db.session.delete(poll)
        db.session.commit()
        return {"message": "Deleted"}, 200
