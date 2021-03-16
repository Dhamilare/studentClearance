from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.forms import forms
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

@login_required(login_url= 'login')
def home(request):
    
    #awaiting_clearance = School.objects.filter(staff = request.user.is_staff, is_accessed = False).count()
    cleared = HOD.objects.filter(is_accessed = True).count()
    not_cleared = HOD.objects.filter(is_accessed = False).count()
    all_students = Student.objects.count()

    #s_awaiting_clearance = Library.objects.filter(staff = request.user.is_staff, is_accessed = False).count()
    s_cleared = School.objects.filter(is_accessed = True).count()
    s_not_cleared = School.objects.filter(is_accessed = False).count()

    #l_awaiting_clearance = Busary.objects.filter(staff = request.user.is_staff, is_accessed = False).count()
    l_cleared = Library.objects.filter(is_accessed = True).count()
    l_not_cleared = Library.objects.filter(is_accessed = False).count()

    #b_awaiting_clearance = Clearance.objects.filter(staff = request.user.is_staff, is_accessed = False).count()
    b_cleared = Busary.objects.filter(is_accessed = True).count()
    b_not_cleared = Busary.objects.filter(is_accessed = False).count()

    all_staff = Staff.objects.count()

    all_clearance = Clearance.objects.count()

    issue_log = Feedback.objects.filter(staff__user = request.user).count()

    context = {

        'not_cleared': not_cleared,
        'all_students': all_students,
        'cleared': cleared,
        's_cleared': s_cleared,
        's_not_cleared': s_not_cleared,
        'l_cleared': l_cleared,
        'l_not_cleared': l_not_cleared,
        'b_cleared': b_cleared,
        'b_not_cleared': b_not_cleared,
        'all_staff' : all_staff,
        'all_clearance': all_clearance,
        'issue_log' : issue_log
    }

    return render(request, 'pages/dashboard.html', context)


def staffLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        staff = authenticate(request, username = username, password = password)

        if staff is not None:
            login(request, staff)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password not correct!')
            return redirect('login')
            
    return render(request, 'login.html')

def staffLogout(request):
    logout(request)
    return redirect('login')


def staffRegister(request):
    form = staffRegisterForm()
    if request.method == 'POST':
        form = staffRegisterForm(request.POST or None)
        if form.is_valid():
            staff = form.cleaned_data.get('first_name')
            staff_obj = form.save(commit = False)
            staff_obj.user = User.objects.create_user(

                password = form.cleaned_data.get('password2'),
                username = form.cleaned_data.get('username'),
            )
            staff_obj.save()
            messages.success(request, 'Account for ' + staff + ' was created successfully!')
            return redirect('staffs')

    else:
        form = staffRegisterForm()
    return render(request, 'pages/admin/add_staff.html', {'form':form})

@login_required(login_url= 'login')
def addStudent(request):
    form = studentRegisterForm()
    if request.method == 'POST':
        form = studentRegisterForm(request.POST or None)
        if form.is_valid():
            student = form.cleaned_data.get('surname')
            stud_obj = form.save(commit = False)
            stud_obj.user = User.objects.create_user(

                password = form.cleaned_data.get('password2'),
                username = form.cleaned_data.get('username'),
            )
            stud_obj.save()
            messages.success(request, 'Account for ' + student + ' was created successfully!')
            return redirect('students')
    else:
        form = studentRegisterForm()
    return render(request, 'pages/admin/add_student.html', {'form':form})

