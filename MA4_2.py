#!/usr/bin/env python3
"""
Solutions to module 4
Student: Cornelia Färdig
Mail: cornelia.fardig.3943@student.uu.se
Reviewed by: Naser Shabani
Reviewed date: 2023-10-12
"""

from person import Person

import random
import matplotlib.pyplot as plt
import math
import concurrent.futures as future

from numba import njit
from time import perf_counter as pc
from time import sleep as pause

"""def main():
	f = Person(5)
	print(f.get())
	f.set(7)
	print(f.get())"""

# ---------- 2.2 ----------
def fib_py(n): 		# recursively calculates fibonacci sequence for n
	if n <= 1:
		return n
	else:
		return fib_py(n-1) + fib_py(n-2)

@njit
def fib_numba(n):	# same as fib_py but using numba decorator
	if n <= 1:	# to speed up compilation
		return n
	else:
		return fib_numba(n-1) + fib_numba(n-2)

def fib_timings(n):
	timings = {}	# creates an empty dictionary

	start = pc()	# starts time rec
	fib_py(n)
	timings['python'] = pc() - start	# takes current time subtracted with start time and
						# stores with the var name 'python' in dict.
	start = pc()
	fib_numba(n)
	timings['numba'] = pc() - start		# same as above but for numba

	f = Person(n)
	start = pc()
	f.fib()
	timings['cpp'] = pc() - start		# same as above but for cpp version

	return timings

def parallell_fib(n_values):		# run fib parallell to speed up process
	with future.ProcessPoolExecutor() as ex:
        	results = list(ex.map(fib_timings, n_values))	# creates a list that maps together timings and n_values
	return results						# distributes workload for different n-values

def plot_fib(n_values, results, filename):	# accepts input for n, fib results and name for the saved file
	fig, ax = plt.subplots()		# sets the same figure and axis for all the subplots

	for i in ['python', 'numba', 'cpp']:	# iterates over timings dict from result list
		ax.plot(n_values, [_[i] for _ in results], label=i)	# extract all result values for each timings dict
									# i.e. time and each fib value calculation
	ax.set_xlabel('n')			# x-label = n
	ax.set_ylabel('Time (seconds)')		# y-label = seconds
	ax.legend()				# enables a legend
	plt.savefig(filename)			# ensures fig is saved

# ---------- 1.1 ----------
def monte_carlo(n):
	inside_circle = 0
	x_inside = []	# creates 4 empty lists for x,y coordinates inside and
	y_inside = []	# outside of the circle
	x_outside = []
	y_outside = []

	for i in range(n):	# iterates over n values
		x, y = random.uniform(-1, 1), random.uniform(-1, 1)	# create randomised x,y coordinates
		if x**2 + y**2 <= 1:		# check if point is within theoretical bound
			inside_circle += 1	# if it is, add +1 to variable inside_circle
			x_inside.append(x)	# store x-coordinate to inside list
			y_inside.append(y)	# store y-coordinate to inside list
		else:				# if not in bounds
			x_outside.append(x)	# store x-coordinate to outside list
			y_outside.append(y)	# store y-coordinate to outside list

	pi_approx = 4 * inside_circle / n	# 2-d space gives approx 2^2*(inside circ / n)

	return pi_approx, x_inside, y_inside, x_outside, y_outside	# return approximation and all lists

def plot(n_values, filename):
	plt.figure(figsize=(10, 10))	# creates a large figure space

	for i, n in enumerate(n_values, 1):	# for every value in n_values (starting from 1)
		pi_approx, x_in, y_in, x_out, y_out = monte_carlo(n)	# calls monte_carlo for each n-value and stores returned result
		plt.subplot(2, 2, i)  # creates a 2x2 grid for 4 plots
		plt.scatter(x_in, y_in, c='red', s=10, marker='o')	# plots values inside bounds with red circles
		plt.scatter(x_out, y_out, c='blue', s=10, marker='o')	# plots values outside bounds with blue circles
		plt.title(f"Monte Carlo for n={n}\nπ ≈ {pi_approx:.4f}")	# title for plots containing pi approximation
		plt.xlim(-1, 1)		# sets plot axis limits
		plt.ylim(-1, 1)
		plt.grid(True)		# enables a grid

	plt.tight_layout()	# tight layout for better fit to make the plot easier to read
	plt.savefig(filename)
	plt.show()

