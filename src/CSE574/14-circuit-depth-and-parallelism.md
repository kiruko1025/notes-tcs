---
title: "Circuit Depth and Parallelism"
author: ""
tags: [CSE574, circuits, NC, AC, parallelism]
draft: false
---

# Circuit Depth and Parallelism

## Depth: NC and AC

Depth = longest input-to-output path. All families below have polynomial size; $d$ is fixed.

| Class | Depth | AND/OR fan-in |
| --- | --- | --- |
| $\mathrm{NC}^d$ | $O(\log^d n)$ | 2 |
| $\mathrm{AC}^d$ | $O(\log^d n)$ | Unbounded |

NOT gates have fan-in one.

$$
\mathrm{NC}=\bigcup_{d\geq1}\mathrm{NC}^d,
\qquad
\mathrm{AC}=\bigcup_{d\geq0}\mathrm{AC}^d,
\qquad
\mathrm{NC}^d\subseteq\mathrm{AC}^d\subseteq\mathrm{NC}^{d+1}.
$$

Last inclusion: replace each unbounded gate by a balanced tree of depth $O(\log n)$. Thus $\mathrm{NC}=\mathrm{AC}$.

- $\mathrm{NC}^0$: each output depends on $O(1)$ inputs.
- $\mathrm{AC}^0$: constant depth; can compute AND of all $n$ inputs.
- Polynomial-size CNF/DNF evaluation fits depth two. This does not solve SAT.

Unqualified circuit classes here are **nonuniform**. For algorithms, require a logspace machine printing $C_n$ from $1^n$:

$$
\text{logspace-uniform NC}\subseteq\mathrm P.
$$

Uniform NC captures polynomially many processors and polylogarithmic parallel time. Uniform NC = P is open.

## P-completeness

In this section, NC means **logspace-uniform NC**.

$A$ is P-complete if $A\in\mathrm P$ and every $B\in\mathrm P$ satisfies $B\leq_\ell A$.

$$
\mathrm{CKT\text{-}EVAL}
=\{\langle C,x\rangle:C(x)=1\}
\quad\text{is P-complete}.
$$

- In P: evaluate gates in topological order.
- Hardness: unfold a polynomial-time computation into a circuit; generate its gate descriptions in logspace.

For P-complete $A$:

$$
\begin{aligned}
A\in\mathrm{NC}&\iff\mathrm P=\mathrm{NC},\\
A\in\mathrm L&\iff\mathrm P=\mathrm L.
\end{aligned}
$$

Use closure under logspace reductions; logspace functions have uniform $\mathrm{NC}^2$ circuits. Linear programming is another P-complete problem.
