from flask_restx import Namespace, Resource, fields
from ..models import Poll, PollOption, Vote
from ..extensions import cache
from flask import request

results_ns = Namespace("results", description="Poll results")

option_result = results_ns.model("OptionResult", {
    "id": fields.Integer(),
    "label": fields.String(),
    "votes_count": fields.Integer()
})

results_model = results_ns.model("PollResults", {
    "poll_id": fields.Integer(),
    "question": fields.String(),
    "options": fields.List(fields.Nested(option_result)),
})

@results_ns.route("/<int:poll_id>")
class PollResults(Resource):
    @results_ns.marshal_with(results_model)
    def get(self, poll_id):
        cache_key = f"poll_results_{poll_id}"
        data = cache.get(cache_key)
        if data:
            return data

        poll = Poll.query.get_or_404(poll_id)
        options = PollOption.query.filter_by(poll_id=poll_id).all()
        opt_list = [{"id": o.id, "label": o.label, "votes_count": o.votes_count} for o in options]
        data = {"poll_id": poll.id, "question": poll.question, "options": opt_list}
        # cache results for short TTL since counts can change frequently; choose TTL small or invalidate on vote
        cache.set(cache_key, data, timeout=10)  # 10 seconds cache by default
        return data
