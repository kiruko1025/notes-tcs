---
title: "Oracles and Relativization"
author: ""
tags: [CSE574, oracles, relativization]
draft: false
---

# Oracles and Relativization

## Oracle machines

Oracle $O\subseteq\{0,1\}^*$. Machine $M^O$ writes $q$, then learns whether $q\in O$ in one oracle step.

Writing queries still costs time. Polynomial time permits polynomially many queries of polynomial length. Answers are fixed by $O$.

$$
O\in\mathrm P^O,\qquad
\mathrm P\subseteq\mathrm P^O\subseteq\mathrm{NP}^O.
$$

$O\in\mathrm P\Rightarrow\mathrm P^O=\mathrm P$, $\mathrm{NP}^O=\mathrm{NP}$: simulate each query.

$\mathrm{TAUTOLOGY}\in\mathrm P^{\mathrm{SAT}}$: ask whether the negated formula is satisfiable; reverse the answer. Thus $\mathrm{coNP}\subseteq\mathrm{NP}^{\mathrm{SAT}}$.

## Equality oracle

Let

$$
A=\{\langle M,x,1^m\rangle:
M\text{ deterministically accepts }x\text{ within }2^m\text{ steps}\}.
$$

$$
\mathrm{EXP}\subseteq\mathrm P^A
\subseteq\mathrm{NP}^A\subseteq\mathrm{EXP}.
$$

- $A\in\mathrm E$: input length $N\ge m$; simulate in $2^{O(N)}$ time.
- $L\in\mathrm{EXP}$: if $M$ takes $2^{p(n)}$ steps, query $\langle M,x,1^{p(|x|)}\rangle$.
- $\mathrm{NP}^A\subseteq\mathrm{EXP}$: enumerate exponentially many branches; answer each polynomial-length query in exponential time.

Hence $\mathrm P^A=\mathrm{NP}^A=\mathrm{EXP}$.

## Separation oracle

$$
L_B=\{1^n:\exists y\in\{0,1\}^n,\ y\in B\}.
$$

$L_B\in\mathrm{NP}^B$: guess $y$, query $B$.

Enumerate deterministic oracle machines with polynomial clocks $(M_i,p_i)$. At stage $i$:

1. Choose fresh length $n$: no length-$n$ membership fixed; $p_i(n)<2^n$.
2. Run $M_i^B(1^n)$ for $p_i(n)$ steps. Respect fixed answers; permanently answer every new query **no**.
3. If it accepts, exclude every length-$n$ string from $B$.
4. Otherwise, add one unqueried length-$n$ string; exclude the rest.

An unqueried string exists: fewer than $2^n$ queries. Freeze that entire length. After all stages, exclude every undecided string.

Each stage fixes finitely many strings, so fresh lengths remain. No recorded answer changes; every simulated error survives in the final oracle.

$$
L_B\in\mathrm{NP}^B\setminus\mathrm P^B.
$$

## Relativization barrier

A proof **relativizes** if it works with every common oracle.

Baker–Gill–Solovay:

$$
\exists A:\mathrm P^A=\mathrm{NP}^A,
\qquad
\exists B:\mathrm P^B\ne\mathrm{NP}^B.
$$

Neither equality nor separation can follow from a fully relativizing proof. Resolving P versus NP needs a nonrelativizing ingredient. This does not exclude every use of diagonalization.

Bennett–Gill, stated only: if each string independently enters $O$ with probability $1/2$, then $\mathrm P^O\ne\mathrm{NP}^O$ almost surely.

Sources: [Lecture 6](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture06/lecture06-Huang-Heidi.pdf>); [Chapter 3](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 03.pdf>).
