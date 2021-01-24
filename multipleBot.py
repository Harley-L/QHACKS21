from selenium import webdriver
import time
api_key = '554300a3c04b316e113c71d1008ae5c6a88149218fc3db03b0e7e6d791b7c779'
import mailslurp_client

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
    print('Registering Account')
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
    #code_field.submit()

    navigate_page('0x8E51dD1d76a59c39F055067858606ab048593caA', email, password)
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
    print("Verifying Email")
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


def print_elements():
    ids = DCC_browser.find_elements_by_xpath('//*[@id]')
    for ii in ids:
        # print ii.tag_name
        print(ii.get_attribute('id'))
    print(DCC_browser.current_url)
    pass


def navigate_page(accountaddress, email, password):
    print('Waiting for Funds')

    time.sleep(3)

    DCC_browser.get('https://portal.distributed.computer/#Accounts')

    time.sleep(3)

    clock = 0
    while True:
        clock += 2
        print('Time Elapsed: ' + str(clock))
        DCC_browser.find_element_by_class_name('reload-icon').click()
        time.sleep(1)
        amount = DCC_browser.find_element_by_xpath('//*[@id="key-bank-balance"]').text
        time.sleep(1)
        if amount[0] != '0':
            break

    print('Transferring Credits')

    element = DCC_browser.find_element_by_class_name("chevron-icon")
    element.click()

    time.sleep(.4)

    element = DCC_browser.find_element_by_id("key-transfer-button")
    element.click()

    element = DCC_browser.find_element_by_id("transfer-to-address")
    element.send_keys(accountaddress)

    element = DCC_browser.find_element_by_xpath('/html/body/div[6]/dialog/form/div[1]/div[2]/div/input')
    element.send_keys("25")

    element = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    element.click()

    time.sleep(3)
    print('Done')
    pass


def run():
    inbox, email = create_email()

    thepassword = 'password'

    register(email, thepassword, inbox)


if __name__ == '__main__':
    path_to_chromedriver = 'C:/Users/harle/Documents/chromedriver'  # change path as needed
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")

    num_iterations = 4

    for i in range(num_iterations):
        headless = True

        if headless:
            DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)
        else:
            DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver)

        run()
        DCC_browser.quit()