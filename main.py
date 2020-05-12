from selenium import webdriver
import configparser
import unittest
import time

from Pagedriver.Indexpage import PageIndex
from Pagedriver.Asidepage import AsidePege
from Pagedriver.Framepage import FramePage

#*----funcional---*#

class testXsales(unittest.TestCase):
    
    def  setUp(self):
        self.__cofig=configparser.ConfigParser()
        self.__cofig.read('config.ini')
        self.edge=self.__cofig['Driver']['Edge']
        self.driver = webdriver.Edge(self.edge)
        self.driver.set_window_position(0,10)
        self.driver.set_window_size(1200,900)
        self.driver.get(self.__cofig['URLS']['P_C'])

        self.pageindex=PageIndex(self.driver)
        self.pageaside=AsidePege(self.pageindex.driver)
        self.pageFrame=FramePage(self.pageaside.driver)


    def test_uno(self):
        if self.pageindex.SelectOpcion():
            self.pageindex.login('','')
            self.pageaside.OpcionSidebar()
            time.sleep(10)

            
            self.pageFrame.Consulta()


if __name__ == "__main__":
    unittest.main(warnings='ignore')
