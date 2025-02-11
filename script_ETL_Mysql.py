import os
import csv
import mysql.connector
from mysql.connector import Error

# Configuration de la base de données MySQL
db_config = {
    "host": "localhost",
    "user": "root",  # Remplacez par votre utilisateur MySQL
    "password": "",  # Remplacez par votre mot de passe MySQL
    "database": "bd_articles"  # Base de données à utiliser
}

def convert_to_txt(dossier):
    fichiers = os.listdir(dossier)
    for fichier in fichiers:
        chemin_complet = os.path.join(dossier, fichier)
        if os.path.isfile(chemin_complet) and not fichier.endswith(".txt"):
            nouveau_nom = os.path.splitext(fichier)[0] + ".txt"
            chemin_nouveau = os.path.join(dossier, nouveau_nom)
            os.rename(chemin_complet, chemin_nouveau)
            print(f"Fichier converti : {fichier} -> {nouveau_nom}")

def process_all_files(input_dir, output_file):
    all_data = []
    if not os.path.exists(input_dir):
        print(f"Le dossier '{input_dir}' n'existe pas.")
        return

    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            print(f"Traitement du fichier : {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if len(lines) < 2:
                    print(f"Fichier avec moins de deux lignes ignoré : {file_path}")
                    continue

                title = lines[0].strip()
                second_line = lines[1].strip()
                entries = second_line.split('|')

                for entry in entries:
                    fields = entry.split(',')
                    if len(fields) == 5:
                        author = fields[0].strip()
                        affiliation = f"{fields[1].strip()} - {fields[2].strip()}"
                        city = fields[3].strip()
                        country = fields[4].strip()
                    elif len(fields) == 4:
                        author = fields[0].strip()
                        affiliation = fields[1].strip()
                        city = fields[2].strip()
                        country = fields[3].strip()
                    else:
                        print(f"Ligne ignorée (format incorrect) : {entry}")
                        continue

                    all_data.append([title, author, affiliation, city, country])

    if all_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Titre", "Auteur", "Affiliation", "Ville", "Pays"])
            writer.writerows(all_data)
        print(f"Les données de tous les fichiers ont été extraites et sauvegardées dans : {output_file}")
    else:
        print("Aucune donnée extraite. Le fichier CSV n'a pas été généré.")

def create_database():
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS bd_articles")
        conn.commit()
        cursor.close()
        conn.close()
        print("Base de données 'bd_articles' créée ou déjà existante.")
    except Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")

def create_tables():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS pays (
                id_pays INT AUTO_INCREMENT PRIMARY KEY,
                nom_pays VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS ville (
                id_ville INT AUTO_INCREMENT PRIMARY KEY,
                nom_ville VARCHAR(255) NOT NULL,
                id_pays INT NOT NULL,
                FOREIGN KEY (id_pays) REFERENCES pays(id_pays)
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS affiliation (
                id_affiliation INT AUTO_INCREMENT PRIMARY KEY,
                nom_affiliation VARCHAR(255) NOT NULL,
                id_ville INT NOT NULL,
                FOREIGN KEY (id_ville) REFERENCES ville(id_ville)
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS auteur (
                id_auteur INT AUTO_INCREMENT PRIMARY KEY,
                nom_auteur VARCHAR(255) NOT NULL,
                id_affiliation INT NOT NULL,
                FOREIGN KEY (id_affiliation) REFERENCES affiliation(id_affiliation)
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS article (
                id_article INT AUTO_INCREMENT PRIMARY KEY,
                titre_article VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS rediger (
                id_article INT NOT NULL,
                id_auteur INT NOT NULL,
                annee INT NOT NULL,
                PRIMARY KEY (id_article, id_auteur),
                FOREIGN KEY (id_article) REFERENCES article(id_article),
                FOREIGN KEY (id_auteur) REFERENCES auteur(id_auteur)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables créées avec succès.")
    except Error as e:
        print(f"Erreur lors de la création des tables : {e}")

def insert_data(csv_file, year):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                nom_article, nom_auteur, nom_affiliation, nom_ville, nom_pays = row

                if nom_pays.endswith("."):
                    nom_pays = nom_pays[:-1]

                # Insérer ou récupérer l'ID du pays
                cursor.execute("SELECT id_pays FROM pays WHERE nom_pays = %s", (nom_pays,))
                result = cursor.fetchone()
                if result:
                    id_pays = result[0]
                else:
                    cursor.execute("INSERT INTO pays (nom_pays) VALUES (%s)", (nom_pays,))
                    id_pays = cursor.lastrowid

                # Insérer ou récupérer l'ID de la ville
                cursor.execute("SELECT id_ville FROM ville WHERE nom_ville = %s AND id_pays = %s", (nom_ville, id_pays))
                result = cursor.fetchone()
                if result:
                    id_ville = result[0]
                else:
                    cursor.execute("INSERT INTO ville (nom_ville, id_pays) VALUES (%s, %s)", (nom_ville, id_pays))
                    id_ville = cursor.lastrowid

                # Insérer ou récupérer l'ID de l'affiliation
                cursor.execute("SELECT id_affiliation FROM affiliation WHERE nom_affiliation = %s AND id_ville = %s", (nom_affiliation, id_ville))
                result = cursor.fetchone()
                if result:
                    id_affiliation = result[0]
                else:
                    cursor.execute("INSERT INTO affiliation (nom_affiliation, id_ville) VALUES (%s, %s)", (nom_affiliation, id_ville))
                    id_affiliation = cursor.lastrowid

                # Insérer ou récupérer l'ID de l'auteur
                cursor.execute("SELECT id_auteur FROM auteur WHERE nom_auteur = %s AND id_affiliation = %s", (nom_auteur, id_affiliation))
                result = cursor.fetchone()
                if result:
                    id_auteur = result[0]
                else:
                    cursor.execute("INSERT INTO auteur (nom_auteur, id_affiliation) VALUES (%s, %s)", (nom_auteur, id_affiliation))
                    id_auteur = cursor.lastrowid

                # Insérer ou récupérer l'ID de l'article
                cursor.execute("SELECT id_article FROM article WHERE titre_article = %s", (nom_article,))
                result = cursor.fetchone()
                if result:
                    id_article = result[0]
                else:
                    cursor.execute("INSERT INTO article (titre_article) VALUES (%s)", (nom_article,))
                    id_article = cursor.lastrowid

                # Insérer dans la table rediger si la relation n'existe pas déjà
                cursor.execute("SELECT * FROM rediger WHERE id_article = %s AND id_auteur = %s", (id_article, id_auteur))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO rediger (id_article, id_auteur, annee) VALUES (%s, %s, %s)", (id_article, id_auteur, year))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Données du fichier {csv_file} insérées avec succès.")
    except Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")

if __name__ == "__main__":
    dossier1 = "Articles_2014"
    dossier2 = "Articles_2015"
    dossier3 = "Articles_2016"
    dossier4 = "Articles_2017"
    fichier_csv_sortie1 = "resultats_2014.csv"
    fichier_csv_sortie2 = "resultats_2015.csv"
    fichier_csv_sortie3 = "resultats_2016.csv"
    fichier_csv_sortie4 = "resultats_2017.csv"

    convert_to_txt(dossier1)
    convert_to_txt(dossier2)
    convert_to_txt(dossier3)
    convert_to_txt(dossier4)
    
    process_all_files(dossier1, fichier_csv_sortie1)
    process_all_files(dossier2, fichier_csv_sortie2)
    process_all_files(dossier3, fichier_csv_sortie3)
    process_all_files(dossier4, fichier_csv_sortie4)
    
    create_database()
    create_tables()
    insert_data(fichier_csv_sortie1, 2014)
    insert_data(fichier_csv_sortie2, 2015)
    insert_data(fichier_csv_sortie3, 2016)
    insert_data(fichier_csv_sortie4, 2017)
