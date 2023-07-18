from django.test import TestCase

base_url = "/api/v1/"

FIRST_USER = {"username": "DMITRY", "password": "36PIZZA!pepperony31", "double_password": "36PIZZA!pepperony31", "email": "andrey.glukhovsky@gmail.sry", "first_name": "Antonio", "last_name": "Golum", "middle_name": "Svarovsky"}
SECOND_USER = {"username": "DMITRY12", "password": "36PIZZA!pepperony31", "double_password": "36PIZZA!pepperony31", "email": "andrey1.glukhovsky@gmail.sry", "first_name": "Antonio", "last_name": "Golum", "middle_name": "Svarovsky"}


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.client.post(f"{base_url}registration/", data=FIRST_USER)

    def test_registration_successful(self):
        response = self.client.post(f"{base_url}registration/", data=SECOND_USER)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "DMITRY12")

    def test_registration_full_duplicate(self):
        response = self.client.post(f"{base_url}registration/", data=FIRST_USER)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], 'this email or username already exists')

    def test_registration_username_duplicate(self):
        third_user = FIRST_USER.copy()
        third_user["email"] = "DILAN@MAIL.RSR"
        response = self.client.post(f"{base_url}registration/", data=third_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], 'this email or username already exists')

    def test_registration_email_duplicate(self):
        third_user = FIRST_USER.copy()
        third_user["username"] = "DILAN"
        response = self.client.post(f"{base_url}registration/", data=third_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], 'this email or username already exists')

    def test_registration_not_valid_password_and_not_valid_length(self):
        third_user = FIRST_USER.copy()
        third_user["password"] = "DILAN"
        response = self.client.post(f"{base_url}registration/", data=third_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], 'Enter a valid value.')
        self.assertEqual(response.data["password"][1], 'Ensure this field has at least 8 characters.')

    def test_registration_not_valid_password(self):
        third_user = FIRST_USER.copy()
        third_user["password"] = "DILAN123123"
        response = self.client.post(f"{base_url}registration/", data=third_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], 'Enter a valid value.')

    def test_registration_not_valid_length(self):
        third_user = FIRST_USER.copy()
        third_user["password"] = "1_aA@!"
        response = self.client.post(f"{base_url}registration/", data=third_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], 'Enter a valid value.')
        self.assertEqual(response.data["password"][1], 'Ensure this field has at least 8 characters.')

    def test_successful_auth(self):
        response = self.client.post(f"{base_url}token/", data=FIRST_USER)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("access"))
        self.assertTrue(response.data.get("refresh"))

    def test_invalid_auth(self):
        response = self.client.post(f"{base_url}token/", data=SECOND_USER)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get("detail"), "No active account found with the given credentials")

    def test_special_raise(self):
        raise Exception("oh, no!")