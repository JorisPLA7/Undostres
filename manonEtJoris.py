from random import *
from tkinter import *
# from PIL import Image, ImageTk
from tkinter import messagebox


def start():
    global fenprinc
    fenprinc = Tk()
    fenprinc.geometry("1350x766")  # redimension de la fenêtre
    fenprinc.title("Undostres")  # renommer la fenêtre
    """
    image = Image.open("uno.gif")
    print("wesh")
    photo = PhotoImage('Users\GE3MS\Desktop\Manon mon seul Amour\monuno.gif')
    print("alors")
    """
    canvas = Canvas(fenprinc)
    """
    canvas.create_image(0,0, anchor = NW, image=photo)
    print("pouloulou")
    canvas.image=photo
    print("yolo")
    """
    canvas.pack()
    Text = Button(fenprinc, text="Commencer la partie", bg="white", relief="raised", font=("Times", "20", "bold"),
                  cursor="heart", command=fenetre_data)
    Text.pack()
    # Text_fenprinc= canvas.create_window(1100, 130, window=Text)
    fenprinc.mainloop()


def melange(paquet):
    """
    Permet de melanger le paquet de cartes
    """
    shuffle(paquet)


def init():
    """
    Creation mains de joueurs et de l'ordre de passage
    """
    global mains, ordre_passage, nb_joueurs, nb_cartes

    main_jou = []
    for j in range(0, nb_cartes):
        carte = paquet.pop(randint(1, len(paquet) - 1))
        main_jou.append(carte)
    mains[nomjou] = main_jou
    ordre_passage[salade] = nomjou


def init2():
    """
    Crée le dictionnaire qui contient les couleurs en fonction de l'indice de la carte, initialise le sens et l'actif.
    """

    global sens, dico, actif, TestDejaPioche
    TestDejaPioche = False
    actif = 0

    dico = {}
    dico[0] = "nul"
    for i in range(1, 26):
        dico[i] = "rouge"
    for i in range(26, 51):
        dico[i] = "bleu"
    for i in range(51, 76):
        dico[i] = "jaune"
    for i in range(76, 101):
        dico[i] = "vert"
    for i in range(101, 109):
        dico[i] = None

    sens = 1


def sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif):
    global sens
    """
    Renvoie le numéro du joueur suivant
    """
    numero_jou = 1
    text3 = texte(tas_jeu[-1])
    if text3[0:15] == "changement_sens":
        sens = -sens  # change le sens si jamais la carte est un changement de sens
    elif text3[0:10] == "passe tour":
        numero_jou = 2  # fait passer 2 joueurs au lieu d'un lorsque la carte est un passe-tour
    actif = (actif + sens * numero_jou) % nb_joueurs - 1
    return actif + 1


def couleur(indice):
    """
    Permet d'obtenir la couleur d'une carte donnee par son indice.
    """
    return dico[indice]


