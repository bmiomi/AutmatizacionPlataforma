from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time
import pandas as pd

class FramePage:

    def __init__(self,driver):
        self.driver=driver
        self.di=[]
        self.n=1

    @property
    def get__colum(self):
        return  len (self.driver.find_elements (By.XPATH,'//*[@id="GrwDatatable"]/thead/tr/th'))

    @property
    def get_fila(self):
        return len(self.driver.find_elements(By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr'))

    @property
    def get_tamanio_paguinacion(self):
        'si se tiene paguinacion mediante la funcion status_paguinacion retornara el tamaño de la paguinacion'
        EP=self.driver.find_elements(By.XPATH,'//*[@id="GrwDatatable"]/tbody/tr[31]/td/table/tbody/tr/td')
        return  len(EP) if len(EP) !=0 else 0


    def frame(self):
        WebDriverWait(self.driver,60).until(lambda x: x.find_elements_by_class_name('main-container'))
        self.driver.switch_to_frame(self.driver.find_element_by_id('frame-content'))

    def Consulta(self,consu):
        self.frame()
        tex=self.driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[4]/div[1]/textarea')
        print('insertando consulta')
        tex.send_keys(consu)
        self.driver.find_element(By.XPATH,'//*[@id="lblBtnExecute"]').click()
        print('ejeutando consulta')
        self.t()

    def status_table(self):
        'verificar si se posee registros en la tabla,limite de registros en  Tabla a mostrar 30'
        return False if '0 row(s))' == self.driver.find_element(By.ID,'lblMensajeResultado').text[31:40]  else  True

    def status_paguinacion(self):
        'Solamente retornara True en caso que exista paguinacion,paguinacion 31'
        return True if self.get_fila == 31 else False


    def __generador(self):
        while self.n<self.get_tamanio_paguinacion:
            self.n+=1
            yield self.n


    def Recorrer_paguinacion(self):
        g=next(self.__generador())
        print('Cambiando a paguina siguiente: ',g)
        k=list(map(lambda x: x.find_elements_by_tag_name('a'),
        self.driver.find_elements(
           By.XPATH,f'//*[@id="GrwDatatable"]/tbody/tr[31]/td/table/tbody/tr/td[{g}]'
           )))
        for i in k[0]:
            i.click()

    def recorrer_tabla(self):
        # -  (fila)
        # |  (columna)
        data=self.driver.find_element_by_xpath ('//*[@id="form1"]/div[2]/div[2]/div[6]/div[2]/div/div').get_attribute('innerHTML')
        data2=pd.read_html(data)
        return pd.DataFrame(data2[0],columns=data2[0].columns)
        
    def Obtener_Data (self,lista):
        data=pd.concat(lista)
        return data.to_excel('reporte.xlsx')

    def t(self):
        #> mayor
        #< menor

        print('tamaño filas: ',self.get_fila)
        print('tamaño columnas: ',self.get__colum)
        print('tamaño paguinacion: ',self.get_tamanio_paguinacion)

        for i in range(1,self.get_tamanio_paguinacion+1):
            print(f'paguina Actual: {i}')
            self.di.append(self.recorrer_tabla())
            print('estoy agregando dataframe')
            if i <= self.get_tamanio_paguinacion:
                print('estoy en paguina ',i)
                self.Recorrer_paguinacion()
        print('estoy creando archivo Excel')
        self.Obtener_Data(self.di)
