---
title: "Diagonalization and Hierarchy Theorems"
author: ""
tags: [CSE574, diagonalization, hierarchy]
draft: false
---

# Diagonalization and Hierarchy Theorems

## Constructible bounds

- Time-constructible $t(n)\ge n$: produce $1^{t(n)}$ from $1^n$ in $O(t(n))$ time.
- Space-constructible $s(n)\ge\log n$: mark $s(n)$ work cells in $O(s(n))$ space.
- $f=o(g)$: $f(n)/g(n)\to0$.

Standard rounded polynomial/exponential bounds are constructible.

## Hierarchy theorems

Constructible bounds; $t_1,t_2\ge n$; $s_1,s_2\ge\log n$.

| Resource | Gap | Strict containment |
| --- | --- | --- |
| Deterministic time | $t_1\log t_1=o(t_2)$ | $\mathrm{DTIME}(t_1)\subsetneq\mathrm{DTIME}(t_2)$ |
| Nondeterministic time | $t_1(n+1)=o(t_2(n))$ | $\mathrm{NTIME}(t_1)\subsetneq\mathrm{NTIME}(t_2)$ |
| Deterministic space | $s_1=o(s_2)$ | $\mathrm{SPACE}(s_1)\subsetneq\mathrm{SPACE}(s_2)$ |

Time simulation: logarithmic overhead. Space simulation: constant overhead for each fixed machine.

## Diagonalization

Show $\mathrm{DTIME}(n)\subsetneq\mathrm{DTIME}(n^2)$.

Machine $D$, input $x$, $n=|x|$:

1. Decode $x$ as $M_x$; invalid code → reject.
2. Simulate $M_x(x)$ for $\lceil n^{3/2}\rceil$ universal-simulator steps.
3. Acceptance → reject; rejection/timeout → accept.

Clock bookkeeping gives $O(n^{3/2}\log n)\subseteq O(n^2)$ time.

Suppose linear-time $Q$ decides $L(D)$. Its simulation costs $O_Q(n\log n)$. Choose a sufficiently long padded description $x$ of $Q$. Simulation finishes, so

$$
D(x)=1-Q(x),
$$

contradicting $L(D)=L(Q)$. Padding changes the description length, not the machine.

### Consequences

- $\mathrm P\subsetneq\mathrm{EXP}$: $\mathrm P\subseteq\mathrm{DTIME}(2^n)$; separate $2^n$ from $2^{n^2}$.
- Space $s\ge\log n$: $2^{O(s)}$ configurations for a fixed machine. An $O(s)$-bit counter detects timeout before repetition.
- Nondeterministic acceptance cannot be complemented by swapping outcomes: “some branch accepts” becomes “some branch rejects,” not “all reject.”

Sources: [Lecture 5, Lee](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture05/lecture05-Lee-Amy.pdf>); [Lecture 5, Wanner](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture05/lecture05-Wanner-Alice.pdf>); [Lecture 4, Cho](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture04/lecture04-Cho-Geonwoo.pdf>); [Chapter 3](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 03.pdf>).
