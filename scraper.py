from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import json

# Calea către Edge Driver
service = Service('C:\\edgedrivers\\msedgedriver.exe')
driver = webdriver.Edge(service=service)

# Maximizarea ferestrei browserului la modul fullscreen
driver.maximize_window()

wait = WebDriverWait(driver, 10)

# Deschide pagina de logare
driver.get("https://edcora.ro/advertoriale-seo/comanda-advertoriale/")

time.sleep(10)

# Așteaptă ca butonul de logare să fie vizibil și apoi faceți clic pe el
login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.xoo-el-login-tgr")))
login_button.click()

time.sleep(10)

# Așteaptă ca formularul de logare să fie vizibil
wait.until(EC.visibility_of_element_located((By.NAME, "xoo-el-username")))

# Introdu datele de logare
driver.find_element(By.NAME, "xoo-el-username").send_keys("my_mail@yahoo.com")
driver.find_element(By.NAME, "xoo-el-password").send_keys("my_password")

# Faceți clic pe butonul de trimitere a formularului de logare
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(10)

# Configurația pentru derularea lentă și fină
scroll_pause_time = 1  # Timp de pauză redus pentru o derulare mai fină
screen_height = driver.execute_script("return window.screen.height;")  # Obține înălțimea ecranului
i = 1

while True:
    # Derulează o fracțiune din ecran pe fiecare iterație, de exemplu, un sfert din înălțimea ecranului
    next_scroll_position = (screen_height / 4) * i  # Ajustarea pentru o derulare mai fină
    driver.execute_script(f"window.scrollTo(0, {next_scroll_position});")
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if next_scroll_position > scroll_height:
        break  # Dacă s-a ajuns la sfârșitul paginii, iese din buclă
    
time.sleep(10)

# Salvează pagina după logare într-un fișier HTML
with open('logged_in_page.html', 'w', encoding='utf-8') as file:
    file.write(driver.page_source)

with open('logged_in_page.html', 'r', encoding='utf-8') as file:
    logged_in_html = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(logged_in_html, 'html.parser')

product_entries = soup.find_all('a', class_='shop-item-title-link')

# Initialize an empty list to hold the product details
product_details = []

# Extract product names and prices
for product in product_entries:
    product_detail = {}
    product_detail['name'] = product.text.strip()
    product_detail['url'] = product['href']
    common_parent = product.parent.parent
    price_elements = common_parent.find_all('span', class_='woocommerce-Price-amount amount')
    if price_elements:
        product_detail['initial_price'] = price_elements[0].get_text(strip=True) if len(price_elements) > 0 else "nu are reducere"
        product_detail['reduced_price'] = price_elements[1].get_text(strip=True) if len(price_elements) > 1 else "nu are reducere"
    else:
        product_detail['initial_price'] = "nu are reducere"
        product_detail['reduced_price'] = "nu are reducere"
    product_details.append(product_detail)

# Save the product details to a JSON file
with open('product_details.json', 'w', encoding='utf-8') as json_file:
    json.dump(product_details, json_file, ensure_ascii=False, indent=4)

# Return the path to the saved JSON file
json_file_path = json_file.name

# Închide browserul
driver.quit()

# Print the path to the JSON
