import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().replace('\u202f', '')).replace('\n', '').replace('Par ', '')


def scrape_voitures(pages=1):
    data = []
    for page in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/voitures-4?page={page}"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        annonces = soup.select(".listings-cards__list-item")

        for annonce in annonces:
            try:
                titre = clean_text(annonce.select_one("h2 a").text)
                parts = titre.split()
                marque = parts[0] if len(parts) > 0 else ""
                annee = parts[-1] if parts[-1].isdigit() and len(parts[-1]) == 4 else ""

                prix = clean_text(annonce.select_one("h3").text).replace("F CFA", "").replace(" ", "")

                km = boite = carburant = ""
                for li in annonce.select("ul.listing-card__attribute-list li"):
                    text = clean_text(li.text)
                    if "km" in text.lower():
                        km = text.replace("km", "").strip()
                    elif "Manuelle" in text or "Automatique" in text:
                        boite = text
                    elif "Essence" in text or "Diesel" in text:
                        carburant = text

                adresse = clean_text(annonce.select_one(".town-suburb").text) + " " + clean_text(annonce.select_one(".province").text)
                proprietaire = clean_text(annonce.select_one(".time-author").text)

                data.append([marque, annee, prix, adresse, km, boite, carburant, proprietaire])
            except:
                continue
        time.sleep(1)
    return pd.DataFrame(data, columns=["marque", "annee", "prix", "adresse", "kilometrage", "boite_vitesse", "carburant", "proprietaire"])


def scrape_motos(pages=1):
    data = []
    for page in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/motos-and-scooters-3?page={page}"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        annonces = soup.select(".listings-cards__list-item")

        for annonce in annonces:
            try:
                titre = clean_text(annonce.select_one("h2 a").text)
                parts = titre.split()
                marque = parts[0] if len(parts) > 0 else ""
                annee = parts[-1] if parts[-1].isdigit() and len(parts[-1]) == 4 else ""

                prix = clean_text(annonce.select_one("h3").text).replace("F CFA", "").replace(" ", "")

                km = ""
                for li in annonce.select("ul.listing-card__attribute-list li"):
                    text = clean_text(li.text)
                    if "km" in text.lower():
                        km = text.replace("km", "").strip()

                adresse = clean_text(annonce.select_one(".town-suburb").text) + " " + clean_text(annonce.select_one(".province").text)
                proprietaire = clean_text(annonce.select_one(".time-author").text)

                data.append([marque, annee, prix, adresse, km, proprietaire])
            except:
                continue
        time.sleep(1)
    return pd.DataFrame(data, columns=["marque", "annee", "prix", "adresse", "kilometrage", "proprietaire"])


def scrape_locations(pages=1):
    data = []
    for page in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/location-de-voitures-19?page={page}"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        annonces = soup.select(".listings-cards__list-item")

        for annonce in annonces:
            try:
                titre = clean_text(annonce.select_one("h2 a").text)
                parts = titre.split()
                marque = parts[0] if len(parts) > 0 else ""
                annee = parts[-1] if parts[-1].isdigit() and len(parts[-1]) == 4 else ""

                prix = clean_text(annonce.select_one("h3").text).replace("F CFA", "").replace(" ", "")

                adresse = clean_text(annonce.select_one(".town-suburb").text) + " " + clean_text(annonce.select_one(".province").text)
                proprietaire = clean_text(annonce.select_one(".time-author").text)

                data.append([marque, annee, prix, adresse, proprietaire])
            except:
                continue
        time.sleep(1)
    return pd.DataFrame(data, columns=["marque", "annee", "prix", "adresse", "proprietaire"])


# Setup Selenium driver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
