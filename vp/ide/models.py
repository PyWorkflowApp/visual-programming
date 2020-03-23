from django.db import models

class Side_Menu_Node(models.Model):
    name = models.TextField()
    type = models.TextField()

class User_Menu_Access(models.Model):
    user = models.TextField()
    nodeName = models.TextField()