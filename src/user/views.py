
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Case, When, Value, IntegerField, F
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .models import User, Student, Advisor, Administrator, Plan, Course, CS_Major_BA, CS_Major_BS, CS_Major_Core, Econ_major, ScienceComponent
import uuid
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import get_prereqs_from_api, sort_plans_by_current, get_full_courses_dict
from .forms import SelectCourseForm, DepartmentSearchForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# for prereq JSON solution
import json


# accessing the website with / renders the login.html page
def index(request):
    logger.debug('Debug message')
    logger.info('Info message')
    return render(request, 'user/login.html')

# accessing the website with /advisor_login/ renders the advisor_login.html page
def advisor_login(request):
    return render(request, 'user/advisor_login.html')

from django.shortcuts import render

# global constant for SEMESTERS bc these never change and are used in 2 diff views
SEMESTERS = ['freshman_fall', 'freshman_spring', 'sophomore_fall', 
             'sophomore_spring', 'junior_fall', 'junior_spring', 
             'senior_fall', 'senior_spring']

# Landing page
def landing(request):
    # This assumes you have a way to link your User to a Student, e.g., via email or a OneToOneField
    user = request.user

    context = {}
    # if user exists in Admin table
    if User.get_user(user.email, Administrator):
        administrator = Administrator.objects.get(email=user.email)
        context = {
            'user': user,
            'user_type': 'administrator',
            'name': administrator.name,
        }
    
    # if user exists in Advisor table
    elif User.get_user(user.email, Advisor):
        advisor = Advisor.objects.get(email=user.email)

        context = {
            'user': user,
            'user_type': 'advisor',
            'name': advisor.name,
            'school': advisor.school,
        }
    
    # if user is neither Advisor nor Admin, they are Student
    else:
        student = User.get_user(user.email, Student)

        # if user isn't in the Student table, add them
        if not student:
            new_student = Student(name=user.first_name, email=user.email)
            new_student.save()

            student = Student.objects.get(email=user.email)

        # in this instance redirect takes a view as its parameter
        if not student.first_login_completed:
            return redirect('user:update_info') # redirect users to update info upon first login
    
        # Progress Bar Tings
        # Fetch the current plan for the student, assuming they only have one plan for simplicity
        # Need to update with main plan ***

        bar_progress = 0  # Default progress

        current_plan = Plan.objects.filter(user=student).first()
        
        if current_plan:
            MAX_CREDITS = 120
            courses = get_full_courses_dict(SEMESTERS, current_plan) if current_plan else {}
            total_credits = 0
            for x in courses:
                    for y in courses[x]:
                        if y:
                            course_data = fetch_data_from_api(y)
                            if course_data:
                                if course_data[0]['course']['creditOptionIds']:
                                    total_credits += float(course_data[0]['course']['creditOptionIds'][0][-3:])
            bar_progress = total_credits / MAX_CREDITS * 100
            bar_progress = int(bar_progress)
            # print(bar_progress, type(bar_progress), total_credits, type(total_credits))
        else:
            total_credits = 0

        context = {
            'user': user,
            'user_type': 'student',
            'name': student.name,
            'school': student.school,
            'majors': [student.major1, student.major2],
            'minors': [student.minor1, student.minor2],
            'total_credits': total_credits, #total credits completed from mainish plan
            'bar_progress': bar_progress, #this is for what percent of progress bar it should take up
        }

    return render(request, 'user/landing.html', context)

from .forms import StudentUpdateForm, SelectCourseForm


def update_info(request):
    user = request.user
    student = Student.objects.get(email=user.email)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            student.first_login_completed = True
            student.save()
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, 'user/update_info.html', {'form': form, 'student': student})



# helper function used in plan
def calculate_major_requirements_progress(student, courses):
    major = student.major1
    fulfilled_requirements_count = 0
    if major[0:2] == 'CS':
        total_major_requirements = len(CS_Major_Core._meta.get_fields()[3:])
        core_list = [field.name for field in CS_Major_Core._meta.get_fields()[3:]]
        for x in courses:
            for y in courses[x]:
                if y in core_list:
                    fulfilled_requirements_count += 1
        if major == 'CS/BS':
            total_major_requirements += len(CS_Major_BS._meta.get_fields()[1:])
            bs_list = [field.name for field in CS_Major_BS._meta.get_fields()[1:]]
            for x in courses:
                for y in courses[x]:
                    if y in bs_list:
                        fulfilled_requirements_count += 1
        if major == 'CS/BA':
            total_major_requirements += len(CS_Major_BA._meta.get_fields()[1:])
            ba_list = [field.name for field in CS_Major_BA._meta.get_fields()[1:]]
            for x in courses:
                for y in courses[x]:
                    if y in ba_list:
                        fulfilled_requirements_count += 1
        return round((fulfilled_requirements_count / total_major_requirements) * 100) if total_major_requirements else 0
    else: # Econ
        total_major_requirements = len(Econ_major._meta.get_fields()[1:])
        econ_list = [field.name for field in Econ_major._meta.get_fields()[1:]]
        for x in courses:
            for y in courses[x]:
                if y in econ_list:
                    fulfilled_requirements_count += 1
        return (fulfilled_requirements_count / total_major_requirements) * 100 if total_major_requirements else 0

