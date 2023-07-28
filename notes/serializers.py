from rest_framework import serializers
from .models import NotesModel


class NotesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesModel
        # exclude = ['date_of_creation']
        fields = '__all__'

    def validate(self, attrs):
        blog_title = attrs.get('title', 'title missing')
        if NotesModel.objects.filter(title__iexact=blog_title).exists():
            raise serializers.ValidationError(detail='This title already exists')
        else:
            return attrs

