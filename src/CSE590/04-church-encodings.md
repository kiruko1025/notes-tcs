---
title: "Church Encodings"
author: ""
tags: [CSE590]
draft: false
---

# Church Encodings

Booleans select; numerals iterate; pairs pass components to a consumer. All names below abbreviate lambda terms.

## Booleans

$$
\begin{aligned}
\mathsf{True}&\triangleq\lambda t.\lambda f.t,\\
\mathsf{False}&\triangleq\lambda t.\lambda f.f,\\
\mathsf{If}&\triangleq\lambda b.\lambda t.\lambda f.b\,t\,f,\\
\mathsf{Not}&\triangleq\lambda b.b\;\mathsf{False}\;\mathsf{True},\\
\mathsf{And}&\triangleq\lambda p.\lambda q.p\,q\,\mathsf{False},\\
\mathsf{Or}&\triangleq\lambda p.\lambda q.p\,\mathsf{True}\,q.
\end{aligned}
$$

CBV needs delayed branches; see [delaying CBV computation](#delaying_cbv_computation).

## Numerals: repeat an operation

$$
\overline n\triangleq\lambda f.\lambda x.f^n(x),
\qquad f^0(x)=x,\quad f^{n+1}(x)=f(f^n(x)).
$$

$$
\overline0=\lambda f.\lambda x.x,
\qquad
\overline1=\lambda f.\lambda x.f\,x,
\qquad
\overline2=\lambda f.\lambda x.f\,(f\,x).
$$

$\overline n\,f\,x$: start at $x$, apply $f$ exactly $n$ times. Bar = encoded number; $f^n$ = repeated application.

$$
\begin{aligned}
\mathsf{Succ}&\triangleq\lambda n.\lambda f.\lambda x.f\,(n\,f\,x),\\
\mathsf{Add}&\triangleq\lambda n.\lambda m.n\;\mathsf{Succ}\;m,\\
\mathsf{Mul}&\triangleq\lambda n.\lambda m.n\;(\mathsf{Add}\;m)\;\overline0,\\
\mathsf{Exp}&\triangleq\lambda n.\lambda m.n\;(\mathsf{Mul}\;m)\;\overline1.
\end{aligned}
$$

**Exponent first:** $\mathsf{Exp}\;\overline2\;\overline3\to_\beta^*\overline9$. Zero repetitions return $\overline1$, including the $0^0$ case under this encoding.

## Pairs and local bindings

$$
\begin{aligned}
\mathsf{Pair}&\triangleq\lambda a.\lambda b.\lambda k.k\,a\,b,\\
\mathsf{First}&\triangleq\lambda p.p\;\mathsf{True},\\
\mathsf{Second}&\triangleq\lambda p.p\;\mathsf{False}.
\end{aligned}
$$

$$
\mathsf{First}\;(\mathsf{Pair}\;a\;b)
\to_\beta^*\mathsf{True}\;a\;b\to_\beta^*a.
$$

**Syntactic sugar:** new notation, translated into existing terms.

$$
\begin{aligned}
\mathsf{let}\;x=e_1\;\mathsf{in}\;e_2
&\triangleq(\lambda x.e_2)\,e_1,\\
\mathsf{let}\;(x,y)=p\;\mathsf{in}\;e
&\triangleq p\;(\lambda x.\lambda y.e).
\end{aligned}
$$

- Ordinary `let`: $x$ bound only in $e_2$; nonrecursive.
- Pair binding: distinct $x,y$; consumer receives components in order.

## Iteration with pairs

A Church numeral can repeat an update on an entire pair.

### Fibonacci

Keep consecutive values: $(a,b)\mapsto(b,a+b)$.

$$
\mathsf{FibStep}\triangleq
\lambda p.\mathsf{Pair}\;(\mathsf{Second}\;p)
\;(\mathsf{Add}\;(\mathsf{First}\;p)\;(\mathsf{Second}\;p)).
$$

$$
\mathsf{Fib}\triangleq\lambda n.\mathsf{First}\;
\bigl(n\;\mathsf{FibStep}\;(\mathsf{Pair}\;\overline0\;\overline1)\bigr).
$$

$$
(0,1)\mapsto(1,1)\mapsto(1,2)\mapsto(2,3)\mapsto(3,5)\mapsto\cdots
$$

After $n$ updates: $(F_n,F_{n+1})$. First component = answer; $F_0=0$, $F_1=1$.

### Zero test and predecessor

$$
\mathsf{IsZero}\triangleq
\lambda n.n\;(\lambda u.\mathsf{False})\;\mathsf{True}.
$$

- Zero iterations: keep true.
- At least one iteration: return false.

For predecessor, remember the previous counter: $(a,b)\mapsto(b,b+1)$.

$$
\mathsf{PredStep}\triangleq
\lambda p.\mathsf{Pair}\;(\mathsf{Second}\;p)
\;(\mathsf{Succ}\;(\mathsf{Second}\;p)).
$$

$$
\mathsf{Pred}\triangleq\lambda n.\mathsf{First}\;
\bigl(n\;\mathsf{PredStep}\;(\mathsf{Pair}\;\overline0\;\overline0)\bigr).
$$

$$
(0,0)\mapsto(0,1)\mapsto(1,2)\mapsto(2,3)\mapsto\cdots
$$

$$
\mathsf{Pred}\;\overline n\to_\beta^*\overline{\max(n-1,0)}.
$$

## Delaying CBV computation

Ordinary $\mathsf{If}\;b\;e_t\;e_f$ evaluates both branch arguments. Thus $\mathsf{If}\;\mathsf{True}\;I\;\Omega$ diverges.

**Thunk:** $\lambda u.e$, with fresh $u$. A value; apply to $I$ to run $e$.

Using the ordinary Church booleans above, with $I=\lambda x.x$:

$$
\mathsf{If}_{\mathrm{cbv}}
\triangleq\lambda b.\lambda t.\lambda f.(b\,t\,f)\,I.
$$

$$
\begin{aligned}
\mathsf{If}_{\mathrm{cbv}}\;\mathsf{True}\;(\lambda u.e_t)\;(\lambda u.e_f)
&\to_{\mathrm{cbv}}^*(\lambda u.e_t)\,I\\
&\to_{\mathrm{cbv}}e_t.
\end{aligned}
$$

Both thunks are values; only the chosen body runs.

**Alternative:** build forcing into the booleans.

$$
\mathsf{True}_{\mathrm{cbv}}=\lambda t.\lambda f.t\,I,
\qquad
\mathsf{False}_{\mathrm{cbv}}=\lambda t.\lambda f.f\,I.
$$

Use $b\,(\lambda u.e_t)\,(\lambda u.e_f)$; update Boolean producers too. Do not also use $\mathsf{If}_{\mathrm{cbv}}$ (double forcing).