def plan(request):
    user = request.user

    # Determine if the user is an advisor
    advisor = User.get_user(user.email, Advisor)
    if advisor:

        # let the view know if student has been changed
        student_change = False

        # if there is no current student yet 
        if 'cur_student' not in request.session:
            request.session['cur_student'] = advisor.students.first().email

        if request.method == 'POST':
            if 'student-select' in request.POST:
                request.session['cur_student'] = request.POST.get('student-select')
                student_change = True
            if 'plan-select' in request.POST:
                request.session['cur_plan_id'] = request.POST.get('plan-select')

        # all students the advisor has access to, by email
        students = advisor.students.all()
        student_emails = [student.email for student in students]

        # the current student the advisor is looking at
        student = Student.objects.filter(email=request.session.get('cur_student'))[0]

        # all plans for the current student
        plans = Plan.objects.filter(user=student)

        # if this is the first time you look at a student, or you have
        # flipped between students, initialize the cur_plan_id to their default (main) plan
        if 'cur_plan_id' not in request.session or student_change:
            request.session['cur_plan_id'] = str(plans.first().id)

        cur_plan_id = request.session.get('cur_plan_id')

        # the current plan the advisor is looking at
        current_plan = Plan.objects.filter(id=cur_plan_id).first()

        courses = get_full_courses_dict(SEMESTERS, current_plan)
        
        plans = sort_plans_by_current(student, current_plan)

        # make sure current student is displayed first
        student_emails.remove(student.email)
        student_emails.insert(0, student.email)
        
        context = {
            'user': user,
            'name': advisor.name,
            'school': advisor.school,
            'plans': plans,
            'cur_plan': current_plan,
            'students': student_emails,
            'courses': courses,
        }
        
        return render(request, 'user/plan_view_advisor.html', context)

    # If not an advisor, assume the user is a student (or handle other roles)
    student = get_object_or_404(Student, email=user.email)
    # if any of the required fields are not filled out, redirect to update_info
    if not all([student.school, student.department, student.start, student.major1]):
        return redirect('update_info')

    user_plans = Plan.objects.filter(user=student)
    major = student.major1
    major_needs = []
    # Existing logic for handling plan operations
    if request.method == 'POST':
        if 'create_plan' in request.POST:
            plan_name = request.POST.get('new_plan_name', 'New Plan')
            new_plan = Plan.objects.create(user=student, name=plan_name)
            request.session['cur_plan_id'] = str(new_plan.id)
            return redirect('user:plan')

        elif 'clear_plan' in request.POST:
            plan = get_object_or_404(Plan, id=request.session['cur_plan_id'])
            plan.delete()
            del request.session['cur_plan_id']
            return redirect('user:plan')

        elif 'plan-select' in request.POST:
            plan_id = request.POST.get('plan-select')
            request.session['cur_plan_id'] = plan_id
            return redirect('user:plan')

    cur_plan_id = request.session.get('cur_plan_id')
    current_plan = None
    if cur_plan_id:
        current_plan = Plan.objects.filter(id=cur_plan_id).first()

    if not current_plan:
        current_plan = user_plans.first()
        if current_plan:
            request.session['cur_plan_id'] = str(current_plan.id)

    courses = get_full_courses_dict(SEMESTERS, current_plan) if current_plan else {}
    total_credits = 0
    for x in courses:
            for y in courses[x]:
                if y:
                    course_data = fetch_data_from_api(y)
                    if course_data:
                        if course_data[0]['course']['creditOptionIds']:
                            total_credits += float(course_data[0]['course']['creditOptionIds'][0][-3:])
    #print(total_credits)
    if major[0:2] == 'CS':
        core_list = [field.name for field in CS_Major_Core._meta.get_fields()[3:]]
        for x in core_list:
    # Check if x is not in any of the courses lists and not already in major_needs
            if all(x not in courses[y] for y in courses) and x not in major_needs:
                major_needs.append(x)

    else: # Econ
        core_list = [field.name for field in Econ_major._meta.get_fields()[1:]]
        for x in core_list:
    # Check if x is not in any of the courses lists and not already in major_needs
            if all(x not in courses[y] for y in courses) and x not in major_needs:
                major_needs.append(x)
    major_progress = calculate_major_requirements_progress(student, courses)
    user_plans = sort_plans_by_current(student, current_plan)
    context = {
        'user': user,
        'name': student.name,
        'school': student.school,
        'majors': [student.major1, student.major2],
        'minors': [student.minor1, student.minor2],
        'user_plans': user_plans,
        'cur_plan': current_plan,
        'courses': courses,
        'major_progress': major_progress,
        'major_needs': major_needs,
        'total_credits': total_credits
    }

    return render(request, 'user/plan_view.html', context)

