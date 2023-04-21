from génération_aléatoire import *
from graphe_from_tache import *
from ordo_from_tache import*
import time
from networkx.algorithms.flow import edmonds_karp
from statistics import *




def test(nb_test,pathwidth,slack,opt):

    li_li_tache = make_batch(nb_test,range_nb_tache=(1000,1000),range_deadline=(1000,1000),range_patwith=(pathwidth,pathwidth),range_slack=(slack,slack))
    li_tps=[]
    li_nb = []
    for i in range(nb_test):
        gen1 = li_li_tache[i]

        graphe1,source,puit = graphe_from_taches(gen1,2,print=False)

        
        if(opt):
            graphe1 = ordo_from_tache(gen1,2,graphe1,pri=False)

        
        tps1 = time.clock_gettime_ns(time.CLOCK_BOOTTIME)
        nx.maximum_flow(graphe1,source,puit,flow_func = edmonds_karp)

        tps2 =time.clock_gettime_ns(time.CLOCK_BOOTTIME)

        tps = ((tps2-tps1)/1000000)
        li_tps.append(tps)
        nb,p,s = get_details(gen1)
        li_nb.append(nb)

    moy = mean(li_tps)
    med = median(li_tps)
    ecartType = pstdev(li_tps)
    variance = pvariance(li_tps)

    moy_nb = mean(li_nb)

    print("nombre moyen de taches :",int(moy_nb),", temps en ms moy :",int(moy),"ms, ratio : ",(moy/moy_nb),"mediane :",int(med),"ms, ecart type :",int(ecartType),"ms, variance :",int(variance),"ms")

test(200,1,1,False)
test(200,2,1,False)
test(200,4,1,False)
test(200,8,1,False)
test(200,16,1,False)
test(200,32,1,False)
test(200,64,1,False)
test(200,128,1,False)


