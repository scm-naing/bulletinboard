import datetime
from django.utils import timezone
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from bulletinboard.models import Post, User


class LoginViewTest(TestCase):
    def setUp(self):
        """
        Initial set up for login view test
        """
        # execute
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_login_initial_view(self):
        """
        Test login view at initial
        """
        # execute
        response = self.client.get(reverse("user_login"))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/login.html"
        )

    def test_login_invalid_email(self):
        """
        Test login view with invalid email
        """
        # execute
        res_invalid_email = self.client.post(
            reverse("user_login"), {"email": "wrong@test.mm", "password": ""})
        messages = list(res_invalid_email.context["messages"])
        # assertion
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email does not exist or deleted")

    def test_login_invalid_password(self):
        """
        Test login view with invalid password
        """
        # execute
        res_invalid_pass = self.client.post(
            reverse("user_login"), {"email": "test@user.com", "password": "wrong"})
        messages = list(res_invalid_pass.context["messages"])
        # assertion
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Email and Password does not match.")

    def test_login(self):
        """
        Test login view with correct email and password
        """
        # execute
        response = self.client.post(reverse("user_login"), {
                                    "email": "test@user.com", "password": "thePass129Z"})
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class PostListViewTest(TestCase):
    def setUp(self):
        """
        Initial set up funtion for post list view
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        # execute
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
        """
        Test route to post list view without login
        """
        # prepare
        response = self.client.get(reverse("index"))
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/')

    def test_redirect_if_logged_in(self):
        """
        Test post list after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(reverse("index"))
        # assertion
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(response.context["page_obj"][0].title, "post of test")
        self.assertEqual(
            response.context["page_obj"][0].description, "This post is created by tester ...")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "index.html"
        )

    def test_form_post_search(self):
        """
        Test post list keyword search
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "post of test"})
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 1)

    def test_form_post_search_invalid(self):
        """
        Test post list search with no data reslt
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse("index"), {"_search": True, "keyword": "xxxxx"})
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 0)

    def test_form_post_redirect_create(self):
        """
        Test redirect to post create
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse("index"), {"_create": True})
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/post/create/")


class UserListViewTest(TestCase):
    def setUp(self):
        """
        Initial set up function for user list view
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        # execute
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
        """
        Test redirect user list without login
        """
        # execute
        response = self.client.get(reverse("user-list"))
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/users/')

    def test_user_list_initial(self):
        """
        Test user list after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(reverse("user-list"))
        # assertion
        self.assertEqual(len(response.context["page_obj"]), 1)
        self.assertEqual(
            response.context["page_obj"][0].email, "test001@gmail.com")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user_list.html"
        )

    def test_user_list_search(self):
        """
        Test user list search form
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        from_date = datetime.date.today()
        to_date = datetime.date.today()
        # execute
        response = self.client.post(
            reverse("user-list"),
            {
                "name": "test001",
                "email": "test001@gmail.com",
                "from_date": from_date,
                "to_date": to_date,
            }
        )
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user_list.html"
        )


class PostCreateViewTest(TestCase):
    def setUp(self):
        """
        Initial set up function for post create view
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_post_create_without_login(self):
        """
        Test redirect to post create without login
        """
        # execute
        response = self.client.get(reverse("post-create"))
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/post/create/')

    def test_post_create_initial(self):
        """
        Test post create view after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(reverse('post-create'))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_create_form_confirm(self):
        """
        Test post create view confirm page
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
                "description": "this is description"}
        )
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_create_form_create(self):
        """
        Test new post create
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        # execute
        response = self.client.post(
            reverse('post-create'),
            {"_save": True, "title": "test title",
             "description": "this is description"}
        )
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

    def test_post_create_form_cancel(self):
        """
        Test submit cancel in post create page
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        # execute
        self.client.get(reverse('post-create'))
        res_cancel = self.client.post(reverse("post-create"), {"_cancel": True, "title": "test title",
                                                               "description": "this is description"})
        # assertion
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse("post-create"))


class UserCreateViewTest(TestCase):
    def setUp(self):
        """
        Initial set up for user create view
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_user_create_without_login(self):
        """
        Test user create view without login
        """
        # execute
        response = self.client.get(reverse("user-create"))
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url == '/accounts/login?next=/user/create/')

    def test_user_create_initial(self):
        """
        Test user create after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(reverse('user-create'))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-create.html"
        )

    def test_user_create_form_confirm(self):
        """
        Test user create confirm view
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "bulletinboard/user-create.html"
            )

    def test_user_create_form_withoutfile(self):
        """
        Test user create without file
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
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
        # assertion
        self.assertEqual(response.status_code, 200)

    def test_user_create_exist_email(self):
        """
        Test user create with existing email
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["profile"] = "sample_img.jpg"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(response.status_code, 400)

    def test_user_create_form_cancel(self):
        """
        Test cancel submit
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        self.client.get(reverse('user-create'))
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse("user-create"))

    def test_user_create_form_create(self):
        """
        Test new user create
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["profile"] = "sample_img.jpg"
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("user-list"))


