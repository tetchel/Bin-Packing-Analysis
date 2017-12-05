import math
import datetime
import random
from timeit import default_timer as timer


# Assumes integer weights, and gives each bin capacity 10.

class Bin:
    CAPACITY = 10

    def __init__(self):
        # Items contains a list of (name, weight) tuples representing items packed into this bin
        self.items = []
        self.weight = 0

    def get_residual_capacity(self, item_weight):
        """
        Returns the amount of space left in this bin if the given item_weight was added.
        If the result is >= zero, the item fits into the bin.
        """
        return self.CAPACITY - (self.weight + item_weight)

    def has_room(self, item_weight):
        return self.get_residual_capacity(item_weight) >= 0

    def try_add_item(self, item_name, item_weight):
        """
        Try and add the given item. Returns success status.
        :param item_name:
        :param item_weight:
        :return: true and adds the item if there is room, false if there is no room.
        """

        if not self.has_room(item_weight):
            return False

        self.weight += item_weight
        self.items.append((item_name, item_weight))
        return True

    def __str__(self):
        result = ''
        total_w = 0
        for item in self.items:
            result += 'Item {} w={}, '.format(item[0], item[1])
            total_w += item[1]
        result = result.strip()
        result += " Total: " + str(total_w)
        return result


def next_fit(items):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    bin = Bin()
    bins.append(bin)
    for index, item in enumerate(items):
        if not bin.try_add_item(index, item):
            bin = Bin()
            if not bin.try_add_item(index, item):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(bin)

    return bins


def first_fit(items):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    # Sort - so this is actually first fit decreasing
    items.sort(reverse=True)
    for index, item in enumerate(items):
        packed = False
        # Below loop can be improved by using a data structure with faster lookup to get a bin with room.
        # Eg a binary tree sorted by residual capacity would allow searching for the emptiest bin
        # in log(|B|) time where B is the set of bins.
        for bin in bins:
            if bin.try_add_item(index, item):
                packed = True
                break
        if not packed:
            b = Bin()
            if not b.try_add_item(index, item):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
    return bins


def best_fit(items):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    # Sort - so this is actually best fit decreasing
    items.sort(reverse=True)
    for index, item in enumerate(items):
        best_bin_rcap = 0
        best_bin = None
        # Below loop can be improved by using a data structure with faster lookup to get a bin with room.
        # Eg a binary tree sorted by residual capacity would allow searching for the emptiest bin
        # in log(|B|) time where B is the set of bins.
        for bin in bins:
            rcap = bin.get_residual_capacity(item)
            if rcap >= best_bin_rcap:
                best_bin_rcap = rcap
                best_bin = bin
                # print('The best bin is {} with rcap {}'.format(best_bin, rcap))

        if not best_bin:
            best_bin = Bin()
            bins.append(best_bin)

        if not best_bin.try_add_item(index, item):
            print('Error! Best bin did not have room for item! Is the item larger than the bin?')
            # else:
            # print('packed item {} with weight {} into bin {}'.format(index, item, str(best_bin)))

    return bins


def pack_and_print(items, algorithm, print_contents=False):
    print('Packing using ' + algorithm.__name__)
    t = timer()
    bins = algorithm(items)
    end_t = timer() - t

    print('Took ' + str(end_t) + "s")
    print('Used {} bins'.format(len(bins)))
    tw = sum(bin.weight for bin in bins)
    print('Total weight was {} and capacity per-bin was {}, so an optimal solution would use at least {} bins'
          .format(tw, Bin.CAPACITY, math.ceil(tw / Bin.CAPACITY)))

    if print_contents:
        for index, bin in enumerate(bins):
            print('bin ' + str(index))
            print(bin)


def pack_print_all(items):
    print('----- Running all packing algorithms on input size ' + str(len(items)))
    print('INPUT: ' + str(items))

    pack_and_print(items, next_fit)
    pack_and_print(items, first_fit)
    pack_and_print(items, best_fit)


def random_list(min, max, length):
    result = []
    for x in range(0, length):
        result.append(random.randint(min, max))

    return result


# pack_print_all(random_list(1, 10, 10000))


for i in range(10):
    pack_print_all(random_list(1, 10, 100000))

# pack_print_all([1, 10, 5, 6, 4, 4, 9, 3, 5] * 1000)
# Demonstrates problem with next_fit
# pack_print_all([9, 8, 9, 2, 1, 1])
