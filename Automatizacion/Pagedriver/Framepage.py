from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import pandas as pd

class FramePage:

    def __init__(self,driver):        
        self.driver=driver
        self.n=1

    @property
    def get__colum(self):
        'retorna total de columnas de la tabla'
        return  len (self.driver.find_elements (By.XPATH,'//*[@id="GrwDatatable"]/thead/tr/th'))

    @property
    def get_fila(self):
        'retorna total de Filas de la tabla'
        return len(self.driver.find_elements(By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr'))

    @property
    def get_tamanio_paguinacion(self):
        'retornara el tamaño de la paguinacion en caso de que posea registro la tabla'
        return int(self.respuesta_consulta()/30)

    def frame(self):
        try:
            self.driver.switch_to_frame( 
                map( 
                    lambda i:i.find_element_by_id('frame-content') , 
                    WebDriverWait(self.driver,100,1).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'main-container')))
                    ).__next__()
            )

        except Exception:

            print('se a encontrado un error al localizar el elemento ')


    def respuesta_consulta(self):
        mensaje=self.driver.find_element(By.ID,'lblMensajeResultado').text 
        if "Comando Ejecutado Exitosamente" in  mensaje:
            return int(''.join([m for m in mensaje if m.isdigit()]))

    def status_table(self):
        'verificar si se posee registros en la tabla,limite de registros en  Tabla a mostrar 30'
        return True if self.respuesta_consulta() >=1 else False


    def status_paguinacion(self):
        'retornara True en caso que que el numero de filas sea igual a 31'
        return True if self.get_fila == 31 else False


    def Consulta(self,consu:str):
        self.frame()
        tex=self.driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[4]/div[1]/textarea')
        print('insertando consulta')
        tex.send_keys(consu)
        print('ejecutando consulta')
        self.driver.find_element_by_xpath('//*[@id="lblBtnExecute"]').send_keys(Keys.ENTER)

    def Descargar_excel(self):
        
        import time
        select=Select(self.driver.find_element_by_xpath('//*[@id="ddlExport"]'))
        select.select_by_visible_text("Exportar Excel")        
        self.driver.find_element_by_xpath('//*[@id="lblBtnExportar"]').send_keys(Keys.ENTER)
        time.sleep(3)

## crear una clase para el procesamiento de la data.

    def extraerhtml(self):
    # -  (fila) # |  (columna)
        return self.driver.find_element_by_xpath('//*[@id="form1"]/div[2]/div[2]/div[6]/div[2]/div/div').get_attribute('innerHTML')

    def Obtener_Data (self,lista):
        data=pd.concat(lista)
        if self.validar_file('reporte.xlsx'):
            self.append_df_to_excel(data, r"reporte.xlsx")
        else:
            print('entre aqui')
            return data.to_excel('reporte.xlsx',index=False,sheet_name='GDD')

