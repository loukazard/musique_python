# importation des bibliothèques nécessaires au programme
import csv
from operator import itemgetter
import matplotlib.pyplot as plt
from PIL import Image
import customtkinter


# ouverture de notre base de données de deux manières différentes
tableau_musique = open("spotify.csv", encoding="latin-1")
tableau_musique2 = open("spotify_sans_virgule.csv", encoding='latin-1')

# mise en forme des fichiers csv pour obtenir une liste
spotify = list(csv.reader(tableau_musique, delimiter=";"))
spotify_sans_virgule = list(csv.reader(tableau_musique2, delimiter=";"))

# dernière mise en forme pour avoir une liste de listes avec une ligne par sous liste dans la variable liste_virgule
liste_virgule = []
for morceau in spotify:
    liste_virgule.append(morceau[0].split(","))

# dernière mise en forme pour avoir une liste de listes avec une ligne par sous liste dans la variable top200
liste_top200 = []
for morceau in spotify_sans_virgule:
    liste_top200.append(morceau[0].split(","))

# création d'une liste contenant l'ensemble des artistes
liste_artiste = []
# on parcourt le fichier ligne par ligne
for ligne in range(1, len(liste_virgule)):
    # si l'artiste n'est pas présent dans la liste alors, on l'ajoute
    if not liste_virgule[ligne][2] in liste_artiste:
        liste_artiste.append(liste_virgule[ligne][2])

# on parcourt la liste pour supprimer les erreurs d'affichage
for artiste in range(1, len(liste_artiste)):
    # si le premier caractère de l'artiste est un guillemet, on le supprime
    if liste_artiste[artiste][0] == '"':
        liste_artiste[artiste] = liste_artiste[artiste][1:]
# On trie la liste par ordre alphabétique
liste_artiste.sort()

# création d'une liste qui contiendra toutes les musiques
liste_musique = []
# on parcourt le fichier ligne par ligne
for ligne in range(1, len(liste_top200)):
    # si la musique n'est pas dans la liste, alors on l'ajoute à la liste des musiques
    if not liste_top200[ligne][3] in liste_musique:
        liste_musique.append(liste_top200[ligne][3])
# On trie la liste par ordre alphabétique
liste_musique.sort()

# Création d'une liste qui contiendra tous les pays
liste_pays = []
# On parcourt le fichier ligne par ligne
for ligne in range(1, len(liste_top200)):
    # Si le pays n'est pas dans la liste, alors on l'ajoute
    if not liste_top200[ligne][-1] in liste_pays:
        liste_pays.append(liste_top200[ligne][-1])
# On trie la liste par ordre alphabétique
liste_pays.sort()


def top200(pays: str) -> str:
    """Première fonction pour obtenir le Top 200 du pays passé en paramètre"""
    # On commence par créer une liste vide qui stockera le résultat
    liste_morceaux = []
    # On parcourt les lignes en vérifiant si le paramètre est le pays de la ligne
    for titre in liste_top200:
        if titre[-1].lower() == pays.lower():
            # Si la condition est vérifiée, on ajoute dans la liste de départ
            liste_morceaux.append(titre[3])
    # mise en forme du résultat sous forme d'une chaîne de caractère
    result = ""
    for mus in liste_morceaux:
        result += mus + "\n"
    return result


