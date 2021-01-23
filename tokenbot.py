from selenium import webdriver
import pyperclip
import time
from pynput.keyboard import Controller, Key


def create_email():
    email_url = 'https://temp-mail.org/en/'

    email_browser.get(email_url)

    time.sleep(10)

    email_browser.find_element_by_id('click-to-copy').click()

    email = pyperclip.paste()

    return email


def register(email, password):
    DCC_browser.get('https://portal.distributed.computer')
    keyboard = Controller()

    reg = DCC_browser.find_element_by_id("splash-signup")
    reg.click()
    one = DCC_browser.find_element_by_id("email")
    one.send_keys(email)

    time.sleep(1)

    for j in range(2):
        keyboard.press("\t")
        keyboard.release("\t")
        for i in password:
            keyboard.press(i)
            keyboard.release(i)

    login = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    login.click()

    time.sleep(15)

    code = verify()

    DCC_browser.find_element_by_xpath('/html/body/div[7]/dialog/form/div[1]/div[1]/div/input').send_keys(code)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    time.sleep(2)

    navigate_page('0x8E51dD1d76a59c39F055067858606ab048593caA')
    pass


def navigate_page(accountaddress):
    time.sleep(2)

    element = DCC_browser.find_element_by_xpath('//*[@id="wallet-category"]/div[1]/button')
    element.click()

    time.sleep(3)

    #while True:
    #    DCC_browser.find_element_by_xpath('//*[@id="keyring-0xc450fbd6e8f039c7b7ba2018d1a9d1cd9938711b"]/div[1]/h6[2]/button').click()
    #    time.sleep(1)
    #    amount = DCC_browser.find_element_by_xpath('//*[@id="key-bank-balance"]').text
    #    time.sleep(1)
    #    print(amount[0])
    #    if amount[0] != '0':
    #        break

    time.sleep(120)

    element = DCC_browser.find_element_by_class_name("chevron-icon")
    element.click()

    time.sleep(2)

    element = DCC_browser.find_element_by_id("key-transfer-button")
    element.click()

    time.sleep(1)

    element = DCC_browser.find_element_by_id("transfer-to-address")
    element.send_keys(accountaddress)
    element.send_keys("\t")

    time.sleep(1)

    keyboard = Controller()
    keyboard.press("2")
    keyboard.release("2")
    keyboard.press("5")
    keyboard.release("5")

    element = DCC_browser.find_element_by_class_name("continue.green-modal-button")
    element.click()
    pass


def verify():
    time.sleep(2)

    open_email = email_browser.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[2]/div[1]/a/span[2]')
    open_email.click()

    time.sleep(2)

    code = email_browser.find_element_by_xpath('//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]').text
    string = code.split(': ')
    code = string[1]
    return code


path_to_chromedriver = 'C:/Users/harle/Documents/chromedriver'  # change path as needed
email_browser = webdriver.Chrome(executable_path=path_to_chromedriver)
DCC_browser = webdriver.Chrome(executable_path=path_to_chromedriver)

email = create_email()

thepassword = 'password'

register(email, thepassword)
