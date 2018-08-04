from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^logout/$', views.signout_request, name='logout'),

    url(r'^$', views.Home.as_view(), name='home'),


    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/$', views.Login.as_view(), name='login'),

    url(r'^enrolment/form-1/$', views.EnrolmentForm1.as_view(), name='enrolment-form1'),
    url(r'^enrolment/form-2/$', views.EnrolmentForm2.as_view(), name='enrolment-form2'),
    url(r'^enrolment/form-3/$', views.EnrolmentForm3.as_view(), name='enrolment-form3'),
    url(r'^enrolment/form-4/$', views.EnrolmentForm4.as_view(), name='enrolment-form4'),
    url(r'^enrolment/print/$', views.EnrolmentPrint.as_view(), name='enrolment-print'),

]
