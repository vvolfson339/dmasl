from django.urls import path, include

from . import views

app_name = 'staff'

urlpatterns = [

    path('login/', views.StaffLogin.as_view(), name='staff-login'),

    path('home/', views.StaffHome.as_view(), name='staff-home'),

    path('org/', views.Organization.as_view(), name='org'),
    path('org/add/', views.AddOrganization.as_view(), name='add-org'),
    path('org/view/', views.ViewOrganization.as_view(), name='view-org'),
    path('org/<org_id>/delete/', views.DeleteOrganization.as_view(), name='delete-org'),
    path('org/<org_id>/detail/', views.DetailOrganization.as_view(), name='detail-org'),
    path('org/<org_id>/edit/', views.EditOrganization.as_view(), name='edit-org'),
    path('org/<org_id>/member/', views.OrganizationMember.as_view(), name='org-member'),

    path('save/<file_name>/', views.some_streaming_csv_view, name='save_file'),

    path('member/', views.Member.as_view(), name='member'),
    path('member/<org_id>/add/', views.AddMember.as_view(), name='add-member'),
    path('member/view/', views.ViewMember.as_view(), name='view-member'),
    path('member/<user_id>/delete/', views.DeleteMember.as_view(), name='delete-member'),
    path('member/<user_id>/detail/', views.DetailMember.as_view(), name='detail-member'),
    path('member/<user_id>/activate-deactivate/', views.ActivateDeactivateAccount.as_view(), name='activate-deactivate-account'),
    path('member/<user_id>/activate-deactivate-staff/', views.ActivateDeactivateStaffStatus.as_view(), name='activate-deactivate-staff'),

    path('member/<user_id>/change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('member/<user_id>/edit/', views.EditMember.as_view(), name='edit-member'),

    path('member/upload/', views.MemberUpload.as_view(), name='member-upload'),

]
