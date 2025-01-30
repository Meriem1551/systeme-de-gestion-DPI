from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
u need to install webdriver from chrome then copy the executable downloaded 'chromedriver.exe' 
to the our project TP_IGL inside a folder that u will create too named  'drivers' that u will create 
and install selenuim in the terminal with pip install selenium
'''
# Spécifiez le chemin du driver Chrome
driver_path = "./drivers/chromedriver.exe" # Remplacez par le chemin de votre fichier chromedriver

# Créer un objet Service et initialiser le driver avec le chemin du chromedriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Accéder à la page Angular
    driver.get("http://localhost:4200/creation-dpi")

    # Attendre que le formulaire soit visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nom"))
    )

    # Remplir les champs du formulaire
    driver.find_element(By.ID, "nom").send_keys("Dahak")
    driver.find_element(By.ID, "prenom").send_keys("Fouad")
    driver.find_element(By.ID, "nss").send_keys("44444444")
    driver.find_element(By.ID, "ddn").send_keys("01-09-1987")
    driver.find_element(By.ID, "adresse").send_keys("1004 logts Example")
    driver.find_element(By.ID, "num_tel").send_keys("0778954667")
    driver.find_element(By.ID, "mutuelle").send_keys("Mutuelle C")
    driver.find_element(By.ID, "medecin").send_keys("bousdjira nadine")
    driver.find_element(By.ID, "contact").send_keys("Contact C")

    # Attendre que le bouton "Ajouter le DPI" soit cliquable avant de cliquer
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Ajouter le DPI')]"))
    )
    submit_button.click()

    print("Test réussi.")
except Exception as e:
    print("Erreur :", e)
finally:
    driver.quit()

'''
To run the test , run the server first then run the frontend and in anothor terminal , be sure to cd to the backend and then run the commande  : python test_create_dpi.py 
'''
