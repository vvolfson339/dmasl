from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from decimal import *
import re

from . import models


#add user form
gender_list = (
    ('male', 'Male'),
    ('female', 'Female')
)

# ----------------- Start of Enrolment App ----------------- #
# Main login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    password = forms.CharField(max_length=40, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if len(username) < 1:
            raise forms.ValidationError('Invalid User ID and/or password. Please try again!')
        else:
            if len(password) < 1:
                raise forms.ValidationError('Invalid User ID and/or password. Please try again!')
            else:
                user = authenticate(username=username, password=password)
                if not user:
                    raise forms.ValidationError("Invalid User ID and/or password. Please try again!")
                else:
                    if not user.is_active:
                        raise forms.ValidationError("This User ID is no longer active, please contact your plan administrator!")


    def login_request(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

#enrolment form 2
class EnrolmentForm2(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    middle_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'middle_name')

#enrolment form3
class EnrolmentForm3(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.current_user = kwargs.pop('current_user')
        super(EnrolmentForm3, self).__init__(*args,**kwargs)

    # email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    email = forms.EmailField()
    hsa_optional = forms.DecimalField(max_digits=6, decimal_places=2, required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    # models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    def clean(self):
        # email = self.cleaned_data.get('email')
        hsa_optional = self.cleaned_data.get('hsa_optional')
        check_number = isinstance(hsa_optional, (int,float,Decimal))

        # email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)

        # if not email_correction:
        #     raise forms.ValidationError('Please enter a valid Email address!')
        if not check_number:
                raise forms.ValidationError('Please enter a valid Optional Health Spending amount!')
        else:
            if hsa_optional < 0:
                raise forms.ValidationError('Please enter a valid Optional Health Spending amount!')
                # else:
                #     hsa_remaining_db = float(self.current_user.hsa_remaining)
                #
                #     if hsa_optional > hsa_remaining_db:
                #             raise forms.ValidationError('Your remaining credit is less than {}'.format(hsa_optional))

    class Meta:
        model = models.UserProfile
        fields = ('email', 'hsa_optional', )

# ----------------- End of Enrolment App ----------------- #

# ----------------- Start of Admin App ----------------- #
# org admin login form
class OrgAdminLoginForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.org = kwargs.pop('org')
        super(OrgAdminLoginForm, self).__init__(*args,**kwargs)


    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    password = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        if len(username) < 1:
            raise forms.ValidationError('Invalid User ID and/or password. Please try again!')
        else:
            if len(password) < 8:
                raise forms.ValidationError("Invalid User ID and/or password. Please try again!")
            else:
                user = authenticate(username=username, password=password)
                if not user:
                    raise forms.ValidationError("Invalid User ID and/or password. Please try again!")
                else:
                    if not user.is_active:
                        raise forms.ValidationError("This User ID is no longer active, please contact your plan administrator!")
                    else:
                        if user.is_staff != True:
                            raise forms.ValidationError('This User ID is not provisioned for Admin access. Please try again!')


    def login_request(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

#enrollment organizarion form
class AddOrganization(forms.Form):
    org_url             = forms.URLField(max_length=255, required=False, widget=forms.URLInput(attrs={'class': 'validate'}))
    org_short_name      = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    org_full_name       = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    contract_holder     = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    class_type          = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    policy_num          = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    policy_agency       = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date_fiscal_start   = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    date_fiscal_end     = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    num_pay_periods     = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    enrolment_period    = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    logo = forms.ImageField(required=False)
    admin_email       = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    misc_1              = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    text_block_1 = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))
    text_block_2 = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))
    text_block_3 = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))

    def check_space(self, org_short_name):
        for x in org_short_name:
            if x == ' ':
                return True
        return False

    def clean(self):
        org_url                 = self.cleaned_data.get('org_url')
        org_short_name          = self.cleaned_data.get('org_short_name')
        org_full_name           = self.cleaned_data.get('org_full_name')
        contract_holder         = self.cleaned_data.get('contract_holder')
        class_type              = self.cleaned_data.get('class_type')
        policy_num              = self.cleaned_data.get('policy_num')
        policy_agency           = self.cleaned_data.get('policy_agency')
        date_fiscal_start       = self.cleaned_data.get('date_fiscal_start')
        date_fiscal_end         = self.cleaned_data.get('date_fiscal_end')
        num_pay_periods         = self.cleaned_data.get('num_pay_periods')
        enrolment_period        = self.cleaned_data.get('enrolment_period')
        #logo_path               = self.cleaned_data.get('logo_path')
        logo                    = self.cleaned_data.get('logo')
        admin_email             = self.cleaned_data.get('admin_email')
        misc_1                  = self.cleaned_data.get('misc_1')
        text_block_1            = self.cleaned_data.get('text_block_1')
        text_block_2            = self.cleaned_data.get('text_block_2')
        text_block_3            = self.cleaned_data.get('text_block_3')

        if len(org_short_name) < 1:
            raise forms.ValidationError('Organization short name is required')
        else:
            check_org_short_name_space = self.check_space(org_short_name)

            if check_org_short_name_space:
                raise forms.ValidationError('Organization short name cannot have spaces')
            else:
                org_exists = models.Organization.objects.filter(org_short_name=org_short_name).exists()

                if org_exists:
                    raise forms.ValidationError('Organization short name allready exists')
                else:
                    email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', admin_email)

                    if not email_correction:
                        raise forms.ValidationError('Email address is not valid')

    def deploy(self):
        org_url                 = self.cleaned_data.get('org_url')
        org_short_name          = self.cleaned_data.get('org_short_name')
        org_full_name           = self.cleaned_data.get('org_full_name')
        contract_holder         = self.cleaned_data.get('contract_holder')
        class_type              = self.cleaned_data.get('class_type')
        policy_num              = self.cleaned_data.get('policy_num')
        policy_agency           = self.cleaned_data.get('policy_agency')
        date_fiscal_start       = self.cleaned_data.get('date_fiscal_start')
        date_fiscal_end         = self.cleaned_data.get('date_fiscal_end')
        num_pay_periods         = self.cleaned_data.get('num_pay_periods')
        enrolment_period        = self.cleaned_data.get('enrolment_period')

        logo                    = self.cleaned_data.get('logo')
        admin_email             = self.cleaned_data.get('admin_email')
        misc_1                  = self.cleaned_data.get('misc_1')
        text_block_1            = self.cleaned_data.get('text_block_1')
        text_block_2            = self.cleaned_data.get('text_block_2')
        text_block_3            = self.cleaned_data.get('text_block_3')


        deploy = models.Organization(org_url=org_url, org_short_name=org_short_name, org_full_name=org_full_name,
                                     contract_holder=contract_holder, class_type=class_type, policy_num=policy_num,
                                     policy_agency=policy_agency, date_fiscal_start=date_fiscal_start,
                                     date_fiscal_end=date_fiscal_end, num_pay_periods=num_pay_periods,
                                     logo=logo, admin_email=admin_email, enrolment_period=enrolment_period, misc_1=misc_1,
                                     text_block_1=text_block_1, text_block_2=text_block_2, text_block_3=text_block_3)

        deploy.save()
        return deploy