def top_pays_artiste(artiste: str) -> str:
    """Deuxième fonction pour obtenir le pays où l'artiste passé en paramètre est le plus écouté"""
    # création de la liste qui stockera le résultat
    stream_pays = []
    # On parcourt le fichier mais de 200 en 200 pour étudier pays par pays
    for pays in range(1, len(liste_top200), 200):
        # variable somme qui accueillera le nombre total de stream et variable p_artiste qui stocke le pays étudié
        somme = 0
        p_artiste = liste_top200[pays][-1]
        # Deuxième boucle pour parcourir toutes les musiques d'un pays
        for stream in range(pays, pays + 199):
            # si l'artiste est dans la ligne étudiée
            if artiste.lower() in liste_top200[stream][2].lower():
                # On ajoute le nombre de stream
                somme += int(liste_top200[stream][7])
            # Si c'est la dernière ligne du pays
            if stream == (pays + 198):
                # on ajoute à la liste un tuple contenant le pays et le nombre de stream
                stream_pays.append([p_artiste, somme])
    # On renvoie le premier élément de la liste triée par nombre de stream décroissant
    top1 = sorted(stream_pays, key=itemgetter(1), reverse=True)[0]
    if top1[1] == 0:
        return "Cet artiste n'est pas présent dans le fichier"
    return f"Le pays où {artiste.title()} est le plus écouté est : {top1[0].title()}"





def top_pays_musique(musique: str) -> str:
    """Troisième fonction qui renvoie le pays où la musique passée en paramètre est la plus écoutée"""
    artiste =""
    for art in liste_top200:
        if musique in art:
            artiste = art[2]
    # création de la liste qui stockera le résultat
    stream_pays = []
    # On parcourt le fichier, mais de 200 en 200 pour étudier pays par pays
    for pays in range(1, len(liste_top200), 200):
        # variable somme qui accueillera le nombre total de stream et variable p_musique qui stocke le pays étudié
        somme = 0
        p_musique = liste_top200[pays][-1]
        # Deuxième boucle pour parcourir toutes les musiques d'un pays
        for stream in range(pays, pays + 199):
            # si la musique passée en paramètre est dans la ligne étudiée
            if musique.lower() == str(liste_top200[stream][3]).lower():
                # On ajoute son nombre de stream
                somme += int(liste_top200[stream][7])
            # Si la ligne étudiée est la dernière du pays
            if stream == (pays + 198):
                # On ajoute le pays et le nombre de stream
                stream_pays.append([p_musique, somme])
    # On renvoie le premier élément de la liste triée par nombre de stream décroissant
    top = sorted(stream_pays, key=itemgetter(1), reverse=True)
    # affichage des résultats sous forme de chaîne de caractères
    if top[0][1] == 0:
        return "Ce morceau n'est pas dans la liste"
    return f"Le pays où {musique.title()} de {artiste.title()} est le plus écouté est : {top[0][0].title()}"


def top_10_pays(pays):
    """Quatrième fonction qui renvoie les 10 musiques ayant été le plus longtemps dans le top 200"""
    # Création de la liste qui stockera le résultat
    liste_topClassement = []
    # on parcourt chaque ligne du fichier
    for ligne in liste_top200:
        # si le pays de la ligne est celui en paramètre
        if ligne[-1].lower() == pays.lower():
            # On ajoute à la liste le nombre de semaines dans le top 200, l'artiste et le titre
            liste_topClassement.append((int(ligne[6]), ligne[2], ligne[3]))
    # on créé une liste triéée des morceaux selon le temps passé dans le top 200
    top = sorted(liste_topClassement, key=itemgetter(0), reverse=True)
    # on renvoie les 10 premiers de la liste top sous forme de chaîne de caractères
    result = "Nb de semaines dans le top/Artiste/Titre\n\n"
    for titre in range(0, 10):
        result += str(top[titre]) + "\n\n"
    return result





def plus_de_stream(nb: int) -> str:
    """Cinquième fonction pour obtenir les musiques ayant plus de streams que la nombre passé en paramètre"""
    # Création de la liste qui stockera le résultat
    liste_musique = []
    # On parcourt toutes les lignes du fichier
    for ligne in range(1, len(liste_top200)):
        # si le nombre de stream de la musique est supérieure au paramètre
        if int(liste_top200[ligne][7]) > nb:
            # On ajoute la musique dans la liste
            liste_musique.append((int(liste_top200[ligne][7]), liste_top200[ligne][2], liste_top200[ligne][3]))
    # On tri la liste par nombre de streams
    top = sorted(liste_musique, key=itemgetter(0))
    # on renvoie le résultat sou forme de chaîne
    if len(top) == 0:
        return f"Aucun morceau n'a plus de {nb} streams"
    result = ""
    for titre in top:
        result += str(titre) + "\n"
    return result