class PostUpdateViewTest(TestCase):
    def setUp(self):
        """
        Initial set up for post update
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        # execute
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
        """
        Test post update view without login
        """
        # execute
        response = self.client.get(
            reverse("post-update",  kwargs={'pk': self.test_post.id}))
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url == "/accounts/login?next=/post/{}/".format(str(self.test_post.id)))

    def test_post_update_initial(self):
        """
        Test post update after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_update_form_confirm(self):
        """
        Test post update confirm page
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update", "post_status": "0"}
        )
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_update_form_confirm_without_status(self):
        """
        Test post update confrim without status
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update test title",
                "description": "this is description update"}
        )
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/post-create.html"
        )

    def test_post_update_form_edit(self):
        """
        Test post update
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session['status'] = "0"
        session.save()
        # execute
        response = self.client.post(
            reverse('post-update',  kwargs={'pk': self.test_post.id}),
            {"_save": True, "title": "update title",
             "description": "this is update description", "post_status": "0"}
        )
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

    def test_post_update_form_cancel(self):
        """
        Test cancel in post update
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session.save()
        self.client.get(
            reverse('post-update', kwargs={'pk': self.test_post.id}),)
        # execute
        res_cancel = self.client.post(reverse('post-update', kwargs={'pk': self.test_post.id}),
                                      {"_cancel": True, "title": "test title",
                                       "description": "this is description"})
        # assertion
        self.assertEqual(res_cancel.status_code, 302)
        self.assertEqual(res_cancel.url, reverse(
            'post-update', kwargs={'pk': self.test_post.id}))


class PostDetail(TestCase):
    def setUp(self):
        """
        Initial set up for post detail
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

        # execute
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
        """
        Test post detail dialog without login
        """
        # execute
        response = self.client.get(
            reverse("post-detail"), {"post_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_post_detail(self):
        """
        Test post detail after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse('post-detail'), {"post_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 200)


class PostDeleteConfirmTest(TestCase):
    def setUp(self):
        """
        Initial set up for post delete
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        # execute
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
        """
        Test post delete confirm dialog without login
        """
        # execute
        response = self.client.get(
            reverse("post-delete-confirm"), {"post_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_post_delete_without_login(self):
        """
        Test post delete dialog without login
        """
        # execute
        response = self.client.get(
            reverse("post-delete"), {"user_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_post_delete_confirm(self):
        """
        Test post delete confirm dialog after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("post-delete-confirm"), {"post_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        """
        Test post delete after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("post-delete"), {"post_id": self.test_post.id})
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class UserProfileTest(TestCase):
    def setUp(self):
        """
        Initial set up for user profile view
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_user_profile_without_login(self):
        """
        Test user profile without login
        """
        # execute
        response = self.client.get(
            reverse("user-profile"))
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_user_profile_initial(self):
        """
        Test user profile after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("user-profile"))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["email"], "test@user.com")


class UserDetail(TestCase):
    def setUp(self):
        """
        Initial set up function for user detail dialog view
        """
        # prepare
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
        """
        Test user detial dialog without login
        """
        # execute
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_user_detail(self):
        """
        Test user detail dialog after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("user-detail"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 200)


class UserDeleteTest(TestCase):
    def setUp(self):
        """
        Initial set up for user delete
        """
        # prepare
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
        """
        Test user delete confirm page without login
        """
        # execute
        response = self.client.get(
            reverse("user-delete-confirm"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_user_delete_without_login(self):
        """
        Test user delete without login
        """
        # execute
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_user_delete_confirm(self):
        """
        Test user delete confirm page after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("user-delete-confirm"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        """
        Test user delete after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("user-delete"), {"user_id": self.user.id})
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/")


class CsvDownloadTest(TestCase):
    def setUp(self):
        """
        Initial set up for csv download
        """
        # prepare
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
        """
        Test csv download without login
        """
        # execute
        response = self.client.get(
            reverse("post-list-download"))
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_csv_download(self):
        """
        Test csv download after login
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse("post-list-download"))
        # assertion
        self.assertEqual(response.status_code, 200)


