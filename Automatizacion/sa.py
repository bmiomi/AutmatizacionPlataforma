import time
import unittest
from Configuracion.config import ConfigSelenium,ExcelFile
from Pagedriver.Asidepage import AsidePege
from Pagedriver.Framepage import FramePage
from Pagedriver.Login     import PageLogin

global consulta

consulta="""declare @inicio VARCHAR(255), @fin VARCHAR(255) set @inicio = '2021-01-07 00:00:00.000' set @fin = '2021-01-07   23:59:00.000' Select Top 1000 Case When company.comName = 'Garvel Product' Then '517' When company.comName = 'Pronaca' Then '202' When company.comName = 'Posso&Cueva' Then '253' When company.comName = 'Cenacop' Then '325' When company.comName = 'Granpir' Then '234' When company.comName = 'Dapromach' Then '331' When company.comName = 'Pronaim' Then '115' When company.comName = 'Dimmia' Then '111' When company.comName = 'Almabi' Then '360' When company.comName = 'Skandinar' Then '121' When company.comName = 'Disproalza' Then '247' When company.comName = 'Madeli' Then '128' When company.comName = 'Ecoal' Then '373' When company.comName = 'Disprovalles' Then '210' When company.comName = 'Pronacnor' Then '303' When company.comName = 'Apronam' Then '162' When company.comName = 'Paul_Florencia' Then '168' When company.comName = 'Discarnicos' Then '261' When company.comName = 'H&M' Then '324' When company.comName = 'Disanahisa' Then '323' When company.comName = 'Patricio_Cevallos' Then '254' When company.comName = 'Alsodi' Then '314' When company.comName = 'Judispro' Then '239' When company.comName = 'Oriental' Then '229' Else '#' end Emp_Codigo, Descu.didCode as Id_Negociacion, Descu.Tipo, Descu.Cliente as Codigo_Cliente, Day(Descu.Fecha) as Dia_Negociacion, Month(Descu.Fecha) as Mes_Negociacion, Year(Descu.Fecha) as Anio_Negociacion, Ruta as Cod_Vendedor, Porcentaje as Descuento_Negociado, 'Si' as Descuento_Realizado, Descu.Status as Descuento_Status, Case When Descu.Fecha < Ped2.Fecha Then 'Si' Else 'No' End as Desc_Prev_Pedido, Descu.Procesado as Descuento_Procesado_XSales, Case When len(Ped2.Fecha) > 4 Then 'Si' Else 'No' End as Pedido_Realizado  From (  Select D.didCode,  D.cusCode CLIENTE,  Convert(Varchar, D.didSystemDate, 25) FECHA,  D.rotCode RUTA,  Replace(I.dlpMinDiscount1, ',', '.') PORCENTAJE,  Case  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) Like '%RECHAZ%' Then 'Rechazado'  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) Like '%Respuesta"%:"SI%' ESCAPE ':' Then 'Aprobado'  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) Like '%Respuesta"%:"No%' ESCAPE ':' Then 'Rechazado'  When D.ApvCode IS NULL Then 'Aprobado'  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) Like '%Respuesta"%:null%' ESCAPE ':' Then 'Pendiente'  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) Like '%Respuesta"%:"EXCEPCION%' ESCAPE ':' Then 'Pendiente'  When (  Select A.ApvResponseDetail  From Approval A  Where A.apvCode = D.apvCode  ) IS NULL Then 'Pendiente'  END As STATUS,  Case  When D.didProcess = '1' Then 'Si'  Else 'No'  End As PROCESADO,  case  when apvcode is NULL then 'RANGO'  else 'FUERA RANGO'  end as TIPO  From DiscountDetailUp D  Inner Join DiscountDetailProductUp I On D.didCode = I.didCode  Where D.didCanceled = '0'  And D.didProcess = '1'  And D.DidSystemDate Between @inicio And @fin  And D.didCode Not In (  Select T.didCode  From demandTeamProductDiscount T  Inner Join Demand P On T.dmdCode = P.dmdCode  Where P.dmdCancelOrder = '1'  And P.dmdProcess IS NULL  )  ) Descu  Left Join Company On 1 = 1  Left Join (  Select D.rotCode,  D.cusCode,  Max(D.dmdDate) as Fecha  From Demand D  Left Join DemandProduct DP On D.dmdCode = DP.dmdCode  Where D.dmdDate Between @inicio And @fin  And docCode = 'ped'  and D.rotCode in (  Select rotCode  From route  Where chaCode = 'V01'  )  And D.dmdCancelOrder = 0  And DP.proCode in (  Select proCode  From product  Where cl4Code = 'IDGDD001'  )  Group By D.rotCode,  D.cusCode  ) Ped2 On Descu.cliente = Ped2.cuscode  and Descu.Ruta = Ped2.rotcode  order by Descu.Ruta"""

