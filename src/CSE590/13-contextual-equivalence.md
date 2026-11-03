---
title: "Contextual Equivalence"
author: ""
tags: [CSE590]
draft: false
---

# Contextual Equivalence

Same behavior in every program context.

## Contexts

$C$ = term with exactly one hole $[\ ]$, in any term position.

Examples: $[\ ]$, $\lambda x:\tau.[\ ]$, $f\,[\ ]$, $([\ ],e)$, an unchosen branch.

- General context $C$: hole allowed under binders and in unevaluated positions.
- Evaluation context $E$: hole marks the next computation.
- Plugging may capture free variables:

$$
(\lambda x:\tau.[\ ])[x]=\lambda x:\tau.x.
$$

Plugging is not capture-avoiding substitution.

## Definition

For $\Gamma\vdash e_1:\tau$ and $\Gamma\vdash e_2:\tau$:

$$
e_1\equiv_{\mathrm{ctx}}e_2
\iff
\forall C,b.\quad
C[e_1]\to_{\mathrm{cbv}}^*b
\iff C[e_2]\to_{\mathrm{cbv}}^*b.
$$

Quantify over $b\in\{\mathsf{true},\mathsf{false}\}$ and well-typed closing contexts:

$$
C:(\Gamma\vdash[\ ]:\tau)\Rightarrow(\varnothing\vdash C[\ ]:\mathsf{bool}).
$$

The hole retains every assumption in $\Gamma$, even unused ones. The context must close them with their given types.

All closed well-typed programs here terminate. Comparing termination alone would identify everything; compare Boolean answers.

To disprove equivalence: one distinguishing context.

$$
e_1=\lambda x:\mathrm{bool}.x,\qquad
e_2=\lambda x:\mathrm{bool}.\mathsf{true}.
$$

$C=[\ ]\,\mathsf{false}$ returns false versus true.

To prove equivalence: equality of denotations is sufficient.

$$
[\![ e_1]\!]=[\![ e_2]\!]
\implies e_1\equiv_{\mathrm{ctx}}e_2.
$$

Reason: compositionality preserves equal meanings inside $C$; [adequacy](12-stlc-denotational-semantics.md#adequacy) gives equal Boolean results.

## Beta and eta

Pure terminating STLC; both sides well-typed at the same type.

$$
\begin{aligned}
(\lambda x:\sigma.e)e'&\equiv_{\mathrm{ctx}}e[x\mapsto e'],
&&\beta_\to\\
(e_1,e_2).i&\equiv_{\mathrm{ctx}}e_i,
&&\beta_\times\\
\lambda x:\sigma.f\,x&\equiv_{\mathrm{ctx}}f,
&&\eta_\to\\
(p.1,p.2)&\equiv_{\mathrm{ctx}}p,
&&\eta_\times\\
u&\equiv_{\mathrm{ctx}}(),
&&\eta_1
\end{aligned}
$$

Conditions: $x\notin\mathrm{FV}(f)$, $p:\sigma\times\tau$, $u:1$.

These are equalities, not necessarily one CBV step. CBV beta still requires a value argument.

**Sum eta:** analyzing and rebuilding a sum changes nothing.

$$
\begin{aligned}
&\mathsf{case}\ s\ \mathsf{of}\\
&\quad\mathsf{inl}\ x\Rightarrow e[z\mapsto\mathsf{inl}_\tau x]\\
&\quad\mid\mathsf{inr}\ y\Rightarrow e[z\mapsto\mathsf{inr}_\sigma y]
\quad\equiv_{\mathrm{ctx}}e[z\mapsto s].
\end{aligned}
$$

$s:\sigma+\tau$; $e$ has free variable $z:\sigma+\tau$; branch binders fresh. Substitutions avoid capture.

Special case: $\mathsf{case}\ s\ \mathsf{of}\ \mathsf{inl}\ x\Rightarrow\mathsf{inl}_\tau x\mid\mathsf{inr}\ y\Rightarrow\mathsf{inr}_\sigma y\equiv_{\mathrm{ctx}}s$.

**Empty eta:** if $z:0\in\Gamma$, any two terms of the same type in $\Gamma$ are contextually equivalent. There is no value to supply for $z$.

## Adding effects

The laws depend on the language. Divergence, state, exceptions, or output can expose evaluation order or duplication.

Example extension: add a diverging term $\Omega_\tau:\tau$.

$$
(\lambda x:\tau.\mathsf{true})\Omega_\tau
\quad\text{diverges; its unrestricted beta contractum is true.}
$$

Likewise $\lambda x:\sigma.\Omega_{\sigma\to\tau}\,x$ is a value, while $\Omega_{\sigma\to\tau}$ diverges. Context $(\lambda f:\sigma\to\tau.\mathsf{true})[\ ]$ distinguishes them.

With state/output, $(p.1,p.2)$ may run $p$ twice. Unit-typed computations may still have effects. Recheck each law; types alone do not justify it.
