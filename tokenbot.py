from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyperclip
import time


def create_email():
    print('Creating Email')
    email_url = 'https://temp-mail.org/en/'

    email_browser.get(email_url)

    time.sleep(10)

    email_browser.find_element_by_id('click-to-copy').click()

    email = pyperclip.paste()

    return email


def register(email, password):
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

    code = verify()

    code_field = DCC_browser.find_element_by_xpath('/html/body/div[7]/dialog/form/div[1]/div[1]/div/input')
    code_field.send_keys(code)
    code_field.submit()

    navigate_page('0x8E51dD1d76a59c39F055067858606ab048593caA')
    pass


def verify():
    tab_url = 'https://www.google.com'  # URL B
    email_browser.execute_script("window.open('');")
    email_browser.switch_to.window(email_browser.window_handles[1])
    email_browser.get(tab_url)
    email_browser.close()
    email_browser.switch_to.window(email_browser.window_handles[0])
    print('Verifying')

    attempts = 0
    completed = False
    while not completed:
        try:
            attempts += 1
            if attempts == 12:
                break
            print(attempts)
            open_email = email_browser.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a/span[2]')
            open_email.click()
            completed = True
        except:
            time.sleep(1)

    if attempts == 12:
        ids = email_browser.find_elements_by_xpath('//*[@id="tm-body"]')
        print(ids)
        for ii in ids:
            print(1)
            print(ii.get_attribute('id'))  # id name as string

        #open_email = email_browser.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a/span[2]')
        #open_email.click()


    code = email_browser.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]').text
    string = code.split(': ')
    code = string[1]
    print(code)
    i = input('-----------------------------------------------------------------------------------------------------------------------')

    return code


def navigate_page(accountaddress):
    print('Waiting for funds')

    completed = False

    while not completed:
        try:
            element = DCC_browser.find_element_by_xpath('//*[@id="wallet-category"]/div[1]/button')
            element.click()
            completed = True
        except:
            time.sleep(1)

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
    element.send_keys("25")

    element = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    element.click()
    print('Done')
    pass


path_to_chromedriver = 'C:/Users/harle/Documents/chromedriver'  # change path as needed
option = webdriver.ChromeOptions()
option.add_argument("--headless")

# email_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)
# DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=option)

email_browser = webdriver.Chrome(executable_path=path_to_chromedriver)
DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver)

email = create_email()

thepassword = 'password'

register(email, thepassword)