#edit org
class EditOrgForm(forms.ModelForm):
    org_url             = forms.URLField(max_length=255, required=False, widget=forms.URLInput(attrs={'class': 'validate'}))
    org_full_name       = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    contract_holder     = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    class_type          = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    policy_num          = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    policy_agency       = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date_fiscal_start   = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    date_fiscal_end     = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    num_pay_periods     = forms.FloatField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    enrolment_period    = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    logo                = forms.ImageField(required=False, widget=forms.FileInput)
    admin_email         = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    misc_1              = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    text_block_1        = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))
    text_block_2        = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))
    text_block_3        = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))



    def check_space(self, org_short_name):
        for x in org_short_name:
            if x == ' ':
                return True
        return False


    def clean(self):
        org_url                 = self.cleaned_data.get('org_url')
        org_full_name           = self.cleaned_data.get('org_full_name')
        contract_holder         = self.cleaned_data.get('contract_holder')
        class_type              = self.cleaned_data.get('class_type')
        policy_num              = self.cleaned_data.get('policy_num')
        policy_agency           = self.cleaned_data.get('policy_agency')
        date_fiscal_start       = self.cleaned_data.get('date_fiscal_start')
        date_fiscal_end         = self.cleaned_data.get('date_fiscal_end')
        num_pay_periods         = self.cleaned_data.get('num_pay_periods')
        enrolment_period        = self.cleaned_data.get('enrolment_period')

        logo                    = self.cleaned_data.get('logo')
        admin_email             = self.cleaned_data.get('admin_email')
        misc_1                  = self.cleaned_data.get('misc_1')
        text_block_1            = self.cleaned_data.get('text_block_1')
        text_block_2            = self.cleaned_data.get('text_block_2')
        text_block_3            = self.cleaned_data.get('text_block_3')

    class Meta:
        model = models.Organization
        fields = ('org_url', 'org_full_name', 'contract_holder', 'class_type', 'policy_num', 'policy_agency', 'date_fiscal_start', 'date_fiscal_end', 'num_pay_periods', 'enrolment_period', 'logo', 'admin_email', 'misc_1', 'text_block_1','text_block_2','text_block_3')