def department_view(request):
    user = request.user
    administrator = Administrator.objects.get(email=user.email)  
    context = {
            'user': user,
            'user_type': 'administrator',
            'name': administrator.name,
        }
    return render(request, 'user/department_view.html', context)

def get_advisor_students_plans(advisor_id):
    advisor = Advisor.objects.get(id=advisor_id)
    students = advisor.students.all()
    plans = []
    for student in students:
        student_plans = Plan.objects.filter(user=student)
        plans.extend(student_plans)
    return plans

def remove_course(request):
    user = request.user
    student = get_object_or_404(Student, email=user.email)
    user_plans = Plan.objects.filter(user=student)

    plan = Plan.objects.get(id=request.session['cur_plan_id'])

    semester = request.GET.get('semester')
    course_code = request.GET.get('course')

    # if user has selected to remove a course
    if request.method == 'POST':
        # remove course from semester
        cur_courses = getattr(plan, semester).split("/")

        cur_courses.remove(course_code)

        setattr(plan, semester, '/'.join(cur_courses))

        plan.save()

        # redirect users to plan_view upon course removal
        return redirect('user:plan')
    
    courses = {}
    
    # make sure current plan is always at the top of the plan selection dropdown
    user_plans = sort_plans_by_current(student, plan)

    # get dict of courses in plan, with empty classes as "" for display
    courses = get_full_courses_dict(SEMESTERS, plan)
    
    context = {
        'user_plans': user_plans,
        'courses': courses
    }

    return render(request, 'user/remove_course.html', context)

from .utils import fetch_data_from_api

def course_search(request):
    user = request.user
    student = get_object_or_404(Student, email=user.email)
    
    user_plans = Plan.objects.filter(user=student)
    cur_plan_id = request.session.get('cur_plan_id')
    if cur_plan_id is None:
        # If not, redirect to a view where they can choose a plan, or handle it another way
        return redirect('user:plan')

    #plan = get_object_or_404(Plan, id=cur_plan_id)
    plan = Plan.objects.get(id=request.session['cur_plan_id'])
    form=''
    # let the add_course.html know if it should display a 'prereqs not in plan' warning,
    # also tell it which prereqs are missing so it can display those
    prereq_warning = False
    missing_prereqs = []
    # let the add_course.html know if it should display a 'too many courses added' warning
    course_warning = False
    # let the add_course.html know if it should display a 'cannot repeat courses in plan' warning
    repeat_warning = False
    # get dict of courses in plan
    courses = {}
    department = None
    data = None
    for sem in SEMESTERS:
        courses_in_sem = getattr(plan, sem).split("/")
        courses[sem] = courses_in_sem
    if request.method == 'POST':
        if 'department' in request.POST:
            department = request.POST.get('department')
            if department:
                data = fetch_data_from_api(department)
                for item in data:
                    item['prereqs'] = get_prereqs_from_api(item['course']['courseCode'])
                    item['credits'] = item['course']['creditOptionIds']
                    if item['credits'] != []:
                        item['credits'] = item['credits'][0][-3:]
        else:
            form = SelectCourseForm(request.POST, user=student)
            # add the new course to the appropriate semester
            semester = request.POST.get('semester')
            print(request.POST)
            cur_courses_in_sem = courses[semester]

            new_course_code = request.POST.get('new_course_code')
            new_course_credits = float(request.POST.get('new_course_credits'))
            # error if semester already has all 5 courses
            if len(cur_courses_in_sem) >= 6:
                course_warning = True
                messages.warning(request, "The selected semester is full")
            elif any(new_course_code in courses[sem] for sem in SEMESTERS):
                repeat_warning = True
                messages.warning(request, "This course is already in your plan")
            else:
                # get a list of the prereqs associated with the desired course code
                # prereqs: a list of course code Strings. '/' indicates choice between 2 courses
                # gets from API
                prereqs = get_prereqs_from_api(new_course_code)

                cur_sem_val = SEMESTERS.index(semester)

                # # first assume prereqs are not being taken
                # # goal to eventually give user feedback on which prereqs they are missing
                has_prereqs = [False] * len(prereqs)
                
                # # check prereqs and check if course is already in plan
                for val, sem in enumerate(SEMESTERS):
                    # break out of loop once current sem is reached
                    if val == cur_sem_val:
                        break
                    if val < cur_sem_val:
                        for i, prereq in enumerate(prereqs):
                            if prereq in courses[sem]:
                                has_prereqs[i] = True
                
                # # if all prereqs are not satisfied, display warning.
                # # otherwise, add the new course to the semester
                if not all(has_prereqs):
                    prereq_warning = True
                    # add missing prereqs to list to be displayed
                    for i, req in enumerate(has_prereqs):
                        if req == False:
                            missing_prereqs.append(prereqs[i])
                else:
                # replace value at the appropriate semester with the old value
                # + the code of the new course
                    new_courses = getattr(plan, semester) + new_course_code + "/"

                # set new value
                    setattr(plan, semester, new_courses)

                plan.save()
                
    context = {
        #'user': user,
        #'name': student.name,
        #'school': student.school,
        #'majors': [student.major1, student.major2],
        #'minors': [student.minor1, student.minor2],
        'user_plans': user_plans,
        #'cur_plan': plan,
        'form': form,
        'prereq_warning': prereq_warning,
        'course_warning': course_warning,
        'repeat_warning': repeat_warning,
        'missing_prereqs': missing_prereqs,
        'courses': courses,
        'department': department,
        'data': data
    }
    return render(request, 'user/course_search.html', context)

