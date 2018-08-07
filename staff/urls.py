from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$', views.StaffLogin.as_view(), name='staff-login'),

    url(r'^home/$', views.StaffHome.as_view(), name='staff-home'),

    url(r'^org/$', views.Organization.as_view(), name='org'),
    url(r'^org/add/$', views.AddOrganization.as_view(), name='add-org'),
    url(r'^org/view/$', views.ViewOrganization.as_view(), name='view-org'),
    url(r'^org/(?P<org_id>[0-9]+)/delete/$', views.DeleteOrganization.as_view(), name='delete-org'),
    url(r'^org/(?P<org_id>[0-9]+)/detail/$', views.DetailOrganization.as_view(), name='detail-org'),
    url(r'^org/(?P<org_id>[0-9]+)/edit/$', views.EditOrganization.as_view(), name='edit-org'),
    url(r'^org/(?P<org_id>[0-9]+)/member/$', views.OrganizationMember.as_view(), name='org-member'),

    url(r'^save/(?P<file_name>[a-zA-Z0-9_-]+)/$', views.some_streaming_csv_view, name='save_file'),


    url(r'^member/$', views.Member.as_view(), name='member'),
    url(r'^member/(?P<org_id>[0-9]+)/add/$', views.AddMember.as_view(), name='add-member'),
    url(r'^member/view/$', views.ViewMember.as_view(), name='view-member'),
    url(r'^member/(?P<user_id>[0-9]+)/delete/$', views.DeleteMember.as_view(), name='delete-member'),
    url(r'^member/(?P<user_id>[0-9]+)/detail/$', views.DetailMember.as_view(), name='detail-member'),
    url(r'^member/(?P<user_id>[0-9]+)/activate-deactivate/$', views.ActivateDeactivateAccount.as_view(), name='activate-deactivate-account'),
    url(r'^member/(?P<user_id>[0-9]+)/change-password/$', views.ChangePassword.as_view(), name='change-password'),
    url(r'^member/(?P<user_id>[0-9]+)/edit/$', views.EditMember.as_view(), name='edit-member'),


    url(r'^member/upload/$', views.MemberUpload.as_view(), name='member-upload'),

]