def graph_artiste_monde(artiste: str) -> None:
    """Sixième fonction pour créer un graphique représentant la répartion des streams d'un artiste dans le monde"""
    # Variable classement pour accueillir les résultats
    classement = []
    # Variables Labels et sizes pour accueillir les pays qui seront sur le graphique et la taille des barres de l'histogramme
    labels = []
    sizes = []
    # Liste proportion pour accueillir la taille des barres en pourcentage
    proportion = []
    # On parcourt la liste pays par pays
    for pays in range(1, len(liste_top200), 200):
        # variable somme qui accueillera le nombre total de stream et variable p_artiste qui stocke le pays étudié
        somme_stream = 0
        pays_artiste = liste_top200[pays][-1]
        for ligne in range(pays, pays + 199):
            # si l'artiste est dans la ligne étudiée et qu'il est le premier artiste en cas de feat
            if artiste.lower() in liste_top200[ligne][2].lower():
                # On ajoute le nombre de stream de la musique
                somme_stream += int(liste_top200[ligne][-2])
            # Si c'est la dernière ligne du pays
            if ligne == (pays + 198):
                # on ajoute à la liste un tuple contenant le pays et le nombre de stream
                classement.append((pays_artiste, somme_stream))
    # On créé la liste Top qui sera triée avec les pays où l'artiste est le plus présent
    top = sorted(classement, key=itemgetter(1), reverse=True)[0:9]
    somme_tot = 0
    # On partcourt top
    for etiquette in top:
        # Si le nombre de stream est supérieur à 0 :
        if etiquette[1] > 0:
            # On ajoute à labels le nom du pays et à sizes et somme_tot le nombre de stream
            labels.append(etiquette[0])
            sizes.append(etiquette[1])
            somme_tot += int(etiquette[1])
    # On parcourt size et on calcule la proportion du nombre de stream
    for taille in sizes:
        proportion.append(taille / somme_tot * 100)
    # Création d'une figure et d'un axe
    fig, ax = plt.subplots(figsize=(15, 10))
    # Création d'un graphique en barres avec les étiquettes (labels) et les proportions fournies
    graph = plt.bar(labels, proportion)
    # Ajout de texte au-dessus de chaque barre pour afficher les pourcentages
    for bar, prop in zip(graph, proportion):
        # On récupère la hauteur de la barre
        height = bar.get_height()
        # On récupère la position x du centre d'une barre et la hauteur pour le placement du pourcentage
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{round(prop, 1)}%', ha='center', va='bottom')
    ax.set_xticklabels(labels, rotation=45, ha='right')
    # Ajout du titre du graphique
    plt.title(f'Répartition des streams de {artiste} dans le monde')
    # Ajout des étiquettes pour les axes x et y :
    plt.xlabel('Pays', fontsize=14, fontweight='bold')
    plt.ylabel('Nombre de stream (%)', fontsize=14, fontweight='bold')
    # affichage du graphique
    plt.savefig('artiste.png')


