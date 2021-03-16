from django.db import models
from random import randint, choice
from string import ascii_uppercase
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

def generateStaffID():
    # generates transaction PIN with 8digits and 2letters
    letters = ascii_uppercase
    pin = ''.join([str(randint(0, 9)) for p in range(0, 8)])
    pin = choice(letters) + pin + choice(letters)
    return pin

pharm_tech = 'Pharmaceutical Technology'
comp_sci = 'Computer Science'
food_tech = 'Food Technology'
mcb = 'Microbiology'
hosp_manag = 'Hospitality Management'
mec_eng = 'Mechanical Engineering'
chem = 'Chemistry'
phy = 'Physics'
sts_mts = 'Statistics and Mathematics'
mass_com = 'Mass Communication'
urp = 'Urban & Regional Planning'
civil_eng = 'Civil Engineering'
mkt = 'Marketing'
biz_admin = 'Business Administration'
acct = 'Accountancy'

DEPARTMENT_OPTION = (
    (pharm_tech, pharm_tech),
    (comp_sci, comp_sci),
    (sts_mts, sts_mts),
    (mcb, mcb),
    (food_tech, food_tech),
    (mass_com, mass_com),
    (urp, urp),
    (civil_eng, civil_eng),
    (biz_admin, biz_admin),
    (mkt, mkt),
    (acct, acct),
)

female = 'Female'
male = 'Male'

GENDER_OPTION = (

    (female, female),
    (male, male),
)

TITLE_CHOICES = (('Miss', 'Miss'),
                 ('Mrs', 'Mrs'),
                 ('Mr', 'Mr'))

hod = 'HOD'
school_officer = 'SCHOOL OFFICER'
library = 'LIBRARY'
busary = 'BUSARY'

OFFICE_CHOICES = (
            
            (hod, hod),
            (school_officer, school_officer),
            (library, library),
            (busary, busary),
    
    )


class Student(models.Model):
    surname = models.CharField(max_length = 100)
    other_names = models.CharField(max_length = 100)
    matric_no = models.CharField(max_length = 20, unique = True)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10, default = 'HND II')
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION, default = comp_sci)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


    def __str__(self):
        return '%s %s' % (self.surname, self.other_names)
        

class Clearance(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    matric_no = models.CharField(max_length = 20, unique = True)
    surname = models.CharField(max_length = 100)
    slug = models.SlugField(null=True,blank=True)
    other_names = models.CharField(max_length = 100)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10)
    signature = models.CharField(max_length = 20)
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION)
    hod = models.CharField(max_length = 50)
    school_officer = models.CharField(max_length = 50)
    library = models.CharField(max_length = 50)
    date_signed = models.DateTimeField()
    is_accessed = models.BooleanField(default = False)
    

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.matric_no

    def save(self, *args, **kwargs):
            if self.slug is None and self.other_names:
                self.slug = slugify(str(self.other_names))
            return super(Clearance, self).save(*args, **kwargs)

class HOD(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    matric_no = models.CharField(max_length = 20, unique = True)
    surname = models.CharField(max_length = 100)
    other_names = models.CharField(max_length = 100)
    slug = models.SlugField(null=True,blank=True)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10)
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION)
    sundry_receipt = models.FileField(upload_to = 'sundry')
    date_created = models.DateTimeField(auto_now_add = True)
    hod_email = models.EmailField()
    is_accessed = models.BooleanField(default = False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
            return self.matric_no

    def save(self, *args, **kwargs):
            if self.slug is None and self.other_names:
                self.slug = slugify(str(self.other_names))
            return super(HOD, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('not_cleared')

    
class School(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    signature = models.CharField(max_length = 20)
    matric_no = models.CharField(max_length = 20, unique = True)
    surname = models.CharField(max_length = 100)
    slug = models.SlugField(null=True,blank=True)
    other_names = models.CharField(max_length = 100)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10)
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION)
    date_signed = models.DateTimeField()
    is_accessed = models.BooleanField(default = False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.matric_no

    def save(self, *args, **kwargs):
            if self.slug is None and self.other_names:
                self.slug = slugify(str(self.other_names))
            return super(School, self).save(*args, **kwargs)

class Library(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    signature = models.CharField(max_length = 20)
    matric_no = models.CharField(max_length = 20, unique = True)
    surname = models.CharField(max_length = 100)
    slug = models.SlugField(null=True,blank=True)
    other_names = models.CharField(max_length = 100)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10)
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION)
    date_signed = models.DateTimeField()
    is_accessed = models.BooleanField(default = False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.matric_no

    def save(self, *args, **kwargs):
            if self.slug is None and self.other_names:
                self.slug = slugify(str(self.other_names))
            return super(Library, self).save(*args, **kwargs)

            
class Busary(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    signature = models.CharField(max_length = 20)
    matric_no = models.CharField(max_length = 20, unique = True)
    surname = models.CharField(max_length = 100)
    slug = models.SlugField(null=True,blank=True)
    other_names = models.CharField(max_length = 100)
    gender = models.CharField(choices = GENDER_OPTION, max_length = 7)
    level = models.CharField(max_length = 10)
    department = models.CharField(max_length = 50, choices = DEPARTMENT_OPTION)
    date_signed = models.DateTimeField()
    is_accessed = models.BooleanField(default = False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
            return self.matric_no

    def save(self, *args, **kwargs):
            if self.slug is None and self.other_names:
                self.slug = slugify(str(self.other_names))
            return super(Busary, self).save(*args, **kwargs)
    

class Feedback(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    comment = models.TextField(max_length = 255, blank = True, null = True)
    slug = models.SlugField(null = True, blank = True)
    student = models.CharField(max_length = 50)
    matric_no = models.CharField(max_length = 20)
    department = models.CharField(max_length = 50)
    date_created = models.DateTimeField(auto_now_add = True)
    is_cleared = models.BooleanField(default = False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.matric_no
    

    def save(self, *args, **kwargs):
            if self.slug is None and self.comment:
                self.slug = slugify(str(self.comment))
            return super(Feedback, self).save(*args, **kwargs)

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 5, choices = TITLE_CHOICES)
    staff_id = models.CharField(max_length = 10, unique = True)
    email = models.EmailField()
    office = models.CharField(max_length = 30, choices = OFFICE_CHOICES)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'

    def __str__(self):
        return '%s %s' % (self.title, self.first_name)
    
    def save(self, *args, **kwargs):
        if not self.staff_id:
                self.staff_id = generateStaffID() 
                while Staff.objects.filter(staff_id = self.staff_id).exists():
                    self.staff_id = generateStaffID()
        super(Staff, self).save(*args, **kwargs)

   