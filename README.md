# The Torchbearer

**Student Name:** Michael Dinh
**Student ID:** 132223907
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  It only tells us the cheapest cost from the starting node S (entrance) to each node. This doesn't explicitly determine the actual optimal order we should be visiting the relics before exiting, and could actually prevent a better route/optimal one since it doesn't track costs between relics.

- **What decision remains after all inter-location costs are known:**
  After they're known, the decision that remains is which relic chamber should be visited in what order starting from a selected first one.

- **Why this requires a search over orders (one sentence):**
  It requires a search over orders because different orders of visiting chambers result in different total fuel costs, even if all the shortest path distances are known already.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| S | S is the starting point at entrance and we want to find the shortest path cost from the entrance to each node |
| R | R is shortest path from the relics (r_i) to other ones using dijkstra to get shortest paths between relics |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | nested dict |
| What the keys represent | The outer keys are the the source nodes (spawn/relic) and inner ones are destination nodes |
| What the values represent | They represent the shortest fuel cost from source node to destination node |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Because dictionary key lookups use hash tables which query a constant number of times |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k+1
- **Cost per run:** O(mlogn)
- **Total complexity:** O((k+1) * mlogn)
- **Justification (one line):** Because each dijkstra algorthim run runs once from start node S and also for each of the relic nodes, which we multiply given that each run is independent.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  - Distance values are already at the shortest since the other edge weights are nonnegative.
  - Other paths would go through unfinalized nodes that either have equal or larger distance.

- **For nodes not yet finalized (not in S):**
  - These are estimated best distances found so far from using paths through finalized nodes.
  - Can still be improved upon if a shorter distance is found later.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  - Source has distance 0, other nodes have inf since no other paths found yet.
  - Since no nodes are finalized, the invariant holds.

- **Maintenance : why finalizing the min-dist node is always correct:**
  - All edge weights are nonnegative, so any other path through an unfinalized node can't be shorter the dist already finalized.

- **Termination : what the invariant guarantees when the algorithm ends:**
  - All reachable finalized nodes will have the shortest path distance from the source, and unreachable ones will stay at inf.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

Shortest path distances obtained from dijkstra ensure that the travel costs between the spawn, relics, and exit are correct, which allows for getting total fuel calculations from relic orders valid.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Greedy can fail because going to nearest unvisited relic won't always be the optimal choice for total fuel cost.
- **Counter-example setup:** (based off spec in assignment) Start S, exit T, Relics: B, C, D. 
  - S->B=1 is cheapest with cost 1, C and D cost 2.
- **What greedy picks:** Greedy picks B since cheapest cost.
- **What optimal picks:** S, B, D, C, T. S->B=1, B->D=1, D->C=1, C->T=1, total cost = 4
- **Why greedy loses:** Greedy chooses based off immediate cost, which could result in expensive costs later.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- Must explore different relic order visits since they each can produce different total fuel costs depending on order.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- lecture notes
- https://stackoverflow.com/questions/37350450/why-is-a-list-access-o1-in-python
