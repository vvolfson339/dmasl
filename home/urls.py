from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('logout/', views.signout_request, name='logout'),

    path('', views.Home.as_view(), name='home'),

    path('home/', views.Links.as_view(), name='links'),
    path('lhin_links/', views.LHIN_Links.as_view(), name='lhin_links'),

    path('<org_short_name>/', views.Login.as_view(), name='login'),

    path('enrolment/form-1/', views.EnrolmentForm1.as_view(), name='enrolment-form1'),
    path('enrolment/form-2/', views.EnrolmentForm2.as_view(), name='enrolment-form2'),
    path('enrolment/form-3/', views.EnrolmentForm4.as_view(), name='enrolment-form4'),
    path('enrolment/print/', views.EnrolmentPrint.as_view(), name='enrolment-print'),
    path('enrolment/closed/', views.EnrolmentClosed.as_view(), name='enrollment-closed'),

    path('<org_short_name>/admin/login/', views.OrgAdminLogin.as_view(), name='org-admin-login'),
    path('<org_short_name>/admin/', views.OrgAdminHome.as_view(), name='org-admin-home'),

    path('<org_short_name>)/admin/member/view/', views.OrgMemberView.as_view(), name='org-member-view'),
    path('<org_short_name>)/admin/member/<user_id>/detail/', views.OrgMemberDetail.as_view(), name='org-member-detail'),
    path('<org_short_name>)/admin/member/<user_id>/activate-deactivate/', views.ActivateDeactivateAccount.as_view(), name='org-member-activate-deactivate'),
    path('<org_short_name>)/admin/member/<user_id>/delete/', views.OrgMemberDelete.as_view(), name='org-member-delete'),

    path('<org_short_name>)/admin/member/add/', views.OrgMemberAdd.as_view(), name='org-member-add'),

    path('<org_short_name>)/admin/member/<user_id>/edit/', views.OrgMemberEdit.as_view(), name='org-member-edit'),
    path('<org_short_name>)/admin/member/<user_id>/change-password/', views.OrgMemberChangePassword.as_view(), name='org-member-change-password'),

    #end org admin url
]
