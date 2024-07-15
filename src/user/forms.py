from django import forms
from .models import Student, Course

from django import forms
from .models import Student

class StudentUpdateForm(forms.ModelForm):
    SCHOOL_CHOICES = [('', 'Select School')] + [
        ('MCAS', 'Morrissey College of Arts & Sciences'),
        ('LYNCH', 'Lynch School of Education & Human Development'),
        ('CSOM', 'Carroll School of Management'),
        ('CSON', 'Connell School of Nursing'),
    ]

    YEAR_CHOICES = [('', 'Select Year')] + [
        ('F2020', 'Fall 2020'),
        ('S2020', 'Spring 2020'),
        ('F2021', 'Fall 2021'),
        ('S2021', 'Spring 2021'),
        ('F2022', 'Fall 2022'),
        ('S2022', 'Spring 2022'),
        ('F2023', 'Fall 2023'),
        ('S2023', 'Spring 2023'),
    ]

    DEPARTMENT_CHOICES = [('', 'Select Department')] + [
        ('ART', 'Art, Art History, and Film'),
        ('ACCT', 'Accounting'),
        ('BIO', 'Biology'),
        ('CHEM', 'Chemistry'),
        ('COMM', 'Communications'),
        ('CS', 'Computer Science'),
        ('ECON', 'Economics'),
        ('HCE', 'Engineering'),
        ('ENG', 'English'),
        ('FIN', 'Finance'),
        ('HIST', 'History'),
        ('MATH', 'Mathematics'),
        ('MKT', 'Marketing'),
    ]

    MAJOR_CHOICES = [('', 'Select Major')] + [
        ('UNDEC', 'Undecided'),
        ('ART', 'Art, Art History, and Film'),
        ('ACCT', 'Accounting'),
        ('BIO', 'Biology'),
        ('CHEM', 'Chemistry'),
        ('COMM', 'Communications'),
        ('CS/BA', 'Computer Science, B.A.'),
        ('CS/BS', 'Computer Science, B.S.'),
        ('ECON', 'Economics'),
        ('HCE', 'Engineering'),
        ('ENG', 'English'),
        ('FIN', 'Finance'),
        ('HIST', 'History'),
        ('MATH', 'Mathematics'),
        ('MKT', 'Marketing'), 
        ('AADS', 'African Diaspora Studies')
    ]

    SECOND_MAJOR_CHOICES = [('', 'Select Major')] + [
        ('ART', 'Art, Art History, and Film'),
        ('ACCT', 'Accounting'),
        ('BIO', 'Biology'),
        ('CHEM', 'Chemistry'),
        ('COMM', 'Communications'),
        ('CS/BA', 'Computer Science, B.A.'),
        ('CS/BS', 'Computer Science, B.S.'),
        ('ECON', 'Economics'),
        ('HCE', 'Engineering'),
        ('ENG', 'English'),
        ('FIN', 'Finance'),
        ('HIST', 'History'),
        ('MATH', 'Mathematics'),
        ('MKT', 'Marketing'),
        ('', 'None'),
    ]

    MINOR_CHOICES = [('', 'Select Minor')] + [
        ('ART', 'Art, Art History, and Film'),
        ('ACCT', 'Accounting'),
        ('BIO', 'Biology'),
        ('CHEM', 'Chemistry'),
        ('COMM', 'Communications'),
        ('CS', 'Computer Science'),
        ('ECON', 'Economics'),
        ('HCE', 'Engineering'),
        ('ENG', 'English'),
        ('FIN', 'Finance'),
        ('HIST', 'History'),
        ('MATH', 'Mathematics'),
        ('MKT', 'Marketing'),
        ('', 'None'),
    ]

    school = forms.ChoiceField(choices=SCHOOL_CHOICES, required=False)
    start = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False)
    major1 = forms.ChoiceField(choices=MAJOR_CHOICES, required=False)
    major2 = forms.ChoiceField(choices=SECOND_MAJOR_CHOICES, required=False)
    minor1 = forms.ChoiceField(choices=MINOR_CHOICES, required=False)
    minor2 = forms.ChoiceField(choices=MINOR_CHOICES, required=False)

    class Meta:
        model = Student
        fields = ['school', 'start', 'department', 'major1', 'major2', 'minor1', 'minor2']


    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance


class SelectCourseForm(forms.ModelForm):
    SEMESTER_CHOICES = [
        ('freshman_fall', 'Freshman Fall'),
        ('freshman_spring', 'Freshman Spring'),
        ('sophomore_fall', 'Sophomore Fall'),
        ('sophomore_spring', 'Sophomore Spring'),
        ('junior_fall', 'Junior Fall'),
        ('junior_spring', 'Junior Spring'),
        ('senior_fall', 'Senior Fall'),
        ('senior_spring', 'Senior Spring'),
    ]

    # ModelChoiceField is used when we are selecting objects from a model,
    # as opposed to regular elements in a regular list (ChoiceField)
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, required=True)

    class Meta:
        model = Student
        fields = ['course', 'semester']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SelectCourseForm, self).__init__(*args, **kwargs)
        if user is not None and user.major1 is not None:
            self.fields['course'].queryset = Course.objects.filter(department=user.major1)

class DepartmentSearchForm(forms.Form):
    department = forms.ChoiceField(choices=[('all', 'All Departments'), ('CSCI', 'Computer Science'), ('ECON', 'Economics')])