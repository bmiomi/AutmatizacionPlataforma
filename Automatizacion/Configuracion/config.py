import os
import pandas as pd

from pandas  import ExcelWriter
from selenium import webdriver
from configparser import ConfigParser

class ConfigFile:
     """
          Clase en donde se obtiene acceso a/al archivo de configuracion de la aplicacion
     """

     paths=os.getcwd()
     __cofig=ConfigParser()

     @classmethod
     def archivo(cls):
          """ retorna archivo de configuracion de la aplicacion (config.ini )"""
          return cls.__cofig.read('Automatizacion\\config.ini')

     @classmethod
     def crearfolder(cls): 
          d=pd.to_datetime('today').strftime('%Y%m%d')
          if not os.path.isdir(f'{cls.paths}\\Automatizacion\\filedownload\\{d}'):
               os.makedirs(os.path.join(cls.paths,'Automatizacion','filedownload',d))
          return f'{cls.paths}\\Automatizacion\\filedownload\\{d}'
     
     @property
     def _cofig(self):
          return self.__cofig
     

class ExcelFile:
     """
         Clase  en donde  se procesan y generan archivos de Excel 
     """

     _path=f'{os.getcwd()}\\Automatizacion\\reporte.xlsx'
     
     df=pd.DataFrame(
     
     columns=[
            "Emp_Codigo","Id_Negociacion","Tipo","Codigo_Cliente",
            "Dia_Negociacion","Mes_Negociacion","Anio_Negociacion",
            "Cod_Vendedor","Descuento_Negociado","Descuento_Realizado",
            "Descuento_Status","Desc_Prev_Pedido","Descuento_Procesado_XSales",
            "Pedido_Realizado"
            ])
            
     @classmethod
     def excelfile(cls):
          if not os.path.isfile(cls._path):     
               write=ExcelWriter(cls._path)
               cls.df.to_excel(write,'data',index=False)
               write.save()
          return True

     @classmethod          
     def recorrer_tabla(cls,data):
        # -  (fila) # |  (columna)
        dataframe=pd.read_html(str(data),converters={'Id_Negociacion':str,'Codigo_Cliente':str})[0]
        dataframe['Id_Negociacion']=dataframe['Id_Negociacion'].astype(str)
        dataframe['Codigo_Cliente']=dataframe['Codigo_Cliente'].astype(str)  
        return pd.DataFrame(dataframe,columns=dataframe.columns)


     @classmethod
     def append_df_to_excel(cls,df):
          df_excel = pd.read_excel(cls._path,converters={'Id_Negociacion':str,'Codigo_Cliente':str})
          df_excel['Id_Negociacion']=df_excel['Id_Negociacion'].astype(str)
          df_excel['Codigo_Cliente']=df_excel['Codigo_Cliente'].astype(str)
          result = pd.concat([df_excel, df], ignore_index=True)
          result.to_csv('demo.txt',sep=' ',index=False)
          result.to_excel(cls._path, index=False,sheet_name='GDD',)


class ConfigSelenium:


     def __init__(self):

          ExcelFile.excelfile()

          if len(ConfigFile.archivo()) <=1:
               value=self.__getbrowser(ConfigFile()._cofig['Navegador']['navegador'])

               if value is not None:
                    self.__driver=value
                    self.__driver.set_window_position(0,10)
               else:
                    raise  ValueError('El nombre del navegador no existe.')
              

     @property
     def driver(self):
          return self.__driver
     
     def __browser_open(self,browser=None):
               return ConfigFile()._cofig['Driver'][browser] if browser is not None else None 

     def set_url(self,dz):
          try:
               self.__driver.get(ConfigFile()._cofig['URLS'][dz])
          except ValueError:
               raise ValueError('error no se a encontrado ese distribuidor zonal')

     def size_window(self,height=900,width=1200):
        self.__driver.set_window_size(width,height)

     def __getbrowser(self,browser):

          driver=self.__browser_open(browser)

          navegador={
                     'Firefox':webdriver.Firefox,
                     'Chrome':webdriver.Chrome,
                     'Edge':webdriver.Edge
                    }
          return navegador.get(browser)(driver,chrome_options=self.Opciones_browser())


     def Opciones_browser(self):
          optchorme=webdriver.ChromeOptions()
          optchorme.add_experimental_option("prefs",{"download.default_directory":  ConfigFile.crearfolder() })
          optchorme.add_argument('headess')
          optchorme.add_argument('log-level=3')
          return optchorme


     def file(self):
          pathfile=ConfigFile.crearfolder()
          paths = [ os.path.join (pathfile,basename)  for basename in  os.listdir(pathfile) ]
          return max(paths, key=os.path.getctime)
     
     def funcname(self,url:str):

          _path=self.file()
          d=_path.rsplit('\\')
          t=d[-1:]
          nuevo=url+'.xlsx'
          nuevo=_path.replace(t[0],nuevo)
          os.rename(_path,nuevo)
          print('\033[31m path anterios: ',_path,'\n \033[34m path nuevo: ',nuevo,'\033[37m')   