from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib.auth.views import login, logout
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from account import models as account_model
from account import forms as account_form

from . import tasks



# sign out
def signout_request(request):
    logout(request)

    direction = request.GET.get('from')

    if direction == 'staff':
        return redirect('staff:staff-login')
    elif direction == 'client':
        return redirect('home:login', org_short_name=request.GET.get('org'))
    else:
        return redirect('home:home')




#home
class Home(View):
    template_name = 'home/home.html'

    def get(self, request):

        variables = {

        }

        return render(request, self.template_name, variables)



#OrganizationDetail
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

                    return redirect('home:enrolment-form1')
            else:
                err_msg = "You are not associated to {}".format(org_short_name)

        variables = {
            'form': form,

            'org_found': org_found,

            'err_msg': err_msg,
        }

        return render(request, self.template_name, variables)




#enrolment form1
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

        #form = account_form.EnrolmentForm2(instance=request.user)
        form = account_form.EnrolmentForm3(instance=request.user, current_user=usr)

        variables = {
            'org': org,

            'form': form,

            'usr': usr,
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
                if form.is_valid():
                    hsa_optional = float(request.POST.get('hsa_optional'))

                    form.save()

                    request.session['hsa_optional_var'] = hsa_optional

                    usr.opt_out_bool = True
                    usr.save()

                    return redirect('home:enrolment-form4')

        #form = account_form.EnrolmentForm2(request.POST or None, instance=request.user)

        #if form.is_valid():
         #   form.save()
          #  return redirect('home:enrolment-form3')



        variables = {
            'org': org,

            'form': form,
            'err_msg': err_msg,

            'usr': usr,
        }

        return render(request, self.template_name, variables)





class EnrolmentForm3(LoginRequiredMixin, View):
    template_name = 'home/enrolment-form3.html'

    def get(self, request):
        org = request.user.org

        usr = request.user

        form = account_form.EnrolmentForm3(instance=request.user, current_user=usr)

        variables = {
            'org': org,

            'form': form,
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






class EnrolmentForm4(LoginRequiredMixin, View):
    template_name = 'home/enrolment-form4.html'

    def get(self, request):
        org = request.user.org

        current_hsa_selection = request.session['hsa_optional_var']

        hsa_remaining = request.user.hsa_remaining - current_hsa_selection
        salary_adjusted = request.user.salary_adjusted - current_hsa_selection

        variables = {
            'org': org,
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org
        member = request.user

        if request.POST.get('next') == 'next':
            if member.submitted:
                pass
            else:
                member.submitted = True
                member.save()

            return redirect('home:enrolment-print')

        variables = {
            'org': org,
        }

        return render(request, self.template_name, variables)









class EnrolmentPrint(LoginRequiredMixin, View):
    template_name = 'home/enrolment-print.html'

    def get(self, request):
        org = request.user.org

        form = account_form.AdditionalInfoForm(instance=request.user)

        current_hsa_selection = request.session['hsa_optional_var']

        hsa_remaining = request.user.hsa_remaining - current_hsa_selection
        salary_adjusted = request.user.salary_adjusted - current_hsa_selection


        variables = {
            'org': org,

            'form': form,
            'hsa_remaining': hsa_remaining,
            'salary_adjusted': salary_adjusted,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org

        usr = request.user

        hsa_remaining_db = usr.hsa_remaining
        salary_adjusted_db = usr.salary_adjusted

        form = account_form.AdditionalInfoForm(request.POST or None, instance=request.user)

        if form.is_valid():
            form.save()

            if request.session.get('hsa_optional_var'):
                hsa_optional = float(request.session['hsa_optional_var'])

                new_hsa_remaining = float(hsa_remaining_db - hsa_optional)
                usr.hsa_remaining = new_hsa_remaining

                salary_adjusted_calc = float(salary_adjusted_db - hsa_optional)
                usr.salary_adjusted = salary_adjusted_calc

                usr.save()

                #sent email to org admin and member
                tasks.sent_hsa_detail_to_member.delay(request.user.id, hsa_optional, new_hsa_remaining, salary_adjusted_calc)
                tasks.sent_hsa_detail_to_admin.delay(request.user.id, hsa_optional, new_hsa_remaining, salary_adjusted_calc)

                #del request.session['hsa_optional_var']

            return redirect('/enrolment/print/?print=yes')


        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)







#=======================================================================================================================
#=======================================================================================================================
#                                           organization admin login
#=======================================================================================================================
#=======================================================================================================================



class OrgAdminPermissionMixin(object):
    def has_permissions(self, request):

        return request.user.email == request.user.org.admin_email

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.has_permissions(request):
                return redirect('home:org-admin-login', request.user.org.org_short_name)
            return super(OrgAdminPermissionMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return redirect('home:home')




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

        members = account_model.UserProfile.objects.filter(org=org_found).order_by('-join_date')
        members_count = account_model.UserProfile.objects.filter(org=org_found).count()

        variables = {
            'org_found': org_found,

            'members': members,
            'members_count': members_count,
        }

        return render(request, self.template_name, variables)



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





#=======================================================================================================================
#=======================================================================================================================
#                                           organization admin login
#=======================================================================================================================
#=======================================================================================================================











