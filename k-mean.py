# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:22:54 2020

@author: mahmoud saeed
"""
import pandas as pd
import numpy as np
##-------------------------------------- get distance by manhattan
def manhattan_distance(data , centroid):
    sum = 0
    for i in range(0,len(data)):
        sum += abs(data[i]-centroid[i])
    return sum
##--------------------------------------asign new cluster
def assign_cluster(distance, data):
    index_of_minimum = min(distance, key=distance.get)
    return [index_of_minimum, data]
##----------------------------------------check equality of two list
def check_equality(new_list , old_list):
    for i in range(len(new_list)):
        if(new_list[i] != old_list[i]):
            return False
    return True    
##------------------------------------------ print groups
def print_groups(groups , length):
    for i in range(length):
        group = groups[groups["group"]==i]
        group = group["data"]
        print("groub number",i+1,"\n")
        for j in group:
            print(j[0])
        print("------------")    
##-----------------------------------------make new centroid        
def consider_new_centroid(centroid_list , length , index):
    new_centroid = []
    for i in range(length):
        nn = centroid_list[centroid_list["group"]==i]
        nn = nn["data"]
        l = []
        for j in range(1,32):
            s = []
            [s.append(k[j]) for k in nn]
            s = float(format(np.sum(s)/len(s),'.1f'))
            l.append(s)
        new_centroid.append(l)
    new_centroid = pd.DataFrame(new_centroid,columns = index)    
    return new_centroid
##-------------------------------------- check cluster        
def check_cluster(course_data ,old_list , new_list , length):
    index = course_data.columns
    ## first iteration only
    if(len(old_list) == 0):
        new_centroid = consider_new_centroid(new_list, length , index[1:])
        K_mean(course_data,new_centroid,new_list)
    ## else (not first iteration)
    else:
        if(check_equality(new_list["group"], old_list["group"])):
            print_groups(new_list, length)
        else:
            new_centroid = consider_new_centroid(new_list, length , index[1:])
            K_mean(course_data,new_centroid,new_list)
##-------------------------------------- K-mean function            
def K_mean(course_data , centroids , old_list):
    new_list = []
    new_centroids = []
    for i in range(len(course_data)):
        distance = {}
        for j in range(len(centroids)):
            distance[j] = manhattan_distance(course_data.iloc[i][1:] , centroids.iloc[j])
        l = assign_cluster(distance, course_data.iloc[i])    
        new_list.append(l)
    new_list = pd.DataFrame(new_list , columns = ["group","data"])
    check_cluster(course_data ,old_list, new_list, len(centroids))
##-------------------------------------------- main function    
if __name__ == '__main__':
    print("hellow to our program")
    course = pd.read_excel("Sales.xlsx")
    K = int(input("write number of cluster(K)\n"))
    n = len(course)//K
    l = []
    for i in range(0,K):
        l.append(course.iloc[i*n][1:])    
    l = pd.DataFrame(l)  
    print("prgram start please wait the result\n \n")        
    K_mean(course,l,[])    
   
        
        
        
        
        
        
        
        
        
        
        