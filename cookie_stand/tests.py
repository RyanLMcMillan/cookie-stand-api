from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CookieStand

###########################################################################################
# ATTENTION:
# DATABASES should be set to use SQLite
# Easiest way to ensure that is to comment out all the Postgres stuff in project/.env
# That will run using defaults, which is SQLite
###########################################################################################


class CookieStandTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_cookie_stand = CookieStand.objects.create(
            location="Hummus Cookie",
            owner=testuser1,
            description="Drizzled with olive oil for extra cookie flavor.",
        )
        test_cookie_stand.save()

    # class 32
    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_cookie_stand_model(self):
        cookie_stand = CookieStand.objects.get(id=1)
        actual_owner = str(cookie_stand.owner)
        actual_location = str(cookie_stand.location)
        actual_description = str(cookie_stand.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_location, "Hummus Cookie")
        self.assertEqual(actual_description, "Drizzled with olive oil for extra cookie flavor.")

    def test_get_cookie_stand_list(self):
        url = reverse("cookie_stand_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = response.data
        self.assertEqual(len(cookie_stand), 1)
        self.assertEqual(cookie_stand[0]["location"], "Hummus Cookie")

    def test_get_cookie_stand_by_id(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = response.data
        self.assertEqual(cookie_stand["location"], "Hummus Cookie")

    def test_create_cookie_stand(self):
        url = reverse("cookie_stand_list")
        data = {"owner": 1, "location": "Snickers", "description": "frozen please", }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cookie_stand = CookieStand.objects.all()
        self.assertEqual(len(cookie_stand), 2)
        self.assertEqual(CookieStand.objects.get(id=2).location, "Snickers")

    def test_update_cookie_stand(self):
        url = reverse("cookie_stand_detail", args=(1,))
        data = {
            "owner": 1,
            "location": "Hummus Cookie",
            "description": "Generously drizzle with olive oil for extra cookie flavor.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = CookieStand.objects.get(id=1)
        self.assertEqual(cookie_stand.location, data["location"])
        self.assertEqual(cookie_stand.owner.id, data["owner"])
        self.assertEqual(cookie_stand.description, data["description"])

    def test_delete_cookie_stand(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cookie_stand = CookieStand.objects.all()
        self.assertEqual(len(cookie_stand), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("cookie_stand_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