def num_carte(indice):
    """
    Permet d'obtenir le numero d'une carte en fonction de son indice.
    +2=10
    chgt de sens =11
    passe tour = 12
    """
    if 108 < indice or indice < 1:
        return "Erreur"  # Permet de déceler une erreur car ces cartes n'existent pas
    k = 1
    for i in range(1, indice + 1):
        if k == 26 or k == 51 or k == 76:
            k = 1
        k += 1

    Paszéro = True
    while Paszéro:
        if k % 2 == 0:
            num = int(k / 2 - 1)
            Paszéro = False
        else:
            num = int(k // 2)
            if num == 0:
                k += 1
                Paszéro = False
            else:
                Paszéro = False
    return num


def texte(indice):
    """
    Reçoit l'indice d'une carte et renvoie le texte complet correspondant
    """
    numero = num_carte(indice)
    if numero == 10:
        numero = "+2"
    elif numero == 11:
        numero = "changement_sens"
    elif numero == 12:
        numero = "passe tour"
    elif 100 < indice < 105:
        numero = "joker"
    elif 104 < indice < 109:
        numero = "+4"

    if couleur(indice) == None:
        text = str(numero)
    else:
        text = str(numero) + " " + couleur(indice)
    return text


def pioche(paquet):
    """
    Permet de piocher une carte dans la pioche
    """
    carte_pioche = paquet.pop(randint(0, len(paquet) - 1))
    return carte_pioche


def piocher(paquet, main_joueur, nombre_cartes):
    """
    Permet de piocher un nombre de cartes donné et de les mettre dans la main d'un joueur
    """
    if len(paquet) < nombre_cartes:
        pioche_vide(paquet, pile_jeu)
    for i in range(nombre_cartes):
        main_joueur.append(pioche(paquet))


def pioche_vide(pioche, pile_jeu):
    """
    Permet de refaire une pioche avec le tas du jeu si celle-ci est vide
    """
    for i in range(len(pile_jeu) - 1):
        a = pile_jeu.pop(0)
        pioche.append(a)
        melange(pioche)


def regles_jeu(carte, tas_jeu):
    """
    Vérifie si les règles du jeu sont respectées
    """
    if (couleur(carte) == couleur(tas_jeu[-1])) or (num_carte(carte) == num_carte(tas_jeu[-1])) or (
        (texte(carte) == "joker") or (texte(tas_jeu[-1]) == "joker") and (texte(tas_jeu[-1]) != "+2") and (
        texte(tas_jeu[-1]) != "+4")) or (texte(carte) == "+4"):
        return True
    else:
        return False


def plus4(tas_jeu):
    i = -1
    compteurpioche = 0
    nom = texte(tas_jeu[i])
    while nom[0:2] == "+2" or nom == "+4":
        if nom[0:2] == "+2":
            compteurpioche = compteurpioche + 2
        else:
            compteurpioche = compteurpioche + 4

        if tas_jeu[i] != tas_jeu[0]:
            i -= 1
            nom = texte(tas_jeu[i])
        else:
            break
    return compteurpioche


def ok():
    global couleur_carte_spe
    couleur_carte_spe_indice = demandecoul.curselection()
    print(couleur_carte_spe_indice)# retourne un 1-uplet tel que (2,)
    couleur_carte_spe = ['bleu','vert','rouge','jaune'][couleur_carte_spe_indice[0]] # on choisit la couleur correspondant à la valeur dans le tuple
    print(couleur_carte_spe)
    totalite_cartes[carte] = totalite_cartes[carte] + " " + couleur_carte_spe
    fencoul.destroy()
    programme_principal()


def fenetre_couleur():
    global demandecoul, fencoul
    fencoul = Toplevel()
    fencoul.title("Couleur")
    textecoul = Label(fencoul, text="Quelle couleur souhaitez-vous ?")
    textecoul.pack()

    demandecoul = Listbox(fencoul)
    demandecoul.insert(1, "bleu")
    demandecoul.insert(2, "vert")
    demandecoul.insert(3, "rouge")
    demandecoul.insert(4, "jaune")
    demandecoul.pack()
    valid = Button(fencoul, text="Valider", command=ok)
    valid.pack()


def joue_ou_pioche(main_joueur, tas_jeu):
    global paquet, couleur4, actif, compteurplus4, sens, verifprint, TestDejaPioche
    """
    Fait piocher le joueur en cas de besoin
    """
    peut_jouer = True  # va être retourné, précise si le joueur peut encore jouer ou non
    compteur_2 = True
    text = (texte(tas_jeu[-1]))
    if text[0:2] == "+2" and TestDejaPioche == False:
        compteur_2 = False
        for i in main_joueur:
            if texte(i)[0:2] == "+2" or texte(i) == "+4":
                compteur_2 = True
        if compteur_2 == False:
            compteur_pioche = plus4(tas_jeu)  # determine le nombre de cartes a piocher
            piocher(paquet, main_joueur, compteur_pioche)  # fait piocher le joueur
            TestDejaPioche = True
            peut_jouer = False

    elif text == "+4":
        compteur_pioche = plus4(tas_jeu)
        piocher(paquet, main_joueur, compteur_pioche)
        peut_jouer = False
        if sens == 1:
            prenom = ordre_passage[(actif - 1) % nb_joueurs]
        if sens == -1:
            prenom = ordre_passage[(actif + 1) % nb_joueurs]
        Tu_as_cette_couleur = False
        while not Tu_as_cette_couleur:
            print("Quelle couleur souhaitez-vous ", prenom, " ? ")
            fenetre_couleur()
            couleur4 = couleur_carte_spe
            for w in mains[ordre_passage[actif]]:
                if texte(w).split()[-1] == couleur4 or texte(w).split()[0] == "+4" or texte(w).split()[0] == "joker":
                    Tu_as_cette_couleur = True
        dico[tas_jeu[-1]] = couleur4

    elif text == "joker":
        fenetre_couleur()
        couleur5 = couleur_carte_spe
        dico[tas_jeu[-1]] = couleur5
        creer_cartes()


    else:
        k = 0
        for i in main_joueur:
            verifie = regles_jeu(i, tas_jeu)
            if verifie == False:
                k += 1
        if k == len(main_joueur):
            affiche = [texte(i) for i in mains[ordre_passage[actif]]]
            print("Au tour du joueur", ordre_passage[actif], affiche)
            piocher(paquet, main_joueur, 1)
            messagebox.showinfo("Pioche", "Vous avez pioché")
            affiche = [texte(i) for i in main_joueur]
            print("Voici votre nouveau jeu : ", affiche)
            verifie = regles_jeu(main_joueur[-1], tas_jeu)
            if verifie == True:
                peut_jouer = True
            else:
                peut_jouer = False
                print("False")
    return peut_jouer
    print("Le joueur", peut_jouer, "jouer")


def carte_a_jouer(main_joueur, tas_jeu, carte):
    global actif
    """
    Verifie si le joueur peut jouer la  carte
    """
    ok = joue_ou_pioche(main_joueur, tas_jeu)
    ok2 = False
    if ok:
        ok2 = regles_jeu(carte, tas_jeu)
        while ok2 == False:
            print(ok2, carte)
            a = mains[ordre_passage[actif]]
            carte = a[carte]
            ok2 = regles_jeu(carte, tas_jeu)
            print(ok2)

        return carte
    else:
        return False


def test_victoire(main_joueur):
    """
    Teste si un joueur a gagné, renvoie True si il a gagné
    """
    if len(main_joueur) == 0:
        print("VOUS AVEZ GAGNE !!!!!!!! \n Fin de la partie ")
        fencarte.destroy()
        return True
    else:
        return False


def Tour_jeux(actif, main_joueur, tas_jeu, nb_joueurs, carte):
    global mains, ordre_passage
    """
    Renvoie l'actif si jamais personne n'a gagné
    """
    test = carte_a_jouer(main_joueur, tas_jeu, carte)
    if test != False:
        print(actif)
        print(main_joueur)
        carte2 = main_joueur.pop(main_joueur.index(test))
        tas_jeu.append(carte2)
        if texte(tas_jeu[-2]).split()[0] == "+2":
            TestDejaPioche = False
    else:
        messagebox.showinfo("Eh non...", "Vous ne pouvez pas jouer")
    vict = test_victoire(main_joueur)
    if vict:
        return None
    else:
        actif = sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif)
        return actif
    print("l'actif est : ... ", actif)


