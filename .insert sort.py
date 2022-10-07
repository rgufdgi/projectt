#task1

"""23.09
сортировка"""

file = open('test.txt', 'r')
numbers = [float(i) for i in file.read().split()]

sorted_numbers = [numbers[0]]  # отсортированная часть списка

for i in range(1, len(numbers)):
    num = numbers[i]  # первый элемент из неотсортированной части
    j = len(sorted_numbers) - 1  # индекс элементов отсортированной части
    while num < sorted_numbers[j] and j > 0:
        j -= 1
    if j == 0 and num < sorted_numbers[0]:  # элемент в крайнем положении
        j = -1
    sorted_numbers.insert(j + 1, num)

# для того, чтобы целые числа выводились без нулей
for i in range(len(sorted_numbers)):
    if int(sorted_numbers[i]) == sorted_numbers[i]:
        sorted_numbers[i] = int(sorted_numbers[i])

print(*sorted_numbers)
