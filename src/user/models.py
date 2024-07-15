import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    
    class Meta:
        abstract = True

    @staticmethod
    def get_user(user_email, subclass):
        user = None

        try:
            user = subclass.objects.get(email=user_email)
        except subclass.DoesNotExist:
            pass

        return user


class Student(User):
    school = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    start = models.CharField(max_length=200)
    major1 = models.CharField(max_length=200)
    major2 = models.CharField(max_length=200, blank=True)
    minor1 = models.CharField(max_length=200, blank=True)
    minor2 = models.CharField(max_length=200, blank=True)
    first_login_completed = models.BooleanField(default=False)


class Advisor(User):
    school = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    students = models.ManyToManyField('Student', related_name='advisors', blank=True)


class Administrator(User):
    pass

class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4 )
    user = models.ForeignKey(Student, on_delete=models.CASCADE)  # Use Student model here
    name = models.CharField(max_length=200, default="Main")
    freshman_fall = models.TextField(default="", blank=True)
    freshman_spring = models.TextField(default="", blank=True)
    sophomore_fall = models.TextField(default="", blank=True)
    sophomore_spring = models.TextField(default="", blank=True)
    junior_fall = models.TextField(default="", blank=True)
    junior_spring = models.TextField(default="", blank=True)
    senior_fall = models.TextField(default="", blank=True)
    senior_spring = models.TextField(default="", blank=True)

    #trying per course bc semester wasn't working
    def calculate_total_credits(self):
        total_credits = 0
        semesters = [
            self.freshman_fall, self.freshman_spring, self.sophomore_fall,
            self.sophomore_spring, self.junior_fall, self.junior_spring,
            self.senior_fall, self.senior_spring
        ]

        # Iterate over each semester's content
        for semester in semesters:
            course_codes = [code.strip() for code in semester.split("/") if code.strip()]
            
            # Iterate over each course code in the current semester
            for code in course_codes:
                course = Course.objects.get(code=code)
                total_credits += course.credits  # Add the course's credits to the total
        
        return total_credits

    '''def calculate_total_credits(self):
        total_credits = 0
        semesters = [self.freshman_fall, self.freshman_spring, self.sophomore_fall,
                     self.sophomore_spring, self.junior_fall, self.junior_spring,
                     self.senior_fall, self.senior_spring]
        for semester in semesters:
            course_codes = semester.split(',')
            courses = Course.objects.filter(code__in=course_codes)
            total_credits += courses.aggregate(models.Sum('credits'))['credits__sum'] or 0
        return total_credits'''

    def __str__(self):
        return f"Plan for {self.user.name}"


class Course(models.Model):
    code = models.CharField(max_length=200, default = "")
    department = models.CharField(max_length=200, default = "")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField()
    department = models.CharField(max_length=200, default = "")
    #core = models.BooleanField(default=False)
    #core_requirement = models.ForeignKey('CoreRequirement', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')


    def __str__(self):
        return f"{self.code} - {self.title}"
    
class CS_Major_Core(models.Model):
    CSCI1101 = models.CharField(max_length=11, default = "CSCI1101" )
    CSCS1102 = models.CharField(max_length=11, default = "CSCS1102" )
    CSCI2243 = models.CharField(max_length=11, default = "CSCI2243" )
    CSCI2244 = models.CharField(max_length=11, default = "CSCI2244" )
    CSCI2271 = models.CharField(max_length=11, default = "CSCI2271" )
    CSCI2272 = models.CharField(max_length=11, default = "CSCI2272" )
    CSCI3383 = models.CharField(max_length=11, default = "CSCI3383" )

    def __str__(self):
        return "CS Major Core"