#add user
class AddUserForm(forms.Form):
    username = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    password1 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password1'}))
    password2 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password2'}))

    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    middle_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    salary_base = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    salary_adjusted = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_annual_credits = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_optional = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_remaining = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))

    additional_info = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))


    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        middle_name = self.cleaned_data.get('middle_name')

        salary_base = self.cleaned_data.get('salary_base')
        salary_adjusted = self.cleaned_data.get('salary_adjusted')
        hsa_annual_credits = self.cleaned_data.get('hsa_annual_credits')
        hsa_optional = self.cleaned_data.get('hsa_optional')
        hsa_remaining = self.cleaned_data.get('hsa_remaining')

        additional_info = self.cleaned_data.get('additional_info')


        if len(username) < 1:
            raise forms.ValidationError('User ID cannot be blank!')
        else:
            username_exists = models.UserProfile.objects.filter(username=username).exists()

            if username_exists:
                raise forms.ValidationError('User ID already exists')
            else:
                email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)
                if not email_correction:
                    raise forms.ValidationError('Email address is not valid!')
                else:
                    email_exists = models.UserProfile.objects.filter(email=email).exists()
                    if email_exists:
                        raise forms.ValidationError('A user with this email address already exists!')
                    else:
                        if len(password1) < 8:
                            raise forms.ValidationError("Password must be at least 8 characters long!")
                        else:
                            if password1 != password2:
                                raise forms.ValidationError("Passwords do not match!")
                            else:
                                check_number = isinstance(salary_base, (int, float, Decimal))

                                if not check_number:
                                    raise forms.ValidationError('Salary amount is not valid!')
                                else:
                                    if salary_base < 0:
                                        raise forms.ValidationError('Salary adjusted amount is not valid!')
                                    else:
                                        check_number = isinstance(salary_adjusted, (int, float, Decimal))

                                        if not check_number:
                                            raise forms.ValidationError('Salary adjusted amount is not valid!')
                                        else:
                                            if salary_adjusted < 0:
                                                raise forms.ValidationError('Salary adjusted amount is not valid!')

                                            else:
                                                check_number = isinstance(hsa_annual_credits, (int, float))

                                                if not check_number:
                                                    raise forms.ValidationError('HSA Base Credit amount is not valid!')
                                                else:
                                                    if hsa_annual_credits < 0:
                                                        raise forms.ValidationError('HSA Base Credit amount is not valid!')

                                                    else:
                                                        check_number = isinstance(hsa_optional, (int, float, Decimal))

                                                        if not check_number:
                                                            raise forms.ValidationError('HSA Optinal amount is not valid!')
                                                        else:
                                                            if hsa_optional < 0:
                                                                raise forms.ValidationError('HSA Optinal amount is not valid!')
                                                            else:
                                                                check_number = isinstance(hsa_remaining, (int, float))

                                                                if not check_number:
                                                                    raise forms.ValidationError('HSA Remaining amount is not valid!')
                                                                else:
                                                                    if hsa_remaining < 0:
                                                                        raise forms.ValidationError('HSA Remaining amount is not valid!')


    def deploy(self, org):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        middle_name = self.cleaned_data.get('middle_name')

        salary_base = self.cleaned_data.get('salary_base')
        salary_adjusted = self.cleaned_data.get('salary_adjusted')
        hsa_annual_credits = self.cleaned_data.get('hsa_annual_credits')
        hsa_optional = self.cleaned_data.get('hsa_optional')
        hsa_remaining = self.cleaned_data.get('hsa_remaining')
        additional_info = self.cleaned_data.get('additional_info')


        user = models.UserProfile(username=username, email=email, org=org, first_name=first_name, last_name=last_name,
                                    middle_name=middle_name, salary_base=salary_base,
                                    salary_adjusted=salary_adjusted, hsa_annual_credits=hsa_annual_credits, hsa_optional=hsa_optional,
                                    hsa_remaining=hsa_remaining, additional_info=additional_info)

        user.set_password(password1)

        user.save()
        return user

