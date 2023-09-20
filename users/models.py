import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        if password is None:
            raise ValueError(_("Password is compulsory"))
        email = self.normalize_email(email)
        user = self.model(
            email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('org_id', 'Mirage')
        extra_fields.setdefault('isAdmin',True)
        
        if not extra_fields.get('isAdmin'):
            raise ValueError(_('Superuser must have isAdmin=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(_("user id"),editable=False,unique=True,primary_key=True,default=uuid.uuid4,db_index=True,)
    org_id = models.CharField(_("organisation name"), max_length=100,unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("email address"), max_length=254, db_index=True, unique=True)
    phonenumber = models.PositiveIntegerField(_("phone number"))
    profile_picture = models.ImageField(_("profile pi"), upload_to=None)
    password_hash = models.CharField(max_length=100)
    isAdmin = models.BooleanField(_("is admin"),default=False)
    refresh_token = models.TextField(_("refresh token"))
    launch_credit_balance = models.CharField(_("launch credit"), max_length=50)
    bank_number = models.CharField(_("bank number"), max_length=50)
    bank_code = models.CharField(_("bank code"), max_length=50)
    bank_name = models.CharField(_("bank name"), max_length=50)
    created_at = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated date"), auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
