from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models

class UserProfileAdmin(ImportExportModelAdmin):
    pass

class OrganizationAdmin(ImportExportModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','org','last_name', 'first_name', 'is_staff',)
    list_filter = ['org', 'is_staff']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('org_short_name', 'org_full_name', 'enrolment_period','salary_adjustment', 'insufficient_benefit_credits')
    list_filter = ['org_short_name']



admin.site.register(models.Organization,OrganizationAdmin)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.MemberUpload)
