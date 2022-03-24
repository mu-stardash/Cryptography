# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 16:33:51 2022
Ассиметричное шифрование
@author: dKnau, Dasha
"""
import random
import sys

# возведение в степень по модулю в кольце
def Zpow(a, p, m):
    result = 1
    while p > 2: # когда степень сократится до квадрата и меньше - завершаем
        if p % 2 == 0: # если степень кратна 2
            a = (a ** 2) % m # понижаем степень, возводя число в квадрат
            p = p // 2
        else:
            # выносим множитель для четной степени
            result = (result * a) % m
            p = p - 1
    a = (a ** p) % m
    result = (result * a) % m
    return result

# тест Рабина-Миллера на простоту
def miller_rabin(n, k):
    if n == 3 or n == 2:
        return True
    if n % 2 == 0:
        return False
        
    # представим n − 1 в виде (2^s)·t, где t нечётно, 
    # это можно сделать последовательным делением n - 1 на 2
    s, t = 0, n - 1
    while t % 2 == 0:
        s += 1 # степень двойки при делении на 2
        t //= 2 # должны получить нечетное t

    for _ in range(k):
        # генерация случайного целого числа в отрезке [2, n-1]
        a = random.randrange(2, n - 1)

        # x ← a^t mod n (с помощью возведения в степень по модулю)
        x = Zpow(a, t, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            # x ← x^2 mod n
            x = Zpow(x, 2, n)

            # если x == n − 1, то перейти на следующую итерацию внешнего цикла
            if x == n - 1:
                break
        else:
            return False
    return True

# генерация чисел
def gen():
    y = False
    while y != True:  # цикл для генерации простых чисел 
        a = random.randint(1000000000000000, 1000000000000000000000) # диапазон генерации чисел
        y = miller_rabin(a, 40)
        if y == True:
            return a    

# Алгоритм Евклида для поиска НОД
def gcd_rem_division(num1, num2):
    while num1 != 0 and num2 != 0:
        if num1 >= num2:
            num1 %= num2
        else:
            num2 %= num1
    return num1 or num2


# Генерируем два простых числа
p = gen()    
q = gen()
print("p = "+ str(p),", q = "+ str(q))

# Вычисляем модуль
n = p*q
print("n = " + str(n))

# Функция Эйлера
fi = (p-1)*(q-1)
print("fi = " + str(fi))

# Открытая экспонента 
e = int(input("Введите e: "))

# Взаимно простые ли числа? НОД должен быть == 1
# Должно быть простым
# Должно быть меньше fi 
a = gcd_rem_division(e, fi)
if a == 1:
    print("e и fi взаимно простые")
else:
    print("e и fi не взаимно простые")
    sys.exit()

# check_simple = miller_rabin(e, 40)
# if check_simple == True:
#     print("Число простое")
# else:
#     print("Число не является простым")
#     sys.exit()

if e > fi:
    print("Число е должно быть меньше fi!")
    sys.exit()
# Теперь пара чисел e, n - открытый ключ. Отправляется для зашифровки

# нахождение обратного элемента в кольце по модулю
# Расширенный алгоритм Евклида
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
 
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    # если остаток равен 1
    if g == 1:
        return x % n

# d должно быть обратное е по модулю f. То есть остаток от деления по модулю f произведения dхe должен быть равен 1    
d = mulinv(e, fi)
print("d = " + str(d))
# Пара d, n - закрытый ключ

# М должно быть меньше n 
M = 10011101000100001111
print("Сообщение для шифрования: "+ str(M))

# Шифрование
C = Zpow(M, e, n)
print("Зашифрованное "+ str(C))

# Для расшифровки
# Решение методом китайских теорем об остатках
dp = mulinv(e, p-1) # обратное значение е к р-1
dq = mulinv(e, q-1) # обратное значение е к q-1
qlnv = mulinv(q, p) # обратное значение q к p

# Разложение процесса расшифровки
m1 = Zpow(C, dp, p)
m2 = Zpow(C, dq, q)

h = (int(qlnv)*((int(m1) - int(m2))%p))%p
m = m2 + h*q

print("Расшифрованное " + str(m))