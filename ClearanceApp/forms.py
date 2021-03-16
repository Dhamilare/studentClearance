from .models import * 
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class staffRegisterForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['user', 'staff_id']

    email = forms.EmailField(
        widget = forms.EmailInput(attrs = {'placeholder': 'Email', 'class': 'form-control'})
    )
    
    username = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Username', 'class': 'form-control'})
    )
    
    first_name = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'First Name', 'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Last Name', 'class': 'form-control'})
    )

    title = forms.CharField(
        widget = forms.Select(choices = TITLE_CHOICES, attrs = {'placeholder': 'Title', 'class': 'form-control'})    
    )

    password1 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Password', 'class': 'form-control'}),
        min_length = 8
     )
        
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password', 'class': 'form-control'}),
        min_length = 8   
    )

    office = forms.CharField(
        widget = forms.Select(attrs = {'class': 'form-control'}, choices = OFFICE_CHOICES), 
    )

    # def __init__(self, *args, **kwargs):
    #     super(staffRegisterForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords Do not Match')
        
        
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email Already Exist')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('The User Name already exits')

class studentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']
    
    username = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Username', 'class': 'form-control'})
    )
    
    other_names = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Other Names', 'class': 'form-control'})
    )
    
    surname = forms.CharField(
        max_length = 50,
        widget = forms.TextInput(attrs = {'placeholder': 'Surname', 'class': 'form-control'})
    )

    matric_no = forms.CharField(
        widget = forms.TextInput(attrs = {'placeholder': '14/69/0000', 'class': 'form-control'})    
    )

    level = forms.CharField(
        widget = forms.TextInput(attrs = {'placeholder': 'Level', 'class': 'form-control', 'value': 'HND II', 'readonly': 'readonly'})    
    )


    gender = forms.CharField(
        widget = forms.Select(choices = GENDER_OPTION, attrs = {'placeholder': 'Select', 'class': 'form-control'})
    )

    department = forms.CharField(
        widget = forms.Select(choices = DEPARTMENT_OPTION, attrs = {'placeholder': 'Select', 'class': 'form-control'})
    )

    password1 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Password', 'class': 'form-control'}),
        min_length = 8
     )
        
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password', 'class': 'form-control'}),
        min_length = 8   
    )

    # def __init__(self, *args, **kwargs):
    #     super(studentRegisterForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         # self.fields['level'].widget.attrs['disabled'] = 'disabled'
    #         #self.fields['level'].required = False
            

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('Passwords Do not Match')
        
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('The User Name already exits')


class clearanceForm(forms.ModelForm):
    class Meta:
        model = HOD
        exclude = ['student']
        fields = ['sundry_receipt']

    def __init__(self, *args, **kwargs):
        super(clearanceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class HODForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ['staff']

    def __init__(self, *args, **kwargs):
        super(HODForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = ['staff']

    def __init__(self, *args, **kwargs):
        super(LibraryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class BusaryForm(forms.ModelForm):
    class Meta:
        model = Busary
        exclude = ['staff']

    def __init__(self, *args, **kwargs):
        super(BusaryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClearedForm(forms.ModelForm):
    class Meta:
        model = Clearance
        exclude = ['staff']

    def __init__(self, *args, **kwargs):
        super(ClearedForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class IssueForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['staff']
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

