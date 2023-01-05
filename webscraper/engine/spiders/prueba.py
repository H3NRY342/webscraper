
    for producto1 in producto_links:
            print(producto1.get_attribute("href"))
            listaDeProdutos.append(producto1.get_attribute("href"))
            time.sleep(10)
            print(listaDeProdutos)
            # * pagina de todos los productos--->
            titulo = driver.find_elements(By.XPATH, '//*[@id="title-pdp-link"]/h2')
            time.sleep(1)
            precios = driver.find_elements(
                By.CSS_SELECTOR, ".product-price-and-logo.jsx-344173702 .main.jsx-344173702")
            time.sleep(0.10)
            imgs = driver.find_elements(
                By.ID, 'testId-Link-brand-pdp-link')
            time.sleep(1)
            for elemento in titulo:
                time.sleep(0.10)
                elemento.text
                print("----------------")
                print(elemento.text)
                elemtet_data["Titulos"].append(elemento.text)
            for elemento1 in precios:
                time.sleep(0.10)
                print("----------------")
                print(elemento1.text)
                elemtet_data["Precios"].append(elemento1.text)

            for elemento2 in imgs:
                time.sleep(0.10)
                print("----------------categorias")
                print(elemento2.get_attribute('href'))
                print(elemento2.text)
                elemtet_data["categorias-link"].append(elemento2.get_attribute('href'))
                elemtet_data["categorias"].append(elemento2.text)
            next_page.click()
            time.sleep(10)
            # print(elemtet_data)
        # bottun_next = driver.find_element(By.XPATH, '//*[@id="bottom-pagination-next-page"]').click()
    df = pd.DataFrame(listaDeProdutos)
    print(df)
    df1 = pd.DataFrame(data)
    print(df1)
    df.to_csv("data4.csv")
    df1.to_excel("data-v1.xlsx")