def okE(key):
    global joueurs
    touche = key.keysym
    if touche == "Return":
        joueurs = entree.get()


def fenetre_data():
    global entree, nb_cartes, nb_joueurs, fenjeu, entree, entree2

    fenjeu = Tk()
    texte_nb_joueurs = Label(fenjeu, text="Combien de joueurs ? ")
    texte_nb_joueurs.pack()

    entree = Entry(fenjeu)
    entree.pack()
    texte_nb_cartes = Label(fenjeu, text="Combien de cartes par main ? ")
    texte_nb_cartes.pack()
    entree2 = Entry(fenjeu)
    entree2.pack()
    valider = Button(fenjeu, text="Valider", command=programme1)
    valider.pack()

    # entree.focus_set()
    # fenjeu.bind("<Return>",okE)


def fenetre_nom():
    global dico_noms, fennom

    fennom = Tk()
    ordre = Label(text="Entrez le nom des joueurs")
    ordre.pack()
    valider2 = Button(fennom, text="Valider", command=initinit)
    valider2.pack()
    dico_noms = {}
    for i in range(nb_joueurs):
        dico_noms[i] = "nom" + str(i)
    for i in range(nb_joueurs):
        dico_noms[i] = Entry(fennom)
        dico_noms[i].pack()


def programme1():
    global nb_joueurs, nb_cartes, totalite_cartes

    nb_joueurs = int(entree.get())
    nb_cartes = int(entree2.get())
    fenjeu.destroy()
    fenprinc.destroy()
    fenetre_nom()