class  PrincialPage:

    url='Al'


    def __init__(self) :

        """
            driver : componente a iniciar en el navegador

            Url: valor que se toma para ingresar a la paguina solicitada 
        """

        self._config=ConfigSelenium()
        self._config.set_url(self.url)
        
        self.login=PageLogin(self._config.driver)
        self.aside=AsidePege(self._config.driver)
        self.frame=FramePage(self._config.driver)

        #

    def ConsultarDescuentos(self):

        self.login.login('soporte.nuo','Nuo2021*')
        self.aside.OpcionSidebar()
        self.frame.Consulta(consulta)
        if self.frame.get_tamanio_paguinacion == 0 and self.frame.status_table() == True:

            print('\033[32m se extraera la informacion de la tabla \033[32m')
            ExcelFile.append_df_to_excel(ExcelFile.recorrer_tabla(self.frame.extraerhtml())) #str

        elif self.frame.get_tamanio_paguinacion >=1 :
             
            print( '\033[33m se descargara el archivo excel para posterior consolidacion.\033[33m' )
            self.frame.Descargar_excel()
            self._config.funcname(self.url)




#*----funcional---*#


class ALmabi(unittest.TestCase):
 

    def test_uno(self):

        dz=['al', 'ap', 'als', 'cp', 'di', 'dico', 'dis', 'diza', 
            'dile', 'dapro', 'Eco', 'Gram','gave', 'H_M', 'jud',
             'MD', 'Or', 'PF', 'PC', 'Ps', 'PRN','PRnor', 'SkR']



        for i in range(len(dz)):
            PrincialPage.url=dz[0]
            self.page=PrincialPage()
            self.page.ConsultarDescuentos()
            self.page._config.driver.execute_script("window.open('');")            
            self.page._config.driver.switch_to.window(self.page._config.driver.window_handles[int(i)+1])
            print(self.page)
 #           self.page._config.set_url(dz[i+1])
 

            # contador=0
            # while len(self.page._config.driver.window_handles) == 5 and contador<=4:                
            #     self.page._config.driver.switch_to.window(self.page._config.driver.window_handles[contador])
            #     PageLogin(self.page._config.driver)
            #     contador+=1
            #     if contador==4:
            #         break
                

        # dz=['al', 'ap', 'als', 'cp', 'di', 'dico', 'dis', 'diza', 
        #     'dile', 'dapro', 'Eco', 'Gram','gave', 'H_M', 'jud',
        #      'MD', 'Or', 'PF', 'PC', 'Ps', 'PRN','PRnor', 'SkR']

        # ite=iter(dz)

        # for i in range(len(dz)):
        #     self.page=PrincialPage(dz[i])
        #     self.page.ConsultarDescuentos()        
        #     self.page._config.driver.quit()
    

def main():
    print(__name__)
    if __name__ == "__main__":

       unittest.main(warnings='ignore')

        # initialize the test suite
#        loader = unittest.TestLoader()
#        suite  = unittest.TestSuite()
#        # add tests to the test suite
#        suite.addTests(

#             [
#              loader.loadTestsFromTestCase(ALmabi),
# #             # loader.loadTestsFromTestCase(Apronam),
# #             #    loader.loadTestsFromTestCase(Alsodi) ,
# #             #    loader.loadTestsFromTestCase(Cenacop),
# #             #    loader.loadTestsFromTestCase(Dapromach),
# #             #  loader.loadTestsFromTestCase(Disanahisa),
# #             #    loader.loadTestsFromTestCase(Disproalza),
# #             #   loader.loadTestsFromTestCase(Dimmia),
# #             #     loader.loadTestsFromTestCase(Disprovalles),
# #             #   loader.loadTestsFromTestCase(Discarnicos),
# #             #    loader.loadTestsFromTestCase(Ecoal),
# #             #     loader.loadTestsFromTestCase(Grampir),
# #             #     loader.loadTestsFromTestCase(Garvelproduct),
# #             #    loader.loadTestsFromTestCase(HM),
# #             #     loader.loadTestsFromTestCase(Judispro),
# #             #     loader.loadTestsFromTestCase(Madeli),
# #             #    loader.loadTestsFromTestCase(PatricioCevallos),
# #             #    loader.loadTestsFromTestCase(PaulFlorencia),
# #             #     loader.loadTestsFromTestCase(Pronaim),
# #             #    loader.loadTestsFromTestCase(PossoCueva),
# #             #   loader.loadTestsFromTestCase(Proncaca),
# #             #     loader.loadTestsFromTestCase(Pronacnor),
# #             #    loader.loadTestsFromTestCase(Skandinar)

#             ]
#         )


# #        initialize a runner, pass it your suite and run it
 #      runner = unittest.TextTestRunner(verbosity=3,warnings='ignore')
#        result = runner.run(suite)

#         print(  "error: ",  [i[0] for i in result.errors])


main()