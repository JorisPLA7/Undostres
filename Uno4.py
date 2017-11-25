


from random import *

def melange(paquet):
    """
    Permet de melanger le paquet de cartes
    """
    shuffle(paquet)


def init():
    global paquet, mains, ordre_passage, nb_joueurs, nb_cartes
    nb_joueurs= int(input("Combien de joueurs ? "))
    nb_cartes=int(input("Combien de cartes par main ? "))
    mains={}
    ordre_passage={}
    for i in range (0,nb_joueurs):
        a=str(input("Entrez le nom du joueur "))
        main_jou=[]
        for j in range(0,nb_cartes):
            carte=paquet.pop(randint(1,len(paquet)-1))
            main_jou.append(carte)
        mains[a]= main_jou
        ordre_passage[i]=a

def sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif):
    #enlever main_joueur à la fin ?
    """
    Renvoie le numéro du joueur suivant
    """
    sens =1
    numero_jou=1
    if texte(tas_jeu[-1])=="changement sens":
       sens=-sens
    elif texte(tas_jeu[-1])=="passe tour":
        numero_jou=2
    actif = (actif+sens*numero_jou)%nb_joueurs-1
    return actif+1

def couleur(indice):
    """
    Permet d'obtenir la couleur d'une carte donnee par son indice.
    """
    if 1<= indice <= 25:
        return "rouge"
    elif 26 <= indice <= 50:
        return "bleu"
    elif 51 <= indice <= 75:
        return "jaune"
    elif 76 <= indice <= 100:
        return "vert"
    elif 101 <= indice <= 108:
        return None

