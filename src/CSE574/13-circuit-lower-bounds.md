---
title: "Circuit Lower Bounds"
author: ""
tags: [CSE574, circuits, lower-bounds, Karp-Lipton]
draft: false
---

# Circuit Lower Bounds

Circuit size and P/poly: [Circuits and advice](12-circuits-and-advice.md).

## Karp-Lipton

$$
\boxed{\mathrm{NP}\subseteq\mathrm{P/poly}
\Rightarrow\mathrm{PH}=\Sigma_2^{\mathrm P}.}
$$

Enough to show $\Pi_2^{\mathrm P}\subseteq\Sigma_2^{\mathrm P}$. Consider

$$
\forall u\;\exists v\;\varphi(u,v)=1.
$$

Under the assumption, SAT has polynomial-size circuits. Self-reduction gives polynomial-size **search** circuits: fix witness bits one at a time, querying whether a completion exists.

Guess a search circuit $C$; check its output directly:

$$
\forall u\;\exists v\;\varphi(u,v)=1
\iff
\exists C\;\forall u\;\varphi(u,C(u))=1.
$$

$C$ has a fixed polynomial size bound; $\varphi$ is hardwired. Right side is a $\Sigma_2^{\mathrm P}$ predicate.

- True formula: a correct search circuit works for every $u$.
- False formula: some $u$ has no witness; every circuit fails there.

No need to certify $C$ on unrelated SAT instances.

Thus $\Sigma_2^{\mathrm P}=\Pi_2^{\mathrm P}$, so PH collapses.

$$
\mathrm{NP}\nsubseteq\mathrm{P/poly}\Rightarrow\mathrm P\ne\mathrm{NP}.
$$

The converse is not known.

## Counting circuits

For $n$ input bits:

$$
\#\text{Boolean functions}=2^{2^n}.
$$

A fan-in-two circuit of size $s\geq n$ has an $O(s\log s)$-bit description. Hence

$$
\#\text{circuits of size at most }s\leq 2^{O(s\log s)}.
$$

Take $s=c2^n/n$ for a sufficiently small constant $c$. Fewer circuits than functions:

$$
\boxed{\text{Some functions require }\Omega(2^n/n)\text{ gates}.}
$$

In fact, almost all do. Counting gives no explicit hard language in NP.

The DNF upper bound is $O(n2^n)$: one term per accepting input.

### Nonuniform hierarchy: example

$$
\mathrm{SIZE}(n)\subsetneq\mathrm{SIZE}(n^2).
$$

Let $m=\lceil1.1\log_2n\rceil$. Choose a hard $m$-bit function $f_m$; set $g_n(x)=f_m(x_1,\ldots,x_m)$.

- DNF upper bound: $O(m2^m)<n^2$.
- Counting lower bound: $\Omega(2^m/m)>n$.

Fixing unused inputs preserves the lower bound. Adjust finitely many small lengths.

Sources: [Chapter 6](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 06.pdf>).
