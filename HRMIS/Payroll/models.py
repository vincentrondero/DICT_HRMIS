from django.db import models

class CleansedData(models.Model):
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_binary = models.BinaryField()

    def __str__(self):
        return self.file_name
