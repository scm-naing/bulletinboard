from django.test import TestCase

from bulletinboard.form import PostForm, PostSearchForm, SignUpForm, UserEditForm, UserForm, UserSearchForm, passwordResetForm


class PostSearchFormTest(TestCase):
    def test_post_search_form(self):
        """
        Test search form for post list
        """
        form = PostSearchForm()
        self.assertEqual(form.fields["keyword"].label, "keyword: ")


class UserSearchFormTest(TestCase):
    def test_user_serarch_form(self):
        """
        Test serch form for user list
        """
        form = UserSearchForm()
        self.assertEqual(form.fields["name"].label, "Name: ")
        self.assertEqual(form.fields["email"].label, "E-Mail: ")
        self.assertEqual(form.fields["from_date"].label, "From: ")
        self.assertEqual(form.fields["to_date"].label, "To: ")


class PostFormTest(TestCase):
    def test_post_form_label(self):
        """
        Test post create and update form label
        """
        form = PostForm()
        self.assertTrue(form.fields["title"].label == "Title *")
        self.assertTrue(form.fields["description"].label == "Description *")

    def test_post_form_invalid(self):
        """
        Test validation fail of post form
        """
        form = PostForm(data={"title": "", "description": ""})
        self.assertFalse(form.is_valid())

    def test_post_form_description(self):
        """
        Test validation of description post form
        """
        form = PostForm(data={"title": "test", "description": "This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. This is test data. "})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        """
        Test valid post form
        """
        form = PostForm(data={"title": "test", "description": "test"})
        self.assertTrue(form.is_valid())


class UserFormTest(TestCase):
    def test_user_form_label(self):
        """
        Test labels in user form
        """
        form = UserForm()
        self.assertTrue(form.fields["name"].label == "Name *")
        self.assertTrue(form.fields["email"].label == "E-Mail Address *")
        self.assertTrue(form.fields["password"].label == "Password *")
        self.assertTrue(
            form.fields["passwordConfirm"].label == "Password confirmation *")
        self.assertTrue(form.fields["type"].label == "Type")
        self.assertTrue(form.fields["phone"].label == "Phone")
        self.assertTrue(form.fields["dob"].label == "Date of birth")
        self.assertTrue(form.fields["address"].label == "Address")
        self.assertTrue(form.fields["profile"].label == "Profile *")

    def test_user_form_invalid(self):
        """
        Test user form validation invalid
        """
        form = UserForm(data={
            "name": "",
            "email": "",
            "type": "0",
            "password": "",
            "passwordConfirm": "",
            "profile": ""
        })
        self.assertFalse(form.is_valid())

    def test_user_form_invalid_email(self):
        """
        Test user form email
        """
        form = UserForm(data={
            "name": "test",
            "email": "false mail",
            "password": "test",
            "passwordConfirm": "test",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_form_valid_email(self):
        """
        Test user form valid email
        """
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "password": "test",
            "passwordConfirm": "test",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_password(self):
        """
        Test user form password and password confirmation
        """
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "password": "test",
            "passwordConfirm": "test12",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_form_valid_password(self):
        """
        Test user form valid
        """
        form = UserForm(data={
            "name": "test",
            "email": "mail@test.com",
            "password": "test",
            "passwordConfirm": "test",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())


class UserEditFormTest(TestCase):
    def test_user_edit_form_label(self):
        """
        Test user edit form labels
        """
        form = UserEditForm()
        self.assertTrue(form.fields["name"].label == "Name *")
        self.assertTrue(form.fields["email"].label == "E-Mail Address *")
        self.assertTrue(form.fields["type"].label == "Type")
        self.assertTrue(form.fields["phone"].label == "Phone")
        self.assertTrue(form.fields["dob"].label == "Date of birth")
        self.assertTrue(form.fields["address"].label == "Address")
        self.assertTrue(form.fields["profile"].label == "Profile")

    def test_user_edit_form_invalid(self):
        """
        Test user edit form validation
        """
        form = UserEditForm(data={
            "name": "",
            "email": ""
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_invalid_email(self):
        """
        Test user edit form invalid email
        """
        form = UserEditForm(data={
            "name": "test",
            "email": "false mail",
            "password": "test",
            "passwordConfirm": "test",
            "profile": "test/path"
        })
        self.assertFalse(form.is_valid())

    def test_user_edit_form_valid(self):
        """
        Test user edit form correct validation
        """
        form = UserEditForm(data={
            "name": "test",
            "email": "mail@test.com",
            "type": "1",
            "profile": "test/path"
        })
        self.assertTrue(form.is_valid())


class PasswordResetFormTest(TestCase):
    def test_reset_form_label(self):
        """
        Test Password reset form labels
        """
        form = passwordResetForm()
        self.assertEqual(form.fields["password"].label, "Current Password *")
        self.assertEqual(form.fields["new_password"].label, "New Password *")
        self.assertEqual(
            form.fields["new_password_confirm"].label, "New Confirm Password *")

    def test_password_reset_form_invalid(self):
        """
        Test password reset form wrong
        """
        form = passwordResetForm(data={
            "password": "",
            "new_password": "",
            "new_password_confirm": ""
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_invalid(self):
        """
        Test password reset form invalid password and password confirmation
        """
        form = passwordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "asdf1234"
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        """
        Test password reset form valid
        """
        form = passwordResetForm(data={
            "password": "qwer1234",
            "new_password": "qwer4321",
            "new_password_confirm": "qwer4321"
        })
        self.assertTrue(form.is_valid())


class SignUpFormTest(TestCase):
    def test_sign_up_form_label(self):
        """
        Test sign up form labels
        """
        form = SignUpForm()
        self.assertEqual(form.fields["name"].label, "Name *")
        self.assertEqual(form.fields["email"].label, "E-Mail Address *")
        self.assertEqual(form.fields["password"].label, "Password *")
        self.assertEqual(
            form.fields["password_confirmation"].label, "Password confirmation *")

    def test_password_reset_form_password_invalid(self):
        """
        Test sign up form password and password confirmation
        """
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "asdf1234",
            "password_confirmation": "asdf4321",
        })
        self.assertFalse(form.is_valid())

    def test_password_reset_form_password_valid(self):
        """
        Test valid sign up form
        """
        form = SignUpForm(data={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "asdf1234",
            "password_confirmation": "asdf1234",
        })
        self.assertTrue(form.is_valid())
