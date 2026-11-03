---
title: "Denotational Semantics of STLC"
author: ""
tags: [CSE590]
draft: false
---

# Denotational Semantics of STLC

Types = sets. Terms = functions from environments to meanings.
Pure terminating STLC; all functions total, no bottom element or fixed point needed. Product/sum syntax: [algebraic data types](10-algebraic-data-types.md).

## Types and environments

Write $[\![\cdot]\!]$ for meaning.

$$
\begin{aligned}
{}[\![\mathrm{int}]\!]&=\mathbb Z,
&[\![\mathrm{bool}]\!]&=\{\mathsf{true},\mathsf{false}\},\\
[\![1]\!]&=\{*\},
&[\![0]\!]&=\varnothing,\\
[\![\sigma\times\tau]\!]
&=[\![\sigma]\!]\times[\![\tau]\!],
&[\![\sigma+\tau]\!]
&=[\![\sigma]\!]\uplus[\![\tau]\!],\\
[\![\sigma\to\tau]\!]
&=[\![\sigma]\!]\to[\![\tau]\!].
\end{aligned}
$$

$A\uplus B=\{(1,a)\mid a\in A\}\cup\{(2,b)\mid b\in B\}$: tags distinguish the sides.

$$
[\![\Gamma]\!]
=\{\rho\mid\operatorname{dom}\rho=\operatorname{dom}\Gamma,
\ \rho(x)\in[\![\tau]\!]\text{ for }x:\tau\in\Gamma\}.
$$

$$
[\![\Gamma\vdash e:\tau]\!]:
[\![\Gamma]\!]\to[\![\tau]\!].
$$

$\Gamma$ stores types; $\rho$ stores mathematical values. $[\![\varnothing]\!]$ contains one environment: the empty map.

## Terms

Omit the typing judgment from brackets.

$$
\begin{aligned}
{}[\![ n]\!]\rho&=n,
&[\![ b]\!]\rho&=b,\\
[\![ x]\!]\rho&=\rho(x),\\
[\![\lambda x:\sigma.e]\!]\rho
&=(a\in[\![\sigma]\!]\mapsto
[\![ e]\!]\rho[x\mapsto a]),\\
[\![ e_1e_2]\!]\rho
&=([\![ e_1]\!]\rho)([\![ e_2]\!]\rho),\\
[\![ e_1+e_2]\!]\rho
&=[\![ e_1]\!]\rho+[\![ e_2]\!]\rho,\\
[\![()]\!]\rho&=*,\\
[\![(e_1,e_2)]\!]\rho
&=([\![ e_1]\!]\rho,[\![ e_2]\!]\rho),\\
[\![ e.i]\!]\rho&=\pi_i([\![ e]\!]\rho),\\
[\![\mathsf{inl}_\tau e]\!]\rho&=(1,[\![ e]\!]\rho),\\
[\![\mathsf{inr}_\sigma e]\!]\rho&=(2,[\![ e]\!]\rho).
\end{aligned}
$$

Here $b$ is a Boolean literal. For `if`, evaluate the branch selected by $[\![ e]\!]\rho$.

For $\mathsf{case}\ e\ \mathsf{of}\ \mathsf{inl}\ x\Rightarrow e_1\mid\mathsf{inr}\ y\Rightarrow e_2$:

$$
\begin{cases}
[\![ e_1]\!]\rho[x\mapsto a]
&[\![ e]\!]\rho=(1,a),\\
[\![ e_2]\!]\rho[y\mapsto b]
&[\![ e]\!]\rho=(2,b).
\end{cases}
$$

Empty elimination: $\Gamma\vdash e:0$ forces $[\![\Gamma]\!]=\varnothing$. Its meaning is the unique empty function to the result set.

Example: $[\![\lambda x:\mathrm{int}.x+1]\!]=(a\mapsto a+1)$.

## Soundness

Evaluation preserves meaning:

$$
\vdash e:\tau,\quad e\to_{\mathrm{cbv}}e'
\implies[\![ e]\!]=[\![ e']\!].
$$

Substitution commutes with interpretation. For $\Gamma,x:\sigma\vdash e:\tau$, $\Gamma\vdash s:\sigma$, and $\rho\in[\![\Gamma]\!]$:

$$
[\![e[x\mapsto s]]\!]\rho
=[\![e]\!](\rho[x\mapsto[\![s]\!]\rho]).
$$

Proof: typing induction; freshen binders. Weakening ignores extra environment entries. Beta uses substitution with a value; context steps use compositionality.

Closed Boolean consequence:

$$
e\to_{\mathrm{cbv}}^*b\implies[\![ e]\!]=b.
$$

## Adequacy

Meaning predicts the actual result. Relate semantic values to closed syntactic values:

$$
a\approx^E_\tau e
\iff\exists v.\ e\to_{\mathrm{cbv}}^*v
\land a\approx^V_\tau v.
$$

Value relation, by type:

- Int/bool: same numeral/Boolean.
- Unit: $*\approx^V_1()$; empty type: no pairs.
- Product: corresponding components related.
- Sum: same tag; payloads related.
- Function:

$$
f\approx^V_{\sigma\to\tau}\lambda x:\sigma.e
\iff
\forall a,v.\ a\approx^V_\sigma v
\implies f(a)\approx^E_\tau e[x\mapsto v].
$$

**Fundamental lemma:** if $\Gamma\vdash e:\tau$ and $\rho(x)\approx^V_{\Gamma(x)}\gamma(x)$ for each $x\in\operatorname{dom}\Gamma$, then

$$
[\![ e]\!]\rho\approx^E_\tau e[\gamma].
$$

Proof: typing induction, like the [termination proof](11-termination-and-logical-relations.md), carrying semantic values too.

Empty environment gives adequacy; with soundness:

$$
\boxed{\vdash e:\mathrm{bool}\implies
\bigl(e\to_{\mathrm{cbv}}^*b\iff[\![ e]\!]=b\bigr).}
$$

Same result for integers. At function types, relate application behavior; a mathematical function is not a lambda term.

## What each theorem says

- Denotational soundness: execution preserves meaning.
- Adequacy: execution reaches the predicted ground value.
- [Type soundness](09-types-and-type-soundness.md#type_soundness): execution never gets stuck.

Total denotations alone do not prove operational termination. The logical relation supplies that connection.

Equal denotations also imply [contextual equivalence](13-contextual-equivalence.md).
