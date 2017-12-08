import math

from bin_pack import pack_print_all, pack_and_print, first_fit, set_epsilon, ptas_awfd, almost_worst_fit
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


def test_all(input_size, outfile):
    for i in range(128):
        pack_print_all(random_list(input_size), outfile)


def test_ptas(input_size, outfile):
    epses = [0.5, 0.25, 0.1, 0.05, 0.01, 0.001]

    for eps in epses:
        set_epsilon(eps)

        with open(outfile, 'a') as f:
            f.write('Doing PTAS, eps={}\n'.format(eps))
        for i in range(64):
            pack_and_print(random_list(input_size), ptas_awfd, outfile, True)


def worst_case_nf(input_size, outfile):
    print('Running a worst case for Next Fit')
    with open(outfile, 'a') as f:
        f.write('Running a worst case for Next Fit\n')

    bad_input_nf = [1 / 2, 1 / (2 * input_size)] * int(math.ceil(input_size / 2))
    pack_print_all(bad_input_nf, outfile)
    pack_and_print(bad_input_nf, first_fit, outfile, False)
    pack_and_print(bad_input_nf, first_fit, outfile, True)


def worst_case_ff(input_size, outfile):
    print('Running a worst case for First Fit')
    with open(outfile, 'a') as f:
        f.write('Running a worst case for First Fit\n')

    one_third = int(math.ceil(input_size / 3))
    bad_input_ff = [1 / 7 + 0.001] * one_third + [1 / 3 + 0.001] * one_third + [1 / 2 + 0.001] * one_third
    pack_print_all(bad_input_ff, outfile)
    pack_and_print(bad_input_ff, first_fit, outfile, False)
    pack_and_print(bad_input_ff, first_fit, outfile, True)


INPUT_SIZE = 100000
OUTFILE = 'bin-pack_' + time.strftime("%m-%d_%H-%M-%S", time.gmtime()) + ".csv"
with open(OUTFILE, 'a') as F:
    F.write('Algorithm, Descending?, n, Runtime (s), SOL, OPT, SOL/OPT\n')

# test_all(INPUT_SIZE, OUTFILE)
test_ptas(INPUT_SIZE, OUTFILE)

#for x in range(128):
#    pack_and_print(random_list(INPUT_SIZE), almost_worst_fit, OUTFILE, True)
#    pack_and_print(random_list(INPUT_SIZE), almost_worst_fit, OUTFILE, False)

# FF is slow, reduce input size by order of mag.
# worst_case_nf(math.ceil(INPUT_SIZE/10), OUTFILE)
# worst_case_ff(math.ceil(INPUT_SIZE/10), OUTFILE)
#for x in range(128):
#    pack_and_print(random_list(math.ceil(INPUT_SIZE/10)), first_fit, OUTFILE, False)
#    pack_and_print(random_list(math.ceil(INPUT_SIZE/10)), first_fit, OUTFILE, True)
