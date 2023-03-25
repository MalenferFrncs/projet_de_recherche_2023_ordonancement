from graphe_from_tache import *
from ordo_from_tache import *
from networkx.algorithms.flow import edmonds_karp

def binary_search(lt , m,  dl):     
    #lt : liste de transition
    #m : minimum 
    #dl : deadline initial

    pi_total = 0    
    for _,pi,_ in lt :         #calcule la somme des temps de calcule 
        pi_total = pi_total + pi


    def modif_deadline(lt,new_dl):
        new_lt = []
        for ri,pi,di in lt :
            if (di>new_dl):
                new_lt = new_lt+[(ri,pi,new_dl)]  #retourne une nouvelle listes ou les deadlines des
            else :                                 # taches sont remplacé par la noouvel dl de l'ordo
                new_lt = new_lt + [(ri,pi,di)]
        return new_lt

    def test (max_dl) :
        # fonction qui test si l'ordo avec max_dl comme date limite

        new_lt = modif_deadline(lt,max_dl)
        G,source,puit = graphe_from_taches(new_lt,m) #crée le graphe
        R = ordo_from_tache(new_lt,m,G) #trouve une 1er solution
        res_v,rest_d = nx.maximum_flow(G,source,puit,flow_func = edmonds_karp, residual = R) #cherche le flôt max 
        if(res_v >= pi_total): # test si l'ordo est valide
            return True
        return False

    min_dl = dl
    max_dl = pi_total

    while not(min_dl==max_dl):
        new_dl = (min_dl + max_dl)/2 #on teste une valeur entre min et max
        # max est toujours une deadline réalisable, on ne sais pas si min est realisable
        if(test(new_dl)):
            max_dl = new_dl # si valeur valide alors max = valeur
        else :
            if(min_dl==new_dl):
                return max_dl
            min_dl = new_dl #si valeur invalide alors min = valeur

    return max_dl

    