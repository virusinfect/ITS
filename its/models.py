from django.contrib.auth.models import User
from django.db import models


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
    updated = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True,null=True)# Automatically updated on each save
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20)
    cc_users = models.ManyToManyField(User, related_name='cc_tasks', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    def __str__(self):
        return f'task {self.title} for {self.user.username}'

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
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.task.title} by {self.user.username}'

class Remark(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remark = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Remark on {self.task.title} by {self.user.username}'


class Personal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    from_date = models.DateField()
    status = models.CharField(max_length=20,null=True)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set upon creation
    updated = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)
    colour = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Notification(models.Model):
    users = models.ManyToManyField(User, related_name='notifications')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    @classmethod
    def create_notification(cls, users, message, created_by, icon, is_read=False):
        """
        Create a notification for the specified users.

        Args:
            users (QuerySet of User): The users to whom the notification belongs.
            message (str): The content of the notification.
            icon (str): The MDI icon name.
            is_read (bool): Whether the notification is marked as read (default is False).
        """

        notification = cls(
            message=message,
            icon=icon,
            is_read=is_read,
            created_by=created_by,
        )
        notification.save()
        notification.users.add(*users)  # Add the users to the notification
        return notification
