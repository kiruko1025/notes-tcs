---
title: "Time-Space Tradeoffs"
author: ""
tags: [CSE574, time, space, SAT]
draft: false
---

# Time-Space Tradeoffs

## Simulating time with less space

Deterministic multitape TMs, $t(n)\ge n$:

$$
\mathrm{DTIME}(t(n))
\subseteq\mathrm{SPACE}\!\left(\frac{t(n)}{\log t(n)}\right)
\qquad\text{(Hopcroft–Paul–Valiant)}.
$$

Williams (2025):

$$
\mathrm{DTIME}(t(n))
\subseteq\mathrm{SPACE}\!\left(\sqrt{t(n)\log t(n)}\right).
$$

The logarithm is inside the square root. [Original theorem, §1](https://people.csail.mit.edu/rrw/time-vs-space.pdf).

## SAT lower bound

$\mathrm{TISP}(t,s)$: one deterministic machine uses time $O(t)$ **and** space $O(s)$.

For $a\ge1$, $b>0$, and $a(a+b)/2<1$,

$$
\mathrm{SAT}\notin\mathrm{TISP}(n^a,n^b).
$$

Example: $a=1.1$, $b=0.1$. This also rules out simultaneous linear time and logarithmic space.

$\Sigma_2\mathrm{TIME}(t)$: existential/universal strings of length $O(t)$, checked in time $O(t)$.

Proof skeleton. Assume $\mathrm{NTIME}(n)\subseteq\mathrm{TISP}(n^a,n^b)$. Put $k=(a+b)/2$; choose constant $r$ with $rk\ge1$.

1. Padding gives $\mathrm{NTIME}(n^r)\subseteq\mathrm{TISP}(n^{ra},n^{rb})$.
2. Guess $n^{r(a-b)/2}$ checkpoints. Universally choose a consecutive pair; simulate its segment. Total checkpoint data and segment time are both $n^{rk}$, up to logs.
3. The assumption gives $\mathrm{NTIME}(n)\subseteq\mathrm{DTIME}(n^a)$. Use this to decide the universal counterexample query deterministically.

Thus

$$
\mathrm{NTIME}(n^r)
\subseteq\Sigma_2\mathrm{TIME}(n^{rk+o(1)})
\subseteq\mathrm{NTIME}(n^{ark+o(1)}).
$$

But $ark<r$, contradicting the nondeterministic time hierarchy.

Transfer to SAT: near-linear Cook–Levin reduction, with output bits computed on demand. The strict exponent inequality absorbs polylogarithmic overhead. The condition $rk\ge1$ covers reading the input.

Sources: [Lecture 11](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture11/lecture11-Frieler-Nicholas.pdf>); [Discussion 5](</home/everett/Desktop/Umich-EECS/CSE574/discussions/disc05.pdf>); [Chapter 5](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 05.pdf>).