def graph_musique_monde(musique: str):
    artiste = ""
    for art in liste_top200:
        if musique in art:
            artiste = art[2]
    # Variable classement pour accueillir les résultats
    classement = []
    # Variables Labels et sizes pour accueillir les pays qui seront sur le graphique et la taille des barres de l'histogramme
    labels = []
    sizes = []
    # Liste proportion pour accueillir la taille des barres en pourcentage
    proportion = []
    # On parcourt la liste pays par pays
    for pays in range(1, len(liste_top200), 200):
        # variable somme qui accueillera le nombre total de stream et variable p_artiste qui stocke le pays étudié
        somme_stream = 0
        pays_artiste = liste_top200[pays][-1]
        for ligne in range(pays, pays + 199):
            # si l'artiste est dans la ligne étudiée et qu'il est le premier artiste en cas de feat
            if musique.lower() == liste_top200[ligne][3].lower():
                # On ajoute le nombre de stream de la musique
                somme_stream += int(liste_top200[ligne][-2])
            # Si c'est la dernière ligne du pays
            if ligne == (pays + 198):
                # on ajoute à la liste un tuple contenant le pays et le nombre de stream
                classement.append((pays_artiste, somme_stream))
    # On crée la liste Top qui sera triée avec les pays où l'artiste est le plus présent
    top = sorted(classement, key=itemgetter(1), reverse=True)[0:9]
    somme_tot = 0
    # On parcourt top
    for etiquette in top:
        # Si le nombre de stream est supérieur à 0 :
        if etiquette[1] > 0:
            # On ajoute à labels le nom du pays et à sizes et somme_tot le nombre de stream
            labels.append(etiquette[0])
            sizes.append(etiquette[1])
            somme_tot += int(etiquette[1])
    # On parcourt size et on calcule la proportion du nombre de stream
    for taille in sizes:
        proportion.append(taille / somme_tot * 100)
    # Création d'une figure et d'un axe
    fig, ax = plt.subplots(figsize=(15, 10))
    # Création d'un graphique en barres avec les étiquettes (labels) et les proportions fournies
    graph = plt.bar(labels, proportion)
    # Ajout de texte au-dessus de chaque barre pour afficher les pourcentages
    for bar, prop in zip(graph, proportion):
        # On récupère la hauteur de la barre
        height = bar.get_height()
        # On récupère la position x du centre d'une barre et la hauteur pour le placement du pourcentage
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{round(prop, 1)}%', ha='center', va='bottom')
    # Ajout du titre du graphique
    plt.title(f'Répartition des streams de {musique} de {artiste} dans le monde')
    # Ajout des étiquettes pour les axes x et y :
    plt.xlabel('Pays', fontsize=14, fontweight='bold')
    plt.ylabel('Nombre de stream (%)', fontsize=14, fontweight='bold')
    # Affichage du graphique
    plt.savefig('stream.png')


""" FENETRE GRAPHIQUE """
# customtkinter.set_ctk_parent_class(tkinterdnd2.Tk)
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# -------------------fenetres --------------------------
# Création de la fenêtre principale index
index = customtkinter.CTk()
# On récupère la taille de la fenêtre
w, h = index.winfo_screenwidth(), index.winfo_screenheight()

# on met la page en plein écran et on programme la touche echap pour pouvoir quitter
index.geometry("%dx%d+0+0" % (w, h))
index.bind('<Escape>', lambda e: index.destroy())

# On donne un nom à la fenêtre
index.title("fenetre utilisateur")
# on créé une frame et on la place sur la page
frame_1 = customtkinter.CTkFrame(master=index)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)
# Création du titre et affichage de ce dernier
logo_label = customtkinter.CTkLabel(frame_1, text="La musique à travers le monde",
                                    font=customtkinter.CTkFont(family='System', size=45, weight="bold"))
logo_label.pack()


