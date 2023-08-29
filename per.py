 # -*- coding: utf-8 -*-
"""
Определение периода переменной звезды

файл -- юлианская дата \tab звёздная величина, два столбца без заголовка

"""

import matplotlib.pyplot as plt

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

def plot_maker(x, y, period):
      fig1 = plt.figure()
      graph = fig1.add_subplot(111)

      graph.set_title(f'Фазовая кривая блеска, P = {period}')
      graph.set_xlabel('Фаза')
      graph.set_ylabel('Звёздная величина')
      
      plt.scatter(x, y, color = 'black', s=10, marker='*')
      plt.show()
      
def minimum(values):   # нахождение минимальных элементов в списке
    global list_of_freq
    list_of_freq_copy = list_of_freq.copy()
   
    final_values = []
    for _ in range(3):
        min_elem = min(values)
        min_i = values.index(min_elem)
        final_values.append(list_of_freq_copy[min_i])
        values.remove(min_elem)
        list_of_freq_copy.remove(list_of_freq_copy[min_i])
        
    for i in range(len(final_values)):
        final_values[i] = 1 / final_values[i]
    return final_values    
        
# открытие файла    
data_file = open('datata.txt')
all_strs = data_file.read().splitlines()  # создание списка строк
data_file.close()

# список списков, каждый список - строка из данных:
for i in range(len(all_strs)):  
    all_strs[i] = all_strs[i].split() 
    
# изменение типа данных
for i in range(len(all_strs)):
    all_strs[i][0] = float(all_strs[i][0])
    all_strs[i][1] = float(all_strs[i][1])

main_list = all_strs    
# вычисления фазы с исходным периодом

period_min = 0.15
period_max = 0.3
d_per = 0.001  # шаг по периоду, он не нужен
d_freq = 0.0005
#JD0 =  2446708.7712  # начальная эпоха 
JD0 =  main_list[0][0]  # начальная эпоха 
M = 15 # для фазовой группировки данных, разбиение блабла
num = int(len(main_list) / M) # число точек в одном элементе

# переход к частотам

freq_min = 1 / period_max
freq_max = 1 / period_min
freq = freq_min

list_of_ilk = []  # статистика Лафлера-Кинмана для каждой частоты
list_of_ipg = []  # статистика для метода фазовой группировки
list_of_freq = []  # список с используемыми частотами

while freq < freq_max:  # общий цикл, проходится по всем значениям частоты

    phases = []  # список только из фаз, нужен для сортировки
    
# вычисление фаз, добавление третьим элементом в главный список и во вспомогательный 
    for i in range(len(main_list)):  
        ph = (main_list[i][0] - JD0) * freq - int((main_list[i][0] - JD0) * freq)
        main_list[i].append(ph)
        phases.append(ph)
    phases.sort()

    sorted_main_list = [0]*len(main_list) # здесь элементы будут сорт. по фазе
    for i in range(len(phases)): 
        for j in range(len(main_list)):
            if phases[i] == main_list[j][2]:
                sorted_main_list[i] = main_list[j]
                continue  
    
    
    for i in range(len(main_list)):
        del main_list[i][2]
        
    # метод Л-К
    ilk = 0
    for i in range(len(sorted_main_list) - 1):
        ilk += (sorted_main_list[i+1][1] - sorted_main_list[i][1]) ** 2
    
    # метод фазовой группировки
    ipg = 0
    for i in range(M):
        all_dots = sorted_main_list[i * num : (i + 1) * num]        
        dots = []
        for j in range(len(all_dots)):
            dots.append(all_dots[j][1])
        ipg += variance(dots)
        
        
    list_of_freq.append(freq)
    list_of_ilk.append(ilk)
    list_of_ipg.append(ipg)
    freq += d_freq

#print(list_of_freq)

finals_ilk = minimum(list_of_ilk)
finals_ipg = minimum(list_of_ipg)

print(finals_ilk)
print(finals_ipg)
print(M, d_freq)
'''
# нахождение минимальных элементов
final_values = []
for _ in range(5):
    min_ilk = min(list_of_ilk)
    min_i = list_of_ilk.index(min_ilk)
    final_values.append(list_of_freq[min_i])
    list_of_ilk.remove(min_ilk)
    list_of_freq.remove(list_of_freq[min_i])
    
for i in range(len(final_values)):
    final_values[i] = 1 / final_values[i]
    
print(final_values)
'''
''' построение графиков '''
# метод 1
for i in range(len(finals_ilk)):
    for j in range(len(main_list)):
        ph = (main_list[j][0] - JD0) / finals_ilk[i] - int((main_list[j][0] - JD0) / finals_ilk[i])
        main_list[j].append(ph)
    x_ax = []
    y_ax = []

    for j in range(len(main_list)):
        
        x_ax.append(main_list[j][2])
        y_ax.append(main_list[j][1])
    plot_maker(x_ax, y_ax, finals_ilk[i])
    
    for i in range(len(main_list)):
        del main_list[i][2]
# метод 2       
for i in range(len(finals_ipg)):
    for j in range(len(main_list)):
        ph = (main_list[j][0] - JD0) / finals_ipg[i] - int((main_list[j][0] - JD0) / finals_ipg[i])
        main_list[j].append(ph)
    x_ax = []
    y_ax = []

    for j in range(len(main_list)):
        
        x_ax.append(main_list[j][2])
        y_ax.append(main_list[j][1])
    plot_maker(x_ax, y_ax, finals_ilk[i])
    
    for i in range(len(main_list)):
        del main_list[i][2]        
