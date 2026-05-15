"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Michael Dinh
Student ID:   132223907

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return (
        "- Why a single shortest-path run from S is not enough:\n"
        "It only tells us the cheapest cost from the starting node S (entrance) to each node. This doesn't explicitly determine the actual optimal order we should be visiting the relics before exiting, and could actually prevent a better route/optimal one since it doesn't track costs between relics.\n\n"
        "- What decision remains after all inter-location costs are known:\n"
        "After they're known, the decision that remains is which relic chamber should be visited in what order starting from a selected first one.\n\n"
        "- Why this requires a search over orders (one sentence):\n"
        "It requires a search over orders because different orders of visiting chambers result in different total fuel costs, even if all the shortest path distances are known already.\n\n"
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    #list of sources
    sources = [spawn]

    #adding each relic to the source nodes list
    for relic in relics:
        #if relic isn't already in sources list, add it
        if relic not in sources:
            sources.append(relic)

    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    #initialize distances for all nodes as inf
    dist = {u: float('inf') for u in graph}

    #source node starts at distance 0
    dist[source] = 0

    #priority queue for dijkstra alg, (distance, node)
    pq = [(0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        #if popped distance is worse than current known one, skip it
        if curr_dist > dist[u]:
            continue

        #exploring neighbors of current node
        for v, weight in graph[u]:
            new_dist = curr_dist + weight

            #if new distance is shorter, update and add to pq
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    #calling select_sources for list of spawns and each relics
    sources = select_sources(spawn, relics, exit_node)
    #initializing table for distances
    dist_table = {}

    #run dijkstra for each source and then store them in dist_table
    for source in sources:
        dist_table[source] = run_dijkstra(graph, source)

    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return (
        "- For nodes already finalized (in S):\n"
        "  - Distance values are already at the shortest since the other edge weights are nonnegative.\n"
        "  - Other paths would go through unfinalized nodes that either have equal or larger distance.\n\n"
        "- For nodes not yet finalized (not in S):\n"
        "  - These are estimated best distances found so far from using paths through finalized nodes.\n"
        "  - Can still be improved upon if a shorter distance is found later.\n\n"
        "- Initialization : why the invariant holds before iteration 1:\n"
        "  - Source has distance 0, other nodes have inf since no other paths found yet.\n"
        "  - Since no nodes are finalized, the invariant holds.\n\n"
        "- Maintenance : why finalizing the min-dist node is always correct:\n"
        "  - All edge weights are nonnegative, so any other path through an unfinalized node can't be shorter the dist already finalized.\n\n"
        "- Termination : what the invariant guarantees when the algorithm ends:\n"
        "  - All reachable finalized nodes will have the shortest path distance from the source, and unreachable ones will stay at inf.\n\n"
        "Shortest path distances obtained from dijkstra ensure that the travel costs between the spawn, relics, and exit are correct, which allows for getting total fuel calculations from relic orders valid.\n"
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
        "- The failure mode:\n"
        "Greedy can fail because going to nearest unvisited relic won't always be the optimal choice for total fuel cost.\n\n"
        "- Counter-example setup: (based off spec in assignment) Start S, exit T, Relics: B, C, D.\n"
        "S->B=1 is cheapest with cost 1, C and D cost 2.\n\n"
        "- What greedy picks:\n"
        "Greedy picks B since cheapest cost.\n\n"
        "- What optimal picks:\n"
        "S, B, D, C, T. S->B=1, B->D=1, D->C=1, C->T=1, total cost = 4\n\n"
        "- Why greedy loses:\n"
        "Greedy chooses based off immediate cost, which could result in expensive costs later.\n\n"
        "- What the Algorithm Must Explore:\n"
        "Must explore different relic order visits since they each can produce different total fuel costs depending on order.\n"
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    #set of relics remaining to visit
    relics_remaining = set(relics)

    #this stores best cost and relic order found so far, initialized to inf at start
    best = [float('inf'), []]

    #start exploring using recursive search
    _explore(dist_table, spawn, relics_remaining, [], 0, exit_node, best)

    return best[0], best[1]


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    #base case, if no more relics left, calc total cost to exit and update best if better
    if not relics_remaining:
        #tally up cost to exit from curr location
        total_cost = cost_so_far + dist_table[current_loc][exit_node]

        #if total cost better than best, update best w/ new cost and relic order
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = relics_visited_order.copy()
        return
    
    #Pruning condition
    lower_bound = cost_so_far + dist_table[current_loc][exit_node]

    if lower_bound >= best[0]:
        #this pruning condition is safe bc the lower bound represents the best possible total cost we could achieve from this point onward (even if we magically visited all remaining relics for free and went straight to the exit). 
        #if this best case scenario is still worse than the best solution we've already found, then we can skip because it can't be better than the current one.
        return

    #recursive case, try visiting each remaining relic and explore more
    for relic in list(relics_remaining):
        travel_cost = dist_table[current_loc][relic]

        #skip the relic if it isn't reachable from current location
        if travel_cost == float('inf'):
            continue

        relics_remaining.remove(relic) #backtracking, remove relic from remaining set
        relics_visited_order.append(relic) #backtracking, add relic to visited order

        _explore(dist_table, relic, relics_remaining, relics_visited_order, cost_so_far + travel_cost, exit_node, best)

        relics_visited_order.pop() #backtracking, remove relic from visited order
        relics_remaining.add(relic) #backtracking, add relic back to remaining set


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    #precompute all the shortest path distances
    dist_table = precompute_distances(graph, spawn, relics, exit_node)

    #find optimal route
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
