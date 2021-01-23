from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyperclip
import time
api_key = '554300a3c04b316e113c71d1008ae5c6a88149218fc3db03b0e7e6d791b7c779'
import mailslurp_client
import re

configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = api_key


def create_email():
    print('Creating Email')
    with mailslurp_client.ApiClient(configuration) as api_client:

        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        inbox = api_instance.create_inbox()

        # check the id and email_address of the inbox
        assert len(inbox.id) > 0
        assert "mailslurp.com" in inbox.email_address
        return inbox, inbox.email_address



def register(email, password, inbox):
    print('Registering')
    DCC_browser.get('https://portal.distributed.computer')

    reg = DCC_browser.find_element_by_id("splash-signup")
    reg.click()
    one = DCC_browser.find_element_by_id("email")
    one.send_keys(email)

    password_field = DCC_browser.find_element_by_xpath('/html/body/div[6]/dialog/form/div[1]/div[3]/div/input')
    password_field.send_keys(password)

    password_field = DCC_browser.find_element_by_xpath('/html/body/div[6]/dialog/form/div[1]/div[4]/div/input')
    password_field.send_keys(password)
    password_field.submit()

    code = verify(inbox)

    code_field = DCC_browser.find_element_by_xpath('/html/body/div[7]/dialog/form/div[1]/div[1]/div/input')
    code_field.send_keys(code)
    code_field.submit()

    navigate_page('0x8E51dD1d76a59c39F055067858606ab048593caA')
    pass


def slicer(startstring, endstring, string):
    key = ''
    index = string.find(startstring)
    string = string[index + len(startstring):]
    for char in range(200):
        if string[char] == endstring:
            return key
        else:
            key += string[char]


def verify(inbox):
    print("Verifying")
    with mailslurp_client.ApiClient(configuration) as api_client:
        # Find the inbox
        inbox_1 = inbox

        # receive email for inbox 1
        waitfor_controller = mailslurp_client.WaitForControllerApi(api_client)
        email = waitfor_controller.wait_for_latest_email(inbox_id=inbox_1.id, timeout=30000, unread_only=True)

        assert email.subject == "Welcome to the DCP Network!"

        html = email.body
        match = slicer("Your verification code is: ","<",html)

        return match


def navigate_page(accountaddress):
    print('Waiting for funds')

    completed = False

    a = 0

    time.sleep(2)

    DCC_browser.get('https://portal.distributed.computer/#Accounts')

    one = DCC_browser.find_element_by_id("splash-email")
    one.clear()
    one.send_keys(email)

    two = DCC_browser.find_element_by_id("splash-password")
    two.clear()
    two.send_keys('password')

    login = DCC_browser.find_element_by_id("splash-signin")
    login.click()

    #element = DCC_browser.find_element_by_xpath('//*[@id="wallet-category"]/div[1]/button')
    #element.click()

    # while not completed:
    #     try:
    #         print(a)
    #         a += 1
    #         element = DCC_browser.find_element_by_xpath('//*[@id="wallet-category"]/div[1]/button')
    #         element.click()
    #         print('found')
    #         completed = True
    #     except:
    #         time.sleep(1)

    print('in wallet')
    time.sleep(1)

    clock = 0
    while True:
        clock += 2
        DCC_browser.find_element_by_class_name('reload-icon').click()
        time.sleep(1)
        amount = DCC_browser.find_element_by_xpath('//*[@id="key-bank-balance"]').text
        time.sleep(1)
        if amount[0] != '0':
            break

    print('Transferring')
    print('Time taken: ' + str(clock))

    element = DCC_browser.find_element_by_class_name("chevron-icon")
    element.click()

    time.sleep(.4)

    element = DCC_browser.find_element_by_id("key-transfer-button")
    element.click()

    element = DCC_browser.find_element_by_id("transfer-to-address")
    element.send_keys(accountaddress)

    element = DCC_browser.find_element_by_xpath('/html/body/div[6]/dialog/form/div[1]/div[2]/div/input')
    element.send_keys("1")

    element = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    element.click()
    print('Done')
    pass


path_to_chromedriver = 'C:/Users/harle/Documents/chromedriver'  # change path as needed
option = webdriver.ChromeOptions()
option.add_argument("--headless")

# email_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)
DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)

# email_browser = webdriver.Chrome(executable_path=path_to_chromedriver)
# DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver)

inbox, email = create_email()

thepassword = 'password'

register(email, thepassword, inbox)
