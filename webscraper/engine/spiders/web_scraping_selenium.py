import io
import json
import numpy
import re
from unicodedata import normalize
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import Image as PImage
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from datetime import date


class webScraper (object):
    product_list: list = []
    categories_data: dict = {}

    # driver = 'D:\ProyectosCarToro\scraping\webscraper\webscraper\ChromeSetup.exe'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = chrome_options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), chrome_options=chrome_options)
    # driver.minimize_window()
    driver.maximize_window()
    driver.get("https://www.homecenter.com.co/")
    html = driver.page_source
    time.sleep(1)
    botones: list = []
    parent_categories: list = []
    child_categories: list = []
    node_count = 0
    list_categories: list = []

    def get_categories_params(self):
        with open('./categories.json', 'r') as f:
            data = f.read()
            f.close()
        self.categories_data = json.loads(data)

    def get_categories_test(self):
        print(self.list_categories)

        for category_i in range(len(self.list_categories)):
            time.sleep(2)
            self.driver.get(
                self.list_categories[category_i]["link"])
            time.sleep(2)
            # se inician guardando registros primer resultado (pagina 1)
            self.list_categories[category_i]["products"] = numpy.concatenate(
                (self.list_categories[category_i]["products"], self.get_link_products()))

            totalButttonsPagination = self.get_total_buttons_by_pagination()

            # se guardan registros de la paginacion desde la pagina 2
            for point_links in range(len(totalButttonsPagination)-1):
                self.driver.get(
                    self.list_categories[category_i]["link"]+f"?currentpage={point_links+2}")
                self.list_categories[category_i]["products"] = numpy.concatenate(
                    (self.list_categories[category_i]["products"], self.get_link_products()))

        print("done")
        print(self.list_categories)

    def get_link_products(self):
        list_products = []
        time.sleep(2)
        self.driver.implicitly_wait(2)
        js_script = '''\
        var banner= document.getElementById('banner-plp');
        if(banner){
            banner.setAttribute("hidden","");
        }
        '''
        self.driver.execute_script(js_script)

        grid = self.driver.find_element(
            By.XPATH, '//*[@id="testId-btn-grid-view"]')
        if (grid):
            grid.click()
        linkDelproducto = self.driver.find_elements(
            By.XPATH, '//*[@id="title-pdp-link"]')
        for a in linkDelproducto:
            list_products.append({'link': a.get_attribute("href"),
                                  'id': a.get_attribute("href").split("/")[-2]})

        return list_products

    def get_total_buttons_by_pagination(self):
        time.sleep(8)
        buttons: list = []
        js_script = '''\
        var banner= document.getElementById('banner-plp');
        if(banner){
            banner.setAttribute("hidden","");
        }
        '''
        self.driver.execute_script(js_script)

        try:
            buttons = self.driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div/div[6]/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/ul').find_elements(By.CSS_SELECTOR, "button.jsx-4278284191")
            return buttons
        except:
            "No se encuentra la paginacion."
        try:
            buttons = self.driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div/div[7]/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div[1]/ul').find_elements(By.CSS_SELECTOR, "button.jsx-4278284191")
            return buttons
        except:
            "No se encuentra la paginacion, se asume no tiene."
        return buttons

    def map_product_data(self):
        workbook = load_workbook(filename='template.xlsx')
        worksheet = workbook.active
        excel_row = 0
        # resize cells
        for row in range(2, self.get_total_products()+2):
            worksheet.row_dimensions[row].height = 160
            col_letter = get_column_letter(34)
            worksheet.column_dimensions[col_letter].width = 40

        for list_category_i in range(len(self.list_categories)):
            for products_i in range(len(self.list_categories[list_category_i]["products"])):
                try:
                    print("[SCAN] PRODUCTO: " +
                          self.list_categories[list_category_i]["products"][products_i]['link'])
                    self.driver.get(
                        self.list_categories[list_category_i]["products"][products_i]['link'])
                    time.sleep(2.5)
                    titulo = self._normalice_string(self.driver.find_element(
                        By.XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[1]/div[1]/h1').text)
                    precio = self.driver.find_element(
                        By. XPATH, '//div[@class="jsx-2167963490 primary"]/span[2]').text
                    marca = self._normalice_string(self.driver.find_element(
                        By. XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[1]/div[1]/div[1]/div[1]').text)
                    dataSheet = self.map_datasheet()
                    try:
                        home_delivery = self._normalice_string(self.driver.find_element(
                            By. XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]').text)
                    except:
                        home_delivery = ""
                    try:
                        pick_up_in_store = self._normalice_string(self.driver.find_element(
                            By. XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[3]/div[4]/div[2]/div[1]/div[1]').text)
                    except:
                        pick_up_in_store = ""
                    try:
                        stock_in_store = self._normalice_string(self.driver.find_element(
                            By. XPATH, '//*[@id="__next"]/div/div/div[4]/div[2]/div[3]/div[5]/div[2]/div[1]/div[1]').text)
                    except:
                        stock_in_store = ""
                    categories = self.list_categories[list_category_i]["categories"]
                    # find and save image
                    image_path = ".\\imagenes\\" + \
                        self.list_categories[list_category_i]["products"][products_i]['id'] + ".png"
                    image = self.driver.find_element(
                        By.XPATH, '//*[@id="pdpMainImage-' + self.list_categories[list_category_i]["products"][products_i]['id'] + '"]')
                    result = image.screenshot_as_png
                    image_to_save = PImage.open(io.BytesIO(result))
                    image_to_save.thumbnail((200, 200))
                    image_to_save.save(image_path, optimize=True, quality=95)

                    time.sleep(3)
                    for index_categories in range(len(categories)):
                        worksheet.cell(row=excel_row+2, column=index_categories+1,
                                       value=categories[index_categories])

                    worksheet.cell(row=excel_row+2,
                                   column=6, value=marca)
                    worksheet.cell(row=excel_row+2,
                                   column=7, value=titulo)
                    if "modelo" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=8, value=dataSheet['modelo'])
                    worksheet.cell(row=excel_row+2,
                                   column=9, value=precio)
                    if "coleccion" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=10, value=dataSheet['coleccion'])
                    if "tipo" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=11, value=dataSheet['tipo'])
                    if "dimensiones" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=12, value=dataSheet['dimensiones'])
                    if "largo_(cm)" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=13, value=dataSheet['largo_(cm)'])
                    if "largo" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=13, value=dataSheet['largo'])
                    if "ancho_(cm)" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=14, value=dataSheet['ancho_(cm)'])
                    if "ancho" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=14, value=dataSheet['ancho'])
                    if "alto_(cm)" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=15, value=dataSheet['alto_(cm)'])
                    if "alto" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=15, value=dataSheet['alto'])
                    if "diametro" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=16, value=dataSheet['diametro'])
                    if "peso" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=17, value=dataSheet['peso'])
                    if "capacidad_volumetrica" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=18, value=dataSheet['capacidad_volumetrica'])
                    if "numero_de_piezas" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=19, value=dataSheet['numero_de_piezas'])

                    if "color" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=20, value=dataSheet['color'])
                    if "material" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=21, value=dataSheet['material'])
                    if "forma" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=22, value=dataSheet['forma'])
                    if "uso_(domestico_o/y_institucional)" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=23, value=dataSheet['uso_(domestico_o/y_institucional)'])
                    if "uso" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=23, value=dataSheet['uso'])
                    if "origen" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=24, value=dataSheet['origen'])
                    if "pais_de_origen" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=24, value=dataSheet['pais_de_origen'])
                    if "procedencia" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=24, value=dataSheet['procedencia'])
                    if "garantia" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=25, value=dataSheet['garantia'])
                    if "caracteristicas" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=26, value=dataSheet['caracteristicas'])
                    if "contenido" in dataSheet:
                        worksheet.cell(row=excel_row+2,
                                       column=27, value=dataSheet['contenido'])
                    worksheet.cell(row=excel_row+2,
                                   column=28, value=home_delivery)
                    worksheet.cell(row=excel_row+2,
                                   column=29, value=pick_up_in_store)
                    worksheet.cell(row=excel_row+2,
                                   column=30, value=stock_in_store)
                    today = date.today()
                    worksheet.cell(row=excel_row+2,
                                   column=31, value=today)
                    worksheet.cell(row=excel_row+2,
                                   column=32, value=self.list_categories[list_category_i]["products"][products_i]['link'])
                    worksheet.cell(row=excel_row+2,
                                   column=33, value=self.list_categories[list_category_i]["products"][products_i]['id'])
            
                    worksheet.add_image(Image(image_path),
                                        anchor='AH'+str(excel_row+2))

                    excel_row += 1

                except Exception as e:
                    print("[ERROR] PRODUCTO NO ENCONTRADO: " +
                          self.list_categories[list_category_i]["products"][products_i]['link'])
                    print("[ERROR]  " + repr(e))
                    continue

        workbook.save('salida.xlsx')
        workbook.close()

    def get_total_products(self):
        total = 0
        for list_category_i in range(len(self.list_categories)):
            total = total + \
                len(self.list_categories[list_category_i]["products"])
        return total

    def _convert_from_array_to_object(self, arr):
        prop: dict = {}
        for x in range(0, len(arr), 2):
            prop[arr[x].lower().replace(" ", "_")] = arr[x+1]
            print(prop)
        return prop

    def _normalice_string(self, text):
        return re.sub(
            r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
            normalize("NFD", text), 0, re.I
        ).strip()

    def producto(self):
        self.driver.get(
            "https://www.homecenter.com.co/homecenter-co/product/455376/bateria-10-piezas-antiadherente-gris-talent/455376/")

        linkDelproducto = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/ol').find_elements(
            By.CLASS_NAME, 'jsx-3306415055')[0].text
        print(linkDelproducto)
        print(linkDelproducto.split('\n'))

        return ""

    def map_datasheet(self):
        dat = {}
        data_sheet = []
        try:
            data_sheet = self.driver.find_element(
                By.XPATH, '//*[@id="pdp-highlights"]').find_elements(By.CSS_SELECTOR, "div.jsx-3969330179.row")
        except:
            print("No se encontro ficha tecnica")
        for data in data_sheet:
            detail = self._normalice_string(
                data.text).split("\n")
            dat[detail[0].lower().replace(" ", "_")] = detail[1]
        return dat

    def load_data(self):
        # self._finditem(self.categories_data, '')
        for key in self.categories_data:
            self.element_depth(self.categories_data, key, [], True)
        print(self.list_categories)

    def element_depth(self, grapho, current_element, analize_elements=[], reset=False):
        if reset:
            self.parent_categories = []
            self.child_categories = []
            self.node_count = 0

        if current_element in analize_elements:
            return

        analize_elements.append(current_element)
        print("elemento: {}".format(current_element))

        for neighbor in grapho[current_element]:
            if "category_" in neighbor:
                if grapho[current_element]["name"] not in self.parent_categories:
                    self.parent_categories.append(
                        grapho[current_element]["name"])

                self.element_depth(
                    grapho[current_element], neighbor, analize_elements)

            elif "end" in neighbor:
                self.node_count = self.node_count+1
                # valida si la solo hay una subcategoria y lo asocia como padre por defecto, indicando un solo nivel
                if len(self.parent_categories) == 0:
                    self.parent_categories.append(
                        grapho[current_element]["name"])
                else:
                    self.child_categories.append(
                        {"name": grapho[current_element]["name"],
                         "link": grapho[current_element]["link"]})
                # Se valida si se ha completada las ramificaciones o si la rama es de un solo nivel
                if ((self.node_count+2 == len(grapho)) or
                        (len(self.parent_categories) == 1 and self.node_count+2 == len(grapho[current_element]))):
                    print("Final de la rama")
                    if len(self.child_categories) >= 1:
                        for child in self.child_categories:
                            # copiar elementos de parent_categories en otro array
                            final_category = [None]*len(self.parent_categories)
                            for i in range(0, len(self.parent_categories)):
                                final_category[i] = self.parent_categories[i]

                            final_category.append(child["name"])
                            self.list_categories.append(
                                {"link": child["link"],
                                 "categories": final_category,
                                 "products": []})
                            final_category = []
                    else:
                        # copiar elementos de parent_categories en otro array
                        final_category = [None]*len(self.parent_categories)
                        for i in range(0, len(self.parent_categories)):
                            final_category[i] = self.parent_categories[i]

                        self.list_categories.append(
                            {"link": grapho[current_element]["link"],
                             "categories": final_category,
                             "products": []})

                        final_category = []

                    # reiniciar escaneo
                    self.parent_categories = [self.parent_categories[0]]
                    self.child_categories = []
                    self.node_count = 0


    #     time.sleep(1000)
clase1 = webScraper()
# clase1.get_categories()

clase1.get_categories_params()
clase1.load_data()
clase1.get_categories_test()
clase1.map_product_data()

# clase1.scan_page()
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
