# This code is copied from an article i wrote here:
# https://www.section.io/engineering-education/the-knapsack-problem/


import numpy as np


def default_knapsack(w, v, max_weight):
    # This initializes our table with the base cases to 0.
    w = [None] + w  # Make the first element None
    v = [None] + v  # Make the first element None
    k = np.array([[0] * (max_weight + 1)] * (len(w)))

    # Loop though all elements of the table, ignoring the base cases
    for i in range(1, len(w)):  # each row
        for j in range(1, max_weight + 1):  # each column
            if w[i] <= j:
                k[i, j] = max(v[i] + k[i - 1, j - w[i]], k[i - 1, j])
            else:
                k[i, j] = k[i - 1, j]
    # Return the table. As the table will be used to reconstruct the solution.
    # The optimal value can be found at the element k[len(w), max_weight]
    return k


def recover_solution_default(k, w):
    w = [None] + w  # Make the first element None
    i = k.shape[0] - 1
    j = k.shape[1] - 1

    solution = []
    while i > 0 and j > 0:
        # Does not adding item i give us the solution?
        if k[i, j] == k[i - 1, j]:
            i -= 1
        else:
            # Or does adding item i give us the solution
            # In this case we want to the the corresponding index to solution
            solution.append(i-1)
            j -= w[i]
            i -= 1
    # FLip solution because we added things backwards
    return solution[::-1]


def alternative_knapsack(w, v):
    # Must assume all values of v > 0 and values of w are < max_weight
    w = [None] + w  # Make the first element None
    v = [None] + v  # Make the first element None
    M = np.array([[0]*(sum(v[1:]) + 1)]*(len(w)))

    for i in range(1, len(w)):
        for V in range(1, sum(v[1:i+1]) + 1):
            if V > sum(v[1:i]):
                M[i, V] = w[i] + M[i-1, V-v[i]]
            else:
                M[i, V] = min(M[i-1, V], w[i] + M[i-1, max(0, V-v[i])])
    # optimal value is the biggest index j such that m[n, j] <= max_weight
    return M


def recover_solution_alternative(M, w, v, max_weight):
    i = M.shape[0] - 1
    V = M.shape[1] - 1
    while M[i, V] > max_weight:
        V -= 1

    w = [None] + w  # Make the first element None
    v = [None] + v  # Make the first element None

    solution = []
    while i > 0 and V > 0:
        if M[i, V] == w[i] + M[i - 1, max(0, V - v[i])]:
            solution.append(i-1)
            V = max(0, V - v[i])
        i -= 1
    # FLip solution because we added things backwards
    return solution[::-1]


def knapsack_approx(w, v, max_weight,  eps):
    b = eps/(2*len(w)) * max(v)
    v_p = [int(v[i]/b) for i in range(len(v))]
    return recover_solution_alternative(alternative_knapsack(w, v_p), w, v_p, max_weight)


def knapsack(w, v, max_weight, override_default_only=False):
    if sum(v) < max_weight and not override_default_only:
        subset = recover_solution_alternative(alternative_knapsack(w, v), w, v, max_weight)
    else:
        subset = recover_solution_default(default_knapsack(w, v, max_weight), w)
    opt_val = sum([v[i] for i in subset])
    return opt_val, subset

