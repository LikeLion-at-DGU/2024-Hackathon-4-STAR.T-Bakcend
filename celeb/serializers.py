from rest_framework import serializers
from .models import Celeb
from rank.models import Rank

class CelebSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Celeb
        fields = ['id', 'name', 'photo', 'routines', 'user_score']

    def get_user_score(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user:
            try:
                score = Rank.objects.get(user=user, celeb=obj).score
                return score
            except Rank.DoesNotExist:
                return 0
        return 0