#additional info form
class AdditionalInfoForm(forms.ModelForm):
    additional_info = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))

    class Meta:
        model = models.UserProfile
        fields = ('additional_info', )

#change user password from staff
class ChangeUserPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate'}))
    new_password2 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate'}))

    def clean(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if len(new_password1) < 8:
            raise forms.ValidationError("Passowrd length must be at least 8 characters!")
        else:
            if new_password1 != new_password2:
                raise forms.ValidationError("Passwords do not match!")

    def deploy(self, user_id):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        hash_pass = make_password(new_password1)

        deploy = models.UserProfile.objects.filter(id=user_id).update(password=hash_pass)

#change user profile
class ChageUserProfile(forms.ModelForm):

    org = forms.ModelChoiceField(queryset=models.Organization.objects.all(), required=False,widget=forms.Select(attrs={'class':'validate'}))

    email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    middle_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    salary_base = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    salary_adjusted = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_annual_credits = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_optional = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_remaining = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))

    additional_info = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))


    def clean(self):
        org = self.cleaned_data.get('org')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        middle_name = self.cleaned_data.get('middle_name')

        salary_base = self.cleaned_data.get('salary_base')
        salary_adjusted = self.cleaned_data.get('salary_adjusted')
        hsa_annual_credits = self.cleaned_data.get('hsa_annual_credits')
        hsa_optional = self.cleaned_data.get('hsa_optional')
        hsa_remaining = self.cleaned_data.get('hsa_remaining')

        additional_info = self.cleaned_data.get('additional_info')

        check_number = isinstance(salary_base, (int, float, Decimal))

        email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)

        if not email_correction:
            raise forms.ValidationError('Email address is not valid!')
        else:
            if not check_number:
                raise forms.ValidationError('Salary amount is not valid!')
            else:
                if salary_base < 0:
                    raise forms.ValidationError('Salary amount is not valid!')
                else:
                    check_number = isinstance(salary_adjusted, (int, float, Decimal))

                    if not check_number:
                        raise forms.ValidationError('Salary adjusted amount is not valid!')
                    else:
                        if salary_adjusted < 0:
                            raise forms.ValidationError('Salary adjusted amount is not valid!')

                        else:
                            check_number = isinstance(hsa_annual_credits, (int, float))

                            if not check_number:
                                raise forms.ValidationError('HSA Base Credit amount is not valid!')
                            else:
                                if hsa_annual_credits < 0:
                                    raise forms.ValidationError('HSA Base Credit amount is not valid!')

                                else:
                                    check_number = isinstance(hsa_optional, (int, float, Decimal))

                                    if not check_number:
                                        raise forms.ValidationError('HSA Optinal amount is not valid!')
                                    else:
                                        if hsa_optional < 0:
                                            raise forms.ValidationError('HSA Optinal amount is not valid!')
                                        else:
                                            check_number = isinstance(hsa_remaining, (int, float))

                                            if not check_number:
                                                raise forms.ValidationError('HSA Remaining amount is not valid!')
                                            else:
                                                if hsa_remaining < 0:
                                                    raise forms.ValidationError('HSA Remaining amount is not valid!')


    class Meta:
        model = models.UserProfile
        fields = ('email', 'org', 'first_name', 'last_name', 'middle_name', 'salary_base', 'salary_adjusted', 'hsa_annual_credits', 'hsa_optional', 'hsa_remaining', 'additional_info')

