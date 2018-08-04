from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import login, logout
import csv
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

        form = account_form.AddOrganization(request.POST or None)

        if form.is_valid():
            form.deploy()

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

        form = account_form.EditOrgForm(request.POST or None, instance=org)


        if form.is_valid():
            form.save()


        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)







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
            form.deploy(org)


        variables = {
            'form': form,

            'org': org,
        }

        return render(request, self.template_name, variables)




#view member
class ViewMember(StaffPermission, View):
    template_name = 'staff/view-member.html'

    def get(self, request):

        members = account_model.UserProfile.objects.all().order_by('-join_date')
        members_count = account_model.UserProfile.objects.all().count()

        form = account_form.MemberSearchForm()

        variables = {
            'members': members,
            'members_count': members_count,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):

        members = account_model.UserProfile.objects.all().order_by('-join_date')
        members_count = account_model.UserProfile.objects.all().count()

        form = account_form.MemberSearchForm(request.POST or None)

        s_members = None
        if form.is_valid():
            s_members = form.deploy()

        variables = {
            'members': members,
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
                password = row[1]
                first_name = row[2]
                middle_name = row[3]
                last_name = row[4]
                gender = row[5]
                org = row[6]
                birthdate = row[7]
                salary_base = row[8]
                hsa_annual_credit = row[9]
                hsa_remaining = row[10]

                date_object = datetime.strptime(birthdate, '%d/%m/%Y')
                birthdate_expected_format = date_object.strftime('%Y-%m-%d')

                check_username = account_model.UserProfile.objects.filter(username=username).exists()

                if check_username:
                    err_msg.append("{} userid already exists!".format(username))
                else:
                    check_org = account_model.Organization.objects.filter(org_short_name=org).exists()
                    if check_org:
                        org_obj = account_model.Organization.objects.get(org_short_name=org)


                        member = account_model.UserProfile(username=username, org=org_obj, first_name=first_name, middle_name=middle_name, last_name=last_name,
                                                           gender=gender, birthdate=birthdate_expected_format, salary_base=salary_base, hsa_annual_credits=hsa_annual_credit, hsa_remaining=hsa_remaining)

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