# ---------- 1.2 ----------
# calculate which coordinates are within bounds in accordance to sum(x1^2+x2^2+ ... +xn^2) < 1
def within_bounds(p):	# function that defines what is within bounds in accordance to assignment
	return sum(x**2 for x in p) <= 1

def monte_carlo_volume(n, d):	# n values and d dimensions
	# lambda function creates a list (through list comprehension) 
	# of d random points
	# map connects each d points with each value of n creating
	# n random points in the d dimensional space
	random_pt = map(lambda i : [random.uniform(-1, 1) for i in range(d)], range(n))
	# filter method connects the random points to what values are 
	# accepted as "within bounds" by calling the within_bounds
	# function for each value of random_pt. it then stores the
	# within bounds values to the variable inside_circ
	inside_circ = filter(within_bounds, random_pt)
	# calculates approximated volume of the hypersphere for d dimensions
	approximation = 2**d * (sum(1 for i in inside_circ) / n)
	return approximation

# ---------- 1.3 ----------
def monte_carlo_parallell(n, d, p):
	with future.ProcessPoolExecutor (max_workers = p) as ex:	# max workers is p
		# syntax: submit(function, argument, additional argument). // = integer division
		# list comprehension that creates a list by executing submit p times (from i=0 to i=p-1)
		# this returns future object that are stored into the list
		fs = [ex.submit(monte_carlo_volume, n, d) for i in range(p)]
		# result() waits and collects future results
		results = [i.result() for i in future.as_completed(fs)]
		return sum(results) / p


if __name__ == '__main__':
	# main()

	# ---------- 2.2 ----------
	# numba warm-up, in accordance to recommendations online (without it the numba values flatlined 
	# on 1.4 sec for all runs.
	fib_numba(10)

	n_values = list(range(30,46))
	results = parallell_fib(n_values)
	plot_fib(n_values, results, 'fib_30_to_45.png')

	# from results the fib(47) done by the c++ version is negative, but fibonacci sequences cannot be negative
	# this is due to limitations in the c++ programming language rending it unable to manage numbers that are too long.
	# fib_cpp(47) = -1323752223
	# fib_numba(47) = 2971215073
	f = Person(47)
	print(f.fib(), fib_numba(47))

	print()


	# ---------- 1.1 ----------
	n_values = [50, 1000, 10000, 100000] # n is the amount of random points to generate
	plot(n_values, 'monte_carlo.png')
	# plot(n_values)	# uncomment this to plot directly


	# ---------- 1.2 ----------
	n, d1, d2 = 100000, 2, 11

	print('----- PART 1.2 -----')
	start = pc()
	approximation_1 = monte_carlo_volume(n, d1)
	end = pc()
	print(f"Approximated volume of {d1}-dimensional hypersphere (sequential): {approximation_1}. Time: {round(end-start, 2)} seconds.")
	exact_value_1 = math.pi**(d1/2) / (math.gamma((d1/2) + 1))
	print(f'Exact volume of {d1}-dimensional hypersphere acc. to gamma equation: {exact_value_1}')
	print()

	start = pc()
	approximation_2 = monte_carlo_volume(n, d2)
	end = pc()
	print(f"Approximated volume of {d2}-dimensional hypersphere (sequential): {approximation_2}. Time: {round(end-start, 2)} seconds.")
	exact_value_2 = math.pi**(d2/2) / (math.gamma((d2/2) + 1))
	print(f'Exact volume of {d2}-dimensional hypersphere acc. to gamma equation: {exact_value_2}')

	print()


	# ---------- 1.3 ----------
	n1, n2, d, p = 10000000, 1000000, 11, 10

	# print values for sequential and parallell programming as well as theoretical value for hypersphere volume
	print('----- PART 1.3 -----')
	start = pc()
	approximation = monte_carlo_volume(n1, d)
	end = pc()
	print(f"Approximated volume of {d}-dimensional hypersphere (sequential): {approximation}. Time: {round(end-start, 2)} seconds.")

	start = pc()
	approximation_parallell = monte_carlo_parallell(n2, d, p)
	end = pc()
	print(f"Approximated volume of {d}-dimensional hypersphere (parallell): {approximation_parallell}. Time: {round(end-start, 2)} seconds.")

	exact_value = math.pi**(d/2) / (math.gamma((d/2) + 1))
	print(f'Exact volume of {d}-dimensional hypersphere (gamma equation): {exact_value}.')
