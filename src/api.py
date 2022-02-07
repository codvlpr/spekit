from rest_framework import routers
from doc_store import views

router = routers.DefaultRouter()
router.register(r'folders', views.FolderViewSet, basename='folder')
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'topics', views.TopicViewSet, basename='topic')
router.register(r'topic_items', views.TopicItemViewSet, basename='topicitem')