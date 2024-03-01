from django.contrib import admin
from django.contrib.auth.models import User
from .models import Employee, Educational_Qualification, Personal_detail, Project, Previous_Work_Experience, Promotions, Address_model, Joining_Details, Deparment_and_salary, hyper_fields, Technology, Languages, client, team_members, monitoring, time_sheet, Leave, Attendance, Children

# Register all models
admin.site.register(Educational_Qualification)
admin.site.register(Previous_Work_Experience)
admin.site.register(Promotions)
admin.site.register(Address_model)
admin.site.register(Joining_Details)
admin.site.register(Deparment_and_salary)
admin.site.register(hyper_fields)
admin.site.register(Technology)
admin.site.register(Languages)
admin.site.register(client)
admin.site.register(team_members)
admin.site.register(monitoring)
admin.site.register(time_sheet)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Children)


# Employee Form in Admin Interface

class PromotionsInline(admin.StackedInline):
    model = Promotions
    extra = 1
    classes = ('collapse',)

class TechnologyInline(admin.StackedInline):
    model = Technology
    extra = 1
    classes = ('collapse',)

class PreviousWorkExperienceInline(admin.StackedInline):
    model = Previous_Work_Experience
    extra = 1
    classes = ('collapse',)

class LanguagesInline(admin.TabularInline):
    model = Languages
    extra = 1
    classes = ('collapse',)

class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1
    classes = ('collapse',)

class DeparmentAndSalaryInline(admin.StackedInline):
    model = Deparment_and_salary
    extra = 1
    can_delete = False
    verbose_name_plural = 'Department and Salary Information'
    classes = ('collapse',)

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    classes = ('collapse',)
    readonly_fields = ['created_at']
    exclude = ["remarks"]
    date_hierarchy = 'created_at'

class LeaveInline(admin.TabularInline):
    model = Leave
    extra = 1
    classes = ('collapse',)
    readonly_fields = ['created_at']
    exclude = ["reason"]
    date_hierarchy = 'created_at'

class TimeSheetInline(admin.StackedInline):
    model = time_sheet
    extra = 1
    classes = ('collapse',)
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

class MonitoringInline(admin.TabularInline):
    model = monitoring
    extra = 1
    classes = ('collapse',)

class JoiningDetailsInline(admin.StackedInline):
    model = Joining_Details
    extra = 1
    classes = ('collapse',)

class EducationalQualificationInline(admin.StackedInline):
    model = Educational_Qualification
    extra = 1
    classes = ('collapse',)  # Add 'collapse' class for collapsing the inline by default

class ChildrenInline(admin.TabularInline):
    model = Children
    extra = 1
    classes = ('collapse',)  # Add 'collapse' class for collapsing the inline by default

class JoiningDetailsInline(admin.TabularInline):
    model = Joining_Details
    extra = 1
    classes = ('collapse',)  # Add 'collapse' class for collapsing the inline by default
    exclude = ["document_id", "procured_by"]
    

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [ "Emp_id", "get_username", "Date_Of_Joining", "Current_Status", "Company"]
    list_filter = ["Date_Of_Joining", "Current_Status", "Company"]
    list_display_links = ["Emp_id", "get_username"]
    list_per_page = 50
    readonly_fields = ["Emp_id", "user"]
    raw_id_fields = ["user"]

    inlines = [DeparmentAndSalaryInline, PromotionsInline, TechnologyInline, PreviousWorkExperienceInline, LanguagesInline, ProjectInline, AttendanceInline, LeaveInline, TimeSheetInline, MonitoringInline]

    fieldsets = (
        ("User-Information", {
            "fields": (
                ("Emp_id", "user")
            ),
        }),
        ("Employee-Details", {
            "fields": ('Current_Status', 'Company', 'Gender', 'Date_Of_Birth','Date_Of_Joining'),
            'classes': ('collapse',),
        }),
        ('Salary Information', {
            'fields': ('Training_Period_CTC', 'Annual_CTC', 'Employment_Type'),
            'classes': ('collapse',),
        }),
        ('Address Information', {
            'fields': ('Permanent_Address', 'present_address'),
            'classes': ('collapse',),
        }),
        ('Other Information', {
            'fields': ('physically_challenged',),
            'classes': ('collapse',),
        }),
    )
    
    @admin.display(description="Employee E-mail")
    def get_email(self, obj):
        return obj.user.email

    @admin.display(description="Employee Name")
    def get_username(self, obj):
        return obj.user.username
    
@admin.register(Personal_detail)
class Personal_detail_admin(admin.ModelAdmin):
    list_display = ["get_username", "Mobile", "Personal_Email", "Blood_Group"]
    list_display_links = ["get_username", "Mobile", "Personal_Email"]
    readonly_fields = ["user"]
    inlines = [EducationalQualificationInline, ChildrenInline, JoiningDetailsInline]
    

    fieldsets = (
        ('Family Members Information', {
            'fields': ('Name_as_per_Aadhar', 'Father_Name', 'Spouse_Name', 'Mother_Name', 'Marital_Status'),
            'classes': ('collapse',),
        }),
        ('ID Proof Information', {
            'fields': ('Aadhar_Card_No', 'Passport_Number', 'Passport_issue_date', 'Password_Valid_upto', 'Password_place_of_issue'),
            'classes': ('collapse',),
        }),
        ('Contact Details', {
            'fields': ('Mobile', 'Alternate_Mobile_Number', 'Personal_Email', 'Prefered_contact_Email', 'Company_Email'),
            'classes': ('collapse',),
        }),
        ('Additional Information', {
            'fields': ('Blood_Group',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description="Employee Name")
    def get_username(self, obj):
        return obj.user.username
    

class TeamMembersInline(admin.StackedInline):
    model = team_members
    extra = 1
    classes = ('collapse',)  # Add 'collapse' class for collapsing the inline by default

class ClientInline(admin.StackedInline):
    model = client
    extra = 1
    classes = ('collapse',)  # Add 'collapse' class for collapsing the inline by default

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]

    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'start_date', 'end_date'),
        }),
        # ... other fieldsets ...
    )

    inlines = [TeamMembersInline, ClientInline]
