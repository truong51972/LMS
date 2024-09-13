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
    
# Form for creating and editing roles
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name']
