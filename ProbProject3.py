import math
import random
import matplotlib.pyplot as plt


use_random_number_generator = True
files = ["10", "30", "50", "100", "250", "500", "1000"]

#Variables used for random number generator
x = 1000
a_1 = 24693
c = 3967
k = 2 ** 18

#Rayleigh distribution of X
tau = 57 #inches
a = 1/tau
mu_x = tau*math.sqrt(math.pi/2)
var_x = (4-math.pi)/(2*(a**2))
sigma_x = math.sqrt(var_x)
c_weak_law_of_large_numbers = 10


def generate_random_number():
    global use_random_number_generator
    if use_random_number_generator:
        global x, a_1, c, k
        x = ((a_1 * x + c) % k)
        return x / k
    else:
        return random.random()


def get_u_values():
    values_to_get = [51, 52, 53]
    return_values = []
    for i in range(values_to_get[-1]):
        value = generate_random_number()
        if i+1 in values_to_get:
            return_values.append(round(value, 4))
            print(i + 1)
    return return_values


def open_file(filename):
    file = open(filename, 'w')
    file.close()
    file = open(filename, 'a')
    return file


def inverse_of_x():
    p = generate_random_number()
    d = math.sqrt((2*math.log(1 - p))/(-(a**2)))
    return d


def realization_of_x():
    return inverse_of_x()


def m_n_of_x(sample_size):
    total = 0
    for i in range(sample_size):
        total += realization_of_x()
    return total / sample_size


def get_estimates_of_m_n(files, estimates_needed):
    for sample_size in files:
        file = open_file(sample_size + ".txt")
        for i in range(estimates_needed):
            file.write(str(round(m_n_of_x(int(sample_size)), 4)) + "\n")
        file.close()


def main():
    print("Rayleigh Distribution of X")
    print("tau:", tau)
    print("a = 1/tau:", a)
    print("mu_x:", mu_x)
    print("var_x:", var_x)
    print("sigma_x:", sigma_x)
    estimates_needed = 110
    get_estimates_of_m_n(files, estimates_needed)
    recommeneded_sample = var_x / 10
    print(recommeneded_sample)
    print(get_u_values())


main()


def make_plot():
    plt.title("M_n Random Variable")
    plt.xlabel("Sample size n")
    plt.ylabel("m_n")
    plt.axhline(mu_x)
    for sample_size in files:
        file = open(sample_size + ".txt", 'r')
        for i in range(110):
            line = file.readline()
            plt.plot([int(sample_size)], [float(line)], marker="o", markersize=2,markeredgecolor="red",markerfacecolor="red")
        file.close()
    plt.show()


make_plot()
