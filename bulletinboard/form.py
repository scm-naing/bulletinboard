from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


class PostSearchForm(forms.Form):
    """
    For post search form
    """
    keyword = forms.CharField(
        required=False,
        label="keyword: ",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )


class UserSearchForm(forms.Form):
    """
    For user search form
    """
    name = forms.CharField(
        required=False,
        label="Name: ",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=False,
        label="E-Mail: ",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    from_date = forms.DateField(
        required=False,
        label="From: ",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    to_date = forms.DateField(
        required=False,
        label="To: ",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )


class PostForm(forms.Form):
    """
    For Post create and update form
    """
    title = forms.CharField(
        required=False,
        label="Title *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        required=False,
        label="Description *",
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    def clean(self):
        """
        Check for valid post form fields
        """
        if not self.cleaned_data.get("title"):
            self.add_error("title", "Title can't be blank")
        if not self.cleaned_data.get("description"):
            self.add_error("description", "Description can't be blank")
        if self.cleaned_data.get("description"):
            des = self.cleaned_data.get("description")
            if len(des) > 255:
                self.add_error(
                    "description", "255 characters is maximum allowed.")


class UserForm(forms.Form):
    """
    For user create form
    """
    name = forms.CharField(
        required=False,
        label="Name *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=False,
        label="E-Mail Address *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        required=False,
        label="Password *",
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "password"})
    )
    passwordConfirm = forms.CharField(
        required=False,
        label="Password confirmation *",
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "password"})
    )
    USER_TYPE = (
        ("0", "Admin"),
        ("1", "User")
    )
    type = forms.CharField(
        required=False, label="Type",
        widget=forms.Select(choices=USER_TYPE, attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        required=False,
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dob = forms.DateField(
        required=False,
        label="Date of birth",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    profile = forms.FileField(
        required=False,
        label="Profile *",
        widget=forms.FileInput(
            attrs={"class": "form-control", "required": False})
    )

    def clean(self):
        """
        Check for valid user create form
        """
        if not self.cleaned_data.get("name"):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get("email"):
            self.add_error("email", "E-Mail can't be blank")
        if not self.cleaned_data.get("password"):
            self.add_error("password", "Password can't be blank")
        if not self.cleaned_data.get("passwordConfirm"):
            self.add_error("passwordConfirm",
                           "Password confirmation can't be blank")
        if self.cleaned_data.get("password") and self.cleaned_data.get("passwordConfirm"):
            if self.cleaned_data.get("password") != self.cleaned_data.get("passwordConfirm"):
                self.add_error(
                    None, "password and password confirmation must be match.")


class UserEditForm(forms.Form):
    """
    For user edit and detail form
    """
    name = forms.CharField(
        required=False,
        label="Name *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=False,
        label="E-Mail Address *",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    USER_TYPE = (
        ("0", "Admin"),
        ("1", "User")
    )
    type = forms.CharField(
        required=True,
        label="Type",
        widget=forms.Select(choices=USER_TYPE, attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        required=False,
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dob = forms.DateField(
        required=False,
        label="Date of birth",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    address = forms.CharField(
        required=False,
        label="Address",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    profile = forms.FileField(
        required=False,
        label="Profile",
        widget=forms.FileInput(
            attrs={"class": "form-control", "required": False})
    )

    def clean(self):
        """
        Check for user edit form valid
        """
        if not self.cleaned_data.get("name"):
            self.add_error("name", "Name can't be blank")
        if not self.cleaned_data.get("email"):
            self.add_error("email", "E-Mail can't be blank")
        if self.cleaned_data.get("password") and self.cleaned_data.get("passwordConfirm"):
            if self.cleaned_data.get("password") != self.cleaned_data.get("passwordConfirm"):
                self.add_error(
                    None, "password and password confirmation must be match.")


class csvForm(forms.Form):
    """
    For csv import
    """
    csv_file = forms.FileField(
        required=False,
        label="CSV file",
        widget=forms.FileInput(
            attrs={"class": "form-control", "required": False, "accept": ".csv"})
    )


class passwordResetForm(forms.Form):
    """
    For user profile password reset form
    """
    password = forms.CharField(
        required=False,
        label="Current Password *",
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "password"})
    )
    new_password = forms.CharField(
        required=False,
        label="New Password *",
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "password"})
    )
    new_password_confirm = forms.CharField(
        required=False,
        label="New Confirm Password *",
        widget=forms.TextInput(
            attrs={"class": "form-control", "type": "password"})
    )

    def clean(self):
        """
        To get clean form data of reset password form
        """
        if not self.cleaned_data.get("password"):
            self.add_error("password",
                           "Password can't be blank")
        if not self.cleaned_data.get("new_password"):
            self.add_error("new_password",
                           "New password can't be blank")
        if not self.cleaned_data.get("new_password_confirm"):
            self.add_error("new_password_confirm",
                           "New confirm password can't be blank")
        if self.cleaned_data.get("new_password") and self.cleaned_data.get("new_password_confirm"):
            if self.cleaned_data.get("new_password") != self.cleaned_data.get("new_password_confirm"):
                self.add_error(
                    "new_password_confirm", "New password and new password confirmation is not match.")


class SignUpForm(forms.Form):
    """
    For create new account form
    """
    name = forms.CharField(
        required=True, label="Name *", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        required=True, label="E-Mail Address *", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        required=True, label="Password *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))
    password_confirmation = forms.CharField(
        required=True, label="Password confirmation *", widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))

    def post(self, request, *args, **kwargs):
        """
        Create new accout (sign up)
        Para: form post method
        Return: render template of signUp form
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/posts")
        return render(request, self.template_name, {"form": form})
