from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import time

# Test not authenticated user urls
class Test1not_authenticated_urls(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")


    def test_urls(self):

        def get_urls_feedback(register_link):
            # Go to login page
            self.driver.get("http://127.0.0.1:8000/login_view")

            # Click register in the navigation
            register_nav_link = self.driver.find_element(By.ID, register_link)
            register_nav_link.click()

            # Check if registration page was loaded successful
            try:
                check_element = self.driver.find_element(By.ID, "register-username")
                # Registration page was rendered
                return True
            except:
                # Registration page was not rendered
                return False

        self.assertTrue(get_urls_feedback("register-nav-link"))
        self.assertTrue(get_urls_feedback("info-register-link"))

    def tearDown(self):
        self.driver.close()


# Test Register
class Test2Register(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")


    def test_register_form(self):

        # Return True for every fill in the feedback if registration was successful
        def get_register_feedback(username_input, email_input, password_input, password_confirmation_input):

            # Go to register page
            self.driver.get("http://127.0.0.1:8000/register_view")

            # Fill in the register form
            register_username = self.driver.find_element(By.ID, "register-username")
            register_username.send_keys(username_input)

            register_email = self.driver.find_element(By.ID, "register-email")
            register_email.send_keys(email_input)

            register_password = self.driver.find_element(By.ID, "register-password")
            register_password.send_keys(password_input)

            register_password_confirmation = self.driver.find_element(By.ID, "register-password-confirmation")
            register_password_confirmation.send_keys(password_confirmation_input)

            register_submit = self.driver.find_element(By.ID, "register-submit-btn")
            register_submit.click()

            # Check if registration was successful and index page was rendered
            try:
                check_element = self.driver.find_element(By.ID, "current-user-id")
                # Index page was rendered
                return True
            except:
                # Index page was not rendered
                return False

        # Register examples
        # Right register data
        self.assertTrue(get_register_feedback("Testman1", "testman1@email.com", "secret12345", "secret12345"))
        # False register data because username is already used
        self.assertFalse(get_register_feedback("Testman1", "testman1A@email.com", "secret12345", "secret12345"))
        # False register data because username to short
        self.assertFalse(get_register_feedback("Te2", "testman2@email.com", "secret12345", "secret12345"))
        # False register data because password to short
        self.assertFalse(get_register_feedback("Testman3", "testman3@email.com", "secret", "secret"))
        # False register data because password confirmation not right
        self.assertFalse(get_register_feedback("Testman4", "testman4@email.com", "secret12345", "secret12346"))
        # False register data because email not in the right format
        self.assertFalse(get_register_feedback("Testman5", "testman5email.com", "secret12345", "secret12345"))
        # False register data because email not in the right format
        self.assertFalse(get_register_feedback("Testman6", "Testman6@.com", "secret12345", "secret12345"))
        # False register data because email not in the right format
        self.assertFalse(get_register_feedback("Testman7", "Testman7@email.", "secret12345", "secret12345"))
        # False register data because email not in the right format
        self.assertFalse(get_register_feedback("Testman8", "Testman8email", "secret12345", "secret12345"))

    def tearDown(self):
        self.driver.close()


# Test Login
class Test3Login(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")

    def test_login_form(self):

        # Return True for every fill in the feedback if registration was successful
        def get_login_feedback(username_input, password_input):

            # Go to login page
            self.driver.get("http://127.0.0.1:8000/login_view")

            # Fill in the login form
            login_username = self.driver.find_element(By.ID, "login-username")
            login_username.send_keys(username_input)

            login_password = self.driver.find_element(By.ID, "login-password")
            login_password.send_keys(password_input)

            login_submit = self.driver.find_element(By.ID, "login-submit")
            login_submit.click()

            # Check if login was successful and index page was rendered
            try:
                check_element = self.driver.find_element(By.ID, "current-user-id")
                # Index page was rendered
                return True
            except:
                # Index page was not rendered
                return False

        # Register examples
        # Right login data created in the register test
        self.assertTrue(get_login_feedback("Testman1", "secret12345"))
        # False login data because password wrong
        self.assertFalse(get_login_feedback("Testman1", "secret"))
        # False login because username wrong
        self.assertFalse(get_login_feedback("Testman9", "secret12345"))

    def tearDown(self):
        self.driver.close()


# Test not authenticated user urls
class Test4authenticated_urls(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")


    def test_urls(self):

        def get_urls_feedback(some_link, response_id):

            # Go to login page
            self.driver.get("http://127.0.0.1:8000/login_view")

            # Fill in the login form
            login_username = self.driver.find_element(By.ID, "login-username")
            login_username.send_keys("Testman1")

            login_password = self.driver.find_element(By.ID, "login-password")
            login_password.send_keys("secret12345")

            login_submit = self.driver.find_element(By.ID, "login-submit")
            login_submit.click()

            # Click links as authenticated user
            register_nav_link = self.driver.find_element(By.ID, some_link)
            register_nav_link.click()

            # Check if the linked page was loaded successful
            try:
                check_element = self.driver.find_element(By.ID, response_id)
                # Registration page was rendered
                return True
            except:
                # Registration page was not rendered
                return False

        # Urls examples
        self.assertTrue(get_urls_feedback("crm-logo-link", "current-user-id"))
        self.assertTrue(get_urls_feedback("customers-link", "customer-firstname"))
        self.assertTrue(get_urls_feedback("tasks-link", "task-name"))
        self.assertTrue(get_urls_feedback("logout-logo-link", "login-username"))

    def tearDown(self):
        self.driver.close()


# Test create customers
class Test5CreateCustomers(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")

        # Go to login page and log in
        self.driver.get("http://127.0.0.1:8000/login_view")

        # Fill in the login form
        login_username = self.driver.find_element(By.ID, "login-username")
        login_username.send_keys("Testman1")

        login_password = self.driver.find_element(By.ID, "login-password")
        login_password.send_keys("secret12345")

        login_submit = self.driver.find_element(By.ID, "login-submit")
        login_submit.click()


    def test_create_customer_form(self):

        # Return True for every fill in the feedback if customer creation was successful
        def get_create_customer_feedback(customer_id, customer_first_name, customer_last_name, customer_email_address):

            # Go to customer page
            self.driver.get("http://127.0.0.1:8000/customers_view")

            # Fill in the create customer form
            first_name = self.driver.find_element(By.ID, "customer-firstname")
            first_name.send_keys(customer_first_name)

            last_name = self.driver.find_element(By.ID, "customer-lastname")
            last_name.send_keys(customer_last_name)

            email_address = self.driver.find_element(By.ID, "customer-email")
            email_address.send_keys(customer_email_address)

            create_customer_submit = self.driver.find_element(By.ID, "customer-create-btn")
            create_customer_submit.click()

            # Check if the customer creation was successful and the customer table was updated
            try:
                # Get data which is in the customer table
                check_id = self.driver.find_element(By.ID, "customer-table-id" + customer_id).text
                check_first_name = self.driver.find_element(By.ID, "customer-table-first-name" + customer_id).text
                check_last_name = self.driver.find_element(By.ID, "customer-table-last-name" + customer_id).text
                check_email_address = self.driver.find_element(By.ID, "customer-table-email-address" + customer_id).text

                # Check if the customer data row in the table is right
                if check_id == customer_id and check_first_name == customer_first_name and check_last_name == customer_last_name and check_email_address == customer_email_address:
                    return True
                else:
                    return False
            except:
                return False

        # Create customer examples
        self.assertTrue(get_create_customer_feedback("1", "Peter", "Peterman", "peterman@email.com"))
        self.assertTrue(get_create_customer_feedback("2", "John", "Johnman", "johnman@email.com"))
        # False because to short first name
        self.assertFalse(get_create_customer_feedback("3", "P", "Peterman", "peterman@email.com"))
        # False because to long last name
        self.assertFalse(get_create_customer_feedback("3", "Peter", "Petermanabcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyzabcdef", "peterman@email.com"))
        # False because email address not in right format
        self.assertFalse(get_create_customer_feedback("3", "Peter", "Peterman", "peterman@com"))
        self.assertFalse(get_create_customer_feedback("3", "Peter", "Peterman", "petermanemail.com"))
        self.assertFalse(get_create_customer_feedback("3", "Peter", "Peterman", "peterman@.com"))

    def tearDown(self):
        self.driver.close()


# Test create tasks
class Test6CreateTasks(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")

        # Go to login page and log in
        self.driver.get("http://127.0.0.1:8000/login_view")

        # Fill in the login form
        login_username = self.driver.find_element(By.ID, "login-username")
        login_username.send_keys("Testman1")

        login_password = self.driver.find_element(By.ID, "login-password")
        login_password.send_keys("secret12345")

        login_submit = self.driver.find_element(By.ID, "login-submit")
        login_submit.click()

    def test_create_task_form(self):

        # Return True for every fill in the feedback if task creation was successful
        def get_create_task_feedback(task_id, task_name, task_customer, task_date, task_price):

            # Go to task page
            self.driver.get("http://127.0.0.1:8000/tasks_view")

            # Fill in the create task form
            tasks_name = self.driver.find_element(By.ID, "task-name")
            tasks_name.send_keys(task_name)

            select_task_customer = self.driver.find_element(By.ID, "select-task-customer")
            select_task_customer.send_keys(task_customer)

            tasks_date = self.driver.find_element(By.ID, "task-date")
            tasks_date.send_keys(task_date)

            tasks_price = self.driver.find_element(By.ID, "task-price")
            tasks_price.send_keys(task_price)

            create_task_submit = self.driver.find_element(By.ID, "create-task-button")
            create_task_submit.click()


            # Check if the task creation was successful and the task table was updated
            try:
                # Get data which is in the task table
                check_id = self.driver.find_element(By.ID, "task-table-id" + task_id).text
                check_task_name = self.driver.find_element(By.ID, "task-table-name" + task_id).text
                check_task_customer = self.driver.find_element(By.ID, "task-table-customer" + task_id).text
                check_task_price = self.driver.find_element(By.ID, "task-table-price" + task_id).text

                # Check if the task data row in the table is right
                if check_id == task_id and check_task_name == task_name and check_task_customer == task_customer and check_task_price == (task_price + "€"):
                    return True
                else:
                    return False
            except:
                return False

        # Create task examples
        self.assertTrue(get_create_task_feedback("1", "Clean the window", "ID:1. Peterman", "17.08.2029", "109.99"))
        # False because old finish date
        self.assertFalse(get_create_task_feedback("2", "Clean the house", "ID:1. Peterman", "17.08.2000", "19.99"))

    def tearDown(self):
        self.driver.close()


# Check if task info page loaded with right data
class Test7TaskInfo(LiveServerTestCase):

    driver = webdriver.Edge()

    def setUp(self):
        # Choose url to visit
        self.driver.get("http://127.0.0.1:8000/")

        # Go to login page and log in
        self.driver.get("http://127.0.0.1:8000/login_view")

        # Fill in the login form
        login_username = self.driver.find_element(By.ID, "login-username")
        login_username.send_keys("Testman1")

        login_password = self.driver.find_element(By.ID, "login-password")
        login_password.send_keys("secret12345")

        login_submit = self.driver.find_element(By.ID, "login-submit")
        login_submit.click()


    def test_task_info(self):

        # Return True if the task info page is right
        def get_task_info_feedback(task_id, task_name, customer_last_name, task_price):

            # Go to task page
            self.driver.get("http://127.0.0.1:8000/tasks_view")
            

            # Click on the task name to get more infos
            task_name_info = self.driver.find_element(By.ID, "task-table-name" + task_id)
            task_name_info.click()


            try:
                # Get data from the task info page
                check_id = self.driver.find_element(By.ID, "task-info-id-t").text
                check_task_name = self.driver.find_element(By.ID, "task-info-name-t").text
                check_customer_last_name = self.driver.find_element(By.ID, "task-info-customer-last-name-t").text
                check_price = self.driver.find_element(By.ID, "task-info-price-t").text


                # Check if the task info data is right
                if check_id == ("ID:" + task_id) and check_task_name == ("Task name:" + task_name) and check_customer_last_name == ("Last name:" + customer_last_name) and check_price == ("Task price:" + task_price + "€"):

                    return True
                else:
                    return False
            except:
                # Return false if page was not loaded
                return False

        # Create task info examples and test the task from Test 6
        self.assertTrue(get_task_info_feedback("1", "Clean the window", "ID:1. Peterman", "109.99"))
        # False because this task not exist (Look Test 6)
        self.assertFalse(get_task_info_feedback("1", "Clean the house", "ID:1. Peterman", "19.99"))

    def tearDown(self):
        self.driver.close()



