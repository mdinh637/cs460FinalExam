# Development Log – The Torchbearer

**Student Name:** Michael Dinh
**Student ID:** 132223907
> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [5/13/26]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

## Entry 1 – May 13, 2026: Initial Plan

I'll first break down the graph problem and understand its parts regarding the shortest path and searching of possible relic orders for the shortest distance. I'll implement everything in the given order as listed in the assignment and files step by step, and then build on from there (starting with Dijkstra's algorithm). I think the most difficult part would be actually finding the optimal relic order. For testing, I'll utilize the already provided test cases, and then potentially make some other graphs just to check for things like relics that aren't reachable, or cases where there's only one relic.

---

## Entry 2 – [May 14, 2026]: [Finished Part 2]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

I followed the assignment guidelines and filled in the corresponding parts in the torchbearer.py, then doing the README section for part 2. Part 1 was very simple, tried testing and noticed that I couldn't run because there were still passes passing through to the test functions, so I did some of my own testing. 

---

## Entry 3 – [5/14/26]: [Parts 3-5]

I got mixed up a bit from the wording at part 5. I noticed some contradictions in the torchbearer.py and the readme, where it wanted us to implement relics_remaining, but in the readme 5a it said relics already visited, which would be relics_visited_order. Thankfully, I checked the class discord hw help section and saw someone else had the same confusion and turns out it didn't matter since both work. I chose to stick with using relics_remaining since it was the structure already in torchbearer.py for recursive search.

---

## Entry 4 – [5/14/26]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

I would definitely choose to start this earlier so that I wouldn't have to grind for a whole day to get it done. If I had more time, I would probably improve on the pruning logic of my code since it only estimates part of the remaining route cost. Maybe there's a way to get to consider even cheaper options to reduce how many branches it explores overall.

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | 2 |
| Part 3: Algorithm Correctness | 1 |
| Part 4: Search Design | 1/2 |
| Part 5: State and Search Space | 1 |
| Part 6: Pruning | 1 |
| Part 7: Implementation | 7-8 hours |
| README and DEVLOG writing | 2 |
| **Total** | 8 1/2 |
