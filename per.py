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
d_freq = 0.005
#JD0 =  2446708.7712  # начальная эпоха 
JD0 =  main_list[0][0]  # начальная эпоха 
N_E = 30 # для фазовой группировки данных, разбиение блабла


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
    
    
    list_of_freq.append(freq)
    list_of_ilk.append(ilk)
    
    freq += d_freq

print(list_of_freq)
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

''' построение графиков '''

for i in range(len(final_values)):
    for j in range(len(main_list)):
        ph = (main_list[j][0] - JD0) / final_values[i] - int((main_list[j][0] - JD0) / final_values[i])
        main_list[j].append(ph)
    x_ax = []
    y_ax = []

    for j in range(len(main_list)):
        
        x_ax.append(main_list[j][2])
        y_ax.append(main_list[j][1])
    plot_maker(x_ax, y_ax, final_values[i])
    
    for i in range(len(main_list)):
        del main_list[i][2]
'''
fig1 = plt.figure()
graph = fig1.add_subplot(111)

graph.set_title(f'Фазовая кривая блеска, P = {final_values[0]}')
graph.set_xlabel('Фаза')
graph.set_ylabel('Звёздная величина')
#graph.set_xlim([x1 - 1, x2])

#graph.set_xticks([_ for _ in range(x1, x2, 2)] )
plt.scatter(pixels_hor, light_hor, color = 'black', s=10, marker='*')
plt.show()
  ''' 
''' зачем я вообще написала этот кусок
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
    
print(disper_list) 
'''

"""    
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
"""

    