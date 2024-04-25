from rest_framework import serializers

class Action:
    CHECK_STATUS = 'check_status'
    FETCH_POSTS = 'fetch_posts'

class ActionSerializer(serializers.Serializer):
    ACTIONS = (
        (Action.CHECK_STATUS, 'Check Facebook Status'),
        (Action.FETCH_POSTS, 'Fetch Facebook Posts'),
    )
    action = serializers.ChoiceField(choices=ACTIONS)
