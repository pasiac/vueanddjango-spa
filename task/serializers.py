from rest_framework import serializers

from .models import Task, Person


class TaskSerializer(serializers.ModelSerializer):
    person = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Task
        fields = ('id', 'description', 'status', 'minutes_spend', 'enjoyed', 'person')

    def validate(self, attrs):
        person = Person.objects.filter(name=attrs.get('person'))
        if person:
            attrs['person'] = person.first()
        return super().validate(attrs)

    def create(self, validated_data):
        person_name = validated_data.get('person')
        if person_name:
            person = Person.objects.get_or_create(name=person_name)
            validated_data['person'] = person
        return super().create(validated_data)