import io
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from PIL import Image as PImage
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter


class webScraper (object):
    listaDeProdutos: list = []

    elemtet_data: dict = {
        "columnas": ["Titulos", "Precios"],
        "Titulos": [],
        "Precios": [],
        "categorias-link": [],
        "categorias": []
    }
    data = [("productos", listaDeProdutos),
            ("titulos", elemtet_data["Titulos"]),
            ("titulos", elemtet_data["Precios"])]

    # driver = 'D:\ProyectosCarToro\scraping\webscraper\webscraper\ChromeSetup.exe'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), chrome_options=chrome_options)
    # driver.minimize_window()
    driver.get("https://www.homecenter.com.co/homecenter-co/landing/cat5130007/")
    html = driver.page_source
    time.sleep(1)
    botones: list = []

    def categorias(self):
        categorias_list = self.driver.find_element(By.XPATH, '//*[@id="main"]/section/div[2]/aside/section/menu/ul').find_element(
            By.CLASS_NAME, 'jq-accordion').find_elements(By.XPATH, '//*[@id="main"]/section/div[2]/aside/section/menu/ul/li/a')
        time.sleep(2)
        self.list_categories: list = []
        rango_lista_1: list = []
        for ul in categorias_list:

            href = ul.get_attribute('href')
            self.list_categories.append(href)
        list_pagination: list = []
        self.productos_list = []
        print(self.list_categories)

        for self.i in range(len(self.list_categories)):
            time.sleep(2)
            self.driver.get(self.list_categories[self.i])
            time.sleep(0.10)
            self.driver.implicitly_wait(10)
            linkDelproducto = self.driver.find_elements(
                By.XPATH, '//*[@id="title-pdp-link"]')
            for a in linkDelproducto:
                time.sleep(0.10)
                self.productos_list.append({'link': a.get_attribute(
                    "href"), 'id': a.get_attribute("href").split("/")[-2]})
            print(self.productos_list)
            break
            # self.driver.get(list_categories[i] + f"?currentpage={point_links}")

    def pasarPagina(self):

        botton = self.driver.find_element(
            By.XPATH, '//*[@id="__next"]/div/div/div[7]/div[3]/div[1]/div[1]/div[4]/div[1]/div').find_elements(By.CSS_SELECTOR, "button.jsx-4278284191")

        for point_links in range(len(botton)):
            a = self.list_categories[self.i]
            print(a[-0:])
            print(point_links)
            print(point_links)
            self.driver.get(
                self.list_categories[self.i][-0:] + f"?currentpage={point_links +2}")
            linkDelproducto = self.driver.find_elements(
                By.XPATH, '//*[@id="title-pdp-link"]')
            for a in linkDelproducto:
                # time.sleep(0.10)
                self.productos_list.append({'link': a.get_attribute(
                    "href"), 'id': a.get_attribute("href").split("/")[-2]})
            print(self.productos_list)
            # for i in self.productos_list:
            #     # print()
            #     # print(self.productos_list[int(i)])

            #     time.sleep(4)
            #     self.driver.get(i)
            #     print("pase, line 104")
            #     time.sleep()

    def dataProducto(self):
        workbook = load_workbook(filename='template.xlsx')
        worksheet = workbook.active
        # resize cells
        for row in range(2, len(self.productos_list)):
            worksheet.row_dimensions[row].height = 160
            col_letter = get_column_letter(8)
            worksheet.column_dimensions[col_letter].width = 40

        for i in range(len(self.productos_list)):
            try:
                self.driver.get(self.productos_list[i]['link'])
                time.sleep(5)
                titulo = self.driver.find_element(
                    By.XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[1]/div[1]/h1').text
                time.sleep(1.30)
                precio = self.driver.find_element(
                    By. XPATH, '//div[@class="jsx-2167963490 primary"]/span[2]').text
                fichaTecnica = self.driver.find_element(
                    By.XPATH, '//div[@class="jsx-3969330179 jsx-3762308956 row jsx-967453414"]')
                categories = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/ol').find_elements(
                    By.CLASS_NAME, 'jsx-3306415055')[0].text.split('\n')
                categories[0] = 'Ollas y Utencilios'
                # find and save image
                image_path = ".\\imagenes\\" + \
                    self.productos_list[i]['id'] + ".png"
                image = self.driver.find_element(
                    By.XPATH, '//*[@id="pdpMainImage-' + self.productos_list[i]['id'] + '"]')
                result = image.screenshot_as_png
                image_to_save = PImage.open(io.BytesIO(result))
                image_to_save.thumbnail((220, 220))
                image_to_save.save(image_path)

                time.sleep(4)
                for index_categories in range(len(categories)):
                    worksheet.cell(row=i+2, column=i+1,
                                   value=categories[index_categories])
                worksheet.cell(row=i+2, column=6, value=titulo)
                worksheet.cell(row=i+2, column=7, value=precio)
                worksheet.add_image(Image(image_path), anchor='H'+str(i+2))
            except:
                print("ERROR AL SOLICITAR PRODUCTO: " +
                      self.productos_list[i]['link'])
                continue

        workbook.save('salida.xlsx')

    def producto(self):
        print("hola estoy aca")
        print("hola estoy aca X2")
        self.driver.get(
            "https://www.homecenter.com.co/homecenter-co/product/455376/bateria-10-piezas-antiadherente-gris-talent/455376/")

        linkDelproducto = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/ol').find_elements(
            By.CLASS_NAME, 'jsx-3306415055')[0].text
        print(linkDelproducto)
        print(linkDelproducto.split('\n'))

        # for i in linkDelproducto:
        #     i.click()
        #     print(titulo)

        #     time.sleep(1000)


clase1 = webScraper()
clase1.categorias()
# clase1.pasarPagina()
clase1.dataProducto()
# clase1.producto()
# clase1.pasarPagina()


# # df = pd.DataFrame(elemtet_data)
# df1 = pd.DataFrame(data=elemtet_data["Titulos"])
# df2 = pd.DataFrame(elemtet_data["Precios"])

# df4 = pd.DataFrame(data=elemtet_data["categorias"])
# df5 = df4.to_csv("Datavajilla.csv" )

# # df = pd.DataFrame({"Precios":[elemtet_data["Precios"]], "Titulos": [elemtet_data["Titulos"]]})
# df2.to_excel("data234112.xlsx" )
# print(df1)
# print(df4)

# print(df4)
# print(df4.iloc[1:], "DF4 HOLA")

# except Exception as error:
#     print(f"ESTE ES EL ERROR!!! {error}")
