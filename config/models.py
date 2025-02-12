from django.db import models
from django.contrib.auth.models import Group

class UIComponent(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "FeatureA"
    is_visible = models.BooleanField(default=True)  # Toggle switch
    allowed_groups = models.ManyToManyField(Group, blank=True)  # User group control

    def __str__(self):
        return f"{self.name} - {'Visible' if self.is_visible else 'Hidden'}"
