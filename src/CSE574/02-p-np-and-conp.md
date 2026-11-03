---
title: "P, NP, and coNP"
author: ""
tags: [CSE574, P, NP, coNP, EXP]
draft: false
---

# P, NP, and coNP

## P and NP

$$
\begin{aligned}
\mathrm{DTIME}(T)&=\{L:L\text{ decided deterministically in }O(T(n))\},\\
\mathrm{NTIME}(T)&=\{L:L\text{ decided nondeterministically in }O(T(n))\},\\
\mathrm P&=\bigcup_{c\ge1}\mathrm{DTIME}(n^c),\qquad
\mathrm{NP}=\bigcup_{c\ge1}\mathrm{NTIME}(n^c).
\end{aligned}
$$

NP = polynomial-time verification. Polynomial $p$, polynomial-time $V$:

$$
x\in L\iff\exists u\in\{0,1\}^{p(|x|)}:\ V(x,u)=1.
$$

- $u$: witness/certificate; shorter witnesses can be padded.
- Machine → verifier: witness records accepting choices.
- Verifier → machine: guess witness, then check.

| Problem | Algorithm or certificate |
| --- | --- |
| Primality | Polynomial-time algorithm; in P |
| Connectivity | BFS/DFS; in P |
| Rational linear programming | Polynomial-time feasibility algorithm; in P |
| Independent Set | $\ge k$ vertices; no edges within |
| Decision-TSP | Tour of cost $\le B$ |
| Graph Isomorphism | Vertex bijection preserving edges/nonedges |
| Bounded factoring | $d\mid N$, $2\le d<N$, $d\le k$ |

Last four: polynomial-time certificate checks, hence in NP. Prime factor in $[a,b]$: also check primality and interval.

Independent set of size $k$ ⇔ size at least $k$; not maximum size exactly $k$.

## coNP

$$
\overline L=\{0,1\}^*\setminus L,\qquad
\mathrm{coNP}=\{L:\overline L\in\mathrm{NP}\}.
$$

$\operatorname{coNTIME}(T)$ defined the same way from NTIME.

NP: certificates for yes. coNP: certificates for no. P is closed under complement:

$$
\mathrm P\subseteq\mathrm{NP}\cap\mathrm{coNP}.
$$

Equivalently, polynomial-length $u$ and polynomial-time $W$:

$$
x\in L\iff\forall u\;W(x,u)=1.
$$

Take $W=1-V$ for a verifier of $\overline L$.

P = NP, NP = coNP, P = NP $\cap$ coNP: all open. P = NP implies all equal; NP = coNP need not imply P = NP by any known result.

## Exponential time

$$
\mathrm E=\bigcup_{c\ge1}\mathrm{DTIME}(2^{cn}),\qquad
\mathrm{EXP}=\bigcup_{c\ge1}\mathrm{DTIME}(2^{n^c}).
$$

$$
\mathrm P\subseteq\mathrm{NP}\subseteq\mathrm{EXP}.
$$

NP simulation: enumerate $2^{p(n)}$ witnesses; polynomial verification each. Total $2^{n^{O(1)}}$.

$2^{\sqrt n}=2^{o(n)}$: superpolynomial, subexponential. See [Hierarchy theorems](04-hierarchy-theorems.md).

Sources: [Lecture 2](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture02/lecture02-Zhengjie-Min.pdf>); [Lecture 3, Hsieh](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture03/lecture03-Hsieh-Benjamin.pdf>); [Lecture 3, Shah](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture03/lecture03-Shah-Namita.pdf>); [Lecture 4, Du](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture04/lecture04-Du-Weining.pdf>).
