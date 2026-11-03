---
title: "PSPACE-Completeness"
author: ""
tags: [CSE574, PSPACE, TQBF, completeness]
draft: false
---

# PSPACE-Completeness

Space bounds and configuration graphs: [Space complexity](08-space-complexity.md).

$B$ is PSPACE-hard if every PSPACE language reduces to $B$ in polynomial time. Complete = hard + in PSPACE.

## Bounded-space acceptance

$$
\mathrm{SPACE\text{-}TMSAT}
=\{\langle M,x,1^b\rangle:
M\text{ deterministically accepts }x\text{ within }b\text{ work cells}\}.
$$

- Membership: simulate; reject on exceeding the space bound or bounded configuration count. Store one configuration and a counter.
- Hardness: for a space-$p(n)$ decider $M_A$, map $x\mapsto\langle M_A,x,1^{p(|x|)}\rangle$.

Unary bound ensures polynomial space in the instance length.

A PSPACE-complete problem in P implies P = PSPACE, hence P = NP.

## Quantified Boolean formulas

$$
\Psi=Q_1x_1\cdots Q_kx_k\;\varphi(x_1,\ldots,x_k),
\qquad Q_i\in\{\exists,\forall\},\quad x_i\in\{0,1\}.
$$

All variables bound. Unlike PH's fixed levels, the number of alternating blocks may grow with the input.

SAT: all $\exists$. TAUTOLOGY: all $\forall$.

$$
\mathrm{TQBF}=\{\Psi:\Psi\text{ is true}\}
\quad\text{is PSPACE-complete.}
$$

### Membership

Evaluate one quantifier at a time:

$$
A(Qx\,\psi)=
\begin{cases}
A(\psi[x=0])\lor A(\psi[x=1])&Q=\exists,\\
A(\psi[x=0])\land A(\psi[x=1])&Q=\forall.
\end{cases}
$$

At a leaf, evaluate the Boolean formula. Run sibling calls sequentially.
For $k$ variables and formula length $m$:

$$
S(k,m)\le S(k-1,m)+O(m)=O(km).
$$

Polynomial space. Keeping one assignment and evaluating the original formula gives $O(m)$ space.

### Hardness

Let $L\in\mathrm{PSPACE}$, decided by $M$ in space $s(n)=\operatorname{poly}(n)$.
Configurations have $m=O(s(n))$ bits; at most $2^m$ configurations. Arrange one accepting configuration.

Construct a polynomial-size formula $\mathrm{Step}_{M,x}(u,v)$ checking one legal transition.

$$
\psi_i(u,v)\iff\text{a path of length at most }2^i\text{ goes from }u\text{ to }v.
$$

$$
\psi_0(u,v)=(u=v)\lor\mathrm{Step}_{M,x}(u,v).
$$

Savitch's recurrence:

$$
\psi_i(u,v)\equiv
\exists z\,[\psi_{i-1}(u,z)\land\psi_{i-1}(z,v)].
$$

Two copies per level give exponential formula size. Use universal selectors:

$$
\begin{aligned}
\psi_i(u,v):=\exists z\,\forall a\,\forall b\;[
&((a=u\land b=z)\lor(a=z\land b=v))\\
&\Longrightarrow\psi_{i-1}(a,b)].
\end{aligned}
$$

Each variable is an $m$-bit block; bound variables fresh at every level.

- $(a,b)=(u,z)$ checks the first half.
- $(a,b)=(z,v)$ checks the second half.
- Other pairs impose nothing.
- Only one copy of $\psi_{i-1}$.

$$
|\psi_i|\le|\psi_{i-1}|+O(m),
\qquad |\psi_m|\le|\psi_0|+O(m^2).
$$

Move fresh quantifiers to the front if needed. Polynomial-time reduction:

$$
x\in L\iff\psi_m(c_{\mathrm{start}},c_{\mathrm{accept}})\in\mathrm{TQBF}.
$$

The construction also works for nondeterministic configuration graphs:

$$
\mathrm{NPSPACE}\subseteq\mathrm{PSPACE},
\qquad\mathrm{PSPACE}=\mathrm{NPSPACE}.
$$

Sources: [Lecture 9, Nie](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture09/lecture09-Nie-Zinnia.pdf>); [Lecture 9, Menacho Ordonez](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture09/lecture09-MenachoOrdonez-Daniel.pdf>); [Lecture 10](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture10/lecture10-Chae-Yeonu.pdf>); [Chapter 4](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 04.pdf>).
