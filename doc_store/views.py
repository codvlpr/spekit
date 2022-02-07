from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Folder, Document, Topic, TopicItem
from .serializers import (
    FolderSerializer,
    DocumentSerializer,
    TopicSerializer,
    TopicItemSerializer,
)


class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned documents to the given topics,
        by filtering against the `q` query parameter in the URL.
        """
        topics = self.request.query_params.getlist('q')
        if topics:
            tis = Topic.objects.get_topic_items(topics, "folder")
            queryset = Folder.objects.filter(pk__in=tis)
        else:
            queryset = Folder.objects.all()
        return queryset


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned documents to the given topics,
        by filtering against the `q` and `folder` query parameter in the URL.
        """
        topics = self.request.query_params.getlist('q')
        folder = self.request.query_params.get('folder')
        if topics:
            tis = Topic.objects.get_topic_items(topics, "document")
            queryset = Document.objects.filter(pk__in=tis)
        else:
            queryset = Document.objects.all()

        if folder:
            queryset = queryset.filter(folder_id=folder)
        return queryset


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned topics to the given namess,
        by filtering against the `q` query parameter in the URL.
        """
        topic = self.request.query_params.get('q')
        if topic:
            queryset = Topic.objects.filter(name__startwith=topic)
        else:
            queryset = Topic.objects.all()
        return queryset


class TopicItemViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TopicItem.objects.all()
    serializer_class = TopicItemSerializer
    implemented_classes = [Document, Folder]

    def create(self, request, *args, **kwargs):
        """
        This will associate a topic with either a folder or a document
        First this will validate if the user is sending the correct payload
        Then it will verify if the document or a folder exists or it will return 404
        Lastly it will associate and return True
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        content_type = serializer.validated_data['content_type'].model_class()
        object_id = serializer.validated_data['object_id']
        topic = serializer.validated_data['topic']

        if content_type not in self.implemented_classes:
            raise NotImplementedError("Only Documents and Folders can be associated with topics")

        validated_object = get_object_or_404(content_type, pk=object_id)

        Topic.objects.assoc_topic([topic], validated_object)

        return Response(True, status=status.HTTP_201_CREATED)
