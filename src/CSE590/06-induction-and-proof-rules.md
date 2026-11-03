---
title: "Induction and Proof Rules"
author: ""
tags: [CSE590]
draft: false
---

# Induction and Proof Rules

## Reading inference rules

$$
\frac{J_1\qquad\cdots\qquad J_k}{J}
\quad(\text{Rule name}).
$$

- Judgment: claim $J$.
- Premises above; conclusion below.
- Axiom: no premises.
- Side condition: extra restriction.
- Rule instance: substitute concrete terms for metavariables.

## Inductive definitions and well-foundedness

**Inductive definition:** least set closed under the rules = judgments with finite proof trees.

$$
\frac{}{0\;\mathsf{isNat}},
\qquad
\frac{n\;\mathsf{isNat}}{(n+1)\;\mathsf{isNat}}.
$$

Zero starts a proof; Successor builds larger proofs. A cyclic rule $J/J$ alone proves nothing.

**Well-founded relation $\prec$:** no infinite descending chain. Induction principle:

$$
\Bigl[\forall a.\;
 (\forall b\prec a.\;P(b))\Rightarrow P(a)\Bigr]
\Longrightarrow\forall a.\;P(a).
$$

Examples: $<$ on $\mathbb N$; proper subterms. Nonexamples: $<$ on $\mathbb Z$; beta reduction ($\Omega\to_\beta\Omega$).

| Method | Cases / hypotheses |
| --- | --- |
| Structural induction on $e$ | Variable; abstraction with body IH; application with two subterm IHs |
| Rule induction on a derivation | One case per final rule; IH for each premise derivation |
| Induction on a finite run | Zero steps; one step followed by a shorter run |

## Proof 1: substitution bounds free variables

$$
\boxed{\mathrm{FV}(e[x\mapsto s])
\subseteq(\mathrm{FV}(e)\setminus\{x\})\cup\mathrm{FV}(s).}
$$

Induct on term size; keep $x,s$ arbitrary. Fresh renaming preserves size.

- **Variable $y$:** $y=x$ gives $s$; otherwise gives $y$.
- **Application:** apply both IHs; take the union.
- **Abstraction $\lambda y.e_0$: $y=x$:** substitution stops; bound follows directly.
- **Abstraction: $y\ne x$:** alpha-rename so $y\notin\mathrm{FV}(s)$; apply IH to the smaller body.

Last case:

$$
\begin{aligned}
\mathrm{FV}((\lambda y.e_0)[x\mapsto s])
&=\mathrm{FV}(e_0[x\mapsto s])\setminus\{y\}\\
&\subseteq
 \bigl((\mathrm{FV}(e_0)\setminus\{x\})\cup\mathrm{FV}(s)\bigr)
 \setminus\{y\}\\
&=(\mathrm{FV}(\lambda y.e_0)\setminus\{x\})\cup\mathrm{FV}(s).
\end{aligned}
$$

Last equality uses freshness of $y$; alpha renaming preserves free variables.

## Proof 2: evaluation introduces no new free variables

$$
e\to_{\mathrm{cbv}}e'
\quad\Longrightarrow\quad
\mathrm{FV}(e')\subseteq\mathrm{FV}(e).
$$

**Rule induction:** three possible final rules.

| Case | Proof step |
| --- | --- |
| Beta | Substitution lemma; no premise IH |
| AppL | IH: $\mathrm{FV}(e_1')\subseteq\mathrm{FV}(e_1)$; union with $\mathrm{FV}(e_2)$ |
| AppR | IH: $\mathrm{FV}(e_2')\subseteq\mathrm{FV}(e_2)$; union with $\mathrm{FV}(v_1)$ |

Beta case explicitly:

$$
\begin{aligned}
\mathrm{FV}(e_0[x\mapsto v])
&\subseteq(\mathrm{FV}(e_0)\setminus\{x\})\cup\mathrm{FV}(v)\\
&=\mathrm{FV}((\lambda x.e_0)\,v).
\end{aligned}
$$

**Consequences:** same property for CBN and finite runs; closedness preserved. Inclusion may be strict:

$$
(\lambda x.I)\,(\lambda z.y)\to_{\mathrm{cbv}}I
\qquad(y\ne z),
$$

discarding free $y$.

Prerequisites: [substitution](02-lambda-calculus.md) and [evaluation rules](03-reduction-and-evaluation.md).

Source: `lec06-slides.pdf`, pp. 7–9; `Lecture 6 09-21.pdf`, p. 1.
