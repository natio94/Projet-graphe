def read(graphe):
    with open("./graphes/"+graphe+".txt", "r") as f:
        nbSommets=int(clean(f.readline()))
        nbArcs=int(clean(f.readline()))
        arcs=[]
        for i in range(nbArcs):
            arcs.append(process(clean(f.readline()).split(" ")))
    return nbSommets, nbArcs, arcs

def matriceAdjacence(arcs, nbSommets):
    matrice = [[0 for i in range(nbSommets)] for j in range(nbSommets)]
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


def maxLen(matrice):
    maxi = 0
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if len(str(matrice[i][j])) > maxi:
                maxi = len(str(matrice[i][j]))
    return maxi

def printMatrice(matrice):
    maxi=maxLen(matrice)
    tailleFinale=maxi*len(matrice)+len(matrice)+1
    print(" ", end="")
    sommets=list(getSommets(arcs))
    for sommet in sommets:
        print(str(sommet).rjust(maxi), end=" ")
    print()
    print(" ", end="")
    print("-" * tailleFinale)
    for i in range(len(matrice)):
        print(sommets[i], end="")
        print("|", end="")
        for j in range(len(matrice[i])):
            print(str(matrice[i][j]).rjust(maxi), end="|")
        print()
        print(" ", end="")
        print("-" * tailleFinale)
    
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
    return new_mat

nbSommets, nbArcs, arcs=read("test")
matrice=matriceAdjacence(arcs,nbSommets)
printMatrice(matrice)
print(floydWarshall(matrice))