@login_required(login_url= 'login')
def clearance(request):
    hd = Staff.objects.all()
    ls = []
    for ls in hd:
        ls.email
    status = False
    try:
        HOD.objects.get(student__user = request.user)
        status = True
    except HOD.DoesNotExist:
        status = False
    form = clearanceForm()
    if request.method == 'POST':
        level = request.POST['level']
        department = request.POST['department']
        gender = request.POST['gender']
        other_names = request.POST['other_names']
        surname = request.POST['surname']
        matric_no = request.POST['matric_no']
        hod_email = request.POST['hod_email']
        form = clearanceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.student = request.user.student
            clear = form.save(commit=False)
            clear.matric_no = matric_no
            clear.gender = gender
            clear.department = department
            clear.level = level
            clear.surname = surname
            clear.other_names = other_names
            clear.hod_email = hod_email
            clear.status = True
            clear.save()
            qs = HOD.objects.filter(is_accessed = False).count()
            if qs >= 5:
                staff = HOD.objects.filter(hod_email = request.POST.get('hod_email'))
                current_site = get_current_site(request)
                send_mail(

                'Please Attend To The Following Students',
                'Your attention is needed in accessing & clearing students that are awaiting clearance. click the link below to do so \n http://{0}{1}'.format
                (current_site.domain, clear.get_absolute_url()),
                settings.EMAIL_HOST_USER,
                [clear.hod_email],fail_silently = False

                ) 
            #messages.success(request, 'Submitted Successfully!')
            return redirect('results')
    else:
        form = clearanceForm()

    return render(request, 'pages/clearance.html', {'form':form, 'status': status, 'ls':ls})


@login_required(login_url= 'login')
def ToSchoolOfficer(request, slug):
    from datetime import datetime
    dt = datetime.now()
    ans = dt.strftime('%Y-%m-%d %H:%M:%S')
    qs = HOD.objects.get(slug = slug)
    if qs.is_accessed != True:
        qs.is_accessed = True
    form = HODForm()
    if request.method == 'POST':
        level = request.POST['level']
        department = request.POST['department']
        gender = request.POST['gender']
        other_names = request.POST['other_names']
        surname = request.POST['surname']
        matric_no = request.POST['matric_no']
        signature = request.POST['signature']
        date_signed = request.POST['date_signed']
        form = HODForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.matric_no = matric_no
            clear.gender = gender
            clear.department = department
            clear.level = level
            clear.surname = surname
            clear.other_names = other_names
            clear.save()
            qs.save()
            messages.success(request, 'Cleared Successfully!')
            return redirect('cleared_students')
    else:
        form = HODForm()

    return render(request, 'pages/hod/clearance_details.html', {'form':form, 'qs': qs, 'ans':ans})

@login_required(login_url= 'login')
def ToLibrary(request, slug):
    from datetime import datetime
    dt = datetime.now()
    ans = dt.strftime('%Y-%m-%d %H:%M:%S')
    qs = School.objects.get(slug = slug)
    if qs.is_accessed != True:
        qs.is_accessed = True
    form = LibraryForm()
    if request.method == 'POST':
        level = request.POST['level']
        department = request.POST['department']
        gender = request.POST['gender']
        other_names = request.POST['other_names']
        surname = request.POST['surname']
        matric_no = request.POST['matric_no']
        signature = request.POST['signature']
        date_signed = request.POST['date_signed']
        form = LibraryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.matric_no = matric_no
            clear.gender = gender
            clear.department = department
            clear.level = level
            clear.surname = surname
            clear.other_names = other_names
            clear.save()
            qs.save()
            messages.success(request, 'Cleared Successfully!')
            return redirect('school_cleared_students')
    else:
        form = LibraryForm()

    return render(request, 'pages/school/clearance_details.html', {'form':form, 'qs': qs, 'ans':ans})

@login_required(login_url= 'login')
def ToBusary(request, slug):
    from datetime import datetime
    dt = datetime.now()
    ans = dt.strftime('%Y-%m-%d %H:%M:%S')
    qs = Library.objects.get(slug = slug)
    if qs.is_accessed != True:
        qs.is_accessed = True
    form = BusaryForm()
    if request.method == 'POST':
        level = request.POST['level']
        department = request.POST['department']
        gender = request.POST['gender']
        other_names = request.POST['other_names']
        surname = request.POST['surname']
        matric_no = request.POST['matric_no']
        signature = request.POST['signature']
        date_signed = request.POST['date_signed']
        form = BusaryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.matric_no = matric_no
            clear.gender = gender
            clear.department = department
            clear.level = level
            clear.surname = surname
            clear.other_names = other_names
            clear.save()
            qs.save()
            messages.success(request, 'Cleared Successfully!')
            return redirect('library_cleared_students')
    else:
        form = LibraryForm()

    return render(request, 'pages/library/clearance_details.html', {'form':form, 'qs': qs, 'ans':ans})

