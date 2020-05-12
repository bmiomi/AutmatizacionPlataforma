
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class PageIndex:
    
    def __init__(self,driver):
        self.driver=driver
        self.user=self.driver.find_element(By.ID,'username')
        self.password=self.driver.find_element(By.ID,'password')
        self.click=self.driver.find_element(By.ID,'btn-login')
    
    def VisiblePageXsales(self):
        tiempo=self.driver.implicitly_wait(5)
        return  WebDriverWait(tiempo,2).until(EC.visibility_of(self.driver.find_element(By.XPATH,'/html/body/div[2]')))

    def SelectOpcion(self):
        if self.VisiblePageXsales():
            try:
                _select=WebDriverWait(self.driver,60,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login"]/form/div[2]/div/div/input')),'no se encontro el elemento')
                if _select:
                    _select.click()
                    self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/form/div[2]/div/div/ul/li[2]').click() #cambia al nombre del Dz            
                    return True
            except ElementClickInterceptedException:
                self.driver.refresh()
    
    def login(self,User,Password):

            while True:
                if self.user.is_enabled() is True:
                    self.user.send_keys(User)
                    self.password.send_keys(Password)
                    self.click.submit()
                    print('Login Pasado exitosamente')
                    break
