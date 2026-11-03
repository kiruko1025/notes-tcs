---
title: "Denotational Semantics of IMP"
author: ""
tags: [CSE590]
draft: false
---

# Denotational Semantics of IMP

operational = execution rules

denotational = mathematical objects, defined compositionally

Meaning of a compound expression depends on meanings of its parts.

## Semantic brackets

States: $\Sigma=\mathrm{Var}\to\mathbb Z$.

$$
\begin{aligned}
{}[\![-]\!]_a&:\mathrm{AExp}\to(\Sigma\to\mathbb Z),\\
[\![-]\!]_b&:\mathrm{BExp}\to(\Sigma\to\{\mathsf{true},\mathsf{false}\}),\\
[\![-]\!]_c&:\mathrm{Com}\to(\Sigma\rightharpoonup\Sigma).
\end{aligned}
$$

Expressions: total. Commands: partial; loops may diverge.

### Arithmetic

$$
\begin{aligned}
{}[\![ n]\!]_a\sigma&=n,\\
[\![ x]\!]_a\sigma&=\sigma(x),\\
[\![ a_1+a_2]\!]_a\sigma
&=[\![ a_1]\!]_a\sigma+[\![ a_2]\!]_a\sigma.
\end{aligned}
$$

Left $+$: program syntax. Right $+$: integer addition. Other operators similarly.

### Booleans

$$
\begin{aligned}
{}[\![\mathsf{true}]\!]_b\sigma&=\mathsf{true},\\
[\![\mathsf{false}]\!]_b\sigma&=\mathsf{false},\\
[\![\neg b]\!]_b\sigma&=\neg[\![ b]\!]_b\sigma,\\
[\![ b_1\land b_2]\!]_b\sigma
&=[\![ b_1]\!]_b\sigma\land[\![ b_2]\!]_b\sigma,\\
[\![ a_1=a_2]\!]_b\sigma
&=([\![ a_1]\!]_a\sigma=[\![ a_2]\!]_a\sigma).
\end{aligned}
$$

## Commands

Write $C_c=[\![ c]\!]_c$, $B_b=[\![ b]\!]_b$.

$$
\begin{aligned}
C_{\mathsf{skip}}(\sigma)&=\sigma,\\
C_{x:=a}(\sigma)&=\sigma[x\mapsto[\![ a]\!]_a\sigma],\\
C_{c_1;c_2}&=C_{c_2}\circ C_{c_1},\\
C_{\mathsf{if}\ b\ \mathsf{then}\ c_1\ \mathsf{else}\ c_2}(\sigma)
&=\begin{cases}
C_{c_1}(\sigma)&B_b(\sigma)=\mathsf{true},\\
C_{c_2}(\sigma)&B_b(\sigma)=\mathsf{false}.
\end{cases}
\end{aligned}
$$

Sequence uses partial-function composition: undefined if either required call is undefined.

Equivalent notation: $C_c:\Sigma\to\Sigma_\bot$, where $\bot$ means divergence. Extend functions strictly: $f^\dagger(\bot)=\bot$, $f^\dagger(\sigma)=f(\sigma)$. Then $C_{c_1;c_2}=C_{c_2}^\dagger\circ C_{c_1}$.

## While = least fixed point

Let $W=C_{\mathsf{while}\ b\ \mathsf{do}\ c}$. Unrolling gives

$$
W(\sigma)=
\begin{cases}
W^\dagger(C_c(\sigma))&B_b(\sigma)=\mathsf{true},\\
\sigma&B_b(\sigma)=\mathsf{false}.
\end{cases}
$$

Circular equation; not yet a definition. Let $F(w)$ be its right side with $w$ replacing $W$.

$$
W_0(\sigma)=\bot,\qquad W_{n+1}=F(W_n).
$$

- $W_1$: returns only when the first guard is false.
- $W_{n+1}$: permits at most $n$ completed body iterations, then a false guard.
- More approximations = more terminating inputs; existing results stay fixed.

Information order:

$$
f\sqsubseteq g
\iff\forall\sigma,\tau\in\Sigma,\quad
f(\sigma)=\tau\Rightarrow g(\sigma)=\tau.
$$

$$
W_0\sqsubseteq W_1\sqsubseteq\cdots,
\qquad
W=\bigsqcup_{n\ge0}W_n=\operatorname{lfp}(F).
$$

Take the union of defined input-output pairs. For this $F$, it is a fixed point. Any fixed point extends every $W_n$, so it extends $W$.

Example: `while x > 0 do x := x - 1`, initially $x=k\ge0$. First defined approximation: $W_{k+1}$; final $x=0$.

Why **least**? For `while true do skip`, the equation is $W=W$. Every function solves it; only the least, everywhere undefined function matches divergence.

## Relation view

Let $R_c\subseteq\Sigma\times\Sigma$ be the graph of $C_c$; let

$$
T_b=\{(\sigma,\sigma):B_b(\sigma)=\mathsf{true}\}.
$$

$$
R_{\mathsf{while}\ b\ \mathsf{do}\ c}
=T_{\neg b}\circ(R_c\circ T_b)^*.
$$

Repeat “guard true, then body” finitely many times; finish with guard false. $R^*$ includes zero repetitions. Composition acts right to left.

## Agreement with operational semantics

$$
\langle a,\sigma\rangle\Downarrow_a n
\iff[\![ a]\!]_a\sigma=n.
$$

Boolean version similarly. For commands:

$$
\langle c,\sigma\rangle\Downarrow\tau
\iff C_c(\sigma)=\tau
\iff\langle c,\sigma\rangle\to^*\langle\mathsf{skip},\tau\rangle.
$$

While case: finite derivations correspond to finite approximations. Inversion and anti-reduction: [the operational-equivalence proof](07-imp-operational-semantics.md#equivalence_proof).

Sources: Lecture 10, `lec10-slides.pdf`, pp. 4–8; Kozen, `kozen-cs6110-lec18-denotational-semantics-of-imp.pdf`, §§3–4.
