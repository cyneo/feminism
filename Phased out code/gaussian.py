"""
16th Feb 2015:
Code meant to generate a gaussian, and get a figure to save. Nothing else.
"""


from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import os
import csv


def pcolor_plotter(xmin, xmax, Nx, ymin, ymax, Ny):
    nx = linspace(xmin, xmax, Nx)
    ny = linspace(ymin, ymax, Ny)
    x, y = meshgrid(nx, ny)
    fun = dgaussian(x, y, 2, 1) + dgaussian(x, y)
    fun += dgaussian(x, y, 0, 0)
    # print(fun)  # returns a bunch of numbers
    # print(type(fun)) # returns a numpy class (d.array)
    plt.pcolormesh(x, y, fun)
    

def gaussian(x, x0, sigma):
    gaussian = exp(-(x-x0)**2/(2*sigma**2))
    return gaussian


def dgaussian(x, y, x0=1, y0=1, sigma_x=3, sigma_y=0.01):
    fun = gaussian(x, x0, sigma_x)*gaussian(y, y0, sigma_y)
    return fun

# pcolor_plotter(0, 3, 3000, 0, 3, 3000)
# plt.show()


# First create a for loop to take in variables to plot
# The loop should only hold one meshgrid at one time


def plotter(filename, xmin=0, xmax=300, Nx=2000,
            ymin=0, ymax=1, Ny=2000, sigma_x=3, sigma_y=0.01):
    root = '/home/cyneo/Work/Scans/Processed Data/Extracted CSV/'
    file1 = os.path.abspath(root + filename + '.csv')
    nx = linspace(xmin, xmax, Nx)
    ny = linspace(ymin, ymax, Ny)
    x, y = meshgrid(nx, ny)
    mastermesh = []
    with open(file1, 'r', encoding='utf8') as filein:
        file_reader = csv.reader(filein)
        next(file_reader)

        for word, frequency, inhubness, outhubness in file_reader:
            # want to feed the values into the center points
            if mastermesh == []:
                mastermesh = dgaussian(x, y, float(frequency),
                                       float(outhubness), sigma_x, sigma_y)
            else:
                mastermesh += dgaussian(x, y, float(frequency),
                                        float(outhubness), sigma_x, sigma_y)

    for x in range(len(mastermesh)):
        for y in range(len(mastermesh[x])):
            mastermesh[x, y] = np.log(mastermesh[x, y]+1)

    x, y = meshgrid(nx, ny)
    plt.pcolormesh(x, y, mastermesh)
    plt.show()
    outfile = os.path.abspath(root + filename + ' Array')
    np.save(outfile, mastermesh)



