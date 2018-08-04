from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib.auth.views import login, logout

from account import models as account_model
from account import forms as account_form


from django.contrib.auth.mixins import LoginRequiredMixin



# sign out
def signout_request(request):
    logout(request)

    direction = request.GET.get('from')

    if direction == 'staff':
        return redirect('staff:staff-login')
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

        form = account_form.EnrolmentForm2(instance=request.user)

        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org

        form = account_form.EnrolmentForm2(request.POST or None, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home:enrolment-form3')



        variables = {
            'org': org,

            'form': form,
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


        variables = {
            'org': org,
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


        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        org = request.user.org

        usr = request.user

        hsa_remaining_db = usr.hsa_remaining

        form = account_form.AdditionalInfoForm(request.POST or None, instance=request.user)


        if form.is_valid():
            form.save()

            if request.session.get('hsa_optional_var'):
                hsa_optional = float(request.session['hsa_optional_var'])

                new_hsa_remaining = float(hsa_remaining_db - hsa_optional)
                usr.hsa_remaining = new_hsa_remaining
                usr.save()

                del request.session['hsa_optional_var']


            return redirect('/enrolment/print/?print=yes')


        variables = {
            'org': org,

            'form': form,
        }

        return render(request, self.template_name, variables)