@login_required(login_url= 'login')
def FinalClearance(request, slug):
    from datetime import datetime
    dt = datetime.now()
    ans = dt.strftime('%Y-%m-%d %H:%M:%S')
    qs = Busary.objects.get(slug = slug)
    hd = School.objects.get(slug = slug)
    lb = Library.objects.get(slug = slug)
    if qs.is_accessed != True:
        qs.is_accessed = True
    form = ClearedForm()
    if request.method == 'POST':
        level = request.POST['level']
        department = request.POST['department']
        gender = request.POST['gender']
        other_names = request.POST['other_names']
        surname = request.POST['surname']
        matric_no = request.POST['matric_no']
        signature = request.POST['signature']
        hod = request.POST['hod']
        school_officer = request.POST['school_officer']
        library = request.POST['library']
        date_signed = request.POST['date_signed']
        form = ClearedForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.matric_no = matric_no
            clear.gender = gender
            clear.department = department
            clear.level = level
            clear.surname = surname
            clear.hod = hod
            clear.school_officer = school_officer
            clear.library = library
            clear.other_names = other_names
            clear.save()
            qs.save()
            messages.success(request, 'Cleared Successfully!')
            return redirect('busary_cleared_students')
    else:
        form = ClearedForm()

    return render(request, 'pages/busary/clearance_details.html', {'form':form, 'qs': qs, 'ans':ans, 'lb': lb, 'hd': hd})

@login_required(login_url= 'login')
def HodIssues(request, slug):
    form = IssueForm()
    hd = HOD.objects.get(slug = slug)
    if request.method == 'POST':
        student = request.POST['student']
        matric_no = request.POST['matric_no']
        department = request.POST['department']
        form = IssueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.student = student
            clear.matric_no = matric_no
            clear.department = department
            clear.save()
            messages.success(request, 'Issues Submitted Successfully!')
            return redirect('issues_details')
    else:
        form = IssueForm()

    return render(request, 'pages/hod/issues.html', {'form':form, 'hd':hd})

@login_required(login_url= 'login')
def SchoolIssues(request, slug):
    form = IssueForm()
    sc = School.objects.get(slug = slug)
    if request.method == 'POST':
        student = request.POST['student']
        matric_no = request.POST['matric_no']
        department = request.POST['department']
        form = IssueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.student = student
            clear.matric_no = matric_no
            clear.department = department
            clear.save()
            messages.success(request, 'Issues Submitted Successfully!')
            return redirect('busary_issues_details')
    else:
        form = IssueForm()

    return render(request, 'pages/school/issues.html', {'form':form, 'sc':sc})

@login_required(login_url= 'login')
def LibraryIssues(request, slug):
    form = IssueForm()
    lb = Library.objects.get(slug = slug)
    if request.method == 'POST':
        student = request.POST['student']
        matric_no = request.POST['matric_no']
        department = request.POST['department']
        form = IssueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.student = student
            clear.matric_no = matric_no
            clear.department = department
            clear.save()
            messages.success(request, 'Issues Submitted Successfully!')
            return redirect('issues_details')
    else:
        form = IssueForm()

    return render(request, 'pages/library/issues.html', {'form':form, 'lb':lb})

@login_required(login_url= 'login')
def BusaryIssues(request, slug):
    form = IssueForm()
    bs = Busary.objects.get(slug = slug)
    if request.method == 'POST':
        student = request.POST['student']
        matric_no = request.POST['matric_no']
        department = request.POST['department']
        form = IssueForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.instance.staff = request.user.staff
            clear = form.save(commit=False)
            clear.student = student
            clear.matric_no = matric_no
            clear.department = department
            clear.save()
            messages.success(request, 'Issues Submitted Successfully!')
            return redirect('busary_issues_details')
    else:
        form = IssueForm()

    return render(request, 'pages/busary/issues.html', {'form':form, 'bs':bs})

class HODListView(LoginRequiredMixin, ListView):
    template_name = 'pages/hod/clearance_list.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = HOD.objects.filter(is_accessed = True)
        return qs

class HODNotClearedListView(LoginRequiredMixin, ListView):
    template_name = 'pages/hod/new_clearance.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = HOD.objects.filter(is_accessed = False)
        return qs