def num_carte(indice):
    """
    Permet d'obtenir le numero d'une carte en fonction de son indice.
    +2=10
    chgt de sens =11
    passe tour = 12
    """
    if 108 < indice or indice < 1:
        return "Erreur"
    k=1
    for i in range (1,indice+1):
        if k==26 or k==51 or k==76 :
            k=1
        k+=1

    Paszéro= True
    while Paszéro:
        if k%2==0 :
            num=int(k/2-1)
            Paszéro=False
        else :
            num=int(k//2)
            if num==0:
                k+=1
                Paszéro=False
            else :
                Paszéro = False
    return num

def texte(indice):
    """
    Reçoit l'indice d'une carte et renvoie le texte complet correspondant
    """
    numero= num_carte(indice)
    if numero == 10 :
        numero="+2"
    elif numero == 11:
        numero = "changement sens"
    elif numero==12:
        numero = "passe tour"
    elif 100<indice<105:
        numero = "joker"
    elif 104 < indice <109:
        numero = "+4"

    if couleur(indice)== None:
        text= str(numero)
    else :
        text= str(numero) + " " + couleur(indice)
    return text

def pioche (paquet):
    """
    Permet de piocher une carte dans la pioche
    """
    carte_pioche=paquet.pop(randint(0,len(paquet)))
    return carte_pioche


def piocher(paquet, main_joueur, nombre_cartes):
    """
    Permet de piocher un nombre de cartes donné et de les mettre dans la main d'un joueur
    """
    if len(paquet) < nombre_cartes :
        pioche_vide(paquet, pile_jeu)
    for i in range (nombre_cartes):
        main_joueur.append(pioche(paquet))

def pioche_vide(pioche, pile_jeu):
    """
    Permet de refaire une pioche avec le tas du jeu si celle-ci est vide
    """
    for i in range (len(pile_jeu)-1):
        a=pile_jeu.pop(0)
        pioche.append(a)
        melange(pioche)

def regles_jeu(carte, tas_jeu):
    """
    Vérifie si les règles du jeu sont respectées
    """
    if (couleur(carte) == couleur(tas_jeu[-1])) or (num_carte(carte)== num_carte(tas_jeu[-1])) or ((texte(carte)== "joker") or (texte(tas_jeu[-1])=="joker") and (texte(tas_jeu[-1]) != "+2") and (texte(tas_jeu[-1]) != "+4")) or (texte(carte)== "+4") :
        return True
    else :
        return False

def plus4(tas_jeu):
    i=-1
    compteurpioche=0
    nom=texte(tas_jeu[i])
    while nom[0:2] == "+2" or nom=="+4" and tas_jeu[-1]!=tas_jeu[0]:
        if nom[0:2]=="+2":
            compteurpioche=compteurpioche+2
        else:
            compteurpioche=compteurpioche+4
        i-=1
    return compteurpioche


def joue_ou_pioche(main_joueur, tas_jeu):
    global paquet
    """
    Fait piocher le joueur en cas de besoin
    """
    peut_jouer=True
    compteur_2=True
    text=(texte(tas_jeu[-1]))
    if text[0:2]=="+2":
        compteur_2=False
        for i in main_joueur:
            if texte(i)=="+2" or texte(i)=="+4":
                compteur_2=True
        if compteur_2==False:
            compteur_pioche=plus4(tas_jeu)
            piocher(paquet, main_joueur, compteur_pioche)
            peut_jouer=False

    elif text =="+4":
        compteur_2=False
        for i in main_joueur:
            if texte(i)=="+4":
                compteur_2=True
        if compteur_2==False:
            compteur_pioche=plus4(tas_jeu)
            piocher(paquet, main_joueur, compteur_pioche)
            peut_jouer=False

    else :
        k=0
        for i in main_joueur :
            verifie = regles_jeu(i, tas_jeu)
            if verifie==False:
                k+=1
        if k==len(main_joueur):
            affiche=[texte(i) for i in mains[ordre_passage[actif]]]
            print("Au tour du joueur", ordre_passage[actif], affiche)
            joueur_piocher = input("Vous ne pouvez pas jouer, voulez-vous piocher ? y/n")
            if joueur_piocher == "y":
                piocher(paquet, main_joueur, 1)
                affiche=[texte(i) for i in main_joueur]
                print("Voici votre nouveau jeu : ", affiche)
                verifie=regles_jeu(main_joueur[-1],tas_jeu)
                if verifie==True:
                    peut_jouer=True
                else :
                    peut_jouer=False
            else :
                print("Vous êtes obligés de piocher")
                piocher(paquet, main_joueur, 1)
                affiche=[texte(i) for i in main_joueur]
                print("Voici votre nouveau jeu : ", affiche)
                verifie=regles_jeu(main_joueur[-1],tas_jeu)
                if verifie==True:
                    peut_jouer=True
                else :
                    peut_jouer=False

    return peut_jouer



def carte_a_jouer(main_joueur, tas_jeu, carte):
    global actif
    """
    Verifie si le joueur peut jouer la  carte
    """
    ok=joue_ou_pioche(main_joueur, tas_jeu)
    ok2=False
    if ok:
        ok2=regles_jeu(carte, tas_jeu)
        while ok2==False:
            print(ok2, carte)
            carte=int(input("Choisissez une autre carte : "))
            ok2=regles_jeu(carte, tas_jeu)
        return carte
    else :
        return False

def test_victoire(main_joueur):
    """
    Teste si un joueur a gagné, renvoie True si il a gagné
    """
    if len(main_joueur)==0:
        print("VOUS AVEZ GAGNE !!!!!!!! \n Fin de la partie ")
        return True
    else :
        return False

def Tour_jeux(actif, main_joueur, tas_jeu, nb_joueurs,carte):
    global mains, ordre_passage
    """
    Renvoie l'actif si jamais personne n'a gagné
    """
    test=carte_a_jouer(main_joueur, tas_jeu, carte)
    if test != False :
        carte2=main_joueur.pop(main_joueur.index(test))
        tas_jeu.append(carte2)
    #print(mains[ordre_passage[actif]])
    vict=test_victoire(main_joueur)
    if vict:
        return None
    else :
        actif=sens_jeu(main_joueur, tas_jeu, nb_joueurs, actif)
        #joue_ou_pioche(main_joueur, tas_jeu)
        return actif




if __name__=="__main__":

    paquet =[i for i in range (1,109)]
    init()
    melange(paquet)
    tas_jeu=[paquet[0]]
    actif=0
    test2=joue_ou_pioche(mains[ordre_passage[0]], tas_jeu)

    while actif != None:
        affiche=[texte(i) for i in mains[ordre_passage[actif]]]
        print("Carte dessus paquet : ",texte(tas_jeu[-1]))
        test2=joue_ou_pioche(mains[ordre_passage[actif]], tas_jeu)
        print("Au tour du joueur", ordre_passage[actif], affiche)

        if test2:
            carte=int(input("Entrez l'indice de la carte que vous souhaitez jouer"))
            a=mains[ordre_passage[actif]]
            carte=a[carte]
            actif=Tour_jeux(actif, mains[ordre_passage[actif]], tas_jeu, nb_joueurs,carte)
        else :
            print("Tas jeu : ", texte(tas_jeu[-1]))
            actif2=sens_jeu(mains[ordre_passage[actif]], tas_jeu, nb_joueurs, actif)
            actif2=actif
