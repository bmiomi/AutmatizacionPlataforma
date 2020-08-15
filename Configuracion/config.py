from configparser import ConfigParser
from selenium import webdriver


class ConfigFile:
    
     def __init__(self):
         self._cofig=ConfigParser()
         self._cofig.read('config.ini')


class ConfigSelenium:

     def __init__(self,browser):
        value=self.__getbrowser(browser)
        if value is not None:
              self.__driver=value
              self.__driver.set_window_position(0,10)

     @property
     def driver(self):
          return self.__driver
     
     def __browser_open(self,browser=None):
          return ConfigFile()._cofig['Driver'][browser] if browser is not None else None 

     def set_url(self,dz):
          self.__driver.get(ConfigFile()._cofig['URLS'][dz])

     def size_window(self,height=900,width=1200):
        self.__driver.set_window_size(width,height)

         
     def __getbrowser(self,browser):
          driver=self.__browser_open(browser)
          if driver is not None:
               if browser == 'Firefox':
                    return webdriver.Firefox(driver)
               elif browser == 'Edge':
                    return webdriver.Edge(driver)
               elif browser == 'Chrome':
                    return webdriver.Chrome(driver)
               else:
                    raise ValueError('El Navegador no se posee registro validar el config.ini')
          else:
               raise ValueError('El path driver no es el correcto validar el config.ini')

