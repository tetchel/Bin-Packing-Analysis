import math

from bin_pack import pack_print_all, pack_and_print, first_fit, set_epsilon, ptas_wf
import random
import time

def random_int_list(min, max, length):
    result = []
    for x in range(0, length):
        result.append(random.randint(min, max))

    return result


def random_list(length):
    result = []
    for x in range(0, length):
        r = 0
        # No zero-weight items
        while r == 0:
            r = random.random()
        result.append(r)

    return result


INPUT_SIZE = 100000
outfile = 'bin-pack_' + time.strftime("%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
with open(outfile, 'a') as f:
    f.write('Algorithm, Descending?, n, Runtime (s), SOL, OPT, SOL/OPT\n')

# for i in range(10):
#    pack_print_all(random_list(1, 10, 100000))

#for i in range(128):
#    pack_print_all(random_list(INPUT_SIZE), outfile)

with open(outfile, 'a') as f:
    f.write('Doing PTAS')
for j in range(1, 5):
    eps = 10**-j
    set_epsilon(eps)

    with open(outfile, 'a') as f:
        f.write('Doing PTAS, eps={}'.format(eps))
    for i in range(32):
        print('i {}, j {}'.format(i, j))
        pack_and_print(random_list(INPUT_SIZE), ptas_wf, outfile, True)
"""
print('Running a worst case for Next Fit')
with open(outfile, 'a') as f:
    f.write('Running a worst case for Next Fit\n')

# INPUT_SIZE /= 10        # FF is slow


worst_case_nf = [1/2, 1/(2*INPUT_SIZE)] * int(math.ceil(INPUT_SIZE / 2))
pack_print_all(worst_case_nf, outfile)
pack_and_print(worst_case_nf, first_fit, outfile, False)
pack_and_print(worst_case_nf, first_fit, outfile, True)

print('Running a worst case for First Fit')
with open(outfile, 'a') as f:
    f.write('Running a worst case for First Fit\n')
onethird = int(math.ceil(INPUT_SIZE / 3))
worst_case_ff = [1 / 7 + 0.001] * onethird + [1 / 3 + 0.001] * onethird + [1 / 2 + 0.001] * onethird
pack_print_all(worst_case_ff, outfile)
pack_and_print(worst_case_ff, first_fit, outfile, False)
pack_and_print(worst_case_ff, first_fit, outfile, True)
"""