from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
# from django.views import View
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.contrib.auth.views import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import csv
import os
from django.http.response import StreamingHttpResponse
from datetime import datetime


from account import models as account_model
from account import forms as account_form

class StaffPermission(PermissionRequiredMixin, View):
    permission_required = 'is_superuser'

    login_url = '/staff/login/'

#OrganizationDetail
class StaffLogin(View):
    template_name = 'staff/staff-login.html'

    def get(self, request):

        form = account_form.LoginForm()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)


    def post(self, request):

        form = account_form.LoginForm(request.POST or None)


        err_msg = None
        if form.is_valid():
            user = form.login_request()

            is_super_user = user.is_superuser

            if is_super_user:
                if user:
                    login(request, user)

                    return redirect('staff:staff-home')
            else:
                err_msg = "You are not allowed to login!"


        variables = {
            'form': form,

            'err_msg': err_msg,
        }

        return render(request, self.template_name, variables)

#home
class StaffHome(StaffPermission, View):
    template_name = 'staff/home.html'

    def get(self, request):

        variables = {

        }

        return render(request, self.template_name, variables)


#Organization
class Organization(StaffPermission, View):
    template_name = 'staff/org.html'

    def get(self, request):

        variables = {

        }

        return render(request, self.template_name, variables)


#add Organization
class AddOrganization(StaffPermission, View):
    template_name = 'staff/add-org.html'

    def get(self, request):

        form = account_form.AddOrganization()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):

        form = account_form.AddOrganization(request.POST or None, request.FILES or None)

        if form.is_valid():
            salary_adjustment = request.POST.get('salary_adjustment')
            insufficient_benefit_credits = request.POST.get('insufficient_benefit_credits')

            add_org = form.deploy()

            if salary_adjustment == 'on':
                add_org.salary_adjustment = True
            else:
                pass

            if insufficient_benefit_credits == 'on':
                add_org.insufficient_benefit_credits = True
            else:
                pass

            add_org.save()

            return redirect('staff:org')


        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)


#add Organization
class ViewOrganization(StaffPermission, View):

    template_name = 'staff/view-org.html'

    def get(self, request):

        orgs = account_model.Organization.objects.all().order_by('-id')
        orgs_count = account_model.Organization.objects.all().count()

        form = account_form.OrgSearchForm()

        variables = {
            'orgs': orgs,
            'orgs_count': orgs_count,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):

        orgs = account_model.Organization.objects.all().order_by('-id')
        orgs_count = account_model.Organization.objects.all().count()

        form = account_form.OrgSearchForm(request.POST or None)

        s_orgs = None
        if form.is_valid():
            s_orgs = form.deploy()

        variables = {
            'orgs': orgs,
            'orgs_count': orgs_count,

            'form': form,
            's_orgs': s_orgs,
        }

        return render(request, self.template_name, variables)


