import random
import math
import xlsxwriter
from scipy.stats import skew


# function to get number of runs of an element in an array of elements
def run(elements, element):
    count, i = 0, 0
    if element not in elements: return count
    while i < len(elements):
        if elements[i] == element:
            count += 1
            j = 0
            while elements[i + j] == element and i + j < len(elements) - 1:
                j += 1
            i += j
        i += 1

    return count



def generate_X(F, H):
    N = F + H
    output = [None] * N
    count = 0
    taken_index = set()
    while count < F:
        index = random.randrange(N)
        if index not in taken_index:
            count += 1
            output[index] = 1
            taken_index.add(index)
    for i,j in enumerate(output):
        if not j:output[i] = 2
    return output



# generate Xs
def generate_Xs(n, f, h):
    arr = [generate_X(f, h) for y in range(n)]
    Xs = [None] * n
    for i in range(n):
        Xs[i] = run(arr[i], 1)
    return Xs


# Write an array into an excel sheet
def add_to_excel(arrays):
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()

    for i, x in enumerate(arrays):
        worksheet.write(i, 0, x)
    workbook.close()
    print('Excel File Created!')
    return


# Calculate Mean
def mean(array):
    return sum([x for x in array]) / len(array)


# Calculate Standard Deviation
def standard_Deviation(array):
    total = sum(((x - mean(array)) ** 2 for x in array))
    variance = total / len(array)
    SD = math.sqrt(variance)
    return SD



# Calculate Skewness
def skewness(array):
    x = sum(((x - mean(array)) ** 3 for x in array)) / len(array)
    skewness = x / (standard_Deviation(array) ** 3)
    return skewness


# Calculate kurtosis
def kurtosis(array):
    x = sum(((x - mean(array)) ** 4 for x in array)) / len(array)
    kurtosis = x / (standard_Deviation(array) ** 4)
    return kurtosis

# textbook formulas
def formula_skew(f,h):
    num = ((f*(h+1))/(f+h))*((f**2*(h+1)**2-f*(4*h+3)+(h+2))/((f+h-2)*(f+h-1)))-3*((f**2*(f-1)*h*(h+1)**2)/((f+h)**3*(f+h-1)))-((f*(h+1))/(f+h))**3
    denum = ((f*(f-1)*h*(h+1))/((f+h)**2*(f+h-1)))**(3/2)

    return num/denum

def formula_kur(f,h):
    a = ((f**3*(h+1)**3 - f**2*(10*h**2+15*h+6) + f*(5*h**2+21*h+11)-(h**2+7*h+6))/((f+h-3)*(f+h-2)*(f+h-1)))
    b = (((f*(h+1))/(f+h))*((f**2*(h+1)**2-f*(4*h+3)+(h+2))/((f+h-2)*(f+h-1))))
    c = (((f*(h+1))/(f+h))**2*((f*(h+1)-1)/(f+h-1)))
    d = ((f*(h+1))/(f+h))**3
    e = (((f+h)**3*(f+h-1)**2)/(f*(f-1)**2*h**2*(h+1)))

    ku = (a-4*b+6*c-3*d)*e
    return ku


# User imputs for simulation
f = int(input('Please Enter F '))
h = int(input('Please Enter h '))

array = generate_Xs(10000, f, h)


#add_to_excel(array)

# skew1 = skewness(array)
# skew2 = formula_skew(f,h)
# kur1 = kurtosis(array)
# kur2 = formula_kur(f,h)
# print()
# print('Skewness 1 based on simulation is ' + str(skew1))
# print('Skewness 2 based on formula is ' + str(skew2))
# print()
# print('Kurtosis 1 based on simulation is ' + str(kur1))
# print('Kurtosis 2 based on formula is ' + str(kur2))

# Question 7
def relativeError(measured, actual):
    absolute_error = actual - measured
    return abs((absolute_error / actual) * 100)


print()
# print('Error of Skewness based on array of length 10000 ' + ' is: ' + str(relativeError(skew1, skew2)) + ' %')
# print('Error of Kurtosis based on array of length 10000 ' + ' is: ' + str(relativeError(kur1, kur2)) + ' %')

thirty_runs = [None]*30
thirty_relative_error_skew = [None]*30
thirty_relative_error_kur = [None]*30
for i in range(30):
    thirty_runs[i] = generate_Xs(10000,f,h)

for i in range(30):
    thirty_relative_error_skew[i] = relativeError(skewness(thirty_runs[i]),formula_skew(f,h))
    thirty_relative_error_kur[i] = relativeError(kurtosis(thirty_runs[i]),formula_kur(f,h))

workbook = xlsxwriter.Workbook('thirty_arrays.xlsx')
worksheet_30_arrays = workbook.add_worksheet('Arrays')
worksheet_skew_error = workbook.add_worksheet('Skewness Errors')
worksheet_kur_error = workbook.add_worksheet('Kurtosis Errors')
for j, array in enumerate(thirty_runs):
    for i, x in enumerate(array):
        worksheet_30_arrays.write(i, j, x)
    worksheet_skew_error.write(0, j, thirty_relative_error_skew[j])
    worksheet_kur_error.write(0, j, thirty_relative_error_kur[j])
workbook.close()

print('Excel File Created!')

