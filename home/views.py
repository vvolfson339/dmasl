from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from account import models as account_model
from account import forms as account_form
from django.http.response import StreamingHttpResponse
from datetime import datetime
import csv
import os


from . import tasks
#from decimal import *


# sign out
def signout_request(request):
    logout(request)

    direction = request.GET.get('from')

    if direction == 'staff':
        return redirect('staff:staff-login')
    elif direction == 'org_admin':
        return redirect('home:org-admin-login', org_short_name=request.GET.get('org'))
    elif direction == 'client':
        return redirect('home:login', org_short_name=request.GET.get('org'))
    else:
        return redirect('home:lhin_links')


#=======================================================================================================================
#=======================================================================================================================
#                                           Enrolment App Forms
#=======================================================================================================================
#=======================================================================================================================

#home view
class Home(View):
    template_name = 'home/home.html'

    def get(self, request):
        variables = {
        }

        return render(request, self.template_name, variables)

class Links(View):
    template_name = 'home/links.html'

    def get(self, request):
        variables = {
        }

        return render(request, self.template_name, variables)

class LHIN_Links(View):
    template_name = 'home/lhin_links.html'

    def get(self, request):
        variables = {
        }

        return render(request, self.template_name, variables)

#Main Login Pgae
class Login(View):
    template_name = 'home/login.html'

    def get(self, request, org_short_name):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        form = account_form.LoginForm()

        variables = {
            'form': form,
            'org_found': org_found,
        }
        return render(request, self.template_name, variables)

    def post(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        form = account_form.LoginForm(request.POST or None)
        err_msg = None
        if form.is_valid():
            user = form.login_request()
            user_org = user.org

            if user_org == org_found:
                if user:
                    login(request, user)
                    if user_org.enrollment_closed:
                        return redirect('home:enrollment-closed')
                    else:
                        return redirect('home:enrolment-form2')
            else:
                err_msg = "This user is not associated with {}!".format(org_short_name)

        variables = {
            'form': form,
            'org_found': org_found,
            'err_msg': err_msg,
        }
        return render(request, self.template_name, variables)

#enrolment form1 - this page is not in use
class EnrolmentForm1(LoginRequiredMixin, View):
    template_name = 'home/enrolment-form1.html'

    def get(self, request):
        org = request.user.org

        variables = {
            'org': org,
        }
        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org

        if request.POST.get('next') == 'next':
            return redirect('home:enrolment-form2')

        variables = {
            'org': org,
        }
        return render(request, self.template_name, variables)

#enrolment form2
class EnrolmentForm2(LoginRequiredMixin, View):
    template_name = 'home/enrolment-form2.html'

    def get(self, request):
        org = request.user.org
        usr = request.user

        form = account_form.EnrolmentForm3(instance=request.user, current_user=usr)

        #Reset values from DB after each page load
        if org.salary_adjustment==True :
            hsa_remaining = request.user.hsa_annual_credits - request.user.hsa_optional
            salary_adjusted = request.user.salary_base - request.user.hsa_optional
        else:
            hsa_remaining = request.user.hsa_annual_credits - request.user.hsa_optional
            salary_adjusted = 0


        # print("On GET")
        # print("HSA Selected value ",request.user.hsa_optional)
        # print("HSA Remaining ",hsa_remaining)
        # print("ADJ Salary ",salary_adjusted)


        if org.insufficient_benefit_credits==False :
            usr.opt_out_bool==False
            usr.save()

        usr.hsa_remaining = formatted_float = "{:.2f}".format(hsa_remaining)
        usr.salary_adjusted = formatted_float = "{:.2f}".format(salary_adjusted)
        usr.save()

        variables = {
            'org': org,
            'form': form,
            'usr': usr,
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }
        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org
        usr = request.user
        form = account_form.EnrolmentForm3(request.POST or None, instance=request.user, current_user=usr)
        err_msg = None

        if request.POST.get('next') == 'next':
            if form.is_valid():

                # retrieve value input from form
                hsa_optional = float(request.POST.get('hsa_optional'))

                #calculate new values and store into the databse
                new_hsa_remaining = float(usr.hsa_annual_credits) - float(hsa_optional)
                usr.hsa_remaining = new_hsa_remaining

                if org.salary_adjustment == True :
                    salary_adjusted_calc = float(usr.salary_base) - float(hsa_optional)
                    usr.salary_adjusted = salary_adjusted_calc
                else :
                    salary_adjusted_calc = 0
                    usr.salary_adjusted = salary_adjusted_calc

                usr.save()

                if request.POST.get('chk') == None :
                    usr.opt_out_bool = False
                    usr.save()
                else:
                    usr.opt_out_bool = True
                    usr.save()

                # print("On POST afer calc")
                # print("HSA Selected value ",hsa_optional)
                # print("HSA Remaining ",new_hsa_remaining)
                # print("ADJ Salary ",salary_adjusted_calc)

            return redirect('home:enrolment-form4')


            variables = {
            'org': org,

            'form': form,
            'err_msg': err_msg,
            'usr': usr,
        }

        return render(request, self.template_name, variables)

#enrolment form3
class EnrolmentForm3(LoginRequiredMixin, View):

# ***************** form code not in use

    template_name = 'home/enrolment-form3.html'

    def get(self, request):
        org = request.user.org
        usr = request.user

        form = account_form.EnrolmentForm3(instance=request.user, current_user=usr)

        variables = {
            'org': org,
            'form': form,
            # 'hsa_remaining': hsa_remaining.decimal_places(2),
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }
        return render(request, self.template_name, variables)


    def post(self, request):
        org = request.user.org
        usr = request.user
        form = account_form.EnrolmentForm3(request.POST or None, instance=request.user, current_user=usr)
        err_msg = None

        if request.POST.get('next') == 'next':
            if request.POST.get('chk') == None:
                if form.is_valid():
                    hsa_optional = float(request.POST.get('hsa_optional'))
                    form.save()
                    request.session['hsa_optional_var'] = hsa_optional
                    usr.opt_out_bool = False
                    usr.save()
                    return redirect('home:enrolment-form4')
            else:
                usr.opt_out_bool = True
                usr.hsa_optional = 0
                usr.save()
                del request.session['hsa_optional_var']
                return redirect('home:enrolment-form4')

        variables = {
            'org': org,
            'form': form,
            'err_msg': err_msg,
        }

        return render(request, self.template_name, variables)

#enrolment form4
class EnrolmentForm4(LoginRequiredMixin, View):
    template_name = 'home/enrolment-form4.html'

    def get(self, request):

        # if not request.session.get('hsa_optional_var'):
        #     return redirect('home:enrolment-form2')

        org = request.user.org
        usr = request.user

        #Reset values from DB after each page load
        hsa_remaining = request.user.hsa_annual_credits - request.user.hsa_optional

        if org.salary_adjustment is True:
            salary_adjusted = request.user.salary_base - request.user.hsa_optional
        else:
            salary_adjusted = 0

        variables = {
            'org': org,
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org
        member = request.user
        usr = request.user

        hsa_remaining = usr.hsa_remaining
        salary_adjusted = usr.salary_adjusted

        if request.POST.get('next') == 'next':
            if member.submitted:
                pass
            else:
                member.submitted = True
                member.save()
                usr.save()

        #*********sent email to org admin and member*********
        #tasks.sent_hsa_detail_to_member.delay(request.user.id, hsa_optional, new_hsa_remaining, salary_adjusted_calc)
        #tasks.sent_hsa_detail_to_admin.delay(request.user.id, hsa_optional, new_hsa_remaining, salary_adjusted_calc)

                # del request.session['hsa_optional_var']
        return redirect('home:enrolment-print')

        variables = {
            'org': org,
        }

        return render(request, self.template_name, variables)

#enrolment form4
class EnrolmentClosed(LoginRequiredMixin, View):
    template_name = 'home/enrolment-closed.html'

    def get(self, request):

        org = request.user.org
        usr = request.user

        #Reset values from DB after each page load
        hsa_remaining = request.user.hsa_annual_credits - request.user.hsa_optional
        salary_adjusted = request.user.salary_base - request.user.hsa_optional

        variables = {
            'org': org,
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org
        member = request.user
        usr = request.user

        hsa_remaining = usr.hsa_remaining
        salary_adjusted = usr.salary_adjusted

        if request.POST.get('next') == 'next':
            if member.submitted:
                pass
            else:
                member.submitted = True
                member.save()
                usr.save()

                # del request.session['hsa_optional_var']
        return redirect('home:enrolment-print')

        variables = {
            'org': org,
        }

        return render(request, self.template_name, variables)


#enrolment printout
class EnrolmentPrint(LoginRequiredMixin, View):
    template_name = 'home/enrolment-print.html'

    def get(self, request):
        org = request.user.org
        usr = request.user
        form = account_form.AdditionalInfoForm(instance=request.user)

        hsa_remaining = request.user.hsa_remaining
        salary_adjusted = request.user.salary_adjusted

        # usr.hsa_remaining = formatted_float = "{:.2f}".format(hsa_remaining)
        # usr.salary_adjusted = formatted_float = "{:.2f}".format(salary_adjusted)
        # usr.save()

        variables = {
            'org': org,
            'form': form,
        }
        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org
        form = account_form.AdditionalInfoForm(request.POST or None, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect('/enrolment/print/?print=yes')

        variables = {
            'org': org,
            'form': form,
        }

        return render(request, self.template_name, variables)



#=======================================================================================================================
#=======================================================================================================================
#                                           Enrolment App Staff Admin login
#=======================================================================================================================
#=======================================================================================================================


class OrgAdminPermissionMixin(object):
    def has_permissions(self, request):

        #return request.user.email == request.user.org.admin_email
        return request.user.is_staff == True
        #permission_required = 'is_staff'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.has_permissions(request):
                return redirect('home:org-admin-login', request.user.org.org_short_name)
            return super(OrgAdminPermissionMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return redirect('home:lhin_links')

#org admin login
class OrgAdminLogin(View):
    template_name = 'home/org-admin/admin-login.html'

    def get(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        form = account_form.OrgAdminLoginForm(org=org_found)

        variables = {
            'org_found': org_found,
            'form': form,
        }

        return render(request, self.template_name, variables)


    def post(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        form = account_form.OrgAdminLoginForm(request.POST or None, org=org_found)

        err_msg = None

        if form.is_valid():
            user = form.login_request()
            user_org = user.org


            if user_org == org_found:
                if user:
                    login(request, user)
                    return redirect('home:org-admin-home', org_short_name=org_short_name)
            else:
                err_msg = "You are not associated to {}".format(org_short_name)

        variables = {
            'org_found': org_found,
            'form': form,
            'err_msg': err_msg,
        }

        return render(request, self.template_name, variables)

#org admin home
class OrgAdminHome(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/home.html'

    def get(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        form = account_form.OrgAdminLoginForm(org=org_found)

        variables = {
            'org_found': org_found,
            'form': form,
        }

        return render(request, self.template_name, variables)

#org admin member view
class OrgMemberView(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/org-member-view.html'

    def get(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        members_list = account_model.UserProfile.objects.filter(org=org_found).order_by('last_name')
        members_count = account_model.UserProfile.objects.filter(org=org_found).count()
        # form = account_form.MemberSearchFormWithOrg(current_org=org_found)
        form = account_form.MemberSearchFormWithOrg()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)

        s_members = None

        variables = {
            'org_found': org_found,
            'page': page,
            'members_count': members_count,
            'form': form,
        }

        return render(request, self.template_name, variables)

    def get_uuid(self):
        uuid = os.urandom(5).hex()

        return uuid

    def  csv_export(self, file_name, members):
        with open('media/csv_output/{}.csv'.format(file_name), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            row_first_line = ['Organization', 'User ID', 'First Name', 'Middle Name', 'Last Name', 'Submitted', 'Last Logged In', 'Effective Date', 'Annual Credits', 'HSA Allocation', 'Taxable Income',  'Additional Info']
            writer.writerow(row_first_line)

            for member in members.order_by('last_name'):
                row = [member.org.org_short_name, member.username, member.first_name, member.middle_name, member.last_name, ("Yes" if member.submitted else "No") , ("Never" if member.last_login==None else (member.last_login.strftime("%Y-%m-%d %I:%M%p"))),  (member.org.date_fiscal_start.strftime("%Y-%m-%d") if member.effective_date==None else (member.effective_date.strftime("%Y-%m-%d"))), member.hsa_annual_credits, member.hsa_optional, member.hsa_remaining,  member.additional_info]
                writer.writerow(row)

            csvfile.close()

    def post(self, request, org_short_name):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        members_list = account_model.UserProfile.objects.filter(org=org_found).order_by('last_name')
        members_count = account_model.UserProfile.objects.filter(org=org_found).count()

        accounts_paginator = Paginator(members_list, 10)
        page_num = request.GET.get('page')
        page = accounts_paginator.get_page(page_num)
        # form = account_form.MemberSearchFormWithOrg(request.POST or None, current_org=org_found)
        form = account_form.MemberSearchFormWithOrg(request.POST or None)
        print('org found value: ',org_found)

        if request.POST.get('export_csv') == 'export_csv':
            uuid = self.get_uuid()
            file_name = str(org_found.org_short_name) + '-member_export-' + datetime.now().strftime("%Y-%m-%d")
            self.csv_export(file_name, members_list)

            return redirect('home:save_file', file_name=file_name)


        s_members = None

        if form.is_valid():
            s_members = form.deploy()
            print('number', s_members.count())


        variables = {
            'org_found': org_found,
            'page': page,
            'members_count': members_count,
            'form': form,
            's_members': s_members,
        }

        return render(request, self.template_name, variables)

def some_streaming_csv_view(request, file_name):
    path = 'media/csv_output/{}.csv'.format(file_name)
    response = StreamingHttpResponse(open(path), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + '{}.csv'.format(file_name)
    return response

#org admin member view
class OrgMemberDetail(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/org-member-detail.html'

    def get(self, request, org_short_name, user_id):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        member = get_object_or_404(account_model.UserProfile, username=user_id)

        if member.org != org_found:
            raise Http404()

        variables = {
            'org_found': org_found,
            'member': member,
        }

        return render(request, self.template_name, variables)

#activate deactivate member
class ActivateDeactivateAccount(OrgAdminPermissionMixin, View):

    def get(self, request, org_short_name, user_id):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        member = get_object_or_404(account_model.UserProfile, username=user_id)

        if member.org != org_found:
            raise Http404()

        usr_is_active = member.is_active

        if usr_is_active:
            member.is_active = False
            member.save()
        else:
            member.is_active = True
            member.save()

        return redirect('home:org-member-detail', org_short_name=org_short_name, user_id=user_id)

#delete member
class OrgMemberDelete(OrgAdminPermissionMixin, View):

    def get(self, request, org_short_name, user_id):

        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        member = get_object_or_404(account_model.UserProfile, username=user_id)

        if member.org != org_found:
            raise Http404()

        member.delete()

        return redirect('home:org-member-view', org_short_name=org_short_name)

#org admin member add
class OrgMemberAdd(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/org-member-add.html'

    def get(self, request, org_short_name):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)

        form = account_form.AddUserForm()
        form.hsa_optional = 0
        form.hsa_remaining = 0

        variables = {
            'org_found': org_found,
            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, org_short_name):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        form = account_form.AddUserForm(request.POST or None)


        if form.is_valid():
            u = form.deploy(org_found)
            return redirect('home:org-member-detail', org_short_name=org_short_name, user_id=u.username)

        variables = {
            'org_found': org_found,
            'form': form,
        }

        return render(request, self.template_name, variables)

#org admin member edit
class OrgMemberEdit(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/org-member-edit.html'

    def get(self, request, org_short_name, user_id):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        user_found = get_object_or_404(account_model.UserProfile, username=user_id, org=org_found)

        form = account_form.ChageUserProfileFromOrgAdmin(instance=user_found)

        variables = {
            'org_found': org_found,
            'user_found': user_found,
            'form': form,
        }

        return render(request, self.template_name, variables)


    def post(self, request, org_short_name, user_id):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        user_found = get_object_or_404(account_model.UserProfile, username=user_id, org=org_found)
        form = account_form.ChageUserProfileFromOrgAdmin(request.POST or None, instance=user_found)

        if form.is_valid():
            if org_found.salary_adjustment is True:
                user_found.salary_base = 0
                user_found.salary_adjusted = 0

            form.save()

        return redirect('home:org-member-detail', org_short_name=org_short_name, user_id=user_id)

        variables = {
            'org_found': org_found,
            'user_found': user_found,
            'form': form,
        }

        return render(request, self.template_name, variables)

#org admin member change password
class OrgMemberChangePassword(OrgAdminPermissionMixin, View):
    template_name = 'home/org-admin/org-member-change-password.html'

    def get(self, request, org_short_name, user_id):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        user_found = get_object_or_404(account_model.UserProfile, username=user_id, org=org_found)

        form = account_form.ChangeUserPasswordForm()

        variables = {
            'org_found': org_found,
            'user_found': user_found,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, org_short_name, user_id):
        org_found = get_object_or_404(account_model.Organization, org_short_name=org_short_name)
        user_found = get_object_or_404(account_model.UserProfile, username=user_id, org=org_found)

        form = account_form.ChangeUserPasswordForm(request.POST or None)

        if form.is_valid():
            form.deploy(user_found.id)

            return redirect('home:org-member-detail', org_short_name=org_short_name, user_id=user_id)

        variables = {
            'org_found': org_found,
            'user_found': user_found,

            'form': form,
        }

        return render(request, self.template_name, variables)
