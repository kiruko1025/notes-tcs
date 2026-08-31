---
title: Dynamic Programming
---

# Dynamic Programming

Dynamic programming is a method for solving complex problems by breaking them down into simpler subproblems. It is applicable when the subproblems are overlapping and can be solved independently.

## DP Recipe:

1. Define value version of what we want to compute
2. Derive a recurrence
3. Size of table: How many dimensions? Range of each dimension?
4. What are the base case(s)?
5. To fill in a cell, which other cells need to be filled already? In
which order do I fill the table?
6. Which cell(s) contain the final answer?
7. Running time is often (size of table)・(time to fill each entry)
8. To reconstruct the solution (instead of just its value) follow
arrows from final answer to base case.

# DP Patterns

## Linear DP

Recurrence: `dp[i] = dp[i-1] + dp[i-2] + ...` (depends on earlier indices)

Common Complexity: O(n)

Example: Fibonacci sequence, climbing stairs with 1 or 2 steps, max sum of non-adjacent numbers, counting ways to make change.

Pattern: How many ways / min cost to reach position $i$.

## Interval DP
Recurrence: `dp[i][j] = min/max over k (dp[i][k] + dp[k+1][j])` (depends on earlier intervals)

Common Complexity: O(n^3)

Example: Matrix chain multiplication, optimal binary search tree, palindrome partitioning.

Pattern: How to optimally split interval [i, j].

## Knapsack DP
Recurrence (1d or 2d): `dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])` (depends on previous items and weights)

Common Complexity: O(nW) or O(n^2)

Example: 0/1 Knapsack, unbounded knapsack, subset sum, partition array into two subsets with equal sum (sugar rush)

Pattern: How to maximize/minimize value/weight with given constraints.

## Sequence Alignment DP
Recurrence: `dp[i][j] = min(dp[i-1][j-1]+cost, dp[i-1][j]+1, dp[i][j-1]+1)` (compares prefixes of two sequences)

Common Complexity: O(nm)

Example: Longest common subsequence, edit distance, DNA matching.

Pattern: Compare two sequences by advancing one or both indices.

## Subsequence DP
