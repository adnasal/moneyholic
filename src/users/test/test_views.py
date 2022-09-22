from faker import Faker
from rest_framework.test import APITestCase

fake = Faker()


class TestUserListTestCase(APITestCase):

    def setUp(self):
        pass

    def test_post_request_with_no_data_fails(self):
        pass

    def test_post_request_with_valid_data_succeeds(self):
        pass


class TestUserDetailTestCase(APITestCase):

    def setUp(self):
        pass

    def test_get_request_returns_a_given_user(self):
        pass

    def test_put_request_updates_a_user(self):
        pass
