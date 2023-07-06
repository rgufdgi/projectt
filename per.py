# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:01:24 2023

@author: Александра
"""
def variance(data): 
    # Number of observations 
    n = len(data) 
    # Mean of the data 
    mean = sum(data) / n 
    # Square deviations 
    deviations = [(x - mean) ** 2 for x in data] 
    # Variance 
    variance = sum(deviations) / n 
    return variance 
 
data_file = open('datata.txt')
all_strs = data_file.read().splitlines()  # создание списка строк
data_file.close()

# список списков, каждый список - строка из данных:
for i in range(len(all_strs)):  
    all_strs[i] = all_strs[i].split() 
    
# тип данных
for i in range(len(all_strs)):
    all_strs[i][0] = float(all_strs[i][0])
    all_strs[i][1] = float(all_strs[i][1])
    
# вычисления фазы с исходным периодом

period = 0.15
period_max = 0.25
d_per = 0.01
JD0 =  2446708.7712
N_E = 20
disper_list = []  # список с фазами

for i in range(len(all_strs)):
    disper_list.append(all_strs[i][0])

magnitudes = []  # список со звёздными величинами
for i in range(len(all_strs)):
    magnitudes.append(all_strs[i][1])

for i in range(len(all_strs)):
    disper_list[i] = [disper_list[i]]
#print(disper_list)

for i in range(len(disper_list)):
    disper_list[i].append(magnitudes[i])
    
period_list = []
main_list = []
second_square = variance(magnitudes)
while period < period_max:
    E = 0
    new_list = []
    list_of_var = []
    for i in range(len(all_strs)):
        new_elem = (all_strs[i][0] - JD0) / period - int((all_strs[i][0] - JD0) / period)
        new_list.append(new_elem)
    for i in range(len(new_list)):
        disper_list[i].append(new_list[i])
    # сортировка по фазам
    new_list.sort()
    sorted_disper_list = [0]*len(disper_list) 
    for i in range(len(disper_list)):
        for j in range(1, len(disper_list)):
            if new_list[i] == disper_list[j][2]:
                sorted_disper_list[i] = disper_list[j]
                continue
    sorted_disper_list.remove(0)
    num = int(len(sorted_disper_list) / N_E)  # число значений в отрезке фазы
    counter = num
    var_list = []
    while counter < len(sorted_disper_list):
        magnitude_list = []
        for i in range(counter + 1):
            magnitude = sorted_disper_list[i][1]
            magnitude_list.append(magnitude)
        first_square = 0
        
        for i in range(num):
            first_square += (magnitude_list[i + 1] - magnitude_list[i]) ** 2
        disper = first_square / second_square
        var_list.append(disper)
        counter += num
    main_list.append(sum(var_list))
    period_list.append(period)
    for i in range(len(disper_list)):
        disper_list[i].pop(2)   
    period += d_per
    #print(var_list)
    #print(len(var_list))
print(main_list)
print(period_list)
for i in range(len(main_list)):
    if main_list[i] == min(main_list):
        index = i
        break
print(period_list[index])        
print(len(main_list))
print(len(period_list))
print(index)


    