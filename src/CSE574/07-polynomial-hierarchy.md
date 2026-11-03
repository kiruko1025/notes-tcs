---
title: "The Polynomial Hierarchy"
author: ""
tags: [CSE574, polynomial-hierarchy, oracles]
draft: false
---

# The Polynomial Hierarchy

## Quantifiers

All quantified strings have polynomial length; $R$ is polynomial-time.

| Class | Membership condition |
| --- | --- |
| $\mathrm{NP}=\Sigma_1^{\mathrm P}$ | $\exists u\;R(x,u)=1$ |
| $\mathrm{coNP}=\Pi_1^{\mathrm P}$ | $\forall u\;R(x,u)=1$ |
| $\Sigma_2^{\mathrm P}$ | $\exists u\forall v\;R(x,u,v)=1$ |
| $\Pi_2^{\mathrm P}$ | $\forall u\exists v\;R(x,u,v)=1$ |

Order matters: $\forall v\exists u\;(u=v)$ is true for bits; $\exists u\forall v\;(u=v)$ is false.

For fixed $i\ge1$,

$$
x\in L\iff\exists u_1\forall u_2\cdots Q_i u_i\;
R(x,u_1,\ldots,u_i)=1
$$

defines $\Sigma_i^{\mathrm P}$. Start with $\forall$ for $\Pi_i^{\mathrm P}$. Count **blocks**, not variables; $i$ cannot grow with input length.

$$
\Sigma_0^{\mathrm P}=\Pi_0^{\mathrm P}=\mathrm P,
\qquad\Pi_i^{\mathrm P}=\operatorname{co}\Sigma_i^{\mathrm P}.
$$

Complement: flip quantifiers and negate $R$.

## Examples

### Exact independent set

Let $I(G,S)$ mean $S$ is independent. Then

$$
\alpha(G)=k\iff\exists S\forall T\;[
I(G,S)\land |S|=k\land
(|T|\ne k+1\lor\neg I(G,T))].
$$

Sets use vertex-incidence vectors. No size-$(k+1)$ set means no larger set.

Thus $\mathrm{EXACT\text{-}INDSET}\in\Sigma_2^{\mathrm P}\cap\Pi_2^{\mathrm P}$: the conditions on $S,T$ are independent, so their quantifiers can be swapped here. No separation from NP or coNP follows.

### Minimum equivalent CNF

Input: CNF $\varphi$, size bound $k$. Seek an equivalent CNF over the same variables:

$$
\exists\psi\forall a\;[
\psi\text{ valid},\ |\psi|\le k,\ \psi(a)=\varphi(a)].
$$

Hence $\mathrm{MIN\text{-}CNF}\in\Sigma_2^{\mathrm P}$. If $k\ge|\varphi|$, use $\varphi$; otherwise the witness has polynomial length.

Complement: every valid size-$\le k$ candidate has a counterexample assignment. Its form is $\forall\psi\exists a$, so it lies in $\Pi_2^{\mathrm P}$.

The same argument handles the handout's MIN-EQ-DNF.

## Containments

$$
\mathrm{PH}=\bigcup_{i\ge0}\Sigma_i^{\mathrm P}
=\bigcup_{i\ge0}\Pi_i^{\mathrm P}.
$$

Each language belongs to some fixed level. Add unused blocks to get

$$
\Sigma_i^{\mathrm P}\cup\Pi_i^{\mathrm P}
\subseteq\Sigma_{i+1}^{\mathrm P}\cap\Pi_{i+1}^{\mathrm P}.
$$

## Collapse

$$
\mathrm P=\mathrm{NP}\Longrightarrow\mathrm{PH}=\mathrm P.
$$

Induct on blocks. The inner predicate is in P by IH; guessing the first block gives NP = P. Complement for $\Pi_i^{\mathrm P}$.

More generally, for $i\ge1$,

$$
\Sigma_i^{\mathrm P}=\Pi_i^{\mathrm P}
\Longrightarrow\mathrm{PH}=\Sigma_i^{\mathrm P}.
$$

A $\Sigma_{i+1}^{\mathrm P}$ formula is $\exists u$ followed by a $\Pi_i^{\mathrm P}$ predicate. Rewrite that predicate in $\Sigma_i^{\mathrm P}$ form; merge the two leading existential blocks. Repeat.

In particular, NP = coNP collapses PH to NP; it does not establish P = NP.

## Complete problems

Polynomial-time many-one reductions. For fixed $i$, quantified Boolean circuits with $i$ alternating blocks are $\Sigma_i^{\mathrm P}$-complete:

$$
\exists u_1\forall u_2\cdots Q_i u_i\;C(u_1,\ldots,u_i)=1.
$$

- Membership: evaluate $C$ in polynomial time.
- Hardness: compile $R(x,\cdot)$ into a polynomial-size circuit; retain its prefix.
- Start universally for $\Pi_i^{\mathrm P}$-completeness.

Quantified formulas give complete problems too. CNF conversion needs correctly placed auxiliary quantifiers.

PH-complete language $K\in\Sigma_k^{\mathrm P}$ would imply PH $=\Sigma_k^{\mathrm P}$: reducing to $K$ adds no blocks. Thus PH has no complete problem unless it collapses.

Oracle machines: [Oracles and relativization](06-oracles-and-relativization.md).

## Oracle characterization

$$
\mathrm{NP}^{\mathcal C}=\bigcup_{A\in\mathcal C}\mathrm{NP}^A.
$$

One fixed oracle per machine. If $K$ is complete for $\mathcal C$, reduce every query to $K$:
$\mathrm{NP}^{\mathcal C}=\mathrm{NP}^K$.

For $i\ge2$ and $\Sigma_{i-1}^{\mathrm P}$-complete $A$,

$$
\Sigma_i^{\mathrm P}=\mathrm{NP}^A,
\qquad\Pi_i^{\mathrm P}=\mathrm{coNP}^A.
$$

$\mathrm{coNP}^A$ complements the accepted language, retaining oracle $A$.

### $\Sigma_2^{\mathrm P}\subseteq\mathrm{NP}^{\mathrm{SAT}}$

Given $x\in L\iff\exists u\forall v\;R(x,u,v)=1$:

1. Guess $u$.
2. Ask whether $\exists v\;R(x,u,v)=0$, encoded as SAT.
3. Accept iff the oracle says no.

### $\mathrm{NP}^{\mathrm{SAT}}\subseteq\Sigma_2^{\mathrm P}$

Existentially guess branch choices $c$, oracle answers $a_j$, and witnesses $u_j$ for claimed yes answers.

Replay using $c,a$ to recover queries $\varphi_j$. This preserves adaptive queries. Require an accepting replay and

$$
a_j=1\Rightarrow\varphi_j(u_j)=1,
\qquad
a_j=0\Rightarrow\varphi_j(v_j)=0.
$$

Universally quantify the tuple $\mathbf v$:

$$
x\in L\iff\exists(c,a,\mathbf u)\forall\mathbf v\;
R(x,c,a,\mathbf u,\mathbf v)=1.
$$

All data have polynomial length. Pad unused entries; malformed queries have answer no. A false no answer fails on a tuple containing its satisfying assignment. Thus every passing transcript uses correct answers.

Hence $\mathrm{NP}^{\mathrm{NP}}=\mathrm{NP}^{\mathrm{SAT}}=\Sigma_2^{\mathrm P}$.

Higher levels: combine yes checks in $\Sigma_{i-1}^{\mathrm P}$ and no checks in $\Pi_{i-1}^{\mathrm P}$ into at most $i$ blocks.
