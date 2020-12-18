from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


#organization model
class Organization(models.Model):
    org_url             = models.URLField(max_length=255, null=True, blank=True)
    org_short_name      = models.CharField(max_length=255, null=True, blank=True)
    org_full_name       = models.CharField(max_length=255, null=True, blank=True)
    contract_holder     = models.CharField(max_length=255, null=True, blank=True)
    class_type          = models.CharField(max_length=255, null=True, blank=True)
    policy_num          = models.CharField(max_length=255, null=True, blank=True)
    policy_agency       = models.CharField(max_length=255, null=True, blank=True)
    date_fiscal_start   = models.DateField(null=True, blank=True)
    date_fiscal_end     = models.DateField(null=True, blank=True)
    num_pay_periods     = models.FloatField(null=True, blank=True)
    #logo_path          = models.CharField(max_length=255, null=True, blank=True)
    logo                = models.ImageField(upload_to='org/image/%Y/%m/%d/', null=True, blank=True)
    admin_email         = models.EmailField(max_length=255, null=True, blank=True)
    enrolment_period    = models.CharField(max_length=255, null=True, blank=True)
    misc_1              = models.CharField(max_length=255, null=True, blank=True)

    #check box
    salary_adjustment   = models.BooleanField(default=False)
    insufficient_benefit_credits = models.BooleanField(default=False)


    def __str__(self):
        return str(self.org_short_name)


# user profile manager
class UserProfileManager(BaseUserManager):
    """Helps django work with our custom user model"""

    def create_user(self, username, password=None):
        """creates a new user profile objecs"""

        if not username:
            raise ValueError('User ID is not valid!')

        user = self.model(username=username,)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, username, password):
        """creates and saves a new super user with given details"""

        user = self.create_user(username=username, password=password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# user profile model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user profile inside our system"""

    username = models.CharField(max_length=50, unique=True)

    email = models.EmailField(max_length=255, null=True, blank=True)

    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)

    salary_base = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    salary_adjusted = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    hsa_annual_credits = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hsa_optional = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hsa_remaining = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    opt_out_bool = models.BooleanField(default=False)

    submitted = models.BooleanField(default=False)

    additional_info = models.TextField(max_length=350, null=True, blank=True)


    join_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('-join_date', )

    def __str__(self):
        """Django uses this when it needs to convert the object to a string"""

        return self.username

    def get_short_name(self):
        return self.username


class MemberUpload(models.Model):
    member_file = models.FileField(upload_to='member_file/%Y/%m/%d/', blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
