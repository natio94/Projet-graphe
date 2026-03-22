from math import inf
import copy
def read(graphe):
    """
    Lecture d'un graphe à partir d'un fichier texte. Le format du fichier doit être le suivant :
    Ligne 1 – Nombre de sommets
    Ligne 2 – Nombre d’arcs
    Lignes 3 à 3 + « nombre d’arcs » – Extrémité initiale, suivie de l’extrémité terminale, suivie de la
    valeur de l’arc
    :param graphe:le nom du graphe à lire (sans l'extension .txt)
    :return:le nombre de sommets, le nombre d'arcs et la liste des arcs du graphe
    """
    with open("./graphes/"+graphe+".txt", "r") as f:
        nbSommets=int(clean(f.readline()))
        nbArcs=int(clean(f.readline()))
        arcs=[]
        for i in range(nbArcs):
            arcs.append(process(clean(f.readline()).split(" ")))
    return nbSommets, nbArcs, arcs

def matriceAdjacence(arcs, nbSommets):
    """
        Construction de la matrice d'adjacence d'un graphe à partir de sa liste d'arcs.
        Chaque élément de la matrice représente le poids de l'arc entre les sommets correspondants.
        Si il n'y a pas d'arc entre les sommets, l'élément est égal à l'infini.
    :param arcs: la liste des arcs du graphe, où chaque arc est représenté par un dictionnaire contenant les clés "debut", "fin" et "poids"
    :param nbSommets: le nombre de sommets du graphe
    :return: la matrice d'adjacence obtenue sous forme de tableau 2D.
    """
    matrice = [[inf for i in range(nbSommets)] for j in range(nbSommets)]
    for arc in arcs:
        matrice[arc["debut"]][arc["fin"]] = arc["poids"]
    return matrice

def clean(text):
    """
    Fonction auxiliaire. Enlève les sauts de ligne d'une chaîne de caractères.
    :param text: la chaîne de caractères à nettoyer
    :return: la chaîne de caractères nettoyée, sans les sauts de ligne
    """
    return text.replace("\n", "")

def process(arc):
    """
    Fonction auxiliaire. Transforme une liste de chaînes de caractères représentant un arc en un dictionnaire avec les clés "debut", "fin" et "poids".
    :param arc: une chaine de caractères représentant un arc, sous la forme "debut fin poids", où "debut" et "fin" sont les extrémités de l'arc et "poids" est la valeur de l'arc
    :return: un dictionnaire représentant l'arc, avec les clés "debut", "fin" et "poids", où les valeurs sont des entiers correspondant aux extrémités et au poids de l'arc
    """
    return {"debut": int(arc[0]), "fin": int(arc[1]), "poids": int(arc[2])}

def getSommets(arcs):
    """
    Fonction auxiliaire. Récupère la liste des sommets d'un graphe à partir de sa liste d'arcs.
    :param arcs: la liste des arcs du graphe sous forme de dictionnaire
    :return: la liste des sommets
    """
    sommets = set()
    for arc in arcs:
        sommets.add(arc["debut"])
        sommets.add(arc["fin"])
    return sommets

def floydWarshall(matrice,file=None):
    """
    Implémentation de l'algorithme de Roy Warshall pour trouver les plus courts chemins entre tous les couples de sommets d'un graphe.
    :param matrice: la matrice d'adjacence du graphe
    :param file: le fichier dans lequel écrire la trace de l'algorithme (optionnel)
    :return: la matrice finale
    """
    n = len(matrice[0])
    mat=matrice
    for k in range(n):
        printBoth("Iteration "+str(k),file=file)
        new_mat = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(n):
                new_mat[i][j]=min(mat[i][j],mat[i][k]+mat[k][j])
        printBoth("--------------------------------------------------",file=file)
        printMatrice(mat,f=file)
        printMatrice(new_mat,f=file)
        mat = new_mat
        printBoth(file=file)
    #On regarde si la matrice contient un cycle absorbant
    if absorbant(mat):
        printBoth("La matrice ne contient pas de cycle absorbant",file=file)
        printBoth("Affichage du cout de chaque  sous la forme [debut,arrivee,chemin, cout]",file=file)
        cout_chemin_FW(mat,file=file)
    else:
        printBoth("La matrice contient au moins un cycle absorbant",file=file)
    return mat

