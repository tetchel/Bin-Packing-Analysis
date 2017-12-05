import math
from binary_tree import BinaryTree
import random
from timeit import default_timer as timer


# Assumes integer weights, and gives each bin capacity 10.

class Bin:
    CAPACITY = 1

    def __init__(self, name):
        # Items contains a list of (name, weight) tuples representing items packed into this bin
        self.items = []
        self.weight = 0
        self.name = name

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
        result = 'Bin {}: '.format(self.name)
        total_w = 0
        for item in self.items:
            result += 'Item {} w={}, '.format(item[0], round(item[1], 6))
            total_w += item[1]
        result = result.strip()
        result += " Total: " + str(round(total_w, 6))
        return result


def next_fit(items):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    # With next fit, sorting can actually make the solution considerably worse.
    #items.sort(reverse=True)
    bin = Bin(0)
    bins.append(bin)
    for index, item in enumerate(items):
        if not bin.try_add_item(index, item):
            bin = Bin(index)
            if not bin.try_add_item(index, item):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(bin)

    return bins


def first_fit(items, decreasing=True):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()

    if decreasing:
        items.sort(reverse=True)

    bin_counter = 0
    for item, weight in enumerate(items):
        packed = False

        lightest_bin_node = bin_weights.min()

        if lightest_bin_node:
            lightest_bin = bins[lightest_bin_node.key.name]
            packed = lightest_bin.try_add_item(item, weight)

        if not packed:
            b = Bin(bin_counter)
            bin_counter += 1
            if not b.try_add_item(item, weight):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
            bin_weights.insert(b.weight, b.name)
        else:
            # Update the tree by removing the old bin weight, and adding the new one, still pointing to the same
            # index in the list of bins.
            bin_weights.remove(lightest_bin_node.key)
            bin_weights.insert(lightest_bin.weight, lightest_bin.name)

    return bins


def best_fit(items, decreasing=True):
    """
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    bins = []
    bin_counter = 0
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()
    # Sort - so this is actually best fit decreasing
    if decreasing:
        items.sort(reverse=True)

    for item, weight in enumerate(items):
        # The current weight of an optimal bin (ie, if this item is weight 6, we want a bin with weight 4)
        optimal_weight = Bin.CAPACITY - weight
        best_bin_node = bin_weights.find_largest_lessthan(optimal_weight)

        if not best_bin_node:
            new_bin = Bin(bin_counter)
            bin_counter += 1

            if not new_bin.try_add_item(item, weight):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(new_bin)
            bin_weights.insert(new_bin.weight, new_bin.name)
        else:
            best_bin = bins[best_bin_node.key.name]
            if not best_bin.try_add_item(item, weight):
                print('Error! Best bin did not have room for item!')
            else:
                bin_weights.remove(best_bin_node.key)
                bin_weights.insert(best_bin.weight, best_bin.name)

    return bins


def pack_and_print(items, algorithm, opt, print_contents=False):
    print('Packing using ' + algorithm.__name__)
    t = timer()
    bins = algorithm(items)
    end_t = timer() - t

    print('Took ' + str(round(end_t, 4)) + "s")
    sol = len(bins)
    print('Used {} bins compared to an optimal {}'.format(sol, opt))
    print('{} approx ratio for this instance is {}'
          .format(algorithm.__name__, round(sol / opt, 6)))

    if print_contents:
        for index, bin in enumerate(bins):
            print(bin)


def pack_print_all(items):
    print('----- Running all packing algorithms on input size ' + str(len(items)))
    # print('INPUT: ' + str(items))

    tw = sum(item for item in items)
    opt = math.ceil(tw / Bin.CAPACITY)
    print('Total weight is {} and capacity per-bin is {}, so an optimal solution would use at least {} bins'
          .format(tw, Bin.CAPACITY, opt))

    pack_and_print(items, next_fit, opt)
    pack_and_print(items, first_fit, opt)
    pack_and_print(items, best_fit, opt)


def random_list(min, max, length):
    result = []
    for x in range(0, length):
        result.append(random.randint(min, max))

    return result


INPUT_SIZE = 100000

worst_case_nf = [5, 1] * int(math.ceil(INPUT_SIZE / 2))
#pack_print_all(worst_case_nf)

onethird = int(math.ceil(INPUT_SIZE / 3))
worst_case_ff = [1/7 + 0.001] * onethird + [1/3 + 0.001] * onethird + [1/2 + 0.001] * onethird
pack_print_all(worst_case_ff)

#for i in range(10):
#    pack_print_all(random_list(1, 10, 100000))