def ff(bt):
    global carte, totalite_cartes
    carte = bt.cget("text")
    for k in totalite_cartes:
        if totalite_cartes[k] == carte:
            carte = k
            while not carte in mains[ordre_passage[actif]]:
                carte += 1
    if regles_jeu(carte, tas_jeu):
        print("La arte est :", carte)
        if texte(carte) == "+4" or texte(carte) == "joker":
            fenetre_couleur()
        else:
            programme_principal()


def initinit():
    global nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage, nomjou, salade, actif, totalite_cartes, carte, fencarte, dictionnaire_trad, affiche
    paquet = [i for i in range(1, 109)]
    melange(paquet)
    init2()
    carteDeBase = 0
    tas_jeu = [paquet[carteDeBase]]
    while texte(paquet[0]) == "+4" or texte(paquet[0]) == "joker" or texte(paquet[0]).split()[-1] == "+2":
        tas_jeu = [paquet[carteDeBase + 1]]

    mains = {}
    ordre_passage = {}

    for salade in range(nb_joueurs):
        nomjou = dico_noms[salade].get()
        init()

    fennom.destroy()

    print(texte(tas_jeu[-1]))

    test2 = joue_ou_pioche(mains[ordre_passage[0]], tas_jeu)
    fencarte = Tk()
    fencarte.title("Fenetre espion")
    affiche = [texte(i) for i in mains[ordre_passage[actif]]]
    totalite_cartes = {}
    dictionnaire_trad = {"bleu": "cyan", "rouge": "red", "vert": "green", "jaune": "yellow"}

    for i in range(1, 109):
        totalite_cartes[i] = str(texte(i))
    clefs_cartes = list(totalite_cartes.keys())
    creer_cartes()


def creer_cartes():
    global nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage, nomjou, salade, actif, totalite_cartes, carte, fencarte, affiche

    messagebox.showinfo("Changement", "Au tour du joueur : " + ordre_passage[actif])  # fenetre de changement de tour
    fencarte.destroy()  # Destruction de la fenêtre de jeu
    fencarte = Tk()
    # raccourci=totalite_cartes[tas_jeu[-1]].split()
    if couleur(tas_jeu[-1]) == None:
        print("haha")
        Carte_tas_jeu = Button(fencarte, text=str(texte(tas_jeu[-1])), width=15, height=15)
    else:
        Carte_tas_jeu = Button(fencarte, bg=str(dictionnaire_trad[str(couleur(tas_jeu[-1]))]),
                               text=str(texte(tas_jeu[-1])), width=15, height=15)
    Carte_tas_jeu.grid(column=1, row=1)
    print("Carte dessus paquet : ", texte(tas_jeu[-1]))
    print("la main de ", ordre_passage[actif], "est ", mains[ordre_passage[actif]])
    test2 = joue_ou_pioche(mains[ordre_passage[actif]], tas_jeu)
    if test2:
        print("Au tour du joueur", ordre_passage[actif], affiche)
        au_tour = Label(fencarte, text="Au tour du joueur " + str(ordre_passage[actif]))

        au_tour.grid(column=1, row=2)
        colonne = 1
        affiche = [texte(i) for i in mains[ordre_passage[actif]]]
        for i in affiche:
            if i.split()[-1] == i.split()[0]:
                i = Button(fencarte, text=i, width=15, height=15)
            else:
                i = Button(fencarte, bg=str(dictionnaire_trad[str(i.split()[-1])]), text=i, width=15, height=15)
            carte = i.config(command=lambda bt=i: ff(bt))
            i.grid(column=colonne, row=3, sticky=E)
            colonne += 1

    else:
        actif2 = sens_jeu(mains[ordre_passage[actif]], tas_jeu, nb_joueurs, actif)
        actif = actif2
        creer_cartes()


def programme_principal():
    global nb_joueurs, nb_cartes, paquet, tas_jeu, actif, mains, ordre_passage, nomjou, salade, actif, carte

    print("carte", carte)

    actif = Tour_jeux(actif, mains[ordre_passage[actif]], tas_jeu, nb_joueurs, carte)
    if actif == None:
        messagebox.showinfo("Victoire", "Vous avez gagné !")

    else:
        creer_cartes()
        fencarte.mainloop()


start()