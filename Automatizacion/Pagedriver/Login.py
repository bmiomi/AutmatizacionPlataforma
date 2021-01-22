from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageLogin:
    
    def __init__(self,driver):

        self.driver=driver
        self.namedz=self.SelectOpcion()
        self.user  =self.driver.find_element(By.ID,'username')
        self.password=self.driver.find_element(By.ID,'password')
        self.click=self.driver.find_element(By.ID,'btn-login')
    
    def VisiblePageXsales(self) :
        #loaded
        return  WebDriverWait(self.driver,15,1).until(EC.visibility_of(self.driver.find_element(By.CLASS_NAME,'loaded'))).is_enabled()

    def SelectOpcion(self):
        while self.VisiblePageXsales():
            try:
                _select=WebDriverWait(self.driver,100,1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login"]/form/div[2]/div/div/input')),message='no se encontro el elemento')
                if _select:
                    self.driver.execute_script("arguments[0].click();", _select)
                    self.driver.find_element(By.XPATH,'//*[@id="login"]/form/div[2]/div/div/ul/li[2]').click() #cambia al nombre del Dz            
                    return True
            except Exception as e:
                print('Error: no se pudo encontrar el elemento DB Conexion',e)
        return False
            
    def login(self,user,password):
        while True:
            if self.user.is_enabled():
                self.user.send_keys(user)
                self.password.send_keys(password)
                self.click.submit()
                text=WebDriverWait(self.driver,100,1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="toast-container"]')))
                if text.text=="User or Password Incorrect":
                    print('Reintenta Ingresando usuario y contraseña')
                break