#change user profile from org admin
class ChageUserProfileFromOrgAdmin(forms.ModelForm):

    email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))
    middle_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    salary_base = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    salary_adjusted = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_annual_credits = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_optional = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))
    hsa_remaining = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class': 'validate', }))

    additional_info = forms.CharField( required=False, max_length=350, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea', 'data-length': '350', }))


    def clean(self):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        middle_name = self.cleaned_data.get('middle_name')

        salary_base = self.cleaned_data.get('salary_base')
        salary_adjusted = self.cleaned_data.get('salary_adjusted')
        hsa_annual_credits = self.cleaned_data.get('hsa_annual_credits')
        hsa_optional = self.cleaned_data.get('hsa_optional')
        hsa_remaining = self.cleaned_data.get('hsa_remaining')

        additional_info = self.cleaned_data.get('additional_info')



        check_number = isinstance(salary_base, (int, float, Decimal))

        email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)

        if not email_correction:
            raise forms.ValidationError('Email address is not valid!')
        else:
            if not check_number:
                raise forms.ValidationError('Salary amount is not valid!')
            else:
                if salary_base < 0:
                    raise forms.ValidationError('Salary amount is not valid!')
                else:
                    check_number = isinstance(salary_adjusted, (int, float, Decimal))

                    if not check_number:
                        raise forms.ValidationError('Salary adjusted amount is not valid!')
                    else:
                        if salary_adjusted < 0:
                            raise forms.ValidationError('Salary adjusted amount is not valid!')

                        else:
                            check_number = isinstance(hsa_annual_credits, (int, float))

                            if not check_number:
                                raise forms.ValidationError('HSA Base Credit amount is not valid!')
                            else:
                                if hsa_annual_credits < 0:
                                    raise forms.ValidationError('HSA Base Credit amount is not valid!')

                                else:
                                    check_number = isinstance(hsa_optional, (int, float, Decimal))

                                    if not check_number:
                                        raise forms.ValidationError('HSA Optinal amount is not valid!')
                                    else:
                                        if hsa_optional < 0:
                                            raise forms.ValidationError('HSA Optinal amount is not valid!')
                                        else:
                                            check_number = isinstance(hsa_remaining, (int, float))

                                            if not check_number:
                                                raise forms.ValidationError('HSA Remaining amount is not valid!')
                                            else:
                                                if hsa_remaining < 0:
                                                    raise forms.ValidationError('HSA Remaining amount is not valid!')


    class Meta:
        model = models.UserProfile
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'salary_base', 'salary_adjusted', 'hsa_annual_credits', 'hsa_optional', 'hsa_remaining', 'additional_info')

#org search form
class OrgSearchForm(forms.Form):
    org_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    def clean(self):
        org_name = self.cleaned_data.get('org_name')

        if len(org_name) < 1:
            raise forms.ValidationError('Organization Name is required!')


    def deploy(self):
        org_name = self.cleaned_data.get('org_name')

        orgs = models.Organization.objects.filter(org_short_name__icontains=org_name)

        return orgs

#org search form
class MemberSearchForm(forms.Form):
    user_id = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', }))

    def clean(self):
        user_id = self.cleaned_data.get('user_id')

        if len(user_id) < 1:
            raise forms.ValidationError('User ID cannot be blank!')

    def deploy(self):
        user_id = self.cleaned_data.get('user_id')
        member = models.UserProfile.objects.filter(username=user_id)

        return member

#org search form
class MemberUploadForm(forms.Form):
    member_file = forms.FileField(required=False, widget=forms.FileInput)

    def clean(self):
        member_file = self.cleaned_data.get('member_file')

        if member_file == None:
            raise forms.ValidationError('Members Upload file must be in CSV format!')

    def deploy(self):
        member_file = self.cleaned_data.get('member_file')

        deploy = models.MemberUpload(member_file=member_file)
        deploy.save()

        return deploy

# ----------------- End of Admin App ----------------- #
