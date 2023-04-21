#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:01:16 2023

@author:   28706664
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

""" 
on definit une fonction graphe_from_taches qui prend en entrée les taches et le nombre de machine m un entier

les tâches sont representées par une liste de tuple [(r1,p1,d1),...,(rn,pn,dn)]

on retourne une structure de données (G,s,t) qui correspond à un graphe de flot pour networkX 

"""

# : list[tuple]

def graphe_from_taches(li,m :int,deadline = True,print=True) :
    G = nx.Graph() # graphe de flot retourné
    i = 0  # état de depart
    
    G.add_node(i)

    S = {}  # listes des moments importants (release et deadline) (representés dans un set pour ne pas avoir de doublons)
    S=set(S)    #sinon il pense que c'est un dictionnaire
    
       
    for t in li :
        i=i+1 
        G.add_node(i) # création d'un nouveau noeud (correspondant à une tâche)

        ri,pi,di = t # extraction des informations importantes sur les tâches

        S.add(ri) 
        if(deadline): 
            S.add(di)  # ajout des deux dates (releases et deadline a la liste des dates)

        G.add_edge(0,i,capacity=pi) # ajout d'une arête entre le sommet initial (sommet 0) et le sommet qui represente la tache courante (sommet i), la capacité est representé par capacity et correspond au processing time de la tache 
        
    nb_taches = i # nombre de taches

    l_date = (list(S)) # on transforme le set en liste car on a plus de problèmes de doublons et on veut pouvoir trier les elements dans un ordre précis

    puit = len(l_date)+nb_taches  # on definit un entier puit qui correspond au dernier sommet du graphe (celui vers lequel les sommets representant les intervalles de temps sont reliés) 
                          # (sa valeur est le nombre d'intervalles + le nombre de tache +1 ) le nombre d'intervalles est le nombre de dates importantes dans la liste -1 cad len(l_date)-1

    G.add_node(puit)    # on ajoute un nouveau sommet d'indice puit
    
    l_date_trie = np.sort(l_date) # on trie la liste des dates importantes dans l'ordre croissant pour obtenir les intervales d'interêt (soit [i,i+1] un intervalle pour tout i de 0 a len-1 )
    
    for k in range(len(l_date_trie)-1):
        i+=1
        G.add_node(i)    # on ajoute/créé un sommet d'indice/d'indentifiant correspondant a l'intervalle courant
        G.add_edge(i,puit,capacity=((l_date_trie[k+1]-l_date_trie[k])*m) )  # on ajoute l'arête qui va de notre intervalle a notre etat final puit sa capacité depend de l'intervalle et du nombre de processeurs de la machine
        
    tache_courante = 1 


    while tache_courante <= nb_taches :

        ri,pi,di = li[tache_courante-1]  # on extrait les valeurs de la tache courante
        
        k = 0


        while not( l_date_trie[k] == ri ) : # tant qu'on à pas atteint les dates a partir desquelles on peut lancer l'éxecution de la tâche courante
            k += 1
        # à la sortie de la boucle k est l'indice de ri dans l_date_trie, l'indice du sommet correspondant a l'intervalle [k,k+1] est nb_taches + k


        while (not( (l_date_trie[k] == di) and deadline )) and (k<len(l_date_trie)) : #tant qu'on a pas atteint la fin de l'intervalle sur laquelle la tâche courante peut s'executer ou la fin du tableau
            G.add_edge(tache_courante,(nb_taches+k+1),capacity=(l_date_trie[k+1]-l_date_trie[k])) #on ajoute l'arête de tâche courante a l'intervalle courant et de poids durée de l'intervalle courant
            k += 1
        tache_courante += 1
    if(print):
        #on définit les positions des noeuds
        G.nodes[0]['pos'] = (0,0)
        for i in range(nb_taches):
            G.nodes[1+i]['pos'] = (2,nb_taches-i*2-1)
        for i in range(len(l_date_trie)-1):
            G.nodes[1+nb_taches+i]['pos'] = (5,(len(l_date_trie)-1)-i*2-1)
        G.nodes[puit]['pos'] = (7,0)
        # #source : http://avinashu.com/tutorial/pythontutorialnew/NetworkXBasics.html
        node_pos=nx.get_node_attributes(G,'pos')
        # The edge capacitys of each arcs are stored in a dictionary
        arc_capacity=nx.get_edge_attributes(G,'capacity')
        # If the nodes is in the shortest path, set it to red, else set it to white color
        node_col = 'white'
        # If the edge is in the shortest path set it to red, else set it to white color
        edge_col = 'black'
        # Draw the nodes
        nx.draw_networkx(G, node_pos,node_color= node_col, node_size=450)
        # Draw the node labels
        # nx.draw_networkx_labels(G, node_pos,node_color= node_col)
        # Draw the edges
        nx.draw_networkx_edges(G, node_pos,edge_color= edge_col)
        # Draw the edge labels
        nx.draw_networkx_edge_labels(G, node_pos, edge_labels=arc_capacity,label_pos=0.7)
        # Remove the axis
        plt.axis('off')
        # Show the plot
        plt.show()
    return (G,0,puit)

#test = graphe_from_taches([(0,2,2),(0,3,4),(2,2,4)],2)