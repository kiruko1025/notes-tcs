---
title: "Computation and Turing Machines"
author: ""
tags: [CSE574, computation, Turing-machines, undecidability]
draft: false
---

# Computation and Turing Machines

## Computation

- Church–Turing thesis: effective computability = TM computability.
- Extended thesis: efficient simulation of reasonable models; classical and quantum versions differ.
- Upper bound: one algorithm. Lower bound: every algorithm.
- Resources: time, space, randomness, samples, communication, oracle calls.

Language $L\subseteq\{0,1\}^*$; $x\in L$ means yes. A decider halts on every input.

Input size $n=|x|$, not the encoded number. Binary $N$ has $\Theta(\log N)$ bits; $O(N)$ time may be exponential in $n$.

## Turing machines

Model: $M=(\Gamma,Q,\delta)$.

$$
\delta:Q\times\Gamma\to Q\times\Gamma\times\{L,S,R\}.
$$

Finite alphabet/states; blank symbol; start/accept/reject states. Tape infinite both ways. Each step: read, change state, write, move.

**Palindrome:** erase first bit, remember it in state, scan right, compare/erase last bit, return left. Repeat; accept when empty or one bit remains. Worst case $\Theta(n^2)$.

Two tapes: copy input; compare forward/backward in $O(n)$. Fixed $k$ tapes, time $T$: one-tape simulation in $O(T^2)$.

**NTM:** two possible transition functions $\delta_0,\delta_1$. Accept if some branch accepts; reject if all reject. Time bound applies to every branch. Nondeterminism is not randomness.

## Undecidability

**Counting:** TMs countable; languages $\mathcal P(\{0,1\}^*)$ uncountable. Some languages have no decider.

**Diagonal language:** enumerate TMs by binary strings.

$$
L_{\mathrm{diag}}=\{\alpha:M_\alpha\text{ does not accept }\alpha\}.
$$

If $M_\alpha$ decided it, then

$$
\alpha\in L_{\mathrm{diag}}
\iff M_\alpha\text{ accepts }\alpha
\iff\alpha\notin L_{\mathrm{diag}}.
$$

**HALT undecidable:** a halting decider would decide $L_{\mathrm{diag}}$. Query whether $M_\alpha(\alpha)$ halts. No → accept. Yes → run it and invert its answer.

Hierarchy diagonalization adds a clock, making the diagonal language decidable.

Sources: [Lecture 2](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture02/lecture02-Zhengjie-Min.pdf>); [Discussion 1](</home/everett/Desktop/Umich-EECS/CSE574/discussions/disc01.pdf>); [Discussion 2](</home/everett/Desktop/Umich-EECS/CSE574/discussions/disc02.pdf>).