# artistes
def open_artiste():
    """Définition d'une fonction pour ouvrir la page artiste en plein écran."""
    artiste = customtkinter.CTkToplevel()
    artiste.geometry("%dx%d+0+0" % (w, h))
    artiste.title("Fenêtre Artiste")

    # On ajoute le même titre en rajoutant "Les artistes" en dessous puis on affiche
    logo_label = customtkinter.CTkLabel(artiste,
                                        text="La musique à travers le monde",
                                        font=customtkinter.CTkFont(family='System', size=35, weight="bold"))
    logo_label.pack()
    logo2 = customtkinter.CTkLabel(artiste,
                                   text="Les artistes\n\n",
                                   font=customtkinter.CTkFont(family='System', size=30))
    logo2.pack()
    # On ajoute un texte pour expliquer ce qu'il faut faire
    title1 = customtkinter.CTkLabel(artiste,
                                    text="Sélectionnez un artiste et obtenez le pays où il est le plus écouté :\n",
                                    font=customtkinter.CTkFont(size=15, weight="bold"))
    # on initialise une variable qui stockera le résultat de la fonction
    reponse1 = customtkinter.StringVar(artiste)
    reponse1.set("")
    # Création d'un menu déroulant qui exécute la fonction top_pays_artiste avec l'artiste sélectionné
    optionmenu_top_pays_a = customtkinter.CTkOptionMenu(artiste,
                                                        values=liste_artiste,
                                                        command=lambda artiste: reponse1.set(top_pays_artiste(artiste)))
    # Création d'une alternative au menu déroulant avec la barre de recherche
    text = customtkinter.CTkLabel(artiste,
                                  text="Ou : \n\n Ecrivez le nom d'un artiste  en particulier :",
                                  font=customtkinter.CTkFont(size=15, weight="bold"))
    barre_recherche = customtkinter.CTkEntry(artiste)

    def search1():
        """Fonction de reherche pour récupérer le résultat et le mettre dans la variable reponse1"""
        recherche = barre_recherche.get()
        reponse1.set(top_pays_artiste(recherche))
    # création d'un bouton pour valider et definition de la zone où sera affiché le résultat
    button_search = customtkinter.CTkButton(artiste, text="Valider", command=search1)
    result1 = customtkinter.CTkLabel(artiste, textvariable=reponse1, font=customtkinter.CTkFont(size=12))
    # affichage de toute sur la page avec des padding de 5px
    title1.pack(pady=5)
    optionmenu_top_pays_a.pack(pady=5, padx=5)
    text.pack(pady=5, padx=5)
    barre_recherche.pack(pady=5, padx=5)
    button_search.pack(padx=5)
    result1.pack(pady=5, padx=5)
    optionmenu_top_pays_a.set("choisissez un artiste")

    def open_page2():
        """Création d'une fonction pour ouvrir une page 2 avec la même taille et le même titre de page"""
        artiste_page_2 = customtkinter.CTkToplevel()
        artiste_page_2.title("fenêtre artiste 2")
        artiste_page_2.geometry("%dx%d+0+0" % (w, h))

        logo_label = customtkinter.CTkLabel(artiste_page_2,
                                            text="La musique à travers le monde",
                                            font=customtkinter.CTkFont(family='System', size=35, weight="bold"))
        logo_label.pack()
        logo2 = customtkinter.CTkLabel(artiste_page_2,
                                       text="Les artistes",
                                       font=customtkinter.CTkFont(family='System', size=30))
        logo2.pack()

        def affiche_image_art(artist):
            """Création d'une fonction qui exécute la fonction graph_artist_monde et met le graphique dans le label resultat"""
            graph_artiste_monde(artist)
            photo = customtkinter.CTkImage(light_image=Image.open('artiste.png'), size=(600, 400))
            result_label.configure(image=photo)
            result_label.pack()

        # Menu déroulant qui exécute la fonction affiche_image_art avec l'artiste sélectionné en paramètre
        optionmenu_graph_a = customtkinter.CTkOptionMenu(artiste_page_2,
                                                         values=liste_artiste,
                                                         command=lambda artiste: affiche_image_art(artiste))
        title2 = customtkinter.CTkLabel(artiste_page_2,
                                        text="Sélectionnez un artiste et regardez la répartition de ses streams à travers la monde :",
                                        font=customtkinter.CTkFont(size=15, weight="bold"))
        # Alternative au menu déroulant avec la barre de recherche
        text = customtkinter.CTkLabel(artiste_page_2,
                                      text="Ou : \n Ecrivez le nom d'un artiste  en particulier :",
                                      font=customtkinter.CTkFont(size=15, weight="bold"))
        entry = customtkinter.CTkEntry(artiste_page_2)

        def search2():
            """Fonction qui récupère l'entrée de la barre de recherche et exécute affiche_image_art"""
            recherche = entry.get()
            affiche_image_art(recherche)
        # bouton pour valider la recherche
        button_search = customtkinter.CTkButton(artiste_page_2,
                                                text="Valider",
                                                command=search2)
        # création du label qui sera mis à jour dans affiche_image_art
        result_label = customtkinter.CTkLabel(artiste_page_2, text="")
        # ajout des zones sur la page
        title2.pack(pady=5)
        optionmenu_graph_a.pack(pady=5)
        text.pack(pady=5)
        entry.pack(pady=5)
        button_search.pack(pady=5)

        # texte du menu déroulant
        optionmenu_graph_a.set("choisissez un artiste")

        # on met la deuxième page au premier plan et on la lance avec mainloop
        artiste.attributes('-topmost', False)
        artiste_page_2.attributes('-topmost', True)
        artiste_page_2.mainloop()

    # Création des boutons présents en page 1 qui sont : 'retour' et 'page2'
    button_exit_artiste = customtkinter.CTkButton(artiste, text='retour ', command=artiste.destroy)
    button_exit_artiste.pack(side="bottom", anchor="se", padx=15, pady=30)
    button_page2 = customtkinter.CTkButton(artiste, text='Page 2', command=open_page2)
    button_page2.pack(side="bottom", anchor="se", padx=15, pady=0)

    # Exécution de la page et mise au premier plan
    artiste.attributes('-topmost', True)
    artiste.mainloop()


