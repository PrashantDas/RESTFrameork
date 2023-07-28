from django.db import models
from django.contrib.auth.models import User

class NotesModel(models.Model):
    title            = models.CharField(max_length=200)
    matter           = models.TextField()
    writer           = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__() + self.title
