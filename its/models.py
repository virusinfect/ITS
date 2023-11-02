from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PartsCategory(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'parts_category'


class Parts(models.Model):
    part_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(PartsCategory, on_delete=models.CASCADE, db_column='category_id')
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return self.code

    class Meta:
        managed = False
        db_table = 'parts'


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    other_telephone = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'company'


class Clients(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, db_column='company_id')
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=25)
    mobile = models.CharField(max_length=25, null=True)
    description = models.CharField(max_length=500)
    is_active = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    def __str__(self):
        return self.f_name

    class Meta:
        managed = False
        db_table = 'clients'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20)
    cc_users = models.ManyToManyField(User, related_name='cc_tasks', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return self.title

    @classmethod
    def create_task(cls, title, description, is_active=True, status=None, user=None, users=None):
        """
        A universal function to create Task model instances.
        :param title: Title for the new task (required)
        :param description: Description for the new task (required)
        :param is_active: is_active value (optional, defaults to True)
        :param status: Status for the new task (optional)
        :param user: User associated with the task (optional)
        """
        task = cls(title=title, description=description, is_active=is_active, status=status, user=user)

        task.creator = user

        if users:
            for user in users:
                task.cc_users.add(user)

        task.save()
        return task


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.task.title} by {self.user.username}'