def open_titre():
    """Définition d'une fonction pour ouvrir la page titre en plein écran."""
    titre = customtkinter.CTkToplevel()
    titre.geometry("%dx%d+0+0" % (w, h))
    titre.title("fenetre titre")

    # On ajoute le même titre en rajoutant "Les artistes" en dessous puis on affiche
    logo_label = customtkinter.CTkLabel(titre, text="La musique à travers le monde",
                                        font=customtkinter.CTkFont(family='System', size=45, weight="bold"))
    logo_label.pack()
    logo2 = customtkinter.CTkLabel(titre, text="Les titres", font=customtkinter.CTkFont(family='System', size=30))
    logo2.pack()

    # variable qui stockera la réponse
    reponse2 = customtkinter.StringVar(titre)
    reponse2.set("")

    # Ajout du texte explicatif
    title3 = customtkinter.CTkLabel(titre,
                                    text="Sélectionnez un morceau et regardez le pays où il est le plus écouté :",
                                    font=customtkinter.CTkFont(size=15, weight="bold"))
    # Création du menu déroulant pour exécuter la fonction top_pays_musique au choix de l'artiste
    optionmenu_artiste = customtkinter.CTkOptionMenu(titre, values=liste_musique,
                                                     command=lambda musique: reponse2.set(top_pays_musique(musique)))
    # Alternative avec la barre de recherche
    text = customtkinter.CTkLabel(titre,
                                  text="Ou écrivez le nom d'un morceau en particulier :",
                                  font=customtkinter.CTkFont(size=15, weight="bold"))
 # création de la barre de recherche
    barre_recherche1 = customtkinter.CTkEntry(titre)

    def search1():
        """Fonction qui récupère l'entrée de la barre de recherche et exécute top_pays_musique"""
        recherche = barre_recherche1.get()
        reponse2.set(top_pays_musique(recherche))
    # Création du bouton pour valider la recherche et exécuter la fonction recherche
    bouton_recherche1 = customtkinter.CTkButton(titre, text="Valider", command=search1)
    # Création du label pour afficher la réponse
    result2 = customtkinter.CTkLabel(titre, textvariable=reponse2, font=customtkinter.CTkFont(size=12))
    # affichage des zones sur la page
    title3.pack(pady=5)
    optionmenu_artiste.pack(pady=5)
    text.pack(pady=5)
    barre_recherche1.pack(pady=5)
    bouton_recherche1.pack(pady=5)
    result2.pack(pady=5)
    optionmenu_artiste.set("choisissez un morceau")

    # Création d'une variable qui accueillera la prochaine réponse
    reponse3 = customtkinter.StringVar(titre)
    barre_recherche2 = customtkinter.CTkEntry(titre)

    def search2():
        """Fonction qui récupère l'entrée de la barre de recherche et exécute plus_de_stream"""
        nombre_texte = int(barre_recherche2.get())
        reponse3.set(plus_de_stream(nombre_texte))

    # Création du texte explicatif
    title5 = customtkinter.CTkLabel(titre,
                                    text="Entrez un nombre et Regardez le musiques qui ont plus de streams que le nombre donné :",
                                    font=customtkinter.CTkFont(size=15, weight="bold"))
    # Création de la zone qui accueillera le résultat
    res = customtkinter.CTkScrollableFrame(titre, width=500, height=150)
    # ajout du résultat dans la zone
    res_label = customtkinter.CTkLabel(res, textvariable=reponse3)
    # affichage des zones dans la fenêtre
    button_search = customtkinter.CTkButton(titre, text="Valider", command=search2)
    title5.pack()
    barre_recherche2.pack(pady=5)
    button_search.pack()
    res.pack()
    res_label.pack()

    def open_page_2():
        """Création d'une fonction qui ouvre une deuxième page titre avec la même taille et le même titre"""
        titre_page_2 = customtkinter.CTkToplevel()
        titre_page_2.title("fenêtre titre2")
        titre_page_2.geometry("%dx%d+0+0" % (w, h))

        logo_label = customtkinter.CTkLabel(titre_page_2, text="La musique à travers le monde",
                                            font=customtkinter.CTkFont(family='System', size=45, weight="bold"))
        logo_label.pack()
        logo2 = customtkinter.CTkLabel(titre_page_2, text="Les titres",
                                       font=customtkinter.CTkFont(family='System', size=30))
        logo2.pack()

        def affiche_image_titre(musique):
            """Création d'une fonction que rend une musique en paramètre et exécute graph_musique_monde avec la musique
            en paramètre. Ensuite, on ajoute le graphique au label résultat"""
            graph_musique_monde(musique)
            photo = customtkinter.CTkImage(light_image=Image.open('stream.png'), size=(600, 400))
            result_label.configure(image=photo)
            result_label.pack()

        # Création du menu déroulant qui exécute affiche_imae_titre avec le morceau sélectionné
        optionmenu_graph_m = customtkinter.CTkOptionMenu(titre_page_2,
                                                         values=liste_musique,
                                                         command=lambda musique: affiche_image_titre(musique))
        title4 = customtkinter.CTkLabel(titre_page_2,
                                     text="Sélectionnez un morceau et regardez la répartition de ses streams à travers la monde :\n",
                                      font=customtkinter.CTkFont(size=15, weight="bold"))

        # Alternative avec la barre de recherche
        text = customtkinter.CTkLabel(titre_page_2,
                                      text="\nOu : \n\nEcrivez le nom d'un morceau  en particulier :",
                                      font=customtkinter.CTkFont(size=15, weight="bold"))
        barre_recherche = customtkinter.CTkEntry(titre_page_2)

        def search():
            """Fonction qui récupère l'entrée de la barre de recherche et exécute affiche_image_titre"""
            recherche = barre_recherche.get()
            affiche_image_titre(recherche)

        # Création du bouton pour valider la recherche
        button_search = customtkinter.CTkButton(titre_page_2,
                                                text="Valider",
                                                command=search)
        # Création de la zone qui accueillera le graphique
        result_label = customtkinter.CTkLabel(titre_page_2)
        # ajout des zones sur la page
        title4.pack(pady=5)
        optionmenu_graph_m.pack(pady=5)
        text.pack(pady=5)
        barre_recherche.pack(pady=5)
        button_search.pack()
        optionmenu_graph_m.set("choisissez un morceau")


        # On met la page 2 au premier plan et on la lance
        titre_page_2.attributes("-topmost", True)
        titre.attributes("-topmost", False)
        titre_page_2.mainloop()

    # Création du boutton d'accès à la page 2
    button_titre_page_2 = customtkinter.CTkButton(text="Page 2", master=titre, command=open_page_2)
    button_titre_page_2.pack(side="left")

    # affichage de la page 2 au premier plan
    titre.attributes("-topmost", True)


