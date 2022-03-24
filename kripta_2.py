# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:21:16 2022

@author: Knaub Denis, Efimova Dasha
"""
import random
import sys

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
        a = random.getrandbits(128) # количество бит генерируемого числа
        y = miller_rabin(a, 40)
        # если число простое, проверяем, надежное ли оно
        if y == True: 
            yy = Sophie_Germain(a)             
            if yy == True: # если число прошло проверку на надежность, возвращаем его
                return a
            else: # если нет, генерируем новое число и проверяем
                y = False 


# проверка на надежность (явл. ли число числом Софи-Жерман?)  
def Sophie_Germain(z):
    z = 2*z + 1
    y = miller_rabin(z, 40)  # простое ли z?              
    return y          

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

# генерация параметров
# N - максимальное значение n
def generateG(N):
    q = gen()
    y = False
    while y == False:
        n = random.randint(2, N)
        p = n*q + 1
        y = miller_rabin(p, 40)
        if y == True:
            break
    g = 1
    # g не должно быть = 1
    while g == 1:
        m = False
        while m != True:
            a = random.randint(2, p-1)
            g = Zpow(a, n, p)
            m = miller_rabin(g, 40) 
            if m == True:
                return (g, q, p)

def generateAB(g, x, q, p):
    x1 = x%q                # это число принадлежит Zp
    x_new = Zpow(g, x1, p)  # вычисляем по формуле
    return x_new

# Генерация открытых ключей p, g
# p - большое простое число, p = n*q + 1
# g - примитивный элемент, порождающий мультипликационную группу Zp
# q - простое большое число
print("Пользователи выбирают параметры...")
g, q, p = generateG(100000)


# Проверяем условия правильной генерации параметров
# 1. q является делителем p-1 (остаток от деления = 0)
q_del = (p - 1) % q

# 2. Проверка генератора g: g != 1, g^q mod p = 1
# также g должно быть меньше p
if g >= p:
    sys.exit("g больше p!")

g_check = Zpow(g, q, p)
if q_del == 0 and g != 1 and g_check == 1:
    print("Параметры сгенерированы верно! \n")
else:
    sys.exit("Параметры ошибочны.")

print(f"Даша и Денис получили открытые числа p = {p},\n\t\t\t\t g = {g} \n")

# чтобы создать неизвестный более никому секретный ключ, 
# оба абонента генерируют большие случайные числа
print("Пользователи выбирают свои закрытые ключи...")
a = gen()
print(f"\tДаша выбирает свой закрытый ключ: a = {a}")
b = gen()
print(f"\tДенис выбирает свой закрытый ключ: b = {b} \n")

# для создания общего секретного ключа:
# создать открытые ключи для обмена из закрытых ключей
# X = g^a mod p
print("Пользователи создают свои ключи, по своим выбранным a, b...")
print("Даша и Денис обмениваются своими открытыми ключами...")
A = generateAB(g, a, q, p)
print(f"\tДаша высылает Денису свой открытый ключ: A = {A}")
B = generateAB(g, b, q, p)
print(f"\tДенис высылает Даше свой открытый ключ: B = {B} \n")

# Проверка
if Zpow(A, q, p) != 1 or Zpow(B, q, p) != 1:
    sys.exit("A, B не принадлежат подгруппе, порожденной g!")

# Вычисление общего закрытого ключа (K1 должно быть равно K2)
K1 = Zpow(B, a, p)
print("Даша вычисляет секретный ключ...")
print(f"\tПолучившийся секретный ключ для Даши: {K1}")

K2 = Zpow(A, b, p)
print("Денис вычисляет секретный ключ...")
print(f"\tПолучившийся секретный ключ для Дениса: {K2} \n")

# Проверяем получившиеся ключи у пользователей
# 3. общий ключ также должен быть равен g^(a*b) mod p <- исходя из предыдущих вычислений
K3 = Zpow(g, a*b, p)

if K1 == K2 == K3:
    print("------------------------------------------")
    print("Общий секретный ключ сгенерирован успешно!")
else:
    print("Общий секретный ключ получен неверно.")


























############# я просто не хочу удалять это, на всякий случай...
# надо использовать это, чтобы найти все примитивные числа какого-то числа
# def gcd(a,b):
#     while b != 0:
#         a, b = b, a % b
#     return a

# def primRoots(modulo):
#     roots = []
#     required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)

#     for g in range(1, modulo):
#         actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
#         if required_set == actual_set:
#             roots.append(g)           
#     return roots

# def check_govno(g):
#     y = False
#     while y != True: 
#         idx = random.randint(0, len(g)-1)
#         prostoe_govno = g[idx]
#         print("Проверяем число: ", prostoe_govno)
#         y = miller_rabin(prostoe_govno, 40)
        
#         if y == True:
#             yy = Sophie_Germain(prostoe_govno)             
#             if yy == True: # если число прошло проверку на надежность
#                 return prostoe_govno
#             # return prostoe_govno
#             else:
#                 y = False 
#                 g.remove(prostoe_govno)
#                 # check_govno(g)

# g = primRoots(p)
# exp_g=primRoots(q)
# print(exp_g)
# # prostoe_g = check_govno(g)
# print("Это g massive ", g)
# print("Это полученное простое g из списка рандомом ", prostoe_g)
# print("Это p ", p)
#########################