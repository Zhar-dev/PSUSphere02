from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView, OrgMemberList , OrgMemberCreateView, OrgMemberUpdateView, OrgMemberDeleteView,  StudentList , StudentCreateView, StudentUpdateView, StudentDeleteView,  CollegeList , CollegeCreateView, CollegeUpdateView, CollegeDeleteView, ProgramList , ProgramCreateView, ProgramUpdateView, ProgramDeleteView, ChartView, StudentCountByProgram, OrganizationGraphData, chart_colleges
from studentorg import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),

    path('dashboard_chart', ChartView.as_view(), name='dashboard-chart'),
    path('student-count-by-program/', StudentCountByProgram, name='student-count-by-program'),
    path('organization-graph-data/', OrganizationGraphData, name='organization-graph-data'),
    path('pie-chart/students/', views.chart_students, name='pie_chart_students'),
    path('pie-chart/org-members/', views.chart_org_members, name='pie_chart_org_members'),
    path('pie-chart/colleges/', chart_colleges, name='pie_chart_colleges'),

    path('organization-list/', OrganizationList.as_view(), name='organization-list'),
    path('organization-list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization-list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization-list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),

    path('orgmember_list', OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<pk>', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete',OrgMemberDeleteView.as_view(), name='orgmember-delete'),

    path('student_list', StudentList.as_view(), name='student-list'),
    path('student_list/add', StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete', StudentDeleteView.as_view(), name='student-delete'),

    path('college_list', CollegeList.as_view(), name='college-list'),
    path('college_list/add', CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/delete/<pk>', CollegeDeleteView.as_view(), name='college-delete'),

    path('program_list', ProgramList.as_view(), name='program-list'),
    path('program_list/add', ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', ProgramDeleteView.as_view(), name='program-delete'),

    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^Logout/$', auth_views.LogoutView.as_view(), name='logout'),

]