#delete Organization
class DeleteOrganization(StaffPermission, View):

    def get(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        org.delete()

        return redirect('staff:view-org')


#detail Organization
class DetailOrganization(StaffPermission, View):
    template_name = 'staff/detail-org.html'

    def get(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        total_member = account_model.UserProfile.objects.filter(org=org).count()

        variables = {
            'org': org,

            'total_member': total_member,
        }

        return render(request, self.template_name, variables)


#edit Organization
class EditOrganization(StaffPermission, View):
    template_name = 'staff/edit-org.html'

    def get(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        form = account_form.EditOrgForm(instance=org)


        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        form = account_form.EditOrgForm(request.POST or None, request.FILES or None, instance=org)


        if form.is_valid():
            form.save()
            return redirect('staff:view-org')

            salary_adjustment = request.POST.get('salary_adjustment')
            insufficient_benefit_credits = request.POST.get('insufficient_benefit_credits')

            if salary_adjustment == 'on':
                org.salary_adjustment = True
            else:
                org.salary_adjustment = False

            if insufficient_benefit_credits == 'on':
                org.insufficient_benefit_credits = True
            else:
                org.insufficient_benefit_credits = False

            org.save()

        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)


#edit Organization
class OrganizationMember(StaffPermission, View):
    template_name = 'staff/org-member.html'

    def get(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        members_list = account_model.UserProfile.objects.filter(org=org).order_by('last_name')
        members_count = account_model.UserProfile.objects.filter(org=org).count()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)

        variables = {
            'org': org,

            'page': page,
            'members_count': members_count,
        }

        return render(request, self.template_name, variables)


    def get_uuid(self):
        uuid = os.urandom(10).hex()

        return uuid


    def  csv_export(self, file_name, members):
        with open('media/csv_output/{}.csv'.format(file_name), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            row_first_line = ['User ID', 'First Name', 'Middle Name', 'Last Name', 'Organiztaion', 'Salary Base', 'HSA Annual Credits', 'HSA Optional', 'HSA Remaining']
            writer.writerow(row_first_line)

            for member in members:
                row = [member.username, member.first_name, member.middle_name, member.last_name, member.org.org_short_name, member.salary_base, member.hsa_annual_credits, member.hsa_optional, member.hsa_remaining]
                writer.writerow(row)

            csvfile.close()



    def post(self, request, org_id):

        org = get_object_or_404(account_model.Organization, id=org_id)

        members_list = account_model.UserProfile.objects.filter(org=org).order_by('-join_date')
        members_count = account_model.UserProfile.objects.filter(org=org).count()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)

        if request.POST.get('export_csv') == 'export_csv':
            uuid = self.get_uuid()
            file_name = str(org.org_short_name) + '-' + str(uuid)
            self.csv_export(file_name, members_list)

            return redirect('staff:save_file', file_name=file_name)


        variables = {
            'org': org,

            'page': page,
            'members_count': members_count,
        }

        return render(request, self.template_name, variables)


def some_streaming_csv_view(request, file_name):
    path = 'media/csv_output/{}.csv'.format(file_name)
    response = StreamingHttpResponse(open(path), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + '{}.csv'.format(file_name)
    return response

#Member
class Member(StaffPermission, View):
    template_name = 'staff/member.html'

    def get(self, request):

        variables = {

        }

        return render(request, self.template_name, variables)


#add Member
class AddMember(StaffPermission, View):
    template_name = 'staff/add-member.html'

    def get(self, request, org_id):
        org = get_object_or_404(account_model.Organization, id=org_id)

        form = account_form.AddUserForm()

        variables = {
            'form': form,

            'org': org,
        }

        return render(request, self.template_name, variables)


    def post(self, request, org_id):
        org = get_object_or_404(account_model.Organization, id=org_id)

        form = account_form.AddUserForm(request.POST or None)

        if form.is_valid():
            user_add = form.deploy(org)

            return redirect('staff:detail-member', user_id=user_add.id)


        variables = {
            'form': form,

            'org': org,
        }

        return render(request, self.template_name, variables)

#view member
class ViewMember(StaffPermission, View):
    template_name = 'staff/view-member.html'

    def get(self, request):

        members_list = account_model.UserProfile.objects.all().order_by('org','id')
        members_count = account_model.UserProfile.objects.all().count()
        form = account_form.MemberSearchForm()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)

        variables = {
            'page': page,
            'members_count': members_count,
            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):

        members_list = account_model.UserProfile.objects.all().order_by('org','id')
        members_count = account_model.UserProfile.objects.all().count()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)

        form = account_form.MemberSearchForm(request.POST or None)

        s_members = None

        if form.is_valid():
            s_members = form.deploy()

        variables = {
            'page': page,
            'members_count': members_count,

            'form': form,
            's_members': s_members,
        }

        return render(request, self.template_name, variables)


#delete member
class DeleteMember(StaffPermission, View):

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        member.delete()

        return redirect('staff:view-member')

#detail member
class DetailMember(StaffPermission, View):
    template_name = 'staff/detail-member.html'

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        variables = {
            'member': member,
        }

        return render(request, self.template_name, variables)

#activate deactivate member
class ActivateDeactivateAccount(StaffPermission, View):

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        usr_is_active = member.is_active

        if usr_is_active:
            member.is_active = False
            member.save()
        else:
            member.is_active = True
            member.save()

        return redirect('staff:detail-member', user_id=user_id)

#activate deactivate member
class ActivateDeactivateStaffStatus(StaffPermission, View):

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        usr_is_staff = member.is_staff

        if usr_is_staff:
            member.is_staff = False
            member.save()
        else:
            member.is_staff = True
            member.save()

        return redirect('staff:detail-member', user_id=user_id)

#change password
class ChangePassword(StaffPermission, View):
    template_name = 'staff/change-password.html'

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        form = account_form.ChangeUserPasswordForm()

        variables = {
            'member': member,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        form = account_form.ChangeUserPasswordForm(request.POST or None)

        if form.is_valid():
            form.deploy(user_id)

            return redirect('staff:detail-member', user_id=user_id)


        variables = {
            'member': member,

            'form': form,
        }

        return render(request, self.template_name, variables)


#detail Organization
class EditMember(StaffPermission, View):
    template_name = 'staff/edit-member.html'

    def get(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        form = account_form.ChageUserProfile(instance=member)

        variables = {
            'member': member,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, user_id):

        member = get_object_or_404(account_model.UserProfile, id=user_id)

        form = account_form.ChageUserProfile(request.POST or None, instance=member)

        if form.is_valid():
            form.save()
            return redirect('staff:detail-member', user_id=user_id)

        variables = {
            'member': member,

            'form': form,
        }

        return render(request, self.template_name, variables)

#member upload
class MemberUpload(StaffPermission, View):
    template_name = 'staff/member-upload.html'

    def get(self, request):
        form = account_form.MemberUploadForm()

        variables = {
            'form': form,
        }

        return render(request, self.template_name, variables)



    def deploy_member_to_db(self, file_name):
        with open(file_name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')

            #skip 1st line
            next(csvfile)

            err_msg = []
            success_msg = []
            for row in readCSV:
                username = row[0]
                email = row[1]
                password = row[2]
                first_name = row[3]
                middle_name = row[4]
                last_name = row[5]
                org = row[6].lower()
                salary_base = row[7]
                salary_adjusted = row[8]
                hsa_annual_credit = row[9]
                hsa_optional = row[10]
                hsa_remaining = row[11]

                check_username = account_model.UserProfile.objects.filter(username=username).exists()

                if check_username:
                    err_msg.append("{} userid already exists!".format(username))
                else:
                    check_org = account_model.Organization.objects.filter(org_short_name=org).exists()
                    if check_org:
                        org_obj = account_model.Organization.objects.get(org_short_name=org)


                        member = account_model.UserProfile(username=username, email=email, org=org_obj, first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                           salary_base=salary_base, salary_adjusted=salary_adjusted, hsa_annual_credits=hsa_annual_credit, hsa_optional=hsa_optional, hsa_remaining=hsa_remaining)

                        member.set_password(password)
                        member.save()

                        success_msg.append("{} userid has been added.".format(username))

                    else:
                        err_msg.append("{} organization not found!".format(org))
        return err_msg, success_msg



    def post(self, request):

        form = account_form.MemberUploadForm(request.POST or None, request.FILES)


        err_msg = None
        success_msg = None
        if form.is_valid():
            member_file = form.deploy()

            full_path = 'media/' + str(member_file.member_file)
            err_msg, success_msg = self.deploy_member_to_db(full_path)

        variables = {
            'form': form,
            'err_msg': err_msg,
            'success_msg': success_msg,
        }

        return render(request, self.template_name, variables)
