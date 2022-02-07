import time
import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# LOCATORS
LOGIN_BUTTON = (By.XPATH, "//*[contains(text(), 'Log In')]")
CARD_IMAGES = (By.CSS_SELECTOR, "form > aside > img")
AMEX_BANNER = (By.CSS_SELECTOR, ".banner__tagline")
FAQ_CHEVRON = (By.CSS_SELECTOR, "div[data-test-pqo='faq']")
FOOTER = (By.CSS_SELECTOR, "footer[data-module-name='axp-footer']")
FIRST_NAME = (By.CSS_SELECTOR, "input[data-test-pqo='first-name']")
LAST_NAME = (By.CSS_SELECTOR, "input[data-test-pqo='last-name']")
HOME_ADDRESS = (By.CSS_SELECTOR, "input[data-test-pqo='address1']")
CITY = (By.CSS_SELECTOR, "input[data-test-pqo='city']")
STATE = (By.CSS_SELECTOR, "select[data-test-pqo='state']")
ZIP_CODE = (By.CSS_SELECTOR, "input[data-test-pqo='zip']")
SSN = (By.CSS_SELECTOR, "input[data-test-pqo='ssn']")
TOTAL_ANNUAL_INCOME = (By.CSS_SELECTOR, "input[data-test-pqo='income']")
NON_TAXABLE_INCOME = (By.CSS_SELECTOR, "input[data-test-pqo='nontaxIncome']")
VIEW_MY_CARD_OFFERS_BTN = (By.CSS_SELECTOR, "button[data-test-pqo='submit']")
RESULT_MESSAGE = (By.XPATH, "//*[contains(text(), 'You pre-qualify for a special Card offer! Apply now.')]")

# URL
MAIN_URL = "https://card.americanexpress.com/d/pre-qualified-offers/"
MEMBER_LOGIN_PAGE_URL = "https://www.americanexpress.com/en-us/account/login?inav=iNavLnkLog"

# TEST DATA
FIRST_NAME_DATA = "PIQONE"
LAST_NAME_DATA = "TIQONE"
HOME_ADDRESS_DATA = "IQ Street"
CITY_DATA = "NEW YORK"
STATE_DATA = "New York"
ZIP_CODE_DATA = "10285"
SSN_DATA = "9999"
TOTAL_ANNUAL_INCOME_DATA = "10,000"
NON_TAXABLE_INCOME_DATA = "9,000"
LOGIN_PAGE_TITLE = "Log In to My Account | American Express US"
PAGE_RESULT_MESSAGE = "You pre-qualify for a special Card offer! Apply now."


class Americanexpress(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(20)
        self.browser.maximize_window()
        self.browser.get(MAIN_URL)

    def test_is_amex_banner_one_the_top_of_the_page(self):
        banner = self.browser.find_element(*AMEX_BANNER)
        banner.is_displayed()
        print(banner.location)
        assert banner.location['y'] == 8, "AMEX banner changed location on the page"

    def test_is_login_button_directs_to_member_login_page(self):
        browser = self.browser
        login_button = browser.find_element(*LOGIN_BUTTON)
        login_button.click()
        browser.close()
        member_login_page = browser.window_handles[0]
        browser.switch_to.window(member_login_page)
        print(browser.current_url)
        print(browser.title)
        assert browser.current_url == MEMBER_LOGIN_PAGE_URL, "You weren't directed to login page"
        assert browser.title == LOGIN_PAGE_TITLE, "The title of current page isn't 'Login into my account'"

    def test_are_card_images_beside_the_form(self):
        browser = self.browser
        card_images = browser.find_element(*CARD_IMAGES).is_enabled()
        assert card_images, "Card images are not beside the form, DOM tree changed"

    def test_is_faq_sections_expand(self):
        browser = self.browser
        chevrons = browser.find_elements(*FAQ_CHEVRON)
        browser.execute_script("window.scrollBy(0, 1400)")
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(FAQ_CHEVRON))
        for chevron in chevrons:
            chevron.click()
            time.sleep(2)
            chevron.click()

    def test_is_footer_displayed(self):
        browser = self.browser
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while not match:
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
            if lastCount == lenOfPage:
                match = True
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located(FOOTER))
        assert WebDriverWait(browser, 10).until(EC.visibility_of_element_located(FOOTER)), \
            "Footer is not displayed on the page"

    def test_fill_form(self):
        browser = self.browser
        f_name = browser.find_element(*FIRST_NAME)
        f_name.send_keys(FIRST_NAME_DATA)
        l_name = browser.find_element(*LAST_NAME)
        l_name.send_keys(LAST_NAME_DATA)
        h_address = browser.find_element(*HOME_ADDRESS)
        h_address.send_keys(HOME_ADDRESS_DATA)
        city = browser.find_element(*CITY)
        city.send_keys(CITY_DATA)
        select = Select(browser.find_element(*STATE))
        select.select_by_visible_text(STATE_DATA)
        zip_code = browser.find_element(*ZIP_CODE)
        zip_code.send_keys(ZIP_CODE_DATA)
        ssn = browser.find_element(*SSN)
        ssn.send_keys(SSN_DATA)
        total_income = browser.find_element(*TOTAL_ANNUAL_INCOME)
        total_income.send_keys(TOTAL_ANNUAL_INCOME_DATA)
        non_taxable = browser.find_element(*NON_TAXABLE_INCOME)
        non_taxable.send_keys(NON_TAXABLE_INCOME_DATA)
        assert f_name.get_property("value") == FIRST_NAME_DATA, "First name data hasn't been entered"
        assert l_name.get_property("value") == LAST_NAME_DATA, "Last name data hasn't been entered"
        assert city.get_property("value") == CITY_DATA, "City data hasn't been entered"
        assert zip_code.get_property("value") == ZIP_CODE_DATA, "Zip code data hasn't been entered"
        assert ssn.get_property("value") == SSN_DATA, "SSN data hasn't been entered"
        assert total_income.get_property("value")[1:7] == TOTAL_ANNUAL_INCOME_DATA, \
            "Total annual income data hasn't been entered"
        assert non_taxable.get_property("value") == NON_TAXABLE_INCOME_DATA, \
            "Non taxable income data hasn't been entered"
        time.sleep(2)  # to make sure all fields were filled

    def test_is_view_my_card_offer_message_present(self):
        browser = self.browser
        browser.find_element(*FIRST_NAME).send_keys(FIRST_NAME_DATA)
        browser.find_element(*LAST_NAME).send_keys(LAST_NAME_DATA)
        browser.find_element(*HOME_ADDRESS).send_keys(HOME_ADDRESS_DATA)
        browser.find_element(*CITY).send_keys(CITY_DATA)
        select = Select(browser.find_element(*STATE))
        select.select_by_visible_text(STATE_DATA)
        browser.find_element(*ZIP_CODE).send_keys(ZIP_CODE_DATA)
        browser.find_element(*SSN).send_keys(SSN_DATA)
        browser.find_element(*TOTAL_ANNUAL_INCOME).send_keys(TOTAL_ANNUAL_INCOME_DATA)
        browser.find_element(*NON_TAXABLE_INCOME).send_keys(NON_TAXABLE_INCOME_DATA)
        browser.find_element(*VIEW_MY_CARD_OFFERS_BTN).click()
        message = browser.find_element(*RESULT_MESSAGE).text
        assert message == PAGE_RESULT_MESSAGE, "Success result message  isn't appeared"
        time.sleep(2)

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
