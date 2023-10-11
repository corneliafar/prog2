import random
import matplotlib.pyplot as plt
import math

# Higher order function document examples

# ----- List Comprehensions -----
# Instead of writing lists within for-loops it can be written directly inside square brackets.
lst_1 = []
for i in range (1,5):
    lst_1.append(i**2)

# Simpler way
lst_2 = [i**2 for i in range(1,5)]

# For example it can be used in the following situation where what happens is that the for-loop sets i to 1, 2, ... , 9, and for each value 
# checks if the remainder (%) of i % 2 equals zero. If so, math.gamma(i) is executed and added as an element to the list.
lst_3 = [math.gamma(i) for i in range(1,10) if i% 2 == 0]

# The for-loop equivalent would be
lst_4 = []
for i in range(1,10):
    if i % 2 == 0:
        lst_4.append(math.gamma(i))

# ----- Lambda Functions -----
# A lambda function in Python is a small, anonymous (unnamed) function that is defined using the lambda keyword. Lambda functions are also 
# known as anonymous functions or lambda expressions. They are used for creating small, one-time-use functions without the need to formally 
# define a function using the def keyword.
# Syntax is lambda <argument> : <expression>

f = lambda x : x*2
f(5)

def multiply(n):
    return lambda a : a * n
double = multiply(2)
double(10)

# ----- map() -----
# In Python, map returns a map-object containing the results of applying a function to each element in an interable (list, tuple, etc.). 
# If you for instance have map(f,[1,2,3]) a map-object with (f(1),f(2),f(3)) will be returned. Note that the map-object needs to be 
# converted from type map using the function list() to get a list, i.e.: list(map(f,[1,2,3])).
# The syntax is map(<function>, <iterable>)

list(map(math.gamma,range(1,5)))

list(map(lambda x : x**2 , range(1,5)))

list1=[1,2,3,4]
list2=[5,6,7,8]
list(map(lambda x,y : x+y, list1, list2))   # input of multiple arguments x+y (1+5, 2+6, ...)

# ----- functools.reduce() -----
# The reduce.function functools.reduce() is often used together with map(); the combination is often called MapReduce, 
# https://en.wikipedia.org/wiki/MapReduce and is an important concept in Data Science and Big Data. The purpose of functools.reduce() 
# is to reduce an iterable (list, tuple, etc) down to a value.

import functools
lst_5 = [1, -2, 3, 4]
functools.reduce(lambda x, y : x+y, lst_5)

# kombiner med map()
lst_6 = [1, -2, 3, 4]
functools.reduce(lambda x, y : x+y , map(abs, lst_6)) # abs() = absolutbelopp, map() makes sure its done for each element

# ----- filter() -----
# The function filter() can be used when you can formulate a yes/no (true/false) question for each element in an iterable. For 
# example, to find all elements in a list greater than 2, one can “ask each element” Is your value greater than 2? This can 
# be formulated as a function returning True for Yes and False for No.

def greaterThanTwo(num):
    if(num > 2):
        return True
    else:
        return False
    
a = [7, 1, -3, 4]
list(filter(greaterThanTwo, a))

# combine this with a lambda function to remove the need of a def function

list(filter(lambda x : x > 2 , a))

# for example, find all vowels
vowels = ['a', 'o', 'u', 'å', 'e', 'i', 'y', 'ä', 'ö']
word = 'xylofon'
list(filter(lambda letter : letter in vowels , word))

# ----- zip() -----
# The function zip is used to create an iterable of tuples from one or more iterables.
djur = ['hund', 'katt', 'orm']
list(zip(range(3), djur))

# One can for example use zip when one wants to find the index of elements with a certain property, e.g. What are the indices for 
# all elements in a list greater than zero?
tal = [2, -1, 7, 9]
zip_tal = list(zip(range(len(tal)),tal))
[ii[0] for ii in zip_tal if ii[1]>0] # adds indices for elements greater than 0 in a list


def random_pt(d):
    return [random.uniform(-1,1) for i in range(d)]

def within_bounds(p):
    return sum(x**2 for x in p) <= 1

def monte_carlo(n, d):
    random_points = map(lambda i : random_pt(d), range(n))
    within_circle_points = filter(within_bounds, random_points)
    approximation = len(list(within_circle_points)) / n
    return approximation

# Test cases
n1, d1 = 100000, 2
n2, d2 = 100000, 11

approximation1 = monte_carlo(n1, d1)
exact_value1 = math.pi**(d1/2) / (math.gamma((d1/2) + 1))

approximation2 = monte_carlo(n2, d2)
exact_value2 = math.pi**(d2/2) / (math.gamma((d2/2) + 1))

print(f"Approximation for V{d1}(1): {approximation1}")
print(f"Exact value for V{d1}(1): {exact_value1}")
print()
print(f"Approximation for V{d2}(1): {approximation2}")
print(f"Exact value for V{d2}(1): {exact_value2}")