---
title: "AC0 and Parity"
author: ""
tags: [CSE574, AC0, parity, switching-lemma]
draft: false
---

# AC0 and Parity

Circuit classes: [Circuit depth and parallelism](14-circuit-depth-and-parallelism.md).

## Parity

$$
\operatorname{PARITY}_n(x)=x_1\oplus\cdots\oplus x_n
=\sum_{i=1}^n x_i\pmod2.
$$

Balanced XOR tree: $O(n)$ size, $O(\log n)$ depth. Each XOR uses constantly many AND/OR/NOT gates.

$$
\operatorname{PARITY}\in\mathrm{NC}^1\setminus\mathrm{NC}^0.
$$

Depth-$d$, fan-in-two output depends on at most $2^d$ inputs. Parity depends on all $n$.

Parity, majority, and threshold functions are symmetric: input order does not matter. A tree of majority gates does not compute majority in general.

## Normalizing AC0 circuits

Fixed depth, polynomial size, unbounded AND/OR fan-in:

1. Push NOT gates to inputs using De Morgan.
2. Duplicate shared subcircuits: internal fan-out one; literals may repeat.
3. Merge consecutive equal gates; arrange alternating AND/OR layers.

At constant depth, duplication keeps size polynomial. This need not hold at growing depth.

Depth two = CNF or DNF.

## Restrictions

A restriction $\rho\in\{0,1,*\}^n$ fixes some inputs. $*$ means free; $f|_\rho$ is the remaining function.

For parity:

$$
\operatorname{PARITY}_n|_\rho
=b\oplus\bigoplus_{i:\rho_i=*}x_i,
\qquad b=\bigoplus_{i:\rho_i\ne *}\rho_i.
$$

At least one free bit $\Rightarrow$ nonconstant.

A nonzero $k$-DNF can be forced to 1 by satisfying one term: fix at most $k$ variables. Dually, a non-tautological $k$-CNF can be forced to 0.

Therefore parity on $n>k$ bits is neither a $k$-DNF nor a $k$-CNF. Any DNF for parity needs $2^{n-1}$ full-width terms; likewise for CNF clauses.

## Switching lemma

Lemma and proof sketch from Chapter 14, §14.1.

Let $f$ be a $k$-DNF on $N$ variables. Choose $t$ variables uniformly and assign independent fair bits. For $s\geq2$:

$$
\Pr_\rho[f|_\rho\text{ is not an }s\text{-CNF}]
\leq
\left(\frac{(N-t)k^{10}}{N}\right)^{s/2}.
$$

Same bound with CNF/DNF exchanged, by complementation. Width changes; the function stays the same. Proof of the lemma: handout §14.1.2.

### Parity is not in AC0

Suppose a normalized depth-$d$, size-$n^b$ circuit computes parity. Add bottom fan-in-one gates if needed.

1. Leave about $\sqrt N$ of the current $N$ variables free.
2. Switch bottom $k$-DNFs to $s$-CNFs, or vice versa.
3. Merge the new top gates with the layer above: depth drops by one.
4. Repeat until depth two.

Choose successive widths as sufficiently large constants depending on $b,d$. The lemma and a union bound make all switches succeed with positive probability.

After constantly many rounds, $n^{\Omega(1)}$ variables remain; the final CNF/DNF has constant width $k$. Fix at most $k$ more variables to make it constant. Parity still has a free bit: contradiction.

$$
\boxed{\operatorname{PARITY}\notin\mathrm{AC}^0,
\qquad \mathrm{AC}^0\subsetneq\mathrm{NC}^1.}
$$
