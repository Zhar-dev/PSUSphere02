from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime

from django.views.generic import View

from django.db import models

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"


class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass


def StudentCountByProgram(request):
    # Fetching student counts per program
    program_counts = Student.objects.values('program__prog_name').annotate(count=Count('program')).order_by('-count')

    # Extracting labels (program names) and counts
    labels = [item['program__prog_name'] for item in program_counts]
    counts = [item['count'] for item in program_counts]

    data = {
        'labels': labels,
        'counts': counts,
    }
    return JsonResponse(data)


def OrganizationGraphData(request):
    # Your code to fetch organization graph data from the database or any other source
    # Example data for demonstration purposes
    labels = ['X', 'Y', 'Z']
    counts = [50, 70, 30]
    
    data = {
        'labels': labels,
        'counts': counts,
    }
    
    return JsonResponse(data)


def chart_students(request):
    program_counts = Program.objects.annotate(student_count=models.Count('student'))
    labels = [program.prog_name for program in program_counts]
    counts = [program.student_count for program in program_counts]
    return JsonResponse({'labels': labels, 'counts': counts})


def chart_org_members(request):
    org_counts = Organization.objects.annotate(member_count=models.Count('orgmember'))
    labels = [org.name for org in org_counts]
    counts = [org.member_count for org in org_counts]
    return JsonResponse({'labels': labels, 'counts': counts})


def chart_colleges(request):
    # Query the database to get data for the college pie chart
    # For example, let's say you want to count the number of students per college
    college_counts = College.objects.annotate(student_count=models.Count('program__student'))
    labels = [college.college_name for college in college_counts]
    counts = [college.student_count for college in college_counts]
    
    # Return the data as JSON response with a unique name
    return JsonResponse({'college_labels': labels, 'college_counts': counts})


# Create your views here.
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'organization/org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                           Q(description__icontains=query) |
                           Q(college__college_name__icontains=query))
        return qs


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_add.html'
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_edit.html'
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organization/org_del.html'
    success_url = reverse_lazy('organization-list')


class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'org_member/orgmember_list.html'
    paginate_by = 10
    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(organization__name__icontains=query))
        return qs


class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member/orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member/orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')


class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member/orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')


class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student/stud_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(firstname__icontains=query) |
                        Q (lastname__icontains=query) |
                        Q (middlename__icontains=query) |
                        Q (student_id__icontains=query))
        return qs


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/stud_add.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/stud_edit.html'
    success_url = reverse_lazy('student-list')


class StudentDeleteView(DeleteView):
    model = Student
    form_class = StudentForm
    template_name = 'student/stud_del.html'
    success_url = reverse_lazy('student-list')


class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college/college_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/college_add.html'
    success_url = reverse_lazy('college-list')


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/college_edit.html'
    success_url = reverse_lazy('college-list')


class CollegeDeleteView(DeleteView):
    model = College
    form_class = CollegeForm
    template_name = 'college/college_del.html'
    success_url = reverse_lazy('college-list')


class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program/program_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
                        Q (college__college_name__icontains=query))
        return qs


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/program_add.html'
    success_url = reverse_lazy('program-list')


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/program_edit.html'
    success_url = reverse_lazy('program-list')


class ProgramDeleteView(DeleteView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/program_del.html'
    success_url = reverse_lazy('program-list')


