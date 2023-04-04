import copy
import random
import numpy as np
from graphe_from_tache import *

def tache_max_pathwidth(pathwith_max :int, nb_tache_max : int, deadline = 100) :
    #initialisation
    
    li_date = {}
    li_date = set(li_date)          # evite les duplicata
    for i in range(nb_tache_max*2):
        li_date.add( random.randint(0,(deadline-1) ))
        
        
        
    li_date = list(li_date)         # permet d'avoir les dates ordonnées
    li_date = np.sort(li_date)      #trie les dates
    nb_date = len(li_date)          # permet de connaitre le nombre de date
    
    
    
    #initialise la liste qui permet de definir si on atteint la largeur max
    li_pathwidth = []
    for i in range(nb_date-1) :              
        li_pathwidth = [pathwith_max]+li_pathwidth
        
    #initialise la liste des intervales (au debut 1 intervalle de 0 a nb_date)
    li_interval = [(0,nb_date-1)]
    
        
    #debut de la creation des taches
    li_tache = []
    for i in range(nb_tache_max) :
        #création de la tache i
        interval = random.randint(0,(len(li_interval)-1))
        min_date,max_date = li_interval[interval]
        
        ri_indice = random.randint(min_date,(max_date-1))
        di_indice = random.randint((ri_indice+1),(max_date))
        
        ri = li_date[ri_indice]
        di = li_date[di_indice]
        max_time = (di-ri)
        
        pi = random.randint(1,(max_time))
        
        ti = (ri,pi,di)
        li_tache = [ti]+li_tache
        
        #modification des intervals
        for i in range(ri_indice,di_indice-1):
            c_pw = li_pathwidth[i]
            li_pathwidth[i] = ( c_pw-1 )         #decrementation du nombre de tache possible a i
            if (li_pathwidth[i]==0) :                   #si on atteint la limite
                debut,fin = li_interval[interval]
                
                nvl_interval_1 = (debut,i)              #on definit les deux nouvaux sous intervals
                nvl_interval_2 = (i+1,fin)
                
                
                if not(debut==i) and not(i+1 == fin) :  #si les deux sont valide on ajoute les deux
                    li_interval = li_interval[:interval] + [nvl_interval_1, nvl_interval_2] + li_interval[interval+1:]
                    interval = interval+1               #on incremente interval car on travail desormais dans le second interval
                    
                else:
                    if i+1 == fin:
                        li_interval[interval] = nvl_interval_1
                    else:
                        li_interval[interval] = nvl_interval_2  #si on ajoute juste un des deux on remplace l'interval d'indice interval
                
            
        
        
    
    return li_tache

    
    
def print_tache(li_tache):
    print(len(li_tache))
    for i in range(len(li_tache)):
        ri,pi,di = li_tache[i]
        print("tache :",i,"ri=",ri," di=", di ,"pi=", pi)    
        

print_tache(tache_max_pathwidth(4,10))