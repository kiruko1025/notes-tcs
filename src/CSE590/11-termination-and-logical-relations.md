---
title: "Termination and Logical Relations"
author: ""
tags: [CSE590]
draft: false
---

# Termination and Logical Relations

Pure STLC with products and sums. No recursion or effects.

## Why the first proof fails

Goal:

$$
\vdash e:\tau \implies e\to_{\mathrm{cbv}}^*v.
$$

Induction on typing: application gets stuck here.

$$
e_1e_2\to_{\mathrm{cbv}}^*(\lambda x:\sigma.e)v
\to_{\mathrm{cbv}}e[x\mapsto v].
$$

IHs cover $e_1,e_2$, not the substituted body. Need a stronger property: functions take good arguments to terminating computations.

## Logical relation

$\mathcal V_\tau$ = good closed values; $\mathcal T_\tau$ = good closed terms.
Define by recursion on types.

$$
\begin{aligned}
\mathcal V_{\mathrm{int}}&=\{n\mid n\in\mathbb Z\},\\
\mathcal V_{\mathrm{bool}}&=\{\mathsf{true},\mathsf{false}\},\\
\mathcal V_1&=\{()\},\qquad \mathcal V_0=\varnothing,\\
\mathcal V_{\sigma\to\tau}
&=\{\lambda x:\sigma.e\mid
\forall v\in\mathcal V_\sigma,\ e[x\mapsto v]\in\mathcal T_\tau\},\\
\mathcal V_{\sigma\times\tau}
&=\{(v,w)\mid v\in\mathcal V_\sigma,\ w\in\mathcal V_\tau\},\\
\mathcal V_{\sigma+\tau}
&=\{\mathsf{inl}_\tau v\mid v\in\mathcal V_\sigma\}
\cup\{\mathsf{inr}_\sigma w\mid w\in\mathcal V_\tau\}.
\end{aligned}
$$

$$
\mathcal T_\tau=\{e\mid \exists v\in\mathcal V_\tau,
\ e\to_{\mathrm{cbv}}^*v\}.
$$

Arrow clause uses only smaller types. No circular definition.

A closing substitution replaces free variables simultaneously:

$$
\gamma\in\mathcal V_\Gamma
\iff \gamma(x)\in\mathcal V_\tau
\quad\text{for each }x:\tau\in\Gamma.
$$

## Fundamental lemma

$$
\Gamma\vdash e:\tau,\quad\gamma\in\mathcal V_\Gamma
\implies e[\gamma]\in\mathcal T_\tau.
$$

Proof: induction on typing, for **every** good closing substitution.

- Variable: given by $\gamma$.
- Constant: already a good value.
- Lambda: choose any $v\in\mathcal V_\sigma$. Apply body IH with $\gamma[x\mapsto v]$.
- Application: IHs evaluate function and argument to good values. Arrow clause gives termination after substitution.
- Pair/injection: evaluate components; use their value clauses.
- Projection/case: evaluate scrutinee; use its components or chosen branch IH.
- Addition/if: integer/Boolean value clauses determine the next rule.
- Empty elimination: impossible premise; $\mathcal T_0=\varnothing$.

Two bookkeeping facts:

$$
e\to_{\mathrm{cbv}}^*e'
\implies E[e]\to_{\mathrm{cbv}}^*E[e'].
$$

For fresh $x$, with $v$ and all substitution images closed:

$$
(\lambda x:\sigma.e)[\gamma]=\lambda x:\sigma.e[\gamma],
\qquad
e[\gamma][x\mapsto v]=e[\gamma[x\mapsto v]].
$$

Also: $e\to_{\mathrm{cbv}}^*e'$ and $e'\in\mathcal T_\tau$ imply $e\in\mathcal T_\tau$.

## Consequences

Take $\Gamma,\gamma$ empty:

$$
\vdash e:\tau\implies e\in\mathcal T_\tau
\implies e\to_{\mathrm{cbv}}^*v.
$$

- Every closed well-typed program terminates at a value.
- Deterministic CBV therefore never gets stuck: another safety proof.
- No closed term of type $0$.
- Example: $\lambda x:\mathrm{int}.x+1\in\mathcal V_{\mathrm{int}\to\mathrm{int}}$; every numeral input gives a numeral output.

**Strong normalization:** every full beta-reduction sequence terminates, including reductions under lambdas. Kozen proves this stronger theorem for pure STLC using a stronger logical predicate. The CBV relation above proves CBV termination.

Sources: `lec15-slides.pdf`, pp. 5–11; `kozen-cs6110-lec23-strong-normalization.pdf`, pp. 1–3.