def cout_chemin_FW(matrice,file=None):
    """
    Fonction auxiliaire. Affiche le coût de chaque chemin entre les sommets du graphe, en utilisant la matrice finale obtenue après l'application de l'algorithme de Roy Warshall.
    :param matrice: la matrice finale
    :param file: le fichier dans lequel écrire la trace de l'algorithme (optionnel)
    """
    cout=[]
    mat = copy.deepcopy(matrice)
    for i in range(len(mat[0])):
        acc=False
        for j in range(len(mat[0])):
            val, idx = min((val, idx) for idx, val in enumerate(mat[i]))
            if val!=inf:
                if acc==False:
                    cout.append([i,idx,str(i)+"->"+str(idx),val])
                else:
                    cout.append([i,idx,str(cout[-1][2])+"->"+str(idx),val])
                mat[i][idx]=inf
                acc=True
    printBoth(cout,file=file)

def absorbant(matrice):
    """
    Fonction auxiliaire. Vérifie si la matrice contient un cycle absorbant, c'est-à-dire si elle contient une valeur négative sur sa diagonale.
    :param matrice: la matrice à vérifier
    :return: True si la matrice ne contient pas de cycle absorbant, False sinon
    """
    for i in range(len(matrice[0])):
        if matrice[i][i]<0:
            return False
    return True

def maxLen(matrice):
    """
    Fonction auxiliaire. Calcule la longueur maximale des éléments de la matrice, afin de pouvoir les afficher correctement.
    :param matrice: la matrice dont on veut calculer la longueur maximale des éléments
    :return: la longueur maximale des éléments de la matrice
    """
    maxi = 0
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if len(str(matrice[i][j])) > maxi:
                maxi = len(str(matrice[i][j]))
    return maxi

def printMatrice(matrice,f=None):
    """
    Fonction auxiliaire. Affiche la matrice d'adjacence du graphe de manière lisible, en alignant les éléments et en affichant les sommets correspondants.
    :param matrice: la matrice a afficher
    :param f: le fichier dans lequel écrire la trace de l'algorithme (optionnel)
    :return:
    """
    maxi=maxLen(matrice)
    tailleFinale=maxi*len(matrice)+len(matrice)+2
    sommets=list(getSommets(arcs))
    #On affiche les sommets en haut de la matrice
    for sommet in sommets:
        printBoth(str(sommet).rjust(maxi), end=" ",file=f)
    printBoth(file=f)
    printBoth("-" * tailleFinale,file=f)
    for i in range(len(matrice)):
        printBoth(sommets[i], end="",file=f)
        #On sépare les éléments de la matrice par des barres verticales et on les aligne à droite
        printBoth("|", end="",file=f)
        for j in range(len(matrice[i])):
            printBoth(str(matrice[i][j]).rjust(maxi), end="|",file=f)
        printBoth(file=f)
        printBoth("-" * tailleFinale,file=f)

def printBoth(txt="",end="\n",file=None):
    """Fonction auxiliaire. Permet d'affiche un texte donné à la fois dans la console et dans un fichier, si celui-ci est spécifié.
    :param txt: le texte à afficher
    :param end: le caractère de fin de ligne à utiliser (par défaut, un saut de ligne)"""
    print(txt,end=end,file=file)
    print(txt,end=end)

def openWrite(graphe):
    """
    Fonction auxiliaire. Ouvre un fichier en mode écriture pour y écrire la trace du code
    :param graphe:
    :return:le fichier ouvert en mode ajout pour y écrire la trace du code
    """
    with open ("./stacktraces/"+graphe+"_StackTrace.txt", "w") as f:
        print("Stack trace de l'algorithme de Roy Warshall pour le graphe", file=f)
        print()
    return open("./stacktraces/"+graphe+"_StackTrace.txt", "a")

if __name__ == "__main__":
    #Le code principal
    for i in range(1,14):
        graphe=str(i)
        with openWrite(graphe) as f:
            printBoth(file=f)
            printBoth("Lecture du graphe " + graphe, file=f)
            printBoth(file=f)
            nbSommets, nbArcs, arcs = read(graphe)
            matrice = matriceAdjacence(arcs, nbSommets)
            printBoth("Affichage de la matrice d'adjacence du graphe", file=f)
            printBoth(file=f)
            printMatrice(matrice, f)
            printBoth(file=f)
            printBoth("Application de l'algorithme de Roy Warshall", file=f)
            printBoth(file=f)
            mat = floydWarshall(matrice, file=f)
    graphe="pbHandicap"
    with openWrite(graphe) as f:
        printBoth(file=f)
        printBoth("Lecture du graphe "+graphe,file=f)
        printBoth(file=f)
        nbSommets, nbArcs, arcs=read(graphe)
        matrice=matriceAdjacence(arcs,nbSommets)
        printBoth("Affichage de la matrice d'adjacence du graphe",file=f)
        printBoth(file=f)
        printMatrice(matrice,f)
        printBoth(file=f)
        printBoth("Application de l'algorithme de Roy Warshall",file=f)
        printBoth(file=f)
        mat=floydWarshall(matrice,file=f)