from rest_framework import serializers
from .models import Folder, Document, Topic, TopicItem


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class TopicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicItem
        fields = "__all__"
