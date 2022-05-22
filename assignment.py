'''Assignment File'''

import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import Configuration
from Library import ConfigReader

class ZenPortal:
    '''Zenportal class'''

    username = "//input[@name='email']"
    password = "//input[@name='password']"
    submit_button = "//button[@type='submit']"
    zenportal_icon = "//div[@class='sc-gsnTZi eHpwon']"
    left_menu = "//div[@class='ml-4']"
    queries_option = "//div[text()='Queries']"
    profile_name = "//h5[text()='Shourya']"
    add_query_button = "//button[@class='NavButtons_add__button__6ukaP']"
    enter_query_textbox = "//textarea[@placeholder='Enter your query in detail']"
    get_answer_button = "//button[text()='Get Answer']"
    confirm_button = "(//div[@class='modal-content radius']//button[@class='modal__btn__continue' and text()='Confirm'])[2]"
    feedback_area = "//textarea[@id='feedbackArea']"
    done_button = "//button[@class='modal__btn__continue' and text()='Done']"

    def setup(self):
        '''Zenportal method'''
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        driver = self.driver
        driver.maximize_window()
        driver.get(ConfigReader.readConfigData('Details','URL'))


    def login(self):
        '''Login to guvi'''
        self.setup()
        self.driver.find_element(By.XPATH,
        value=self.username).send_keys(ConfigReader.readConfigData('Details','username'))
        self.driver.find_element(By.XPATH,
        value=self.password).clear()
        self.driver.find_element(By.XPATH,
        value=self.password).send_keys(ConfigReader.readConfigData('Details','password'))
        self.driver.find_element(By.XPATH, value=self.submit_button).click()
        wait = WebDriverWait(self.driver,30)
        wait.until(EC.url_contains("https://www.zenclass.in/class"))
        return self.driver.current_url

    def scrap_data(self):
        '''scrap data'''
        url = self.login()
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'lxml')
        return soup.prettify()

    def list_elements(self):
        '''List all menu options'''
        self.login()
        zen_portal_menu=[]
        zenicon = self.driver.find_element(By.XPATH, value=self.zenportal_icon)
        actions = ActionChains(self.driver)
        actions.move_to_element(zenicon)
        actions.perform()
        ele = self.driver.find_elements(By.XPATH, value=self.left_menu)
        for i in ele:
            time.sleep(2)
            zen_portal_menu.append(i.text)
        return zen_portal_menu

    def raise_queries(self):
        '''Raise Queries'''
        self.login()
        self.driver.implicitly_wait(10)
        zenicon = self.driver.find_element(By.XPATH, value=self.zenportal_icon)
        actions = ActionChains(self.driver)
        actions.move_to_element(zenicon)
        actions.perform()
        wait=WebDriverWait(self.driver,30)
        queries_menu=self.driver.find_element(By.XPATH, value=self.queries_option)
        wait.until(EC.visibility_of(queries_menu))
        queries_menu.click()
        profile=self.driver.find_element(By.XPATH,value=self.profile_name)
        wait.until(EC.visibility_of(profile))
        actions.move_to_element(profile)
        actions.perform()
        for i in range(5):
            add_query=self.driver.find_element\
            (By.XPATH,value=self.add_query_button)
            wait.until(EC.visibility_of(add_query))
            add_query.click()
            enterquery=self.driver.find_element\
            (By.XPATH,value=self.enter_query_textbox)
            wait.until(EC.visibility_of(enterquery))
            enterquery.send_keys\
            (ConfigReader.readConfigData('Details','queryText'))
            self.driver.find_element(By.XPATH,value=self.get_answer_button).click()
            self.driver.find_element(By.XPATH,
            value=self.confirm_button).click()
            feedback=self.driver.find_element(By.XPATH,value=self.feedback_area)
            wait.until(EC.visibility_of(feedback))
            feedback.send_keys("Feedback")
            submit=self.driver.find_element\
            (By.XPATH,value=self.done_button)
            wait.until(EC.visibility_of(submit))
            submit.click()
        return True

    def close_browser(self):
        '''Close browser'''
        self.driver.close()
