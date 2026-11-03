---
title: "Reduction and Evaluation"
author: ""
tags: [CSE590]
draft: false
---

# Reduction and Evaluation

Capture-avoiding [substitution](02-lambda-calculus.md#capture-avoiding_substitution); terms identified up to alpha equivalence.

## Reduction and normal forms

**Beta:** apply a function by substitution.

$$
(\lambda x.e)\,s\to_\beta e[x\mapsto s].
$$

**Full beta reduction:** allowed anywhere, including inside lambda bodies.

$$
\frac{e_1\to_\beta e_1'}{e_1\,e_2\to_\beta e_1'\,e_2},
\qquad
\frac{e_2\to_\beta e_2'}{e_1\,e_2\to_\beta e_1\,e_2'},
\qquad
\frac{e\to_\beta e'}{\lambda x.e\to_\beta\lambda x.e'}.
$$

| Notation / term | Meaning |
| --- | --- |
| Beta redex | $(\lambda x.e)\,s$ |
| Contractum | $e[x\mapsto s]$ |
| $e\to_\beta^*e'$ | Zero or more forward steps |
| $e=_\beta e'$ | Beta convertibility: forward **or backward** steps, allowing alpha renaming |
| Beta normal form | No beta redex anywhere; e.g. $\lambda x.x$ or $x\,y$ |

**Eta:** remove a wrapper that only forwards its argument.

$$
\lambda x.e\,x\to_\eta e
\qquad x\notin\mathrm{FV}(e).
$$

- Valid: $\lambda f.\lambda y.f\,y\to_\eta\lambda f.f$.
- Invalid: $\lambda x.x\,x\to_\eta x$; side condition fails.
- CBV caution: $\lambda x.\Omega\,x$ is a value; $\Omega$ diverges. Unrestricted eta contraction can change termination.

## Divergence versus normalization

$$
\omega\triangleq\lambda x.x\,x,
\qquad
\Omega\triangleq\omega\,\omega\to_\beta\omega\,\omega=\Omega.
$$

- $\omega$: normal form.
- $\Omega$: only redex reproduces itself; no normal form.
- **Weakly normalizing:** some reduction sequence reaches a normal form.
- **Strongly normalizing:** every reduction sequence terminates.

With $I=\lambda y.y$:

$$
(\lambda x.I)\,\Omega\to_\beta I.
$$

Weakly normalizing, but not strongly: repeatedly reducing the argument loops forever.

## Confluence: Church–Rosser

Any two finite reduction paths from the same term can rejoin:

$$
\bigl(e\to_\beta^*e_1\land e\to_\beta^*e_2\bigr)
\Longrightarrow
\exists q.\;e_1\to_\beta^*q\land e_2\to_\beta^*q.
$$

Example: let $a=(\lambda y.y)\,z$.

$$
\begin{aligned}
(\lambda x.x\,x)\,a
&\to_\beta(\lambda x.x\,x)\,z\to_\beta z\,z,
\\
(\lambda x.x\,x)\,a
&\to_\beta a\,a\to_\beta z\,a\to_\beta z\,z.
\end{aligned}
$$

**Consequence:** normal forms unique up to alpha equivalence.

Proof outline: two normal forms must have a common reduct; neither can step, so they must already agree.

Confluence allows multiple next steps; determinism allows at most one. Full beta reduction: confluent, not deterministic.

Confluence does not imply termination. The strategy determines which redex runs next.

## Evaluation strategies

| Strategy | Next redex | Inside lambda bodies? |
| --- | --- | --- |
| Normal order | Leftmost outermost | Yes |
| Applicative order | Leftmost innermost | Yes |
| Call-by-name (CBN) | Function position; then substitute unevaluated argument | No |
| Call-by-value (CBV) | Function, then argument to a value, then apply | No |

- **Outermost:** outside every other redex.
- **Innermost:** contains no smaller redex.
- **Leftmost:** first eligible redex in left-to-right syntax order.
- **Weak evaluation:** no reduction under lambdas; values $v::=\lambda x.e$.

Example: $(\lambda x.I)\,\Omega$. Normal order/CBN return $I$; applicative order/CBV diverge.

**Normalization theorem:** normal order finds a beta normal form whenever one exists.

$\lambda x.\Omega$: a CBN/CBV value, but no beta normal form.

| Argument handling | Tradeoff |
| --- | --- |
| CBN: substitute unevaluated argument | Avoid unused work; repeated uses may duplicate work |
| CBV: evaluate before substitution | Compute argument once; evaluate even unused arguments |
| Call-by-need: delay and share result | Avoid unused work and repeated argument evaluation |

Open terms may be stuck, e.g. $x\,v$. [Inference rules](06-induction-and-proof-rules.md) specify the steps below.

## Call-by-value (CBV)

Order: **function → argument → substitute**. Capture-avoiding substitution throughout.

$$
\frac{}{(\lambda x.e)\,v\to_{\mathrm{cbv}}e[x\mapsto v]}
\quad(\text{Beta})
$$

$$
\frac{e_1\to_{\mathrm{cbv}}e_1'}
{e_1\,e_2\to_{\mathrm{cbv}}e_1'\,e_2}
\quad(\text{AppL})
\qquad
\frac{e_2\to_{\mathrm{cbv}}e_2'}
{v_1\,e_2\to_{\mathrm{cbv}}v_1\,e_2'}
\quad(\text{AppR})
$$

No reduction under lambdas. AppR and Beta require values as shown.

**Sequence versus proof tree.** Let $I=\lambda z.z$:

$$
(\lambda f.f)\,(I\,I)
\to_{\mathrm{cbv}}(\lambda f.f)\,I
\to_{\mathrm{cbv}}I.
$$

Proof of the **first step only**:

$$
\frac{
 \displaystyle\frac{}{I\,I\to_{\mathrm{cbv}}I}\;(\text{Beta})
}{
 (\lambda f.f)\,(I\,I)\to_{\mathrm{cbv}}(\lambda f.f)\,I
}\quad(\text{AppR}).
$$

## Call-by-name (CBN)

Order: **function → substitute unevaluated argument**.

$$
\frac{}{(\lambda x.e_1)\,e_2\to_{\mathrm{cbn}}e_1[x\mapsto e_2]}
\quad(\text{Beta})
$$

$$
\frac{e_1\to_{\mathrm{cbn}}e_1'}
{e_1\,e_2\to_{\mathrm{cbn}}e_1'\,e_2}
\quad(\text{AppL})
$$

No AppR; no reduction under lambdas.

$$
(\lambda x.I)\,\Omega\to_{\mathrm{cbn}}I.
$$

CBV loops on the same input by repeatedly stepping its argument.

**Both strategies:**

- $\to^*$: zero or more steps.
- Termination: reach a value. Divergence: infinite run.
- Deterministic up to alpha equivalence. Proof: disjoint rule cases; IH for subterm steps.

Sources: Lectures 4–6: `lec04-slides.pdf`, pp. 4–6; `Lecture 4.pdf`, p. 1; `lec05-slides.pdf`, pp. 3–6; `Lecture 5 09-16.pdf`, p. 1; `lec06-slides.pdf`, pp. 7–9; `Lecture 6 09-21.pdf`, p. 1.
