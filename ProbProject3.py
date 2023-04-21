import math
import random
import matplotlib.pyplot as plt
import scipy.stats as ss
import numpy as np


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


def get_sample_variance(file, sample, mean):
    total = 0
    for i in range(number_of_estimates[sample]):
        line = file.readline()
        total += (float(line)**2)
    return abs((total / number_of_estimates[sample]) - (mean**2))



def get_sample_mean(file, sample):
    total = 0
    for i in range(number_of_estimates[sample]):
        line = file.readline()
        total += float(line)
    return total / number_of_estimates[sample]


def get_m_n_values(file, sample_size):
    file2 = open("m_n" + str(samples[sample_size]) + ".txt", 'w')
    file2.close()
    file2 = open("m_n" + str(samples[sample_size]) + ".txt", 'a')
    for i in range(number_of_estimates[sample_size]):
        m_n = float(file.readline())
        z_n = (m_n - mu_x) / math.sqrt(var_x / math.sqrt(samples[sample_size]))
        file2.write(str(z_n) + "\n")


def get_sample_data():
    means, variances = [], []
    for sample_size in range(len(samples)):
        file = open(str(samples[sample_size]) + ".txt", 'r')
        mean = get_sample_mean(file, sample_size)
        file.close()
        file = open(str(samples[sample_size]) + ".txt", 'r')
        variance = get_sample_variance(file, sample_size, mean)
        file.close()
        file = open(str(samples[sample_size]) + ".txt", 'r')
        get_m_n_values(file, sample_size)
        file.close()
        print("Sample Size:", str(samples[sample_size]), "mean:", mean, "variance:", variance)
        means.append(mean)
        variances.append(variance)
    return means, variances




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


def tofloat(number):
    for i in range(len(number)):
        try:
            return float(number[i:])
        except ValueError:
            None





def put_data_bins(sample_index, mu_x, var_x, probability_values):
    file = open(str(samples[sample_index]) + ".txt", 'r')
    file2 = open("z_n" + str(samples[sample_index]) + ".txt", 'a')
    data = [0 for i in range(7)]
    total = 0
    for i in range(number_of_estimates[sample_index]):
        line = float(file.readline())
        z = (line - mu_x) / math.sqrt(var_x)
        file2.write(str(z))
        # print(line, mu_x, var_x)
        if z <= -1.4:
            data[0] += 1
        if z <= -1:
            data[1] += 1
        if z <= -0.5:
            data[2] += 1
        if z <= 0:
            data[3] += 1
        if z <= 0.5:
            data[4] += 1
        if z <= 1:
            data[5] += 1
        if z <= 1.4:
            data[6] += 1
        total += 1
    for i in range(len(data)):
        data[i] = data[i] / total
    file.close()
    file2.close()
    mad_values = [-1 for i in range(7)]
    for i in range(len(probability_values)):
        mad_values[i] = abs(data[i] - probability_values[i])
    # print("data for population of sample n = " + str(samples[sample_index]))
    # print(mad_values)
    # print(max(mad_values))
    return data, mad_values.index(max(mad_values))


def plot_data(means, variances):
    z_scores = [-1.4, -1, -0.5, 0, 0.5, 1, 1.4]
    probability_values = [0.0808, 0.1587, 0.3086, 0.5, 0.6915, 0.8413, 0.9192]
    z_score = np.linspace(-2.5, 2.5, 1000)
    probs = ss.norm.cdf(z_score)
    for i in range(4):
        data, mad = put_data_bins(i, means[i], variances[i], probability_values)
        mad_points = [data[mad], probability_values[mad]]
        plt.title("CDF of Standard Normal and Population (n,K) = (" + str(samples[i]) + "," + str(number_of_estimates[i]) + ")")
        plt.xlabel("Normalized Z Scores")
        plt.ylabel("Probability")
        plt.scatter(z_scores, data, marker="o", label="CDF of Population (" + str(samples[i]) + ", " + str(number_of_estimates[i]) + ")")
        plt.plot(z_score, probs, label="CDF of Standard Normal")
        plt.plot([z_scores[mad], z_scores[mad]], mad_points, label="Maximum Absolute Difference")
        plt.legend()
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
    # print(get_u_values())


main()

make_plot()

means, variances = get_sample_data()

plot_data(means, variances)
