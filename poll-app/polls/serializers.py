# polls/serializers.py
from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True, source='votes.count')

    class Meta:
        model = Option
        fields = ('id', 'text', 'votes_count')
        read_only_fields = ('id', 'votes_count')


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'question', 'created_by', 'created_at', 'expires_at', 'options')
        read_only_fields = ('id', 'created_by', 'created_at')

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        user = self.context['request'].user
        poll = Poll.objects.create(created_by=user, **validated_data)
        opts = [Option(poll=poll, text=o['text']) for o in options_data]
        Option.objects.bulk_create(opts)
        return poll