# pays
def open_pays():
    """Définition d'une fonction pour ouvrir la page pays en plein écran avec le même titre"""
    pays = customtkinter.CTkToplevel()
    pays.geometry("%dx%d+0+0" % (w, h))
    pays.title("fenetre pays")

    logo_label = customtkinter.CTkLabel(pays, text="La musique à travers le monde",
                                        font=customtkinter.CTkFont(family='System', size=45, weight="bold"))
    logo_label.pack()
    logo2 = customtkinter.CTkLabel(pays, text="Les pays", font=customtkinter.CTkFont(family='System', size=30))
    logo2.pack()

    # Variable qui accueillera le résultat
    reponse4 = customtkinter.StringVar(pays)
    reponse4.set("")

    # Menu déroulant qui exécute la fonction top200 avec le pays sélectionné
    optionmenu_pays = customtkinter.CTkOptionMenu(pays, values=liste_pays,
                                                  command=lambda pays: reponse4.set(top200(pays)))
    # Création de la zone qui accueillera le résultat
    result4 = customtkinter.CTkScrollableFrame(pays, width=500, height=500)
    # ajout_du_résultat dans la zone
    result4_label = customtkinter.CTkLabel(result4, textvariable=reponse4)
    # ajout des zones sur la page
    result4_label.pack()
    optionmenu_pays.place(x=100, y=100)
    result4.pack(side="left")
    optionmenu_pays.set("choisissez un pays")

    # Varibale qui stckera la prochaine réponse
    reponse5 = customtkinter.StringVar(pays)
    reponse5.set("")

    # menu déroulant qui exécute la fonction top_10_pays avec le pays sélectionné
    optionmenu_pays_10 = customtkinter.CTkOptionMenu(pays, values=liste_pays,
                                                     command=lambda pays: reponse5.set(top_10_pays(pays)))
    # Création de la zone qui accueillera le résultat
    result5 = customtkinter.CTkScrollableFrame(pays, width=500, height=500)
    # Ajout du résultat dans la zone
    result5_label = customtkinter.CTkLabel(result5, textvariable=reponse5, font=customtkinter.CTkFont(size=15))
    # ajout des zones dans la page
    result5_label.pack()
    optionmenu_pays_10.place(x=1000, y=100)
    result5.pack(side="right")
    optionmenu_pays_10.set("choisissez un pays")

    # Création du bouton retour
    button_exit_pays = customtkinter.CTkButton(pays, text='retour ', command=pays.destroy)
    button_exit_pays.pack(side="bottom", pady=40)

    # mise au premier plan de la page pays
    pays.attributes("-topmost", True)
    pays.mainloop()


# ------------------------------ Boutons -------------------------------------------------
# placement des boutons sur la page index pour ouvrir les autres pages
bouton_artiste = customtkinter.CTkButton(text='artiste ', master=frame_1, command=open_artiste)
bouton_artiste.pack(pady=10, padx=10)

bouton_titre = customtkinter.CTkButton(text='titres ', master=frame_1, command=open_titre)
bouton_titre.pack(pady=10, padx=10)

bouton_pays = customtkinter.CTkButton(text='pays ', master=frame_1, command=open_pays)
bouton_pays.pack(pady=10, padx=10)

# lancement de la fenêtre index au lancement du programme
index.mainloop()


