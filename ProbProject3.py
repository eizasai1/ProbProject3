import math
import random
import matplotlib.pyplot as plt


use_random_number_generator = True
# samples = [10, 30, 50, 100, 250, 500, 1000]
# number_of_estimates = [110 for i in range(len(samples))]

samples = [3, 9, 27, 81]
number_of_estimates = [5, 25, 110, 550]


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


def get_estimates_of_m_n():
    for sample_size in range(len(samples)):
        file = open_file(str(samples[sample_size]) + ".txt")
        for i in range(number_of_estimates[sample_size]):
            file.write(str(round(m_n_of_x(samples[sample_size]), 4)) + "\n")
        file.close()


def get_sample_variance(file, sample):
    total = 0
    for i in range(number_of_estimates[sample]):
        line = file.readline()
        total += (float(line)**2)
    return abs((total / number_of_estimates[sample]) - (mu_x**2))



def get_sample_mean(file, sample):
    total = 0
    for i in range(number_of_estimates[sample]):
        line = file.readline()
        total += float(line)
    return total / number_of_estimates[sample]


def get_z_n_values(file, sample_size):
    file2 = open("z_n" + str(samples[sample_size]) + ".txt", 'w')
    file2.close()
    file2 = open("z_n" + str(samples[sample_size]) + ".txt", 'a')
    for i in range(number_of_estimates[sample_size]):
        m_n = float(file.readline())
        z_n = (m_n - mu_x) / math.sqrt(var_x / math.sqrt(samples[sample_size]))
        file2.write(str(z_n) + "\n")


def get_sample_data():
    for sample_size in range(len(samples)):
        file = open(str(samples[sample_size]) + ".txt", 'r')
        mean = get_sample_mean(file, sample_size)
        file.close()
        file = open(str(samples[sample_size]) + ".txt", 'r')
        variance = get_sample_variance(file, sample_size)
        file.close()
        file = open(str(samples[sample_size]) + ".txt", 'r')
        get_z_n_values(file, sample_size)
        file.close()
        print("Sample Size:", str(samples[sample_size]), "mean:", mean, "variance:", variance)



def make_plot():
    plt.title("$M_{n}$ Random Variable")
    plt.xlabel("Sample size $n$")
    plt.ylabel("$m_{n}$")
    plt.axhline(mu_x)
    for sample_size in range(len(samples)):
        file = open(str(samples[sample_size]) + ".txt", 'r')
        for i in range(number_of_estimates[sample_size]):
            line = file.readline()
            plt.plot([samples[sample_size]], [float(line)], marker="o", markersize=2,markeredgecolor="red",markerfacecolor="red")
        file.close()
    plt.show()


def main():
    print("Rayleigh Distribution of X")
    print("tau:", tau)
    print("a = 1/tau:", a)
    print("mu_x:", mu_x)
    print("var_x:", var_x)
    print("sigma_x:", sigma_x)
    get_estimates_of_m_n()
    recommended_sample = var_x / 10
    print(recommended_sample)
    get_sample_data()
    # print(get_u_values())


main()

make_plot()
