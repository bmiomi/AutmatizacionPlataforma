from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageIndex:
    
    def __init__(self,driver):
        self.driver=driver
        self.user=self.driver.find_element(By.ID,'username')
        self.password=self.driver.find_element(By.ID,'password')
        self.click=self.driver.find_element(By.ID,'btn-login')
    
    def VisiblePageXsales(self):
        return  WebDriverWait(self.driver,5).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME,'loaded'))).is_enabled()

    def SelectOpcion(self):
        if self.VisiblePageXsales():
            
            try:
                _select=WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login"]/form/div[2]/div/div/input')),message='no se encontro el elemento')
                if _select:
                    self.driver.execute_script("arguments[0].click();", _select)
                    self.driver.find_element(By.XPATH,'//*[@id="login"]/form/div[2]/div/div/ul/li[2]').click() #cambia al nombre del Dz            
                    return True
            except Exception as e:
                print('Error: ',e)
                
    
    def login(self,User,Password):
        while True:
            if self.user.is_enabled():
                self.user.send_keys(User)
                self.password.send_keys(Password)
                self.click.submit()
                print( 'Login Pasado exitosamente  \U0001F60B')
                break
