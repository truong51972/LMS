from django import forms
from .models import User, Role

# Form for creating and editing users
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'full_name', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super(UserForm, self).__init__(*args, **kwargs)
        role_names = ['Admin', 'Instructor', 'Student']
        
        roles_in_form = Role.objects.all()
        for role_name in role_names:
            if role_name == user_role: break
            roles_in_form = roles_in_form.exclude(role_name= role_name)

        self.fields['role'].queryset = roles_in_form

# Form for creating and editing roles
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']