import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def qparser(output):

    lines=output.splitlines()
     
    lines = [line.replace(',', '') for line in lines]
    lines = [line.replace('=', ',') for line in lines]
    lines = [line.replace(':', ', 0') for line in lines]
    lines = [line.replace(' million', '*10e6') for line in lines]
    
    field_list=[]
    values_list=[]

    for item in lines:
        field_list.append(item.split(",")[0])
        values_list.append(item.split(",")[1])
            
    for element in range(len(field_list)):
        field_list[element] = field_list[element].strip()
        
    for element in range(len(values_list)):
        values_list[element]=values_list[element].lstrip()
        values_list[element]=values_list[element].split(" ")[0]
    
    for v in range(len(values_list)):
        if "*10e6" in values_list[v]:
            temp=values_list[v].split("*")[0]
            values_list[v]=float(temp)*10e5
        
    udp_bw_indeces=[i for i, x in enumerate(field_list) if x == 'udp_bw']
    udp_lat_indeces=[i for i, x in enumerate(field_list) if x == 'udp_lat']
    
    bw_field_list_start=field_list[(udp_bw_indeces[0]+1):udp_lat_indeces[0]]
    lat_field_list_start=field_list[(udp_lat_indeces[0]+1):udp_bw_indeces[1]]
    
    for i in range(len(udp_bw_indeces)):
        if i!=0:
            bw_field_list=field_list[(udp_bw_indeces[i]+1):udp_lat_indeces[i]]
            if i!=len(udp_bw_indeces)-1:
                lat_field_list=field_list[(udp_lat_indeces[i]+1):udp_bw_indeces[i+1]]
            else:
                lat_field_list=field_list[(udp_lat_indeces[i]+1):]       
            missing_bw = set(bw_field_list).difference(bw_field_list_start)
            if list(missing_bw)!=[]:
                for m in range(len(list(missing_bw))):
                  bw_field_list_start.append(list(missing_bw)[m]) 
            missing_lat = set(lat_field_list).difference(lat_field_list_start)
            if list(missing_lat)!=[]:
                for m in range(len(list(missing_lat))):
                  lat_field_list_start.append(list(missing_lat)[m]) 
     
    
    bw_ind_start=[]
    lat_ind_start=[]
    bw_ind=[]
    lat_ind=[]
    
    for finder in bw_field_list_start:          
        bw_ind_start.append([i for i, x in enumerate(field_list) if x == finder])
    
    for d in range(len(bw_ind_start)):
        if len(bw_ind_start[d])>len(udp_bw_indeces):
            bw_ind.append(bw_ind_start[d][0::2])
        elif len(bw_ind_start[d])<len(udp_bw_indeces):
            tmp=[]
            for el in range(len(bw_ind_start[d])):
                tmp.append(bw_ind_start[d][el])
            for r in range(abs(len(tmp)-len(udp_bw_indeces))):
                tmp.append(0)
            for cycle in range(len(bw_ind_start[d])):
                if bw_ind_start[d][cycle]==bw_ind_start[d-1][cycle]+1:
                    tmp.append(0)
                else:
                    tmp.insert(cycle-1, 0)
            bw_ind.append(tmp)               
        else:
            bw_ind.append(bw_ind_start[d])
        
    for finder in lat_field_list_start:          
        lat_ind_start.append([i for i, x in enumerate(field_list) if x == finder])
        
    for d in range(len(lat_ind_start)):
        if len(lat_ind_start[d])>len(udp_lat_indeces):
            lat_ind.append(lat_ind_start[d][1::2])
        elif len(lat_ind_start[d])<len(udp_lat_indeces):
            tmp=[]
            for el in range(len(lat_ind_start[d])):
                tmp.append(lat_ind_start[d][el])
            for r in range(abs(len(tmp)-len(udp_lat_indeces))):
                tmp.append(0)
            for cycle in range(len(lat_ind_start[d])):
                if lat_ind_start[d][cycle]==lat_ind_start[d-1][cycle]+1:
                    tmp.append(0)
                else:
                    tmp.insert(cycle-1, 0)
            lat_ind.append(tmp)               
        else:
            lat_ind.append(lat_ind_start[d])
            
    bw_values_matrix=np.zeros([len(udp_bw_indeces), len(bw_field_list_start)])
    lat_values_matrix=np.zeros([len(udp_lat_indeces), len(lat_field_list_start)])
    
    for value in range(len(bw_field_list_start)):
        for each in range(len(udp_bw_indeces)):
            bw_values_matrix[each, value]=float(values_list[bw_ind[value][each]])
            
    for value in range(len(lat_field_list_start)):
        for each in range(len(udp_lat_indeces)):
            lat_values_matrix[each, value]=float(values_list[lat_ind[value][each]])
        
    df_bw = pd.DataFrame(bw_values_matrix, columns=bw_field_list_start)
    df_lat = pd.DataFrame(lat_values_matrix, columns=lat_field_list_start)
    
    df_bw.to_csv("qperf_bw.csv", index=False)
    df_lat.to_csv("qperf_lat.csv", index=False)  
    
    plt.plot(range(len(df_bw['send_bw'])), df_bw['send_bw']) 
    plt.xlabel("Run number")
    plt.ylabel("Bandwith [Gb/s]")
    plt.figure()
    plt.plot(range(len(df_lat['latency'])), df_lat['latency']) 
    plt.xlabel("Run number")
    plt.ylabel("Latency [us]")
                              