class UserPasswordResetTest(TestCase):
    def setUp(self):
        """
        Initial set up function for user password reset page
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_password_reset_without_login(self):
        """
        Test password reset view without login
        """
        # execute
        response = self.client.get(
            reverse("post-list-download"))
        # assertion
        self.assertTrue(
            response.url == "/accounts/login?next=/post/list/download")
        self.assertEqual(response.status_code, 302)

    def test_password_reset_with_wrong_password(self):
        """
        Test password reset view with wrong current password
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(reverse(
            "password-reset"), {"password": "wrong111", "new_password": "thePass123Z", "new_password_confirm": "thePass123Z"})
        # assertion
        self.assertContains(response, "Current password is wrong!", html=True)

    def test_password_reset(self):
        """
        Test password reset
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(reverse(
            "password-reset"), {"password": "thePass129Z", "new_password": "thePass123Z", "new_password_confirm": "thePass123Z"})
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user-list"))


class SignUpViewTest(TestCase):
    def test_sign_up_initial(self):
        """
        Test create account view at initial
        """
        # execute
        response = self.client.get(reverse("create_account"))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "registration/sign_up.html"
        )

    def test_sign_up(self):
        """
        Test create new account (sign up)
        """
        # execute
        response = self.client.post(reverse("create_account"), {
            "name": "new_acc",
            "email": "accnew@example.com",
            "password": "accNew0077",
            "password_confirmation": "accNew0077",
        })
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class CsvImportViewTest(TestCase):
    def setUp(self):
        """
        Initial set up for csv import
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()

    def test_csv_import_without_login(self):
        """
        Test csv import without login
        """
        # execute
        res = self.client.get(reverse("csv-import"))
        # assertion
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/accounts/login?next=/csv/import/')

    def test_csv_import_initial(self):
        """
        Test csv import page after login success
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(reverse("csv-import"))
        # assertion
        self.assertTrue(response.status_code == 200)

    def test_csv_import_without_file(self):
        """
        Test csv import without file
        """
        # prepare 
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.post(reverse("csv-import"), {"csv_file": ""})
        # assertion
        self.assertEqual(
            response.context["err_message"], "Please choose a file")

    def test_csv_import_with_invalid_file(self):
        """
        Test csv import with invalid file
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as csv_file:
            # execute
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            # assertion
            self.assertEqual(
                response.context["err_message"], "Please choose csv format")

    def test_csv_import_with_multi_role_file(self):
        """
        Test csv import with invalid file (multiple row)
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\csv_wrong.csv", "rb") as csv_file:
            # execute
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            # assertion
            self.assertEqual(
                response.context["err_message"], "Post upload csv must have 3 columns")

    def test_csv_import(self):
        """
        Test csv success import
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\csv.csv", "rb") as csv_file:
            # execute
            response = self.client.post(
                reverse("csv-import"), {"csv_file": csv_file})
            # assertion
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse("index"))


class UserEditViewTest(TestCase):
    def setUp(self):
        """
        Initial set up for user edit
        """
        # prepare
        test_user = User.objects.create_user(
            email="test@user.com", password="thePass129Z")
        test_user.type = "1"
        test_user.save()
        self.user = test_user

    def test_user_update_without_login(self):
        """
        Test user update without login
        """
        # execute
        response = self.client.get(
            reverse("user-update", kwargs={'pk': self.user.id}))
        # assertion
        self.assertEqual(response.status_code, 302)

    def test_user_update_initial(self):
        """
        Test user update after login
        """
        # prepare 
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
        response = self.client.get(
            reverse('user-update', kwargs={'pk': self.user.id}))
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-update.html"
        )

    def test_user_update_form_confirm(self):
        """
        Test user update confirmation page
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        # execute
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
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bulletinboard/user-update.html"
        )

    def test_user_update_form_confirm_withfile(self):
        """
        Test user update confirmation page without login
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(
                response, "bulletinboard/user-update.html"
            )

    def test_user_edit_form_cancel(self):
        """
        Test user edit form cancel submit
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["updated_image"] = True
        session.save()
        self.client.get(reverse('user-update', kwargs={'pk': self.user.id}))
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(res_cancel.status_code, 302)
            self.assertEqual(res_cancel.url, reverse(
                'user-update', kwargs={'pk': self.user.id}))

    def test_user_edit_form_nofile(self):
        """
        Test user edit without file
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = True
        session["updated_image"] = False
        session["profile"] = ""
        session.save()
        # execute
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
        # assertion
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user-list"))

    def test_user_edit_form_withfile(self):
        """
        Test user edit with file
        """
        # prepare
        self.client.login(email="test@user.com", password="thePass129Z")
        session = self.client.session
        session['save_confirm_page'] = False
        session["updated_image"] = True
        session.save()
        with open(str(settings.BASE_DIR)+"\\media\\test\\sample_img.jpg", "rb") as profile:
            # execute
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
            # assertion
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.url, reverse("user-list"))
