# your_app/tests/test_tasks.py
# from django.test import TestCase
# from utils.email_task import send_email_task
# from django.core.mail import outbox

# class CeleryEmailTaskTest(TestCase):
#     def test_send_email_task(self):
#         # Perform the task
#         send_email_task.delay('Test Subject', 'Test Message', ['test@example.com'])

#         # Check if the email is in the outbox
#         self.assertEqual(len(outbox), 1)
#         self.assertEqual(outbox[0].subject, 'Test Subject')
#         self.assertEqual(outbox[0].to, ['test@example.com'])



# =========================================================================
import json
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .utils import (
    JsonResponse,
    get_app_list,
    get_admin_site,
    get_admin_site_name,
    SuccessMessageMixin,
    get_model_queryset,
    get_possible_language_codes,
    get_original_menu_items,
    get_menu_item_url,
    get_menu_items,
    context_to_dict,
    user_is_authenticated,
)

class YourFileTests(TestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_JsonResponse(self):
        data = {'key': 'value'}
        response = JsonResponse(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(json.loads(response.content.decode()), data)

        # Print the actual response content
        print("Actual Response Content:", response.content.decode())

    def test_get_app_list(self):
        # Create a sample request for testing
        request = RequestFactory().get('/admin/')

        # Ensure the function runs without errors
        app_list = get_app_list({'request': request})

        # Print the actual app list
        print("Actual App List:", app_list)

        # Add more specific assertions based on your expectations

    # Add more test methods for other functions/classes in your file

    def test_user_is_authenticated(self):
        # Ensure the function correctly identifies an authenticated user
        self.assertTrue(user_is_authenticated(self.user))

        # Ensure the function correctly identifies an unauthenticated user
        self.assertFalse(user_is_authenticated(User()))

        # Print a message indicating the user authentication status
        print("Is User Authenticated?", user_is_authenticated(self.user))

    # Add more test methods as needed

        

    





