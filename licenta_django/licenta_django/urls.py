"""
URL configuration for licenta_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ontology import views as ontology_view
from dashboard import views as dashboard_view
from student import views as student_view

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/students/$', student_view.students),
    re_path(r'^api/student/$', student_view.create_student),
    # path('api-auth/', include('rest_framework.urls')),
    re_path(r'^api/goals/$', ontology_view.get_goals),
    re_path(r'^api/goals/([0-9]+)/$', student_view.get_goals_by_id),
    re_path(r'^api/interests/$', ontology_view.get_interests),
    re_path(r'^api/interests/([0-9]+)/$', student_view.get_interests_by_id),
    re_path(r'^api/vark_questions/$', student_view.vark_questions),
    re_path(r'^api/level_questions/$', student_view.level_questions),
    re_path(r'^api/calculate_vark/$', student_view.vark_model),
    re_path(r'^api/calculate_level/$', student_view.level_model),
    re_path(r'^api/domains/$', ontology_view.all_domains),
    re_path(r'^api/domains/([a-zA-Z_]+)/$', ontology_view.courses_by_domain),
    re_path(r'^api/users/$', student_view.get_user_by_username_and_password, name='get_user_by_username_and_password'),
    re_path(r'^api/curricula/$', ontology_view.generate_curricula),
    re_path(r'^api/my_courses/([0-9]+)/$', student_view.get_student_courses),
    re_path(r'api/student/([0-9]+)/course_details/([a-zA-Z_]+)/$', dashboard_view.course_details),
    re_path(r'^api/student_details/([0-9]+)/$', student_view.student_details),
    re_path(r'^api/update_course_status/$', dashboard_view.update_course_status),
    re_path(r'^api/project/([0-9]+)/$', dashboard_view.get_project_by_enrollment),
    re_path(r'^api/dashboard/current_courses/([0-9]+)$', dashboard_view.get_current_courses),
    re_path(r'^api/dashboard/student_data/([0-9]+)/$', dashboard_view.get_student_data),
    re_path(r'^api/dashboard/stats/$', dashboard_view.get_stats),

]
