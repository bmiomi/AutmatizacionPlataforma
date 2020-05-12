import time
from selenium.webdriver.common.by import By

class AsidePege:
    def __init__(self,driver):
        self.driver=driver
   
    def VisibleAside(self):
        time.sleep(4)
        if self.driver.find_element(By.ID,'slide-out') .is_displayed()  is not  True:
            print ('El aside esta oculto de procedera a dar click para visualizarlo')
            time.sleep(7)
            self.driver.find_element(By.XPATH,'//*[@id="left-sidebar-nav"]/a').click()
        else:
            print ('El aside esta visible genial')


    def OpcionSidebar(self):

        self.VisibleAside()
        time.sleep(4)
        self.driver.find_element(By.XPATH,'/html/body/div[3]/div/aside/ul/li[4]/ul/li/a').click()
        self.driver.find_element(By.XPATH,'//*[@id="slide-out"]/li[4]/ul/li/div/ul/li[1]').click()
        self.driver.find_element(By.XPATH,'//*[@id="left-sidebar-nav"]/a/i').click()

