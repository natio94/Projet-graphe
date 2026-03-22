from math import inf
import copy
def read(graphe):
    with open("./graphes/"+graphe+".txt", "r") as f:
        nbSommets=int(clean(f.readline()))
        nbArcs=int(clean(f.readline()))
        arcs=[]
        for i in range(nbArcs):
            arcs.append(process(clean(f.readline()).split(" ")))
    return nbSommets, nbArcs, arcs

def matriceAdjacence(arcs, nbSommets):
    matrice = [[inf for i in range(nbSommets)] for j in range(nbSommets)]
    for arc in arcs:
        matrice[arc["debut"]][arc["fin"]] = arc["poids"]
    return matrice

def clean(text):
    return text.replace("\n", "")

def process(arc):
    return {"debut": int(arc[0]), "fin": int(arc[1]), "poids": int(arc[2])}

def getSommets(arcs):
    sommets = set()
    for arc in arcs:
        sommets.add(arc["debut"])
        sommets.add(arc["fin"])
    return sommets

def floydWarshall(matrice):
    n = len(matrice[0])
    mat=matrice
    for k in range(n):
        new_mat = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(n):
                new_mat[i][j]=min(mat[i][j],mat[i][k]+mat[k][j])
        print("--------------------------------------------------")
        printMatrice(mat)
        printMatrice(new_mat)
        mat = new_mat
    if absorbant(mat):
        print("la matrice ne contient pas de cycle absorbant")
    else:
        print("la matrice contient au moins un cycle absorbant")
    cout_chemin_FW(mat)
    return mat

def cout_chemin_FW(matrice):
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
    print(cout)

def absorbant(matrice):
    for i in range(len(matrice[0])):
        if matrice[i][i]<0:
            return False
    return True

def maxLen(matrice):
    maxi = 0
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if len(str(matrice[i][j])) > maxi:
                maxi = len(str(matrice[i][j]))
    return maxi

def printMatrice(matrice):
    maxi=maxLen(matrice)
    tailleFinale=maxi*len(matrice)+len(matrice)+2
    sommets=list(getSommets(arcs))
    for sommet in sommets:
        print(str(sommet).rjust(maxi), end=" ")
    print()
    print("-" * tailleFinale)
    for i in range(len(matrice)):
        print(sommets[i], end="")
        print("|", end="")
        for j in range(len(matrice[i])):

            print(str(matrice[i][j]).rjust(maxi), end="|")
        print()
        print("-" * tailleFinale)

def printTxt(matrice,graphe):
    with open("./graphes/"+graphe+"StackTrace.txt", "a") as f:
        print("Affichage de la matrice d'adjacence du graphe", file=f)
        maxi = maxLen(matrice)
        tailleFinale = maxi * len(matrice) + len(matrice) + 2
        sommets = list(getSommets(arcs))
        for sommet in sommets:
            print(str(sommet).rjust(maxi), end=" ", file=f)
        print(file=f)
        print("-" * tailleFinale)
        for i in range(len(matrice)):
            print(sommets[i], end="", file=f)
            print("|", end="", file=f)
            for j in range(len(matrice[i])):
                print(str(matrice[i][j]).rjust(maxi), end="|", file=f)
            print(file=f)
            print("-" * tailleFinale, file=f)
        print("Calcul puis affichage de la matrice apres l'algorithme de roy warshall", file=f)

nbSommets, nbArcs, arcs=read("test")
matrice=matriceAdjacence(arcs,nbSommets)
printMatrice(matrice)
printTxt(matrice,"test")
print(floydWarshall(matrice))