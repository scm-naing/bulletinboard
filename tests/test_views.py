import datetime
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from bulletinboard.models import Post, User


class LoginViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_login_initial_view(self):
        response = self.client.get(reverse("user_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/login.html"
        )

    def test_login_invalid_email(self):
        res_invalid_email = self.client.post(
            reverse("user_login"), {"email": "wrong@test.mm", "password": ""})
        messages = list(res_invalid_email.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email does not exist or deleted")

    def test_login_invalid_password(self):
        res_invalid_pass = self.client.post(
            reverse("user_login"), {"email": "test@user.com", "password": "wrong"})
        messages = list(res_invalid_pass.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Email and Password does not match.")

    def test_login(self):
        response = self.client.post(reverse("user_login"), {
                                    "email": "test@user.com", "password": "thePass129Z"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class PostListViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        # Create post
        test_post = Post.objects.create(
            title="post of test",
            description="This post is created by tester ...",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        test_post.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/')

    def test_redirect_if_logged_in(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(reverse("index"))
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(response.context["page_obj"][0].title, "post of test")
        self.assertEqual(
            response.context["page_obj"][0].description, "This post is created by tester ...")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "index.html"
        )

    def test_form_post_search(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "post of test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_form_post_search_invalid(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "xxxxx"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 0)

    def test_form_post_redirect_create(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse("index"), {"_create": True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/post/create/")


class UserListViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        # user create
        user = User.objects.create(
            name="test001",
            email="test001@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        user.save()

    def test_user_list_without_login(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/users/')

    def test_user_list_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(reverse("user-list"))
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(
            response.context["page_obj"][0].email, "test001@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user_list.html"
        )

    def test_user_list_search(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        from_date = datetime.date.today()
        to_date = datetime.date.today()
        response = self.client.post(
            reverse("user-list"),
            {
                "name": "test001",
                "email": "test001@gmail.com",
                "from_date": from_date,
                "to_date": to_date,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user_list.html"
        )


class PostCreateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_post_create_without_login(self):
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/post/create/')

    def test_post_create_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_create_form_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
                "description": "this is description"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_create_form_create(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
             "description": "this is description"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

    def test_post_create_form_cancel(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        self.client.get(reverse('post-create'))
        res_cancel = self.client.post(reverse("post-create"), {"_cancel": True, "title": "test title",
                                                               "description": "this is description"})
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse("post-create"))


class UserCreateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_user_create_without_login(self):
        response = self.client.get(reverse("user-create"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/user/create/')

    def test_user_create_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(reverse('user-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-create.html"
        )

    def test_user_create_form_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "testemail@gmail.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "bulletinboard/user-create.html"
            )

    def test_user_create_form_withoutfile(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse('user-create'),
            {
                "_save": True,
                "name": "test name",
                "email": "testemail@gmail.com",
                "password": "thePass00911",
                "passwordConfirm": "thePass00911",
                "type": "0",
                "phone": "09222292",
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_user_create_exist_email(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["profile"] = "sample_img.jpg"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "test@user.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )

    def test_user_create_form_cancel(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        self.client.get(reverse('user-create'))
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            res_cancel = self.client.post(
                reverse('user-create'),
                {
                    "_cancel": True,
                    "name": "test name",
                    "email": "testemail@gmail.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse("user-create"))

    def test_user_create_form_create(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["profile"] = "sample_img.jpg"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            response = self.client.post(
                reverse('user-create'),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "testemail@gmail.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("user-list"))


class PostUpdateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="test title",
            description="Hello world!!",
            status="1",
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_update_without_login(self):
        response = self.client.get(
            reverse("post-update",  kwargs={'pk': self.test_post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url == "/accounts/login?next=/post/{}/".format(str(self.test_post.id)))

    def test_post_update_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_update_form_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update", "post_status": "0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )
    
    def test_post_update_form_confirm_without_status(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_update_form_edit(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session['status'] = "0"
        session.save()
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update title",
             "description": "this is update description", "post_status": "0"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

    def test_post_update_form_cancel(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}),)
        res_cancel = self.client.post(reverse('post-update', kwargs={'pk': self.test_post.id}),
                                      {"_cancel": True, "title": "test title",
                                       "description": "this is description"})
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse(
            'post-update', kwargs={'pk': self.test_post.id}))


class PostDetail(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="detail test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_detail_without_login(self):
        response = self.client.get(
            reverse("post-detail"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)

    def test_post_detail(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse('post-detail'), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 200)


class PostDeleteConfirmTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="delete test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_post_delete_confirm_without_login(self):
        response = self.client.get(
            reverse("post-delete-confirm"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)

    def test_post_delete_without_login(self):
        response = self.client.get(
            reverse("post-delete"), {"user_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)

    def test_post_delete_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("post-delete-confirm"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("post-delete"), {"post_id": self.test_post.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class UserProfileTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_user_profile_without_login(self):
        response = self.client.get(
            reverse("user-profile"))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("user-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["email"], "test@user.com")


class UserDetail(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        self.user = User.objects.create(
            name="test001",
            email="test001@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.user.save()

    def test_user_detail_without_login(self):
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)

    def test_user_detail(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 200)


class UserDeleteTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        self.user = User.objects.create(
            name="deleteUser",
            email="deleteuser@gmail.com",
            password="passwordTest11",
            profile="fake/path",
            type="0",
            phone="01234543",
            address="yangon",
            dob=timezone.now(),
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.user.save()

    def test_user_delete_confirm_without_login(self):
        response = self.client.get(
            reverse("user-delete-confirm"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)

    def test_user_delete_without_login(self):
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)

    def test_user_delete_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("user-delete-confirm"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/")


class CsvDownloadTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        self.test_post = Post.objects.create(
            title="detail test",
            description="Hello world!!",
            status="1",
            user=test_user,
            created_user_id=test_user.id,
            updated_user_id=test_user.id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.test_post.save()

    def test_csv_download_without_login(self):
        response = self.client.get(
            reverse("post-list-download"))
        self.assertEqual(response.status_code, 302)

    def test_csv_download(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse("post-list-download"))
        self.assertEqual(response.status_code, 200)


class UserPasswordResetTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_password_reset_without_login(self):
        response = self.client.get(
            reverse("post-list-download"))
        self.assertTrue(
            response.url == "/accounts/login?next=/post/list/download")
        self.assertEqual(response.status_code, 302)

    def test_password_reset_with_wrong_password(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(reverse(
            "password-reset"), {"password": "wrong111", "new_password": "thePass123Z", "new_password_confirm": "thePass123Z"})
        self.assertContains(response, "Current password is wrong!", html=True)

    def test_password_reset(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(reverse(
            "password-reset"), {"password": "thePass129Z", "new_password": "thePass123Z", "new_password_confirm": "thePass123Z"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user-list"))


class SignUpViewTest(TestCase):
    def test_sign_up_initial(self):
        response = self.client.get(reverse("create_account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/sign_up.html"
        )

    def test_sign_up(self):
        response = self.client.post(reverse("create_account"), {
            "name": "new_acc",
            "email": "accnew@example.com",
            "password": "accNew0077",
            "password_confirmation": "accNew0077",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class CsvImportViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_csv_import_without_login(self):
        res = self.client.get(reverse("csv-import"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/accounts/login?next=/csv/import/')

    def test_csv_import_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(reverse("csv-import"))
        self.assertTrue(response.status_code == 200)

    def test_csv_import_without_file(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(reverse("csv-import"), {"csv_file": ""})
        self.assertEqual(
            response.context["err_message"], "Please choose a file")

    def test_csv_import_with_invalid_file(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(
                response.context["err_message"], "Please choose csv format")

    def test_csv_import_with_multi_role_file(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\csv_wrong.csv", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(
                response.context["err_message"], "Post upload csv must have 3 columns")

    def test_csv_import(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\csv.csv", "rb") as csv_file:
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("index"))


class UserEditViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        self.user = test_user

    def test_user_update_without_login(self):
        response = self.client.get(
            reverse("user-update", kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 302)

    def test_user_update_initial(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.get(
            reverse('user-update', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-update.html"
        )

    def test_user_update_form_confirm(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        response = self.client.post(
            reverse('user-update', kwargs={'pk': self.user.id}),
            {
                "_save": True,
                "name": "test name",
                "email": "testemail@gmail.com",
                "password": "thePass00911",
                "passwordConfirm": "thePass00911",
                "type": "0",
                "phone": "09222292",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-update.html"
        )

    def test_user_update_form_confirm_withfile(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            response = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "testemail@gmail.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "bulletinboard/user-update.html"
            )

    def test_user_edit_form_cancel(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["updated_image"] = True
        session.save()
        self.client.get(reverse('user-update', kwargs={'pk': self.user.id}))
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            res_cancel = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_cancel": True,
                    "name": "test name",
                    "email": "testemail@gmail.com",
                    "password": "thePass00911",
                    "passwordConfirm": "thePass00911",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse(
                'user-update', kwargs={'pk': self.user.id}))

    def test_user_edit_form_nofile(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["updated_image"] = False
        session["profile"] = ""
        session.save()
        response = self.client.post(
            reverse('user-update', kwargs={'pk': self.user.id}),
            {
                "_save": True,
                "name": "test name",
                "email": "test@user.com",
                "type": "0",
                "phone": "09222292",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user-list"))

    def test_user_edit_form_withfile(self):
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = False
        session["updated_image"] = True
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "testupdate@gmail.com",
                    "type": "0",
                    "phone": "09222292",
                    "profile": profile
                }
            )
            session['save_confirm_page'] = True
            session["profile"] = "sample_img.jpg"
            session.save()
            res = self.client.post(
                reverse('user-update', kwargs={'pk': self.user.id}),
                {
                    "_save": True,
                    "name": "test name",
                    "email": "testupdate@gmail.com",
                    "type": "0",
                    "phone": "09222292",
                }
            )
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.url, reverse("user-list"))
