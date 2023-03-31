from django.urls import reverse_lazy
from rest_framework.test import APITestCase, APIClient

from users_and_orgs.models import CustomUser
from users_and_orgs.serializers import UserSerializer


class UsersAndOrgsModelTestCase(APITestCase):
    def test_custom_user_has_no_username(self):
        """This test will check if the user has no username attribute"""
        user = CustomUser.objects.create(
            email="test@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        self.assertIsNone(user.username)

    def test_custom_user_creation(self):
        """This test will check if the user can be created successfully"""
        user = CustomUser.objects.create(
            email="test@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.last_name, "Last")
        self.assertEqual(user.first_name, "First")

    def test_custom_user_password(self):
        """This test will check if the user's password can be set"""
        user = CustomUser.objects.create(
            email="test@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        user.set_password("newpassword5678")
        self.assertTrue(user.check_password("newpassword5678"))


class UsersAndOrgsViewSetTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "password1234",
            "last_name": "Last",
            "first_name": "First",
        }
        self.put_data = {
            "email": "newtest@test.com",
            "password": "password1234",
            "first_name": "New First",
            "last_name": "New Last",
        }

    def test_user_viewset_list_users(self):
        """This test will check if a list of users can be retrieved using a GET request"""
        user1 = CustomUser.objects.create(
            email="test1@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        user2 = CustomUser.objects.create(
            email="test2@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        client = APIClient()
        client.force_authenticate(user=user1)
        response = client.get(reverse_lazy("customuser-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_user_viewset_post_new_user(self):
        """This test will check if a new user can be created using a POST request"""
        client = APIClient()
        response = client.post(reverse_lazy("customuser-list"), self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], "test@test.com")

    def test_user_viewset_delete_user(self):
        """This test will check if a user can be deleted using a DELETE request"""
        user = CustomUser.objects.create(
            email="test@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(
            reverse_lazy("customuser-detail", kwargs={"pk": user.id})
        )
        self.assertEqual(response.status_code, 204)

    def test_user_viewset_put_unauthorized(self):
        """This test will check if a user can be updated using a PUT request while unauthorized"""
        user = CustomUser.objects.create(
            email="test1@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        client = APIClient()
        response = client.put(
            reverse_lazy("customuser-detail", kwargs={"pk": user.id}), self.put_data
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Учетные данные не были предоставлены."}
        )

    def test_user_viewset_put_user(self):
        """This test will check if an authorized user can be updated using a PUT request"""
        client = APIClient()
        user = create_and_auth_user_by_token(self.user_data, client)
        response = client.put(
            reverse_lazy("customuser-detail", kwargs={"pk": user.id}), self.put_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "newtest@test.com")
        self.assertEqual(response.data["first_name"], "New First")
        self.assertEqual(response.data["last_name"], "New Last")

    def test_user_viewset_patch_user(self):
        """This test will check if a user can be updated using a PATCH request"""
        client = APIClient()
        user = create_and_auth_user_by_token(self.user_data, client)
        response = client.patch(
            reverse_lazy("customuser-detail", kwargs={"pk": user.id}),
            {"first_name": "New First", "password": "newpassword5678"},
        )
        self.assertEqual(response.status_code, 200)


def create_and_auth_user_by_token(user_data, client):
    response = client.post(reverse_lazy("customuser-list"), user_data)
    user = CustomUser.objects.get(id=response.data["id"], email=response.data["email"])
    access_token = client.post(
        reverse_lazy("token_obtain_pair"),
        data={"email": user_data["email"], "password": user_data["password"]},
    )
    client.force_authenticate(user=user, token=access_token)
    return user


class UsersAndOrdsSerializersTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "email": "test@test.com",
            "password": "password1234",
            "last_name": "Last",
            "first_name": "First",
        }

    def test_create_user_serializer(self):
        serializer = UserSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password("password1234"))

    def test_update_user_serializer_with_password(self):
        user = CustomUser.objects.create(
            email="test@test.com",
            password="password1234",
            last_name="Last",
            first_name="First",
        )
        data = {"password": "newpassword5678"}
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        user.refresh_from_db()
        self.assertTrue(user.check_password("newpassword5678"))
