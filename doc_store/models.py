from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction


class FolderQuerySet(models.query.QuerySet):
    pass


class FolderManager(models.Manager.from_queryset(FolderQuerySet)):

    @staticmethod
    def add_folder_assoc_document(folder, documents, *args, **kwargs):
        """
        Creates a new folder and associate documents with newly created folder

        Params
        ----------
        folder : str
            name of the folder

        documents : list
            list of dicts for documents contains name and topics

        Return
        ----------
        data : dict
            Folder instance as a key and value will be the list of created instances of Document

        """
        with transaction.atomic():
            created_folder = Folder.objects.create(name=folder["name"])
            Topic.objects.assoc_topic(folder["topics"], created_folder)
            data = {created_folder: []}
            for document in documents:
                created_document = created_folder.document_set.create(name=document["name"])
                data[created_folder].append(document)
                Topic.objects.assoc_topic(document["topics"], created_document)

        return data


class Folder(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FolderManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class Document(models.Model):
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(
        'doc_store.Folder',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.folder.name} / {self.name}"

    class Meta:
        unique_together = ("name", "folder")
        ordering = ['created_at']


class TopicQuerySet(models.query.QuerySet):
    pass


class TopicManager(models.Manager.from_queryset(TopicQuerySet)):

    @staticmethod
    def add_topic(name, short_description, long_description, *args, **kwargs):
        """
        Creates a new topic or returns the already created one

        Params
        ----------
        folder : str
            name of the topic

        short_description : str
            short description for the topic

        long_description : str
            brief description for the topic

        Return
        ----------
        topic : Topic
            returns the Topic instance

        """
        topic, _ = Topic.objects.get_or_create(
            name=name,
            short_description=short_description,
            long_description=long_description,
        )

        return topic

    @staticmethod
    def assoc_topic(topics, instance, *args, **kwargs):
        """
        Filter topics by name from Topic and associate them with the model instance through Generic relations

        Params
        ----------
        topics : list
            list of strings

        model : str
            name of the model on which topics should be associated

        Return
        ----------
        topics : Topic
            Queryset of the filtered topics

        """
        model = ContentType.objects.get_for_model(instance)

        topics = Topic.objects.filter(name__in=topics)
        for topic in topics:
            topic_item, _ = TopicItem.objects.get_or_create(content_type=model, object_id=instance.id, topic=topic)

        return topics

    @staticmethod
    def get_topic_items(topics, instance, *args, **kwargs):
        """
        Filter topic items from targeted model

        Params
        ----------
        topics : list
            list of strings

        instance : str
            get target model from ContentType framework

        Return
        ----------
        tis : TopicItem
            Queryset of the filtered topic items

        """
        if instance == "document":
            instance = Document
        elif instance == "folder":
            instance = Folder
        else:
            raise NotImplementedError

        ct = ContentType.objects.get_for_model(instance)
        tis = TopicItem.objects.filter(
            topic__name__in=topics,
            content_type=ct,
        ).values_list("object_id", flat=True)

        return tis


class Topic(models.Model):
    name = models.CharField(max_length=25)
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TopicManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


class TopicItem(models.Model):
    topic = models.ForeignKey(
        'doc_store.Topic',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
