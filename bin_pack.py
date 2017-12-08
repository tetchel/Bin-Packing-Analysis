import math
from timeit import default_timer as timer
from copy import deepcopy

from binary_tree import BinaryTree


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


def next_fit(items, decreasing):
    """
    Runtime: O(n)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    # With next fit, sorting can actually make the solution considerably worse.
    if decreasing:
        items.sort(reverse=True)

    bins = []
    bin_index = 0
    b = Bin(bin_index)
    bin_index += 1
    bins.append(b)
    for item, weight in enumerate(items):
        if not b.try_add_item(item, weight):
            b = Bin(bin_index)
            bin_index += 1
            if not b.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)

    return bins

def first_fit(items, decreasing, existing_bins=None):
    """
    Runtime: O(n**2)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    if decreasing:
        items.sort(reverse=True)

    if existing_bins is None:
        bins = []
    else:
        bins = existing_bins

    bin_index = 0
    for index, item in enumerate(items):
        packed = False
        for b in bins:
            if b.try_add_item(index, item):
                packed = True
                break
        if not packed:
            b = Bin(bin_index)
            bin_index += 1
            if not b.try_add_item(index, item):
                print('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
    return bins


def set_epsilon(eps):
    global epsilon
    epsilon = eps


def ptas_awf(items, descending):     # Descending is ignored, but we accept it because pack_and_print will pass it
    print('Running PTAS with epsilon={}'.format(epsilon))

    small_items = []
    large_items = []
    for item in items:
        if item > epsilon / 2:
            large_items.append(item)
        else:
            small_items.append(item)

    large_packed = almost_worst_fit(large_items, True)
    return almost_worst_fit(small_items, True, large_packed)


def almost_worst_fit(items, decreasing, existing_bins=None):
    """
    Runtime: O(n*logn)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    if decreasing:
        items.sort(reverse=True)

    if existing_bins:
        bins = existing_bins
    else:
        bins = []
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()

    bin_counter = 0
    for item, weight in enumerate(items):
        packed = False

        second_lightest_bin_node = bin_weights.second_min()

        if second_lightest_bin_node:
            lightest_bin = bins[second_lightest_bin_node.key.name]
            packed = lightest_bin.try_add_item(item, weight)

        if not packed:
            b = Bin(bin_counter)
            bin_counter += 1
            if not b.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(b)
            bin_weights.insert(b.weight, b.name)
        else:
            # Update the tree by removing the old bin weight, and adding the new one, still pointing to the same
            # index in the list of bins.
            bin_weights.remove(second_lightest_bin_node.key)
            bin_weights.insert(lightest_bin.weight, lightest_bin.name)

    return bins


def best_fit(items, decreasing, existing_bins=None):
    """
    Runtime: O(nlogn)
    :param items: List of integer item weights, each less than Bin.CAPACITY
    :param decreasing: Whether or not to sort the items by non-increasing weights before packing
    :param existing_bins: The algorithm can run on an already-packed set of bins, for supporting the PTAS.
    :return: A list of 'bins', each a list of items contained in that bin.
    """

    # Sort - so this is actually best fit decreasing
    if decreasing:
        items.sort(reverse=True)

    if existing_bins:
        bins = existing_bins
    else:
        bins = []

    bin_counter = 0
    # The tree nodes' VALUES are the bin weight (this is what it is sorted by)
    # Each node's NAME is the bin index (in bins[]) that has that weight
    bin_weights = BinaryTree()

    for item, weight in enumerate(items):
        # The current weight of an optimal bin (ie, if this item is weight 6, we want a bin with weight 4)
        optimal_weight = Bin.CAPACITY - weight
        best_bin_node = bin_weights.find_largest_lessthan(optimal_weight)

        if not best_bin_node:
            new_bin = Bin(bin_counter)
            bin_counter += 1

            if not new_bin.try_add_item(item, weight):
                raise Exception('Error! Could not add item into empty bin. Is the item larger than the bin?')
            bins.append(new_bin)
            bin_weights.insert(new_bin.weight, new_bin.name)
        else:
            best_bin = bins[best_bin_node.key.name]
            if not best_bin.try_add_item(item, weight):
                raise Exception('Error! Best bin did not have room for item!')
            else:
                bin_weights.remove(best_bin_node.key)
                bin_weights.insert(best_bin.weight, best_bin.name)
                #print('Update: name {}, weight {}, to name {}, weight {}'
                #      .format(best_bin_node.key.name, best_bin_node.key.value, best_bin.name, best_bin.weight))

    return bins


def pack_and_print(items, algorithm, outfile, descending):
    # print(items)
    tw = sum(item for item in items)
    opt = math.ceil(tw / Bin.CAPACITY)
    print('Total weight is {} and capacity per-bin is {}, so an optimal solution would use at least {} bins'
          .format(round(tw, 6), Bin.CAPACITY, opt))

    name = algorithm.__name__
    print('Packing {} items using {}, descending={}'.format(len(items), name, descending))
    # Copy items so that the algorithm's changes to the list don't persist
    items_copy = deepcopy(items)

    t = timer()
    bins = algorithm(items_copy, descending)
    elapsed = round(timer() - t, 6)

    print('Took ' + str(elapsed) + "s")
    sol = len(bins)
    print('Used {} bins compared to a best-case optimal of {}'.format(sol, opt))
    ratio = round(sol / opt, 6)
    print('{} approx ratio for this instance is {}'.format(name, ratio))

    with open(outfile, 'a') as f:
        f.write("{}, {}, {}, {}, {}, {}, {}\n"
                .format(name, descending, len(items), elapsed, sol, opt, ratio))
"""
    for index, b in enumerate(bins):
        print(b)
"""

def pack_print_all(items, outfile):
    pack_and_print(items, next_fit, outfile, False)
    pack_and_print(items, almost_worst_fit, outfile, False)
    # pack_and_print(items, best_fit, outfile, False)

    pack_and_print(items, next_fit, outfile, True)
    pack_and_print(items, almost_worst_fit, outfile, True)
    pack_and_print(items, best_fit, outfile, True)

