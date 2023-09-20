from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
        if password is None:
            raise ValueError(_("Password is compulsory"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('org_id', 1)
        # extra_fields.setdefault('is_admin',True)

        # if not extra_fields.get('is_admin'):
        #     raise ValueError(_('Superuser must have is_admin=True.'))

        return self.create_user(email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    # by default django uses auto increament for the id
    # uncomment org_id when organization model has been created
    # org_id = models.ForeignKey("app.Model", verbose_name=_("organisation name"), on_delete=models.CASCADE,null=True)
    first_name = models.CharField(_("first name"), max_length=225)
    last_name = models.CharField(_("last name"), max_length=225, blank=True, null=True)
    profile_pic = CloudinaryField(_("profile pic"))
    email = models.EmailField(
        _("email address"), max_length=225, db_index=True, unique=True
    )
    phone = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    password_hash = models.CharField(max_length=100)
    is_admin = models.BooleanField(_("is admin"), blank=True, null=True)
    lunch_credit_balance = models.PositiveIntegerField(_("launch credit"))
    refresh_token = models.TextField(_("refresh token"), blank=True, null=True)
    bank_number = models.CharField(
        _("bank number"), max_length=50, blank=True, null=True
    )
    bank_code = models.CharField(_("bank code"), max_length=50, blank=True, null=True)
    bank_name = models.CharField(_("bank name"), max_length=50, blank=True, null=True)
    bank_region = models.CharField(
        _("bank region"), max_length=50, blank=True, null=True
    )
    currency = models.CharField(
        _("country currency"), max_length=128, blank=True, null=True
    )
    currency_code = models.CharField(
        _("country code"), max_length=4, blank=True, null=True
    )
    created_at = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated date"), auto_now=True)
    is_deleted = models.BooleanField(_("deleted user"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
