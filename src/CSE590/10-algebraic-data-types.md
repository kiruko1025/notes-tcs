---
title: "Algebraic Data Types"
author: ""
tags: [CSE590]
draft: false
---

# Algebraic Data Types

Products: both. Sums: either. Extend the [simply typed lambda calculus](09-types-and-type-soundness.md).

## Products

$1$: nullary product, value $()$. $A\times B$: pair, with both components.

$$
\Gamma\vdash():1,
\qquad
\frac{\Gamma\vdash e_1:A\qquad\Gamma\vdash e_2:B}
{\Gamma\vdash(e_1,e_2):A\times B},
\qquad
\frac{\Gamma\vdash e:A_1\times A_2}{\Gamma\vdash e.i:A_i}.
$$

$$
(v_1,v_2).i\to v_i\qquad(i=1,2).
$$

Pairs evaluate left to right; projection evaluates its pair first.

## Sums

$A+B$: either an $A$ or a $B$, with a tag. Injection annotation gives the **other** type.

$$
\frac{\Gamma\vdash e:A}{\Gamma\vdash\mathsf{inl}_B\,e:A+B},
\qquad
\frac{\Gamma\vdash e:B}{\Gamma\vdash\mathsf{inr}_A\,e:A+B}.
$$

Both cases must return the same type:

$$
\frac{\Gamma\vdash e:A+B\qquad
\Gamma,x:A\vdash e_1:C\qquad\Gamma,y:B\vdash e_2:C}
{\Gamma\vdash\mathsf{case}\ e\ \mathsf{of}\
\mathsf{inl}\ x\Rightarrow e_1\mid\mathsf{inr}\ y\Rightarrow e_2:C}.
$$

$$
\begin{aligned}
\mathsf{case}\ (\mathsf{inl}_B\,v)\ \mathsf{of}\cdots&\to e_1[x\mapsto v],\\
\mathsf{case}\ (\mathsf{inr}_A\,v)\ \mathsf{of}\cdots&\to e_2[y\mapsto v].
\end{aligned}
$$

Evaluate payloads and the scrutinee; evaluate only the selected branch.

Example:

$$
\mathsf{case}\ (\mathsf{inl}_{\mathsf{bool}}\,3)\ \mathsf{of}\
\mathsf{inl}\ x\Rightarrow x+1\mid\mathsf{inr}\ y\Rightarrow0
\to3+1\to4.
$$

## Empty type

$0$: nullary sum. No values, no introduction rule.

$$
\frac{\Gamma\vdash e:0}{\Gamma\vdash\mathsf{case}_C\ e\ \mathsf{of}\{\}:C}.
$$

Empty case has no branches. It evaluates its scrutinee; there is no value-reduction rule.

New canonical forms: $1$ gives $()$; $A\times B$ gives a pair; $A+B$ gives an injection; $0$ gives no possible value. Progress and preservation extend using these forms and substitution for case branches.

## Type isomorphisms

$A\cong B$: programs $f:A\to B$, $g:B\to A$ undo each other:

$$
g(f(a))=a,\qquad f(g(b))=b.
$$

$$
\begin{aligned}
A\times1&\cong A,& A+0&\cong A,& A\times0&\cong0,\\
A\times B&\cong B\times A,& \mathsf{bool}&\cong1+1,\\
A\times(B+C)&\cong(A\times B)+(A\times C),\\
(A\times B\to C)&\cong(A\to B\to C).
\end{aligned}
$$

Examples: swap $(a,b)\mapsto(b,a)$; $\mathsf{Option}(A)\cong1+A$; `Result<A,B>` is a sum.

Currying and its inverse:

$$
\mathsf{curry}\ h=\lambda a:A.\lambda b:B.h\,(a,b),
$$

$$
\mathsf{uncurry}\ k=\lambda p:A\times B.k\,(p.1)\,(p.2).
$$

## Curry–Howard correspondence

Type = proposition; program = proof; evaluation = proof simplification.

| Type | Logic | Program/proof |
| --- | --- | --- |
| $1$ | True $\top$ | $()$ |
| $0$ | False $\bot$ | Empty case: from false, anything |
| $A\times B$ | $A\land B$ | Pair; projections |
| $A+B$ | $A\lor B$ | Tagged choice; proof by cases |
| $A\to B$ | $A\Rightarrow B$ | Lambda; application = modus ponens |

Example: $(v_1,v_2).1\to v_1$ removes an introduction/elimination detour.

Logic is intuitionistic. General excluded middle $A\lor\neg A$ is not derivable here; $\neg A=A\to0$. Its double negation is derivable.

Dependent types extend this: $\Pi x:A.B(x)$ corresponds to $\forall$; $\Sigma x:A.B(x)$ stores a witness and evidence. In Rocq, a `Prop` existential has stricter elimination than a `Type`-level dependent pair.

Categorical view: types are objects, programs are arrows; products, sums, and functions give a bicartesian closed category, modulo the corresponding beta/eta equations.
