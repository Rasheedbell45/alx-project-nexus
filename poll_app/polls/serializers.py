from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Poll, Option, Vote

User = get_user_model()

class OptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Option
        fields = ("id", "text", "votes_count")
        read_only_fields = ("id", "votes_count")


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, required=False)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "question", "created_by", "created_at", "expires_at", "options")
        read_only_fields = ("id", "created_by", "created_at")

    def create(self, validated_data):
        options_data = self.initial_data.get("options", [])
        user = self.context["request"].user
        poll = Poll.objects.create(
            created_by=user,
            question=validated_data["question"],
            expires_at=validated_data.get("expires_at")
        )
        opts = [Option(poll=poll, text=o["text"]) for o in options_data if o.get("text")]
        Option.objects.bulk_create(opts)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.StringRelatedField(read_only=True)
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all())

    class Meta:
        model = Vote
        fields = ("id", "poll", "option", "voter", "created_at")
        read_only_fields = ("id", "voter", "created_at", "poll")

    def validate(self, attrs):
        option = attrs["option"]
        attrs["poll"] = option.poll  # ensure vote always belongs to the correct poll
        return attrs
