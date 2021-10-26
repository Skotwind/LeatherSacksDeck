from rest_framework import serializers

from slaves.models import *


class HardSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardSkill
        fields = ['title', 'description']


class InfoSerializer(serializers.ModelSerializer):
    hard_skills = HardSkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserInfo
        fields = ['name', 'sur_name', 'age', 'birthday', 'gender', 'experience', 'height', 'weight', 'hard_skills']


class WorkerSerializer(serializers.ModelSerializer):
    info = InfoSerializer(many=False, read_only=True)
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.pk

    class Meta:
        model = Worker
        fields = ('id', 'title', 'info')


class ManagerSerializer(serializers.ModelSerializer):
    info = InfoSerializer(many=False, read_only=True)
    children = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.pk

    def get_children(self, obj):
        return [WorkerSerializer(i).data for i in Worker.objects.filter(warden=obj.pk)]

    def get_count(self, obj):
        return len(Worker.objects.filter(warden=obj.pk))

    class Meta:
        model = Manager
        fields = ('id', 'title', 'info', 'count', 'children')
