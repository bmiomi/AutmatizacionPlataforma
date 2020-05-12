
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import time

class FramePage:
    
    
    def __init__(self,driver):
        self.driver=driver
        self._row=[]
        self._colum=[]   

    @property
    def get__colum(self):
        return  len (self.driver.find_elements (By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/thead/tr/th'))
    
    @property
    def get_fila(self):
        return len(self.driver.find_elements(By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr'))

    def Consulta(self):

       consu="""declare @inicio VARCHAR(255),@fin VARCHAR(255) set @inicio='2020-03-28 00:00:00.000'set @fin='2020-03-28 23:59:00.000' Select Top 1000000 Case When company.comName='Pronaca' Then'202' Else'253' end Emp_Codigo,    Descu.didCode as Id_Negociacion, Descu.Tipo, Descu.Cliente as Codigo_Cliente, Day(Descu.Fecha) as Dia_Negociacion, Month(Descu.Fecha) as Mes_Negociacion, Year(Descu.Fecha) as Anio_Negociacion,  Ruta as Cod_Vendedor, Porcentaje as Descuento_Negociado, 'Si' as Descuento_Realizado, Descu.Status as Descuento_Status, Case When Descu.Fecha< Ped2.Fecha Then'Si' Else'No' End as Desc_Prev_Pedido,Descu.Procesado as Descuento_Procesado_XSales, Case When len(Ped2.Fecha)> 4 Then'Si' Else'No' End as Pedido_Realizado From (Select  D.didCode,D.cusCode CLIENTE,Convert(Varchar,D.didSystemDate,25) FECHA, D.rotCode RUTA, Replace(I.dlpMinDiscount1,',','.') PORCENTAJE, Case When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%RECHAZ%' Then'Rechazado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"SI%' ESCAPE':' Then'Aprobado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"No%' ESCAPE':' Then'Rechazado'When D.ApvCode IS NULL Then'Aprobado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:null%' ESCAPE':' Then'Pendiente'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"EXCEPCION%' ESCAPE':' Then'Pendiente'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) IS NULL Then'Pendiente'END As STATUS, Case When D.didProcess='1' Then'Si' Else'No' End As PROCESADO, case when apvcode is NULL then'RANGO' else'FUERA RANGO' end as TIPO From DiscountDetailUp D   Inner Join DiscountDetailProductUp I On D.didCode=I.didCode Where D.didCanceled='0' And D.didProcess='1' And D.DidSystemDate Between @inicio And @fin And D.didCode Not In (Select T.didCode From demandTeamProductDiscount T Inner Join Demand P On T.dmdCode=P.dmdCode Where P.dmdCancelOrder='1' And P.dmdProcess IS NULL) ) Descu Left Join Company On 1=1 Left Join (Select  D.rotCode, D.cusCode,Max(D.dmdDate) as Fecha From Demand D Left Join DemandProduct DP On D.dmdCode= DP.dmdCode Where D.dmdDate Between @inicio And @fin And docCode='ped' and D.rotCode in (Select rotCode From route Where chaCode='V01') And D.dmdCancelOrder= 0 And DP.proCode in (Select proCode From product  Where cl4Code='IDGDD001') Group By D.rotCode, D.cusCode) Ped2 On Descu.cliente= Ped2.cuscode and Descu.Ruta= Ped2.rotcode order by Descu.Ruta"""
       #consu="select top 100 * from customer where cuscode='0'"
       #consu="select top 10000 rotcode from demand"
       #consu="select distinct top 10000  dmdCustomerName,cuscode  from demand"
       self.frame=WebDriverWait(self.driver,200,10).until(EC.visibility_of(self.driver.find_element_by_id('frame-content')))
       self.driver.switch_to_frame(self.frame)
       tex=self.driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[4]/div[1]/textarea')
       print('ejeutando consulta')
       tex.send_keys(consu)
       self.driver.find_element(By.XPATH,'//*[@id="lblBtnExecute"]').click()
       self.t()

    def status_table(self):
        #  limite de registros en  Tabla a mostrar 30         
        # verificar si se posee registros en la tabla
        #    self.driver.execute_script("alert('no se encontro registros')")
        return False if '0 row(s))' == self.driver.find_element(By.ID,'lblMensajeResultado').text[31:40]  else  True
        
    def status_paguinacion(self):
        #  paguinacion 31
        time.sleep(3)
        print('Verificando si se Tiene Paguinacion') 
        if type(self.driver.find_element(By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr[31]')) is WebElement:
            print('Existe Paguinacion')
            return True
        else:
            print('No existe Paguinacion')
            return False

    def tamanio_paguinacion(self):
      
        EP=self.driver.find_elements(By.XPATH,'/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr[31]/td/table/tbody/tr/td')
        print(f'Tamaño de Paguinacion {len(EP)}')
        return  len(EP) if len(EP) !=0 else 'Error'

    contador=2

    def Recorrer_paguinacion(self):    

        TPaginacion=self.tamanio_paguinacion()

        if TPaginacion !='Error':
            while self.contador <= TPaginacion:
                for x in self.driver.find_elements(By.XPATH,"/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr[31]/td/table/tbody/tr/td["+str(self.contador)+"]"):                
                    if x.text == str(self.contador) and x.text.isdigit():
                        for a in x.find_elements_by_tag_name('a'):
                            print('click')
                            a.click()
                            self.contador+=1
                            self.recorrer_tabla()
        

    def recorrer_tabla(self,):
        # - (linea)  (fila)
        # | (palito) (columna)
        contador=self.contador-1
        
        for c in range(1,self.get__colum+1):
            for f in range (1,self.get_fila+1):
                if f == self.get_fila and c == self.get__colum:

                    print(f'Cambiando de paguina:{contador}')
                    self.Recorrer_paguinacion()
                elif f != self.get_fila:
                    head=self.driver.find_element(By.XPATH,"/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/thead/tr[1]/th["+str(c)+"]").text
                    if head not in self._row:
                        self._row.append(head)
                    value=self.driver.find_element(By.XPATH,"/html/body/form/div[2]/div[2]/div[6]/div[2]/div/div/table/tbody/tr["+str(f)+"]/td["+str(c)+"]").text
                    self._colum.append(value)

    def Obtener_Data (self):
        with open ('archivo','a',encoding="UTF-8") as archivo:
            print(self._row,self._colum,sep=',',file=archivo)

    def t(self):
        if self.status_table() and self.status_paguinacion():
            self.recorrer_tabla()
            self.Obtener_Data()
        else:
            print('No hay registro para recorrer')
