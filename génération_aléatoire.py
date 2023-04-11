import copy
import random
import numpy as np
from graphe_from_tache import *

def print_tache(li_tache):
    print(len(li_tache))
    for i in range(len(li_tache)):
        ri,pi,di = li_tache[i]
        print("tache :",i,"ri=",ri," di=", di ,"pi=", pi)    

def tache_max_pathwidth(pathwith_max :int, nb_tache_max : int, deadline = 100,slack = 100) :
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
    j=0
    while (j <nb_tache_max) and (len(li_interval)>0) :
        #création de la tache j
        interval = random.randint(0,(len(li_interval)-1))
        min_date,max_date = li_interval[interval]
        ri_indice=0
        di_indice=0
        if((min_date+1)==max_date):
            ri_indice = min_date
            di_indice = max_date
            
        else:
            ri_indice = random.randint(min_date,(max_date-1))
            di_indice = random.randint((ri_indice+1),max_date)
        
        ri = li_date[ri_indice]
        di = li_date[di_indice]
        max_time = (di-ri)
        
        pi = max(random.randint(1,(max_time)),max_time-slack)
        
        ti = (ri,pi,di)
        li_tache = [ti]+li_tache
        
                
        
        #modification des intervals
        for i in range(ri_indice,di_indice):
            c_pw = li_pathwidth[i]
            li_pathwidth[i] = ( c_pw-1 )         #decrementation du nombre de tache possible a i
            if (li_pathwidth[i]<=0) :                   #si on atteint la limite
                debut,fin = li_interval[interval]
                
                nvl_interval_1 = (debut,i)              #on definit les deux nouvaux sous intervals
                nvl_interval_2 = (i+1,fin)
                
                
                if not(debut==i) and not(i+1 == fin) :  #si les deux sont valide on ajoute les deux
                    li_interval = li_interval[:interval] + [nvl_interval_1, nvl_interval_2] + li_interval[interval+1:]
                    interval = interval +1               #on incremente interval car on travail desormais dans le second interval
                    
                else:
                    if i+1 == fin :
                        nvl_d,nvl_f = nvl_interval_1
                        if nvl_d==nvl_f :
                            li_interval.remove(li_interval[interval]) 
                                                    
                        else :
                            li_interval[interval] = nvl_interval_1
                            
                    elif  (debut==i):
                        nvl_d,nvl_f = nvl_interval_2
                        if nvl_d==nvl_f :
                            li_interval.remove(li_interval[interval])
                            
                        else:
                            li_interval[interval] = nvl_interval_2  #si on ajoute juste un des deux on remplace l'interval d'indice interval
                        
                    
        j = j+1     
            
        
        
    
    return li_tache

    
def random_values(n,limite_max):
    l_values=[]
    r=0
    p=0
    d=0
    for i in range(n):
        d=random.randint(1, limite_max)
        p=random.randint(1, d)
        r=random.randint(0, d-p)
        l_values.append((r,p,d))
    #print(l_values)
    return l_values    

        


def get_details(li_tache):
    S = {}
    S=set(S)

    pathwidth_moy=0
    pathwidth_moy1=0
    nb_elem_pathwidth1=0    
    pathwidth_moy2=0
    nb_elem_pathwidth2=0    
    pathwidth_moy3=0
    nb_elem_pathwidth3=0    
    pathwidth_moy4=0
    nb_elem_pathwidth4=0    
    pathwidth_moy5=0
    nb_elem_pathwidth5=0    
    pathwidth_max=0

    slack_moy=0    
    slack_moy1=0
    nb_elem_slack1=0   
    slack_moy2=0
    nb_elem_slack2=0    
    slack_moy3=0
    nb_elem_slack3=0   
    slack_moy4=0
    nb_elem_slack4=0    
    slack_moy5=0
    nb_elem_slack5=0   
    slack_max=0

    for ri,pi,di in li_tache:#création liste intervalles
        S.add(ri)
        S.add(di)
        
    S = list(S)
    S = np.sort(S)
    
    
    
    for i in range(len(S)):#traitement du pathwidth
        pathwidth=0
        for ri,pi,di in li_tache:
            if (i<len(S)/5):
                nb_elem_pathwidth1+=1
            elif (i<2*len(S)/5):
                nb_elem_pathwidth2+=1
            elif (i<3*len(S)/5):
                nb_elem_pathwidth3+=1
            elif (i<4*len(S)/5):
                nb_elem_pathwidth4+=1
            elif (i<5*len(S)/5):
                nb_elem_pathwidth5+=1
            if not(ri>=S[i] or di<S[i]):#si la tache ne commmence pas après l'intervalle et ne se termine pas avant l'intervalle
                pathwidth_moy+=1
                pathwidth+=1
                if (i<len(S)/5):
                    pathwidth_moy1+=1
                elif (i<2*len(S)/5):
                    pathwidth_moy2+=1
                elif (i<3*len(S)/5):
                    pathwidth_moy3+=1
                elif (i<4*len(S)/5):
                    pathwidth_moy4+=1
                elif (i<5*len(S)/5):
                    pathwidth_moy5+=1

        if(pathwidth>pathwidth_max):
            pathwidth_max=pathwidth
    i=0
    for ri,pi,di in li_tache:#traitement du slack
        slack=di-(ri+pi)
        slack_moy+=slack
        if (i<len(li_tache)/5):
            slack_moy1+=slack
            nb_elem_slack1+=1
        elif (i<2*len(li_tache)/5):
            slack_moy2+=slack
            nb_elem_slack2+=1
        elif (i<3*len(li_tache)/5):
            slack_moy3+=slack
            nb_elem_slack3+=1
        elif (i<4*len(li_tache)/5):
            slack_moy4+=slack
            nb_elem_slack4+=1
        elif (i<5*len(li_tache)/5):
            slack_moy5+=slack
            nb_elem_slack5+=1

        if(slack>slack_max):
            slack_max=slack
        i+=1
    
    pathwidth_moy= pathwidth_moy / len(S)
    #pathwidth_moy1/=nb_elem_pathwidth1
    #pathwidth_moy2/=nb_elem_pathwidth2
    #pathwidth_moy3/=nb_elem_pathwidth3
    #pathwidth_moy4/=nb_elem_pathwidth4
    #pathwidth_moy5/=nb_elem_pathwidth5
    slack_moy= slack_moy/len(li_tache)
    #slack_moy1/=nb_elem_slack1
    #slack_moy2/=nb_elem_slack2
    #slack_moy3/=nb_elem_slack3
    #slack_moy4/=nb_elem_slack4
    #slack_moy5/=nb_elem_slack5

    print("pathwidth = ",pathwidth_max)
    print("slack = ",slack_max)
    print("pathwidth moyen",pathwidth_moy)
    print("slack moyen = ",slack_moy)
    print("nb taches :",len(li_tache))

    return pathwidth_max,slack_max


print("controlé :")
lt = tache_max_pathwidth(100,200,slack=12,deadline=1000)
get_details(lt)
#print_tache(lt)
#print("random :")
#lt2 = random_values(50,100)
#get_details(lt2)