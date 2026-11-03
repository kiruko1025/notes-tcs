---
title: "Recursion and Fixed Points"
author: ""
tags: [CSE590]
draft: false
---

# Recursion and Fixed Points

Combinators below use [Church encodings](04-church-encodings.md). Evaluation conventions: [reduction and evaluation](03-reduction-and-evaluation.md).

## Recursion as a fixed point

Separate one layer of factorial from its recursive calls:

$$
T\triangleq\lambda r.\lambda n.
\mathsf{If}\;(\mathsf{IsZero}\;n)\;\overline1
\;(\mathsf{Mul}\;n\;(r\;(\mathsf{Pred}\;n))).
$$

- $r$: implementation of recursive calls.
- $T\,r$: one layer of factorial logic using $r$.
- Desired function: $\mathsf{Fact}=_\beta T\;\mathsf{Fact}$.
- **Fixed point:** unchanged by $T$ under beta convertibility; not literal equality of syntax.

### Curry's Y combinator

$$
Y\triangleq\lambda t.
(\lambda f.t\,(f\,f))\,(\lambda f.t\,(f\,f)).
$$

Let $A_t=\lambda f.t\,(f\,f)$, with $f$ fresh for $t$:

$$
\begin{aligned}
Y\,t&\to_\beta A_t\,A_t\to_\beta t\,(A_t\,A_t),\\
t\,(Y\,t)&\to_\beta t\,(A_t\,A_t).
\end{aligned}
$$

Same reduct, hence

$$
\boxed{Y\,t=_\beta t\,(Y\,t).}
$$

Self-application recreates recursion. Fixed-point equation = beta convertibility.

Set $\mathsf{Fact}=Y\,T$. Unfolding the recursive calls gives these beta-convertible expressions:

$$
\begin{aligned}
\mathsf{Fact}\;\overline3
&=_\beta\mathsf{Mul}\;\overline3\;
 (\mathsf{Mul}\;\overline2\;
  (\mathsf{Mul}\;\overline1\;\overline1))\\
&=_\beta\overline6.
\end{aligned}
$$

**No termination guarantee:** for $I=\lambda x.x$, $Y\,I=_\beta\Omega$ and normal-order evaluation diverges.

### A combinator with direct unfolding

$$
B\triangleq\lambda y.\lambda f.f\,(y\,y\,f),
\qquad \Theta\triangleq B\,B.
$$

$$
\Theta\,t
\to_\beta(\lambda f.f\,(B\,B\,f))\,t
\to_\beta t\,(B\,B\,t)=t\,(\Theta\,t).
$$

## Making recursion work under CBV

Ordinary $Y$ unfolds $f\,f$ before passing it to $t$, causing endless recursive expansion.

**Fix:** delay self-application behind a lambda.

$$
Y_{\mathrm{cbv}}\triangleq\lambda t.
(\lambda f.t\,(\lambda z.f\,f\,z))
(\lambda f.t\,(\lambda z.f\,f\,z)).
$$

For a value $t$, define

$$
A=\lambda f.t\,(\lambda z.f\,f\,z),
\qquad R=\lambda z.A\,A\,z.
$$

$$
Y_{\mathrm{cbv}}\,t\to_{\mathrm{cbv}}A\,A
\to_{\mathrm{cbv}}t\,R.
$$

- $R$ already a value; body waits for an argument.
- Recursive call on value $v$: $R\,v\to_{\mathrm{cbv}}A\,A\,v\to_{\mathrm{cbv}}(t\,R)\,v$.
- Factorial also needs **delayed branches**, so the base case avoids recursion.

## CBV factorial

Use $Y_{\mathrm{cbv}}$ above and the [encoded conditional with branch thunks](04-church-encodings.md#delaying_cbv_computation):

$$
\begin{aligned}
T_{\mathrm{cbv}}\triangleq\lambda r.\lambda n.
\mathsf{If}_{\mathrm{cbv}}\;&(\mathsf{IsZero}\;n)\\
& (\lambda u.\overline1)\\
& (\lambda u.\mathsf{Mul}\;n\;(r\;(\mathsf{Pred}\;n))).
\end{aligned}
$$

$$
\mathsf{Fact}_{\mathrm{cbv}}\triangleq Y_{\mathrm{cbv}}\;T_{\mathrm{cbv}}.
$$

Two necessary delays:

1. $Y_{\mathrm{cbv}}$: delay recursive unfolding until a call.
2. Branch thunks: avoid a recursive call in the zero case.

Result represents $n!$; weak CBV need not normalize the body.
