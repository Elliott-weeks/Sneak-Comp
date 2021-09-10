from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from competitions.models import Competition
from pages.models import HomePageImage
import datetime
from django.core.files.base import ContentFile
from footgasm.settings import base
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Create your tests here.


class PagesTestCase(TestCase):
    def setUp(self):
        competiton = Competition()
        d = datetime.date(2021, 10, 19)
        competiton.name = "Travis ones"
        competiton.competition_end_date = d
        competiton.competition_answers_one = "london"
        competiton.competition_answers_two = "nyc"
        competiton.competition_question = "capital of the world"
        competiton.competition_answers_three = "dubai"
        competiton.price = "2.66"
        competiton.size = "10"
        competiton.description = "i am desc"
        competiton.competition_correct_answer = 1
        competiton.ticket_limit = 1000
        competiton.state = "published"
        path = os.path.join(
            base.BASE_DIR, "media/images/2021/03/28/dunkHien.jpeg")
        competiton.image = path
        competiton.save()
        home_page = HomePageImage()
        home_page.image = path
        home_page.save()
        home_page_2 = HomePageImage()
        home_page_2.image = path
        home_page_2.save()

    def test_page_index_load_with_context(self):
        c = Client()
        response = c.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.context['comps']), 1)
        self.assertEqual(len(response.context['banner']), 2)

    def test_page_faq_load(self):
        c = Client()
        response = c.get("/faq")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_page_how_to_play(self):
        c = Client()
        response = c.get("/how-to-play")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_page_index_post_req(self):
        c = Client()
        response = c.post("/")
        status_code = response.status_code
        self.assertEqual(status_code, 405)

    def test_page_faq_post_req(self):
        c = Client()
        response = c.post("/faq")
        status_code = response.status_code
        self.assertEqual(status_code, 405)

    def test_page_how_to_play_post_req(self):
        c = Client()
        response = c.post("/how-to-play")
        status_code = response.status_code
        self.assertEqual(status_code, 405)
       


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.close()
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_id('login-btn').click()
        google_login_btn = self.selenium.find_element_by_id('google-sign-in')
        facebook = self.selenium.find_element_by_id('facebook-sign-in')
        self.assertIn("Sneaker Competition", self.selenium.title)
        self.assertIsNotNone(google_login_btn)
        self.assertIsNotNone(facebook)
        
        

