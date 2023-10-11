#!/usr/bin/env python3

# from person import Person

import random
import matplotlib.pyplot as plt
import math
import concurrent.futures as future

from time import perf_counter as pc
from time import sleep as pause

""" def main():
	f = Person(5)
	print(f.get())
	f.set(7)
	print(f.get()) """

# ----- 1.1 -----

def monte_carlo(n):
	inside_circle = 0
	x_inside = []	# creates 4 empty lists for x,y coordinates inside and
	y_inside = []	# outside of the circle
	x_outside = []
	y_outside = []

	for i in range(n):
		x, y = random.uniform(-1, 1), random.uniform(-1, 1)
		if x**2 + y**2 <= 1:
			inside_circle += 1
			x_inside.append(x)
			y_inside.append(y)
		else:
			x_outside.append(x)
			y_outside.append(y)
	
	pi_approx = 4 * inside_circle / n

	return pi_approx, x_inside, y_inside, x_outside, y_outside

def plot(n_values):
	plt.figure(figsize=(10, 10))

	for i, n in enumerate(n_values, 1):
		pi_approx, x_in, y_in, x_out, y_out = monte_carlo(n)
		plt.subplot(2, 2, i)  # 2x2 grid for 4 plots
		plt.scatter(x_in, y_in, c='red', s=10, marker='o')
		plt.scatter(x_out, y_out, c='blue', s=10, marker='o')
		plt.title(f"Monte Carlo for n={n}\nπ ≈ {pi_approx:.4f}")
		plt.xlim(-1, 1)
		plt.ylim(-1, 1)
		plt.grid(True)

	plt.tight_layout()
	plt.show()

# ----- 1.2 -----

# help for assignment: https://juanitorduz.github.io/vol_d_ball/

def within_bounds(p):
	return sum(x**2 for x in p) <= 1

def monte_carlo_volume(n, d):
	random_pt = map(lambda i : [random.uniform(-1, 1) for i in range(d)], range(n))
	inside_circ = filter(within_bounds, random_pt)
	approximation = 2**d * (sum(1 for i in inside_circ) / n)
	return approximation

# ----- 1.3 -----
def monte_carlo_parallell(n, d, p):
	with future.ProcessPoolExecutor (max_workers = p) as ex:
		# submit(function, argument, additional argument). // = integer division
		fs = [ex.submit(monte_carlo_volume, n, d) for i in range(p)]
		# result() waits and collects future results
		results = [i.result() for i in future.as_completed(fs)]
		return sum(results) / p


if __name__ == '__main__':
	# main()

	# ----- 1.1 -----
	n_values = [50, 100, 200, 400] # n is the amount of random points to generate
	#plot(n_values)

	# ----- 1.2 -----
	n1, d1 = 100000, 2
	n2, d2 = 100000, 11
	n3, p = 10000, 10

	start1_1 = pc()
	approximation1_1 = monte_carlo_parallell(n3, d2, p)
	end1_1 = pc()
	print(f"Approximation for V{d1}(1): {approximation1_1}. Time: {round(end1_1-start1_1, 2)} seconds.")

	start1 = pc()
	approximation1 = monte_carlo_volume(n1, d1)
	end1 = pc()
	exact_value1 = math.pi**(d1/2) / (math.gamma((d1/2) + 1))

	#start2 = pc()
	#approximation2 = monte_carlo_volume(n2, d2)
	#end2 = pc()
	#exact_value2 = math.pi**(d2/2) / (math.gamma((d2/2) + 1))

	print(f"Approximation for V{d1}(1): {approximation1}. Time: {round(end1-start1, 2)} seconds.")
	print(f"Exact value for V{d1}(1): {exact_value1}")
	#print()
	#print(f"Approximation for V{d2}(1): {approximation2}. Time: {round(end2-start2, 2)} seconds.")
	#print(f"Exact value for V{d2}(1): {exact_value2}")

	