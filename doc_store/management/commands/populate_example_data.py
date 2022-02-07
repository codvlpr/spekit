from django.core.management.base import BaseCommand
from doc_store.models import *


class Command(BaseCommand):
    help = 'Populate example documents in the store'

    @staticmethod
    def populate_topics(topics):
        """
        Installing topics

        Params
        ----------
        topics : list
            list of dicts containing topics data

        Return
        ----------
        bool : Returns True if everything goes as expected

        """
        topics_count = 0
        for topic in topics:
            try:
                Topic.objects.add_topic(**topic)
                topics_count += 1
            except Exception as e:
                print(f"Something went wrong while installing topic (topic): {e}")

        print(f"- Installed {topics_count} topic(s)")
        return True

    @staticmethod
    def populate_folders_documents(folder_and_documents):
        """
        Installing folders and documents

        Params
        ----------
        folder_and_documents : list
            list of dicts containing folder and documents data

        Return
        ----------
        bool : Returns True if everything goes as expected

        """
        for folder in folder_and_documents:
            documents = folder.pop("documents")
            try:
                Folder.objects.add_folder_assoc_document(
                    folder,
                    documents,
                )
                print(f"- Created folder: {folder['name']} and added {len(documents)} documents")
            except Exception as e:
                print(f"Something went wrong while installing {folder['name']}: {e}")
            print("---------------")
        return True

    def handle(self, *args, **options):

        folder_and_documents = [
            {
                "documents": [
                    {
                        "name": "resume.pdf",
                        "topics": ["development"],
                    },
                    {
                        "name": "loan.pdf",
                        "topics": ["development"],
                    },
                    {
                        "name": "stuff.pdf",
                        "topics": ["development", "workout"],
                    },
                    {
                        "name": "daily.pdf",
                        "topics": ["workout"],
                    },
                ],
                "topics": ["development", "workout"],
                "name": "personal",
            },
            {
                "documents": [
                    {
                        "name": "contract.pdf",
                        "topics": ["development"],
                    },
                    {
                        "name": "design.pdf",
                        "topics": ["development"],
                    },
                    {
                        "name": "development.pdf",
                        "topics": ["development"],
                    },
                    {
                        "name": "backlog.pdf",
                        "topics": ["development"],
                    },
                ],
                "topics": ["development"],
                "name": "workspace",
            },
            {
                "documents": [
                    {
                        "name": "routine.pdf",
                        "topics": ["workout", "recipe"],
                    },
                    {
                        "name": "cycle.pdf",
                        "topics": ["workout"],
                    },
                    {
                        "name": "cheesecake.pdf",
                        "topics": ["recipe"],
                    },
                    {
                        "name": "banana_bread.pdf",
                        "topics": ["recipe", "workout"],
                    },
                ],
                "topics": ["recipe", "workout"],
                "name": "misc",
            }
        ]

        topics = [
            {
                "name": "development",
                "short_description": "Development related matters",
                "long_description": "Development related matters 10x",
            },
            {
                "name": "workout",
                "short_description": "Workout related matters",
                "long_description": "Workout related matters 10x",
            },
            {
                "name": "recipe",
                "short_description": "Recipe related matters",
                "long_description": "Recipe related matters 10x",
            },
        ]

        self.populate_topics(topics)
        self.populate_folders_documents(folder_and_documents)

