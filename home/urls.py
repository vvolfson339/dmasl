from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^logout/$', views.signout_request, name='logout'),

    url(r'^$', views.Home.as_view(), name='home'),


    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/$', views.Login.as_view(), name='login'),

    url(r'^enrolment/form-1/$', views.EnrolmentForm1.as_view(), name='enrolment-form1'),
    url(r'^enrolment/form-2/$', views.EnrolmentForm2.as_view(), name='enrolment-form2'),
    #url(r'^enrolment/form-3/$', views.EnrolmentForm3.as_view(), name='enrolment-form3'),
    url(r'^enrolment/form-3/$', views.EnrolmentForm4.as_view(), name='enrolment-form4'),
    url(r'^enrolment/print/$', views.EnrolmentPrint.as_view(), name='enrolment-print'),


    #org admin url
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/login/$', views.OrgAdminLogin.as_view(), name='org-admin-login'),
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/$', views.OrgAdminHome.as_view(), name='org-admin-home'),

    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/view/$', views.OrgMemberView.as_view(), name='org-member-view'),
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/(?P<user_id>[0-9a-zA-Z-_.]+)/detail/$', views.OrgMemberDetail.as_view(), name='org-member-detail'),
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/(?P<user_id>[0-9a-zA-Z-_.]+)/activate-deactivate/$', views.ActivateDeactivateAccount.as_view(), name='org-member-activate-deactivate'),
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/(?P<user_id>[0-9a-zA-Z-_.]+)/delete/$', views.OrgMemberDelete.as_view(), name='org-member-delete'),


    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/add/$', views.OrgMemberAdd.as_view(), name='org-member-add'),

    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/(?P<user_id>[0-9a-zA-Z-_.]+)/edit/$', views.OrgMemberEdit.as_view(), name='org-member-edit'),
    url(r'^(?P<org_short_name>[0-9a-zA-Z-_.]+)/admin/member/(?P<user_id>[0-9a-zA-Z-_.]+)/change-password/$', views.OrgMemberChangePassword.as_view(), name='org-member-change-password'),
    #end org admin url
]