class SchoolNotClearedListView(LoginRequiredMixin, ListView):
    template_name = 'pages/school/new_clearance.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = School.objects.filter(is_accessed = False)
        hd = HOD.objects.all()
        queryset = zip(qs, hd)
        return queryset

class LibraryNotClearedListView(LoginRequiredMixin, ListView):
    template_name = 'pages/library/new_clearance.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = Library.objects.filter(is_accessed = False)
        hd = HOD.objects.all()
        queryset = zip(qs, hd)
        return queryset

class BusaryNotClearedListView(LoginRequiredMixin, ListView):
    template_name = 'pages/busary/new_clearance.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = Busary.objects.filter(is_accessed = False)
        hd = HOD.objects.all()
        lb = Library.objects.all()
        so = School.objects.all()
        queryset = zip(qs, hd, lb, so)
        return queryset

class SchoolOfficerListView(LoginRequiredMixin, ListView):
    template_name = 'pages/school/clearance_list.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = School.objects.filter(is_accessed = True)
        return qs

class LibraryListView(LoginRequiredMixin, ListView):
    template_name = 'pages/library/clearance_list.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = Library.objects.filter(is_accessed = True)
        return qs

class BusaryListView(LoginRequiredMixin, ListView):
    template_name = 'pages/busary/cleared_students.html'
    context_object_name = 'clearances'
    ordering = ['-id']

    def get_queryset(self):
        qs = Busary.objects.filter(is_accessed = True)
        hd = HOD.objects.all()
        lb = Library.objects.all()
        so = School.objects.all()
        cl = Clearance.objects.all()
        queryset = zip(qs, hd, lb, so, cl)
        return queryset

class ClearanceListView(LoginRequiredMixin, ListView):
    template_name = 'pages/result.html'
    context_object_name = 'results'

    def get_queryset(self):
        qs = HOD.objects.filter(matric_no = self.request.user.student.matric_no)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cleared"] = Clearance.objects.filter(surname = self.request.user.student.surname)
        return context
    
       
class ClearanceFormListView(LoginRequiredMixin, ListView):
    template_name = 'pages/clearance_form.html'
    context_object_name = 'clearance_details'

    def get_queryset(self):
        cl = Clearance.objects.filter(matric_no = self.request.user.student.matric_no)
        hd = HOD.objects.filter(matric_no = self.request.user.student.matric_no)
        bs = Busary.objects.all()
        lb = Library.objects.all()
        so = School.objects.all()
        queryset = zip(cl, hd, bs, lb, so)
        return queryset


class IssuesListView(LoginRequiredMixin, ListView):
    context_object_name = 'issues'
    template_name = 'pages/hod/issue_details.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Feedback.objects.filter(staff = self.request.user.staff)
        return qs

class SchoolIssuesListView(LoginRequiredMixin, ListView):
    context_object_name = 'issues'
    template_name = 'pages/school/issue_details.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Feedback.objects.filter(staff = self.request.user.staff)
        return qs

class LibraryIssuesListView(LoginRequiredMixin, ListView):
    context_object_name = 'issues'
    template_name = 'pages/library/issue_details.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Feedback.objects.filter(staff = self.request.user.staff)
        return qs

class BusaryIssuesListView(LoginRequiredMixin, ListView):
    context_object_name = 'issues'
    template_name = 'pages/busary/issue_details.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Feedback.objects.filter(staff = self.request.user.staff)
        return qs
        
class FeedbackListView(LoginRequiredMixin, ListView):
    context_object_name = 'feedbacks'
    template_name = 'pages/feedback.html'

    def get_queryset(self):
        fb = Feedback.objects.filter(matric_no = self.request.user.student.matric_no)
        return fb
       
class StudentListView(LoginRequiredMixin, ListView):
    context_object_name = 'students'
    template_name = 'pages/admin/students.html'

    def get_queryset(self):
        student = Student.objects.all()
        return student

class StaffListView(LoginRequiredMixin, ListView):
    context_object_name = 'staffs'
    template_name = 'pages/admin/staffs.html'

    def get_queryset(self):
        staff = Staff.objects.all()
        return staff
       
       