@login_required
def view_major_courses(request):
    student = get_object_or_404(Student, email=request.user.email)
    major_courses = []
    if student.major1:
        if student.major1 == "CS/BS":  # Example of checking for a specific major
            major_courses = CS_Major_BS.objects.first()  # You will need to filter by student's actual major
        elif student.major1 == "CS/BA":
            major_courses = CS_Major_BA.objects.first()
        elif student.major1 == "Econ":
            major_courses = Econ_major.objects.first()
    return render(request, 'user/view_major_courses.html', {'major_courses': major_courses, 'student': student})

from collections import defaultdict

def aggregate_course_enrollment():
    from collections import defaultdict
    enrollment_data = defaultdict(lambda: defaultdict(int))

    # Adjust these based on your actual model structure and fields
    plans = Plan.objects.all()
    for plan in plans:
        start_year = int(plan.user.start[1:])  # assuming start format is F2021 or S2022
        start_semester = plan.user.start[0]  # 'F' or 'S'

        semesters = [
            'freshman_fall', 'freshman_spring', 'sophomore_fall', 
            'sophomore_spring', 'junior_fall', 'junior_spring', 
            'senior_fall', 'senior_spring'
        ]
        
        for i, semester_field in enumerate(semesters):
            semester_courses = getattr(plan, semester_field).split("/")
            year_offset = i // 2 + (0 if start_semester == 'F' else -1) + (1 if i % 2 == 0 else 0)
            actual_year = start_year + year_offset
            semester_label = ('spring' if i % 2 else 'fall') + str(actual_year)
            
            for course_code in semester_courses:
                if course_code:
                    enrollment_data[course_code][semester_label] += 1

    return enrollment_data


def convert_to_regular_dict(defaultdict_obj):
    if isinstance(defaultdict_obj, defaultdict):
        regular_dict = dict(defaultdict_obj)
        for key, value in regular_dict.items():
            regular_dict[key] = convert_to_regular_dict(value)
        return regular_dict
    else:
        return defaultdict_obj

# def department_view(request):
#     enrollment_data = aggregate_course_enrollment()
#     enrollment_data = convert_to_regular_dict(enrollment_data)
#     for x in enrollment_data:
#         print(x)  # Now it should print a regular dictionary structure
#     context = {
#         'enrollment_data': enrollment_data,
#     }
#     return render(request, 'user/department_view.html', context)




def department_view(request):
    logger.debug('Debug message')
    logger.info('Info message')
    enrollment_data = aggregate_course_enrollment()
    enrollment_data = convert_to_regular_dict(enrollment_data)
    semester = request.GET.get('semester')
    
    for x in enrollment_data:
        print(x)  
    department = request.GET.get('department')
    if department:
        if department == 'Computer Science':
            enrollment_data = {key: value for key, value in enrollment_data.items() if key.startswith('CSCI')}        
        if department == 'Math':
            enrollment_data = {key: value for key, value in enrollment_data.items() if key.startswith('MATH')}
        if department == 'Economics':
            enrollment_data = {key: value for key, value in enrollment_data.items() if key.startswith('ECON')}        
    if semester:
        for key in enrollment_data.keys():
            enrollment_data[key] = {semester: enrollment_data[key].get(semester, 0)}
    context = {
        'enrollment_data': enrollment_data,
    }

    return render(request, 'user/department_view.html', context)
