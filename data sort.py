# task 2
data_file = open('task2_data.dat')
all_strs = data_file.read().splitlines()  # создание списка строк
data_file.close()

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
    all_strs[i][1] = '24' + all_strs[i][1]
    all_strs[i][1] = float(all_strs[i][1])
    #all_strs[i][3] = float(all_strs[i][3])
    
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
    print(*current_filters_list)
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
     
    
# список для конкретного объекта
star_name = input('Введите имя объекта: ')
# проверка правильности вводимых данных
if star_name not in names_list:
    print('Нет данных для этого объекта')
    star_name = input('Введите имя объекта: ')

star_list = []
for i in range(1, len(sorted_data_list)):
    if sorted_data_list[i][0] == star_name:
        star_list.append(sorted_data_list[i])
        
# конкретные фильтры
all_filters = available_filters(star_name, star_list)
filters = input('Введите названия фильтров, через пробел: ').split()
# проверка правильности вводимых данных
if len(filters) > 1:
    for i in range(len(filters)):
        if filters[i] not in all_filters:
            print('Нет данных для этих фильтров')
            print('Доступные фильтры: ')
            print(*all_filters)
            filters = input('Введите названия фильтров, через пробел: ').split()
else:
    if filters[0] not in all_filters:
        print('Нет данных для этих фильтров')
        print('Доступные фильтры: ')
        print(*all_filters)
        filters = input('Введите названия фильтров, через пробел: ').split()
        
almost_final_list = []  # список для данной звезды с данными фильтрами
for i in range(len(star_list)):
        if star_list[i][2] in filters:
            almost_final_list.append(star_list[i])
            
def Date_and_time(JD):  # перевод юлианской даты в григорианскую, UT
    JDN = int(JD)
    a = JDN + 32044
    b = (4*a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4*c + 3) // 1461
    e = c - 1461*d //4
    m = (5 * e + 2)//153
    day = e + 1 - (153 * m + 2) // 5
    month = m + 3 - 12 * (m // 10)
    year = 100*b + d - 4800 + m // 10
    Jtime = JD - JDN
    hour = int(Jtime * 24)
    minute = int((Jtime*24 - hour) * 60)
    second = round(((Jtime*24 - hour) * 60 - minute) * 60)
    hour +=12
    if hour > 24:
        hour -= 24
        day += 1
    if len(str(hour)) == 1:
        hour = f'0{str(hour)}'
    if len(str(minute)) == 1:
        minute = f'0{str(minute)}' 
    if len(str(second)) == 1:
        second = f'0{str(second)}'
    if len(str(day)) == 1:
        day = f'0{str(day)}'   
    if len(str(month)) == 1:
        month = f'0{str(month)}'        
    date_and_time = f'{day}.{month}.{year} {hour}:{minute}:{second}'
    return date_and_time

usual_date = []

for i in range(len(almost_final_list)):
    usual_date_elem = Date_and_time(almost_final_list[i][1])
    usual_date.append(usual_date_elem)
    
# преобразование юлианского дня к красивому виду    
for i in range(len(almost_final_list)):
    num = len(str(almost_final_list[i][1]))
    if num != 13:
        almost_final_list[i][1] = str(almost_final_list[i][1]) + '0' * (13 - num)
    almost_final_list[i][1] = str(almost_final_list[i][1])[2:] 
    
usual_date.insert(0, 'Date')
almost_final_list.insert(0, [0, 'JD, 24...', 'Filter', 'Magnitude'])
    
final_file = open(f'{star_name}.data', 'w')
#final_file.write('Date \t JD, 24.. \t Magnitude \t Filter\n')
for i in range(len(almost_final_list)):
    final_file.write(f'{usual_date[i]}\t{almost_final_list[i][1]}\t\
 {almost_final_list[i][3]}\t{almost_final_list[i][2]}\n')
final_file.close()
        
#исправить табуляцию