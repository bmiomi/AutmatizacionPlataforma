from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AsidePege:
    def __init__(self,driver):
        self.driver=driver
   
    def VisibleAside(self):
        self.aside= WebDriverWait(self.driver,5).until(lambda x: x.find_elements_by_id('left-sidebar-nav'))
        if self.aside is False:
            print ('El aside esta oculto de procedera a dar click para visualizarlo')
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH,'//*[@id="left-sidebar-nav"]/a'))
        else:            
            print ('El aside esta visible genial')
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH,'//*[@id="left-sidebar-nav"]/a'))


    def OpcionSidebar(self):
        self.VisibleAside() 
        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,'/html/body/div[3]/div/aside/ul/li[4]/ul/li/a'))
        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,'//*[@id="slide-out"]/li[4]/ul/li/div/ul/li[1]/a'))
        self.driver.implicitly_wait(5)
