# Imports
from selenium import webdriver
import time
import mailslurp_client


def create_email():  # Create a temporary email using the mailslurp api
    print('Creating Email')  # Identifier
    with mailslurp_client.ApiClient(configuration) as api_client:
        # create an inbox using the inbox controller
        api_instance = mailslurp_client.InboxControllerApi(api_client)
        inbox = api_instance.create_inbox()

        # check the id and email_address of the inbox
        assert len(inbox.id) > 0
        assert "mailslurp.com" in inbox.email_address
        return inbox, inbox.email_address


def register(email, password, inbox, destination):  # Register user by creating account/validation/navigation
    print('Registering Account')  # Identifier

    # Navigation using selenium
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

    code = verify(inbox)  # Verify in register, Once account verified, continue

    # Submit
    code_field = DCC_browser.find_element_by_xpath('/html/body/div[7]/dialog/form/div[1]/div[1]/div/input')
    code_field.send_keys(code)

    # Navigate the user interface with inputting where the token destination is
    navigate_page(destination, email, password)
    pass


def slicer(startstring, endstring, string):  # Helper funct6ion to navigate the html in email body
    key = ''
    index = string.find(startstring)
    string = string[index + len(startstring):]
    for char in range(200):
        if string[char] == endstring:
            return key
        else:
            key += string[char]


def verify(inbox):  # Helper function for register user to interact with mail and return verification code
    print("Verifying Email")
    with mailslurp_client.ApiClient(configuration) as api_client:
        # Find the inbox
        inbox_1 = inbox

        # receive email for inbox 1
        waitfor_controller = mailslurp_client.WaitForControllerApi(api_client)
        email = waitfor_controller.wait_for_latest_email(inbox_id=inbox_1.id, timeout=30000, unread_only=True)

        assert email.subject == "Welcome to the DCP Network!"

        html = email.body
        code = slicer("Your verification code is: ", "<", html)

        return code


def navigate_page(accountaddress, email, password):  # Navigate user interface primarily using selenium
    print('Waiting for Funds')

    time.sleep(3)  # account for reload time

    DCC_browser.get('https://portal.distributed.computer/#Accounts')  # Avoid clicking another button (Easier)

    time.sleep(3)  # account for reload time

    clock = 0
    while True:  # Function to check bank balance over and over again until the free credits have been applied
        clock += 2
        print('Time Elapsed: ' + str(clock))
        DCC_browser.find_element_by_class_name('reload-icon').click()
        time.sleep(1)
        amount = DCC_browser.find_element_by_xpath('//*[@id="key-bank-balance"]').text
        time.sleep(1)
        if amount[0] != '0':
            break

    print('Transferring Credits')  # Check statement

    # Selenium code
    element = DCC_browser.find_element_by_class_name("chevron-icon")
    element.click()

    time.sleep(.4)

    element = DCC_browser.find_element_by_id("key-transfer-button")
    element.click()

    element = DCC_browser.find_element_by_id("transfer-to-address")
    element.send_keys(accountaddress)

    # Input amount to transfer over
    element = DCC_browser.find_element_by_xpath('/html/body/div[6]/dialog/form/div[1]/div[2]/div/input')
    element.send_keys("25")

    element = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    element.click()

    time.sleep(3)
    print('Done')
    pass


def run():  # Run one iteration of the program by calling all necessary functions
    inbox, email = create_email()

    accountpassword = 'password'
    tokendestination = '0x8E51dD1d76a59c39F055067858606ab048593caA'

    register(email, accountpassword, inbox, tokendestination)


if __name__ == '__main__':  # Main function that support multiple iterations
    # Configuring the Temporary mail account
    api_key = '554300a3c04b316e113c71d1008ae5c6a88149218fc3db03b0e7e6d791b7c779'
    configuration = mailslurp_client.Configuration()
    configuration.api_key['x-api-key'] = api_key

    # Configure the chromedriver
    path_to_chromedriver = 'C:/Users/harle/Documents/chromedriver'  # change path as needed
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")

    num_iterations = 4  # Number of iterations

    # For loop for the multiple iterations
    for i in range(num_iterations):
        headless = True
        if headless:
            DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)
        else:
            DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver)

        run()
        DCC_browser.quit()
