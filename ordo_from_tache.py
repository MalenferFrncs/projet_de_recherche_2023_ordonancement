#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:44:55 2023

@author: 28706664
"""

"""
on prend en entré une une liste de triple (ri,pi,qi) et on retourne un ordonancement

"""
#import networkx as nx
import copy
import random
import numpy as np
#import matplotlib.pyplot as plt
from graphe_from_tache import *

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
    print(l_values)
    return l_values

def tri_liste(li):
    ordre=[0]*len(li)
    for i in range(len(li)):
        ordre[i]=i
    #source:https://stackoverflow.com/questions/13979714/heap-sort-how-to-sort
    def swap(i, j):                    
        li[i], li[j] = li[j], li[i] 
        ordre[i], ordre[j] = ordre[j], ordre[i]

    def heapify(end,i):   
        l=2 * i + 1  
        r=2 * (i + 1)   
        max=i   
        if l < end and li[i][2] < li[l][2]:   
            max = l   
        if r < end and li[max][2] < li[r][2]:   
            max = r   
        if max != i:   
            swap(i, max)   
            heapify(end, max)   

    def heap_sort():     
        end = len(li)   
        start = end // 2 - 1 # use // instead of /
        for i in range(start, -1, -1):   
            heapify(end, i)   
        for i in range(end-1, 0, -1):   
            swap(i, 0)   
            heapify(i, 0)
    
    def sift_down(start, end):         
        root = start                   

        while (root * 2 + 1) <= end:   
            child = root * 2 + 1       
            temp = root                
            if li[temp] < li[child]: 
                temp = child+1         
            if temp != root:           
                swap(root, temp)       
                root = temp            
            else:                      
                return
    heap_sort()
    # print(li)
    return li,ordre

def ordo_from_tache(li,m :int,G):#return un résiduel(graphe de avec des valeurs de flow)
    ordo_fontionnel=True
    node_pos_G=copy.deepcopy(nx.get_node_attributes(G,'pos'))
    arc_capacity_G=copy.deepcopy(nx.get_edge_attributes(G,'capacity'))
    nx.draw_networkx_edges(G, node_pos_G,edge_color= "black")
    nx.draw_networkx_edge_labels(G, node_pos_G, edge_labels=arc_capacity_G,label_pos=0.7)
    li_trie,ordre=tri_liste(li)#trie nos tâches par ordre croissant des deadlines
    R = G # résiduel retourné
    arretes_de_bases=list(G.edges)  #on save les arrêtes du début
    capacity_de_bases=list(G.edges.data('capacity'))
    usage=len(capacity_de_bases)*[0]    #controlleur de surcharge sur les dernières arretes
    nb_nodes=R.number_of_nodes()
    for noeud1 in range(len(li_trie)):  #on enlève juste les arrêtes qui sont au millieu
        for noeud2 in range(nb_nodes-2-len(li_trie)):
            if((noeud1+1, noeud2+1+len(li_trie)) in list(G.edges)):
                R.remove_edge(noeud1+1, noeud2+1+len(li_trie))
    for i in range(len(li_trie)):   #on parcours toutes les tâches
        for j in range(len(li_trie)): #on parcours toutes les tâches
            if(ordre[j]==i):    #si je suis sur le noeud que je dois traiter (par ordre de priorite sur la deadline)
                qt_flot=G[0][j+1]["capacity"]
                for intervalle in range(nb_nodes-2-len(li_trie)):   #on parcours les intervalles
                    intervalle_pos=intervalle+len(li_trie)+1
                    arrete_dest=0
                    for a in range(len(capacity_de_bases)): #on cherche l'arrete qui est derrière
                        if((capacity_de_bases[a][0]==intervalle_pos and capacity_de_bases[a][1]==nb_nodes-1)or(capacity_de_bases[a][1]==intervalle_pos and capacity_de_bases[a][0]==nb_nodes-1)):
                            arrete_dest=a
                    if(((j+1,intervalle_pos) in arretes_de_bases) and qt_flot>0 and capacity_de_bases[arrete_dest][2]-usage[arrete_dest]>0):   #si l'arrête existe et que il nous reste du flot et que 'arrête suivante n'est pas déjà surchargée
                        for arrete_act in capacity_de_bases:
                            if(j+1==arrete_act[0] and intervalle_pos==arrete_act[1]):   #on cherche ici à obtenir la capacity de notre arrete
                                new_cap=min(arrete_act[2], qt_flot, capacity_de_bases[arrete_dest][2]-usage[arrete_dest])  #on calcule alors le flot qui va aller dans cette arrete
                                usage[arrete_dest]+=new_cap   #on met à jour le controlleur
                                print(j+1,intervalle_pos," : ",new_cap)
                                R.add_edge(j+1, intervalle_pos, capacity=new_cap) #on envoi tt la capacité ou le flot qu'il nous reste ou suffisament pour remplir l'arrête suivante
                                qt_flot-=new_cap    #on met à jour notre flot restant
                if (qt_flot>0): #si on à pas réussi à vider le flot alors ça ne fonctionne pas et on rajoute une croix rouge
                    # source : https://www.includehelp.com/python/cross-x-scatter-marker-in-matplotlib.aspx
                    x,y=node_pos_G[j+1]
                    ss = 200
                    c = 1
                    plt.scatter(x/2,y/2, s=ss, c=c, marker='X', cmap='Reds_r')
                    ordo_fontionnel=False
    if(ordo_fontionnel):
        print("ordo fonctionnel")
    else:
        print("ordo non fonctionnel")
    #source : http://avinashu.com/tutorial/pythontutorialnew/NetworkXBasics.html
    node_pos=nx.get_node_attributes(R,'pos')
    # The edge capacitys of each arcs are stored in a dictionary
    arc_capacity=nx.get_edge_attributes(R,'capacity')
    # If the nodes is in the shortest path, set it to red, else set it to white color
    node_col = 'white'
    # If the edge is in the shortest path set it to red, else set it to white color
    edge_col = 'blue'
    # Draw the nodes
    nx.draw_networkx(R, node_pos,node_color= node_col, node_size=450)
    # Draw the edges
    nx.draw_networkx_edges(R, node_pos,edge_color= edge_col)
    # Draw the edge labels
    nx.draw_networkx_edge_labels(R, node_pos, edge_labels=arc_capacity,label_pos=0.7,font_color='red')
    # Remove the axis
    plt.axis('off')
    # Show the plot
    plt.show()
    return R
# lt=[(0,4,4),(0,3,8),(0,5,9)]
lt=[(3, 2, 7), (3, 2, 5), (1, 3, 5)]
#lt=random_values(3,10)
G,s,t=graphe_from_taches(lt,2)
ordo_from_tache(lt,2,G)