from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from doc_store.models import Folder, Document, Topic
from doc_store.serializers import DocumentSerializer


class GetLoveTest(TestCase):
    """
    Test case to fetch documents in `customer feedback` folder associated
    with topic `SpekiLove!`
    """

    def setUp(self):
        self.document = Folder.objects.filter(name="customer feedback").first()
        self.topic = "SpekiLove!"

    def test_get_documents(self):
        client = Client()

        url = reverse('document-list') + f"?q={self.topic}&folder={self.document.id}"
        response = client.get(url)

        tis = Topic.objects.get_topic_items([self.topic], "document")
        documents = Document.objects.filter(pk__in=tis, folder_id=self.document.id)
        serializer = DocumentSerializer(documents, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


