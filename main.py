import unittest

from Pagedriver.Indexpage import PageIndex
from Pagedriver.Asidepage import AsidePege
from Pagedriver.Framepage import FramePage
import time
from Configuracion.config import ConfigSelenium


#*----funcional---*#

class testXsales(unittest.TestCase):
    
    def  setUp(self):
        config=ConfigSelenium('Chrome')
        config.set_url('PC')
       
        self.pageindex=PageIndex(config.driver)
        self.pageaside=AsidePege(self.pageindex.driver)
        self.pageFrame=FramePage(self.pageaside.driver)


    def test_uno(self):
        if self.pageindex.SelectOpcion():
            self.pageindex.login('soporte.nuo','Nuo2020*')
            self.pageaside.OpcionSidebar()
            self.pageFrame.Consulta("""declare @inicio VARCHAR(255), @fin VARCHAR(255)
set @inicio='2020-08-11 00:00:00.000'set @fin='2020-08-11 23:59:00.000'
Select Top 1000000 Case When company.comName='Pronaca' Then'202' Else'253' end Emp_Codigo, 
Descu.didCode as Id_Negociacion, 
Descu.Tipo,
Descu.Cliente as Codigo_Cliente, 
Day(Descu.Fecha) as Dia_Negociacion, 
Month(Descu.Fecha) as Mes_Negociacion, 
Year(Descu.Fecha) as Anio_Negociacion, 
Ruta as Cod_Vendedor, Porcentaje as Descuento_Negociado,
'Si' as Descuento_Realizado, Descu.Status as Descuento_Status,
Case When Descu.Fecha< Ped2.Fecha Then'Si' Else'No' End as Desc_Prev_Pedido,Descu.Procesado as Descuento_Procesado_XSales,
Case When len(Ped2.Fecha)> 4 Then'Si' Else'No' End as Pedido_Realizado From 
(Select  D.didCode,D.cusCode CLIENTE,Convert(Varchar,D.didSystemDate,25) FECHA, D.rotCode RUTA,
Replace(I.dlpMinDiscount1,',','.') PORCENTAJE, 
Case When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%RECHAZ%' Then'Rechazado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"SI%' ESCAPE':' Then'Aprobado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"No%' ESCAPE':' Then'Rechazado'When D.ApvCode IS NULL Then'Aprobado'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:null%' ESCAPE':' Then'Pendiente'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) Like'%Respuesta"%:"EXCEPCION%' ESCAPE':' Then'Pendiente'When (Select A.ApvResponseDetail From Approval A Where A.apvCode=D.apvCode) IS NULL Then'Pendiente'END As STATUS, 
Case When D.didProcess='1' Then'Si' Else'No' End As PROCESADO, 
case when apvcode is NULL then'RANGO' else'FUERA RANGO' end as TIPO From DiscountDetailUp D 
Inner Join DiscountDetailProductUp I On D.didCode=I.didCode 
Where D.didCanceled='0' And D.didProcess='1' And D.DidSystemDate Between @inicio And @fin And D.didCode Not In (Select T.didCode From demandTeamProductDiscount T 
Inner Join Demand P On T.dmdCode=P.dmdCode Where P.dmdCancelOrder='1' And P.dmdProcess IS NULL) ) Descu 
Left Join Company On 1=1 
Left Join (Select  D.rotCode, D.cusCode,Max(D.dmdDate) as Fecha From Demand D Left Join DemandProduct DP On D.dmdCode= DP.dmdCode 
Where D.dmdDate Between @inicio And @fin And docCode='ped' and D.rotCode in (Select rotCode From route Where chaCode='V01') And D.dmdCancelOrder= 0 And DP.proCode in (Select proCode From product
 Where cl4Code='IDGDD001') Group By D.rotCode, D.cusCode) Ped2 On Descu.cliente= Ped2.cuscode and Descu.Ruta= Ped2.rotcode 
order by Descu.Ruta""")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
