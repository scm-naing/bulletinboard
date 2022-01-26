from django.utils import timezone
from django.test import TestCase
from bulletinboard.models import Post, User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            name="test",
            email="test@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id="1",
            updated_user_id="1",
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_label(self):
        user = User.objects.get(id=1)
        name_label = user._meta.get_field("name").verbose_name
        email_label = user._meta.get_field("email").verbose_name
        password_label = user._meta.get_field("password").verbose_name
        profile_label = user._meta.get_field("profile").verbose_name
        type_label = user._meta.get_field("type").verbose_name
        phone_label = user._meta.get_field("phone").verbose_name
        address_label = user._meta.get_field("address").verbose_name
        dob_label = user._meta.get_field("dob").verbose_name
        c_user_label = user._meta.get_field("created_user_id").verbose_name
        u_user_label = user._meta.get_field("updated_user_id").verbose_name
        d_user_label = user._meta.get_field("delete_user_id").verbose_name
        c_at_label = user._meta.get_field("created_at").verbose_name
        u_at_label = user._meta.get_field("updated_at").verbose_name
        d_at_label = user._meta.get_field("deleted_at").verbose_name
        self.assertEqual(name_label, "name")
        self.assertEqual(email_label, "email address")
        self.assertEqual(password_label, "password")
        self.assertEqual(profile_label, "profile")
        self.assertEqual(type_label, "type")
        self.assertEqual(phone_label, "phone")
        self.assertEqual(address_label, "address")
        self.assertEqual(dob_label, "dob")
        self.assertEqual(c_user_label, "created user id")
        self.assertEqual(u_user_label, "updated user id")
        self.assertEqual(d_user_label, "delete user id")
        self.assertEqual(c_at_label, "created at")
        self.assertEqual(u_at_label, "updated at")
        self.assertEqual(d_at_label, "deleted at")

    def test_max_length(self):
        user = User.objects.get(id=1)
        name_max = user._meta.get_field("name").max_length
        email_max = user._meta.get_field("email").max_length
        password_max = user._meta.get_field("password").max_length
        profile_max = user._meta.get_field("profile").max_length
        type_max = user._meta.get_field("type").max_length
        phone_max = user._meta.get_field("phone").max_length
        address_max = user._meta.get_field("address").max_length
        self.assertEqual(name_max, 30)
        self.assertEqual(email_max, 255)
        self.assertEqual(password_max, 255)
        self.assertEqual(profile_max, 255)
        self.assertEqual(type_max, 1)
        self.assertEqual(phone_max, 20)
        self.assertEqual(address_max, 255)

    def test_default(self):
        user = User.objects.get(id=1)
        type_default = user._meta.get_field("type").default
        c_user_default = user._meta.get_field("created_user_id").default
        u_user_default = user._meta.get_field("updated_user_id").default
        c_at_default = user._meta.get_field("created_at").default
        u_at_default = user._meta.get_field("updated_at").default
        is_staff_default = user._meta.get_field("is_staff").default
        is_superuser_default = user._meta.get_field("is_superuser").default
        is_active_default = user._meta.get_field("is_active").default
        self.assertEqual(type_default, "1")
        self.assertEqual(c_user_default, 1)
        self.assertEqual(u_user_default, 1)
        self.assertEqual(c_at_default, timezone.now)
        self.assertEqual(u_at_default, timezone.now)
        self.assertEqual(is_staff_default, True)
        self.assertEqual(is_superuser_default, True)
        self.assertEqual(is_active_default, True)

    def test_user_object_is_email(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.email}'
        self.assertEqual(str(user), expected_object_name)

    def test_staff_user_register(self):
        user = User.objects.create_staffuser(
            "staffuser@example.com", "thestaffuser123")
        self.assertEqual(user.staff, True)
        self.assertEqual(user.active, True)
        self.assertEqual(user.email, "staffuser@example.com")

    def test_create_super_user(self):
        user = User.objects.create_superuser(
            "superuser@example.com", "theSuperUser123")
        self.assertEqual(user.staff, True)
        self.assertEqual(user.active, True)
        self.assertEqual(user.admin, True)
        self.assertEqual(user.email, "superuser@example.com")

    def test_user_has_perm(self):
        user = User.objects.get(id=1)
        has_perm = user.has_perm(None)
        self.assertEqual(has_perm, True)

    def test_user_has_module_perms(self):
        user = User.objects.get(id=1)
        has_module_perms = user.has_module_perms(None)
        self.assertEqual(has_module_perms, True)

    def test_user_create_without_mail(self):
        try:
            User.objects.create_user(None, "1234")
        except ValueError:
            pass



class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Post.objects.create(
            title="test title",
            description="Hello world!!",
            status="1",
            created_user_id="1",
            updated_user_id="1",
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_label(self):
        post = Post.objects.get(id=1)
        title_label = post._meta.get_field("title").verbose_name
        des_label = post._meta.get_field("description").verbose_name
        status_label = post._meta.get_field("status").verbose_name
        c_user_label = post._meta.get_field("created_user_id").verbose_name
        u_user_label = post._meta.get_field("updated_user_id").verbose_name
        c_at_label = post._meta.get_field("created_at").verbose_name
        u_at_label = post._meta.get_field("updated_at").verbose_name
        self.assertEqual(title_label, "title")
        self.assertEqual(des_label, "description")
        self.assertEqual(status_label, "status")
        self.assertEqual(c_user_label, "created user id")
        self.assertEqual(u_user_label, "updated user id")
        self.assertEqual(c_at_label, "created at")
        self.assertEqual(u_at_label, "updated at")

    def test_post_max_length(self):
        post = Post.objects.get(id=1)
        title_max = post._meta.get_field("title").max_length
        des_max = post._meta.get_field("description").max_length
        status_max = post._meta.get_field("status").max_length
        self.assertEqual(title_max, 255)
        self.assertEqual(des_max, 255)
        self.assertEqual(status_max, 1)

    def test_post_default(self):
        post = Post.objects.get(id=1)
        status_default = post._meta.get_field("status").default
        self.assertEqual(status_default, "1")

    def test_post_object_is_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(str(post), expected_object_name)
