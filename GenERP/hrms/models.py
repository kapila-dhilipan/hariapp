import random
import string
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
User = get_user_model()


# users employee related data designed

class Employee(models.Model):
    status = (('1','Active'),
              ('2','on maternity leave'),
              ('3','on notice period'),
              ('4','Terminated'),
              ('5','on medical leave'))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='employement_details')
    Emp_id = models.CharField(max_length=10, blank=True, unique=True, verbose_name="Employee ID")
    Company = models.CharField(max_length=50, blank=True, null=True, default='SightSpectrum')
    Current_Status = models.CharField(max_length=50, choices=status, default='1')
    Gender = models.CharField(max_length=50, choices=(('male','Male'),('female','Female'),('other','Other')),default='select')
    Date_Of_Birth = models.DateField(blank=True, null=True)
    Date_Of_Joining = models.DateField(blank=True, null=True)
    Training_Period_CTC = models.IntegerField(blank=True, null=True)
    Annual_CTC = models.IntegerField(blank=True, null=True, verbose_name="Annual Salary")
    Employment_Type = models.CharField(max_length=50, choices=(('R','Regular'),('C','Contract'),('E','Permenent')))
    physically_challenged = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.Emp_id = "SS-"+"".join(random.choice(string.digits) for _ in range(5))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + self.user.last_name

# common templates for using in the model designing
########################################################################################################

class Address_model(models.Model):
    Old_No = models.CharField(max_length=10, blank=True, null=True, verbose_name= "Old Num.")
    New_No = models.CharField(max_length=10, blank=True, null=True, verbose_name= "New Num.")
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Pin-Code")

#############################################################################################################

