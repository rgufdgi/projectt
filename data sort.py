# task 2
data_file = open('task2_data.dat')

all_strs = data_file.read().splitlines()  # создание списка строк

# список списков, каждый список - строка из данных:
for i in range(len(all_strs)):  
    all_strs[i] = all_strs[i].split() 

# исправление первой строки   
all_strs[0] = ['Object', 'HJD, 24...', 'Filter', 'Magnitude']

# удаление пустых элементов
while [] in all_strs:
    all_strs.remove([])
    
# исправление названий звёзд

# был пробел в названии:
for i in range(1, len(all_strs)):
    if len(all_strs[i]) > 4:
        all_strs[i][0] = all_strs[i][0].upper() \
            + '_' + all_strs[i][1].capitalize()
        del all_strs[i][1]


# нет нижнего подчеркивания в названии:
for i in range(1, len(all_strs)):
    if '_' not in all_strs[i][0]:
        all_strs[i][0] = all_strs[i][0][:2].upper() \
            + '_' + all_strs[i][0][2:].capitalize()

# исправление названий фильтров
for i in range(1,len(all_strs)):
    if all_strs[i][2][0].islower() == True:
        all_strs[i][2] = all_strs[i][2].capitalize()

# изменение типа данных числовых значений       
for i in range(1,len(all_strs)):
    all_strs[i][1] = float(all_strs[i][1])
    all_strs[i][3] = float(all_strs[i][3])
    
names_list = []  #список имён объектов
for i in range(1, len(all_strs)):
    if all_strs[i][0] not in names_list:
        names_list.append(all_strs[i][0])

# вывод имён объектов
print('Имена объектов:')
for i in range(len(names_list)):      
    print(names_list[i]) 
print()

def available_filters(name, data_list):
    filter_list = []
    for i in range(1, len(data_list)):
        if data_list[i][0] == name and data_list[i][2] not in filter_list:
            filter_list.append(data_list[i][2])
    return filter_list

# вывод фильтров
for i in range(len(names_list)):
    print(f'Объект {names_list[i]} доступен в следующих фильтрах:')
    current_filters_list = available_filters(names_list[i], all_strs)
    for j in range(len(current_filters_list)):
        print(current_filters_list[j])
    print()

# сортировка данных по юлианским датам 
JD_list = []
for i in range(1, len(all_strs)):
    JD_list.append(all_strs[i][1])

JD_list.sort()
JD_list.insert(0, 'JD, 24')

sorted_data_list = [0] * len(all_strs)
sorted_data_list[0] = all_strs[0]

all_strs_copy = all_strs.copy()
for i in range(1, len(JD_list)):
    for j in range(1, len(all_strs)):
        if JD_list[i] == all_strs_copy[j][1]:
            sorted_data_list[i] = all_strs_copy[j]
            continue
      
#for i in range(len(sorted_data_list)):
 #   print(sorted_data_list[i])
""" 
star_name = input('Введите имя объекта: ')

if star_name not in names_list:
    print('Нет данных для этого объекта')
    star_name = input('Введите имя объекта: ')
"""


 
































