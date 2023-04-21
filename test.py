from génération_aléatoire import *
from graphe_from_tache import *
from ordo_from_tache import*
import time
from networkx.algorithms.flow import edmonds_karp
from statistics import *




def test(nb_test):

    li_li_tache = make_batch(nb_test,range_nb_tache=(100,100),range_deadline=(100,100),range_patwith=(4,4),range_slack=(50,50))
    li_tps=[]
    for i in range(nb_test):
        gen1 = li_li_tache[i]

        graphe1,source,puit = graphe_from_taches(gen1,2,print=False)

        tps1 = time.clock_gettime_ns(time.CLOCK_BOOTTIME)

        nx.maximum_flow(graphe1,source,puit,flow_func = edmonds_karp)

        tps2 =time.clock_gettime_ns(time.CLOCK_BOOTTIME)

        tps = ((tps2-tps1)/1000000)
        li_tps.append(tps)

    moy = mean(li_tps)
    med = median(li_tps)
    ecartType = pstdev(li_tps)
    variance = pvariance(li_tps)

    print("moy :",moy,"median :",med,"ecart type :",ecartType,"variance :",variance)

test(200)
