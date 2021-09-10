from django.test import TestCase, Client
from competitions.models import Competition
import datetime
import os
from footgasm.settings import base
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class OrdersTests(TestCase):
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
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

    def test_cart_with_no_login(self):
        c = Client()
        response = c.get("/cart/order-summary/")
        status_code = response.status_code
        self.assertEqual(status_code, 302) # check login redirect
       # self.assertEqual(str(messages[0]), 'You do not have an active order')
    
    def test_no_active_cart_with_login(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        response = c.get("/cart/order-summary/", follow=True)
        status_code = response.status_code
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have an active order')
        self.assertEqual(status_code, 200)
    
    def test_add_item_to_cart(self):
        c = Client()
        logged_in = c.login(username='testuser', password='12345')

        response = c.get("/cart/add-to-cart/1/1/1", follow=True)
        status_code = response.status_code
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This item was added to your cart.')
        self.assertEqual(status_code, 200)
    
    # def test_add_more_than_20(self):
    #     c = Client()
    #     logged_in = c.login(username='testuser', password='12345')
    #     response = c.get("/cart/add-to-cart/1/25/1", follow=True)
    #     status_code = response.status_code
    #     messages = list(get_messages(response.wsgi_request))
    #     print(messages)
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'You have already purchased 0 tickets so you only 20 remaining.')
    #     self.assertEqual(status_code, 200)

        
        
       