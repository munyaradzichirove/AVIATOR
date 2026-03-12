from django.db import models

class GameID(models.Model):
    
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return f"Current Game ID: {self.current_id}"