class Deparment_and_salary(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Deparment = models.CharField(max_length=50, blank=True, null=True)
    Designation = models.CharField(max_length=50, blank=True, null=True)
    Reports_to = models.CharField(max_length=50, blank=True, null=True)
    Grade = models.CharField(max_length=50, blank=True, null=True)
    Branch = models.CharField(max_length=50, blank=True, null=True)
    Salary_Mode = models.CharField(max_length=50, blank=True, null=True)
    Payroll_Cost_Center = models.CharField(max_length=50, blank=True, null=True)
    PAN_Number = models.CharField(max_length=50, blank=True, null=True)
    Provident_Fund_Account = models.CharField(max_length=50, blank=True, null=True)    
    
    class Meta:
        verbose_name = _("Deparment_and_Grade")
        verbose_name_plural = _("Deparment_and_Grade")

    def __str__(self):
        return self.user.first_name
    
class Promotions(models.Model):
	user = models.ForeignKey(Employee, blank=True, null=True,related_name='Promotions',on_delete=models.CASCADE)
	date_promotion=  models.DateField(editable=True, blank=True, null=True)
	designation  = models.CharField(max_length=255, blank=True, null=True) 
	pay_scale = models.CharField(max_length=255, blank=True, null=True) 
	nature_promotion = models.CharField(max_length=255, blank=True, null=True) 


class hyper_fields(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)   
    
    def __str__(self):
            return self.category
    
class Technology(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Technology = models.CharField(max_length=50)
    proficiency = models.IntegerField()
    hyperlinked_fields = models.ManyToManyField(hyper_fields)

    def __str__(self):
        return self.user.first_name + self.user.last_name

class Previous_Work_Experience(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    reason_for_leaving = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name

class Languages(models.Model):
    user = models.ForeignKey(Employee, blank=True, null=True, related_name='languages', on_delete=models.CASCADE)
    languages = models.CharField(max_length=255, blank=True, null=True)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    speak = models.BooleanField(default=False)

    def __str__(self):
        return self.languages    

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Project Name")
    lead = models.ForeignKey(Employee, blank=True, null=True, related_name='lead_detail', on_delete=models.CASCADE, verbose_name="Project Lead")
    description = models.TextField()
    start_date = models.DateField(editable=True)
    end_date = models.DateField(editable=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} under {self.lead.user.username}"
    
class team_members(models.Model):
    name = models.ForeignKey(Project, blank=True, null=True, related_name='project_name', on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, blank=True, null=True, related_name='team_members', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.name
    
class client(models.Model):
    RESOURCE_TYPE = [
        ('E','EXTERNEL'),
        ('I','INTERNEL'),
        ('U','UNDER TRAINING'),
    ]
    client_name = models.ForeignKey(Project, blank=True, null=True, related_name='client_name', on_delete=models.CASCADE)
    company = models.CharField(max_length=50, default='SightSpectrum')
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE, default='U')

    
# model for users personal details
class Personal_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='personal_details')
    Name_as_per_Aadhar = models.CharField(max_length=50, blank=True, null=True)
    Father_Name = models.CharField(max_length=50, blank=True, null=True)
    Spouse_Name = models.CharField(max_length=50, blank=True, null=True)
    Mother_Name = models.CharField(max_length=50, blank=True, null=True)
    Aadhar_Card_No = models.BigIntegerField(blank=True, null=True)
    Passport_Number = models.BigIntegerField(blank=True, null=True)
    Passport_issue_date = models.DateField(blank=True, null=True)
    Password_Valid_upto = models.DateField(max_length=200, blank=True, null=True)
    Password_place_of_issue = models.CharField(max_length=150, blank=True, null=True)
    Marital_Status = models.CharField(max_length=50, choices=(('single','Single'),('married','Married')))
    Blood_Group = models.CharField(max_length=50, blank=True, null=True)
    Mobile = models.CharField(max_length=50, blank=True, null=True)
    Alternate_Mobile_Number = models.CharField(max_length=50, blank=True, null=True)
    Personal_Email = models.EmailField(max_length=50, blank=True, null=True)
    Prefered_contact_Email = models.EmailField(max_length=50, blank=True, null=True)
    Company_Email = models.EmailField(max_length=50, blank=True, null=True)
    Permanent_Address = models.ForeignKey(Address_model, on_delete=models.CASCADE, related_name='permanent_add')
    present_address = models.ForeignKey(Address_model, on_delete=models.CASCADE, related_name='present_add')
    
    class Meta:
        verbose_name = _("Personal_detail")
        verbose_name_plural = _("Personal_detail")

    def __str__(self):
        return self.user.employement_details.Emp_id


class Educational_Qualification(models.Model):
    user = models.ForeignKey(Personal_detail ,on_delete=models.CASCADE)
    institution = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50, blank=True, null=True) 
    degree = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    Year_Of_Passing = models.CharField(max_length=50)
    Precentage = models.CharField(max_length=50)

    def __str__(self):
        return self.institute

class Children(models.Model):
	user = models.ForeignKey(Personal_detail, blank=True, null=True,related_name='Children',on_delete=models.CASCADE)
	name = models.CharField(max_length=100, blank=True, null=True) 
	sex = models.CharField(max_length=32, choices=(('male','male'),('female','female'),('otherother','other')), blank=True) 
	dob = models.DateField( blank=True, null=True)

class Joining_Details(models.Model):
    user = models.ForeignKey(Personal_detail, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    document_id = models.CharField(max_length=50, blank=True, null=True)
    date_submitted = models.DateField(default=timezone.now)
    procured_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name   

###############################       Attendance related model    #####################################

class Attendance(models.Model):
    ATTENDANCE_STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]
    
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS_CHOICES)
    remarks = models.TextField(blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attendance for {self.user.username} on {self.date}"


class Leave(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Leave request for {self.user.username}: {self.start_date} to {self.end_date}"
    

class time_sheet(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)  
    first_hour = models.CharField(max_length=250, blank=True, null=True)
    second_hour = models.CharField(max_length=250, blank=True, null=True)
    third_hour = models.CharField(max_length=250, blank=True, null=True)
    fourth_hour = models.CharField(max_length=250, blank=True, null=True)
    fifth_hour = models.CharField(max_length=250, blank=True, null=True)
    sixth_hour = models.CharField(max_length=250, blank=True, null=True)
    seventh_hour = models.CharField(max_length=250, blank=True, null=True)
    eighth_hour = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
class monitoring(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True)
    leave = models.ForeignKey(Leave,blank=True, null= True, on_delete=models.CASCADE)
    timesheet = models.ForeignKey(time_sheet , null=True, on_delete=models.CASCADE)
    
