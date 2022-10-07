# task 2
data_file = open('task2_data.dat')

all_strs = data_file.read().splitlines()  # создание списка строк

# список списков, каждый список - строка из данных:
for i in range(len(all_strs)):  
    all_strs[i] = all_strs[i].split() 

# исправление перой строки   
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
        print(all_strs[i])

# изменение типа данных числовых значений       
for i in range(1,len(all_strs)):
    all_strs[i][1] = float(all_strs[i][1])
    all_strs[i][3] = float(all_strs[i][3])
    
names_list = []
for i in range(1, len(all_strs)):
    names_list.append(all_strs[0])
    
names_set = set(names_list)
print(names_set) 
    
#for i in range(len(all_strs)):
#    print(all_strs[i])
    

        
        









