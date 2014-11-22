from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


class SqUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class SqUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'

    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    objects = SqUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Gate(models.Model):
    point_id = models.AutoField(unique=True, primary_key=True)
    coord_x = models.FloatField()
    coord_y = models.FloatField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' %(self.coord_x, self.coord_y)


class Check(models.Model):
    type = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    trip = models.ForeignKey('Trip')
    gate = models.ForeignKey('Gate')


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    card = models.ForeignKey('Card')
    point_start = models.ForeignKey(Gate, related_name='point_start')
    point_finish = models.ForeignKey(Gate, related_name='point_finish')

    def __str__(self):
        return '%d' %(self.id)


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.number




