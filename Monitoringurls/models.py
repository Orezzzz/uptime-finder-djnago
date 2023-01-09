from django.db import models
from Accounts.models import User

# Create your models here.

class urlslist(models.Model):
    id = models.AutoField(primary_key=True)
    url_name = models.URLField(max_length=200,)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    ACTIVE = 'ACTIVE'
    DOWN = 'DOWN'
    STATUS = [
        (ACTIVE, 'ACTIVE'),
        (DOWN, 'DOWN'),
    ]
    status = models.CharField(
        max_length=6,
        choices=STATUS,
    )

    def __str__(self):
        return self.url_name

class urlshistory(models.Model):
    id = models.AutoField(primary_key=True)
    urlslist = models.ForeignKey(urlslist, on_delete=models.CASCADE)
    created_at = models.CharField( max_length=100,    )
    updated_at = models.DateTimeField(auto_now=True)

    ACTIVE = 'ACTIVE'
    DOWN = 'DOWN'
    STATUS = [
        (ACTIVE, 'ACTIVE'),
        (DOWN, 'DOWN'),
    ]
    status = models.CharField(
        max_length=6,
        choices=STATUS,
    )

    


class deletedurls(models.Model):
    id = models.AutoField(primary_key=True)
    url_name = models.URLField(max_length=200,)
    created_at = models.CharField( max_length=100,    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.url_name