class ScienceComponent(models.Model):
    PHYSICS_CHOICES = (
        ("PHYS2100", "PHYS2100"),
        ("PHYS2050", "PHYS2050"),
        ("PHYS2101", "PHYS2101"),
        ("PHYS2051", "PHYS2051")
    )
    Physics = models.CharField(max_length=11, default = "", choices = PHYSICS_CHOICES)
    physics_credits = models.IntegerField(default=6)
    BIOLOGY_CHOICES = (
        ("BIOL2010", "BIOL2010"),
        ("BIOL2000", "BIOL2000"),
        ("BIOL2040", "BIOL2040"),
        ("BIOL1300", "BIOL1300"),
    )
    Biology = models.CharField(max_length=11, default = "", choices = BIOLOGY_CHOICES)
    biology_credits = models.IntegerField(default=9)
    CHEMISTRY_CHOICES = (
        ("CHEM1011", "CHEM1011"),
        ("CHEM1012", "CHEM1012"),
        ("CHEM1013", "CHEM1013"),
        ("CHEM1014", "CHEM1014"),
        ("CHEM1117", "CHEM1117"),
        ("CHEM1118", "CHEM1118"),
        ("CHEM1119", "CHEM1119"),
        ("CHEM1120", "CHEM1120"),
    )
    chemisyry_credits = models.IntegerField(default=8)
    Chemistry = models.CharField(max_length=11, default = "", choices= CHEMISTRY_CHOICES)
    ENVIRONMENTAL_CHOICES = (
        ("EESC1132", "EESC1132"),
        ("EESC2202", "EESC2202"),
        ("EESC2203", "EESC2203"),
        ("EESC2204", "EESC2204"),
        ("EESC2205", "EESC2205"),
        ("EESC2206", "EESC2206"),
        ("EESC2207", "EESC2207"),
        ("EESC2208", "EESC2208"),
    )
    Environmental = models.CharField(max_length=11, default = "", choices = ENVIRONMENTAL_CHOICES)
    environmental_credits = models.IntegerField(default=7)
    environmental_elective_credits = models.IntegerField(default=3) ##must be 2000+
    
class CS_Major_BS(models.Model):
    core = models.OneToOneField(CS_Major_Core, on_delete=models.CASCADE)
    MATH1103 = models.CharField(max_length=11, default = "MATH1103" )
    MATH2202 = models.CharField(max_length=11, default = "MATH2202" )
    MATH2210 = models.CharField(max_length=11, default = "MATH2210" )
    CSCI2267 = models.CharField(max_length=11, default = "CSCI2267" )
    cs_3000 = models.CharField(max_length=11, default = "")
    elective_credits = models.IntegerField(default=12)
    math_elective_credits = models.IntegerField(default=3)
    math_3000 = models.CharField(max_length=11, default = "")
    ethics_credits = models.IntegerField(default=3)
    science_component = models.ForeignKey(ScienceComponent, on_delete=models.CASCADE)

    def __str__(self):
        return "CS Major BS"

class CS_Major_BA(models.Model):
    core = models.OneToOneField(CS_Major_Core, on_delete=models.CASCADE)
    MATH1103 = models.CharField(max_length=11, default = "MATH1103" )
    MATH2202 = models.CharField(max_length=11, default = "MATH2202" )
    cs_2000_credits = models.IntegerField(default=3)
    cs_3000_credits = models.IntegerField(default=9)
    def __str__(self):
        return "CS Major BA"
    
class Econ_major(models.Model):
    MICRO_CHOICES = (
        ("ECON2201", "ECON2201"),
        ("ECON2203", "ECON2203"),
    )
    MACRO_CHOICES = (
        ("ECON2202", "ECON2202"),
        ("ECON2204", "ECON2204"),
    )
    ECON1101 = models.CharField(max_length=11, default = "ECON1101")
    ECON1151 = models.CharField(max_length=11, default = "ECON1151")
    Micro = models.CharField(max_length=11, default = "ECON2201", choices = MICRO_CHOICES)
    Macro = models.CharField(max_length=11, default = "ECON2202", choices = MACRO_CHOICES)
    ECON2228 = models.CharField(max_length=11, default = "ECON2228")
    econ_2200_credits = models.IntegerField(default=6)
    econ_3000_credits = models.IntegerField(default=12)
    MATH1102 = models.CharField(max_length=11, default = "MATH1102")
    def __str__(self):
        return "Econ Major"
