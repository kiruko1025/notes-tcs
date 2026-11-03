---
title: "Types and Type Soundness"
author: ""
tags: [CSE590]
draft: false
---

# Types and Type Soundness

Types rule out invalid operations. Well typed = a typing derivation exists.

## Syntax

$$
\begin{aligned}
\tau&::=\mathsf{int}\mid\mathsf{bool}\mid\tau_1\to\tau_2,\\
e&::=n\mid\mathsf{true}\mid\mathsf{false}\mid x\mid\lambda x:\tau.e\mid e_1\,e_2\\
&\quad\mid e_1+e_2\mid\mathsf{if}\ e\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2,\\
v&::=n\mid\mathsf{true}\mid\mathsf{false}\mid\lambda x:\tau.e.
\end{aligned}
$$

Integers and Booleans are primitive here. Lambda parameters carry types.

Application associates left; arrows associate right:

$$
f\,x\,y=(f\,x)\,y,
\qquad A\to B\to C=A\to(B\to C).
$$

## Typing judgment

$$
\Gamma\vdash e:\tau,
\qquad\Gamma::=\cdot\mid\Gamma,x:\tau.
$$

$\Gamma$: variable types. $\vdash e:\tau$: empty context. Rename binders to avoid repeated names.

$$
\Gamma\vdash n:\mathsf{int},\qquad
\Gamma\vdash\mathsf{true}:\mathsf{bool},\qquad
\Gamma\vdash\mathsf{false}:\mathsf{bool}.
$$

$$
\frac{x:\tau\in\Gamma}{\Gamma\vdash x:\tau}
\qquad
\frac{\Gamma,x:\tau_1\vdash e:\tau_2}
{\Gamma\vdash\lambda x:\tau_1.e:\tau_1\to\tau_2}
$$

$$
\frac{\Gamma\vdash e_1:\tau_1\to\tau_2\qquad\Gamma\vdash e_2:\tau_1}
{\Gamma\vdash e_1\,e_2:\tau_2}
$$

$$
\frac{\Gamma\vdash e_1:\mathsf{int}\qquad\Gamma\vdash e_2:\mathsf{int}}
{\Gamma\vdash e_1+e_2:\mathsf{int}}
$$

$$
\frac{\Gamma\vdash e:\mathsf{bool}\qquad\Gamma\vdash e_1:\tau\qquad\Gamma\vdash e_2:\tau}
{\Gamma\vdash\mathsf{if}\ e\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2:\tau}
$$

Both branches need the same type, even if one is never taken.

## Example derivation

$$
\frac{
  \frac{x:\mathsf{int},y:\mathsf{bool}\vdash x:\mathsf{int}}
  {x:\mathsf{int}\vdash\lambda y:\mathsf{bool}.x:\mathsf{bool}\to\mathsf{int}}
}{\vdash\lambda x:\mathsf{int}.\lambda y:\mathsf{bool}.x:
\mathsf{int}\to\mathsf{bool}\to\mathsf{int}}
$$

Apply twice:

$$
\vdash(\lambda x:\mathsf{int}.\lambda y:\mathsf{bool}.x)\,2\,\mathsf{true}:\mathsf{int}.
$$

Evaluation returns $2$.

## Type checking

Syntax-directed: outer expression determines the rule. Check subterms recursively; verify their types match.

$$
\Gamma\vdash e:\tau\ \land\ \Gamma\vdash e:\tau'
\Rightarrow\tau=\tau'.
$$

Unique type for a fixed context and annotated term. Proof: induction on syntax.

- `true + 1`: Boolean where integer required.
- `3 4`: integer where function required.
- `if true then 1 else false`: branch types differ.

Self-application $x\,x$ requires $x:A$ and $x:A\to B$, hence $A=A\to B$. Impossible for finite simple types. So $\Omega$ and the usual $Y$ combinator are untypable.

$$
\Gamma\vdash e:\tau\Rightarrow\mathrm{FV}(e)\subseteq\operatorname{dom}(\Gamma).
$$

In particular, empty context implies closed term.

Discussion examples: refinement types add predicates; linear types track resource use; security types track information flow; session types track communication protocols. The property proved depends on the type system.

## Evaluation contexts

Here $\to$ means CBV. Types do not change the computation rules.

$E$: expression with one hole, in the next evaluation position.

$$
E::=[\ ]\mid E\,e\mid v\,E\mid E+e\mid n+E
\mid\mathsf{if}\ E\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2.
$$

$E[e]$: fill the hole with $e$.

- Application: function first, then argument.
- Addition: left first; right only after a numeral.
- Conditional: guard first; only the chosen branch runs.
- No holes under lambdas or inside unchosen branches.

Local computation rules:

$$
\begin{aligned}
(\lambda x:\tau.e)\,v&\to e[x\mapsto v],\\
n_1+n_2&\to n_3\qquad(n_3=n_1+n_2),\\
\mathsf{if}\ \mathsf{true}\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2&\to e_1,\\
\mathsf{if}\ \mathsf{false}\ \mathsf{then}\ e_1\ \mathsf{else}\ e_2&\to e_2.
\end{aligned}
$$

Close under contexts: $r\to r'\Rightarrow E[r]\to E[r']$.

Example: $E=(\lambda x:\mathsf{int}.x+1)\,[\ ]$.

$$
(\lambda x:\mathsf{int}.x+1)\,(2+3)
\to(\lambda x:\mathsf{int}.x+1)\,5
\to5+1\to6.
$$

Rocq's `{e : exp | value e}` stores an expression and a proof it is a value. Evaluation contexts use this for the $v$ in $v\,E$.

## Values and stuck terms

Value = finished. Stuck = not a value, with no next step.

Examples: $\mathsf{true}+1$, $3\,4$, $\mathsf{if}\ 3\ \mathsf{then}\ 1\ \mathsf{else}\ 2$.

For a closed nonvalue, repeatedly follow the context grammar to the unique next evaluation position. Its active subterm is a redex or a stuck operation.

Unique position + unique local result $\Rightarrow$ deterministic evaluation.

A lambda is a value even if its body contains redexes. Value $\ne$ full beta normal form.

## Canonical forms

For a closed value $\vdash v:\tau$:

| Type | Possible value |
| --- | --- |
| $\mathsf{int}$ | Numeral $n$ |
| $\mathsf{bool}$ | $\mathsf{true}$ or $\mathsf{false}$ |
| $A\to B$ | $\lambda x:A.e$ |

Proof: inspect value forms and their typing rules.

The value assumption matters: a typed application need not already be a lambda or numeral.

## Progress

$$
\boxed{\vdash e:\tau\Rightarrow e\text{ is a value }\lor\exists e'.\ e\to e'.}
$$

Proof: induction on the typing derivation.

| Case | Reason |
| --- | --- |
| Constant, lambda | Already a value |
| Variable | Impossible in empty context |
| Application | Step function; else step argument; else canonical forms give beta redex |
| Addition | Step left; else step right; else both are numerals |
| Conditional | Step guard; else Boolean canonical form selects a branch |

Application's final case:

$$
\vdash v_1:A\to B,\quad\vdash v_2:A
\Rightarrow v_1=\lambda x:A.e
\Rightarrow v_1\,v_2\to e[x\mapsto v_2].
$$

Closedness is necessary: $x:\mathsf{int}\vdash x:\mathsf{int}$, but $x$ neither steps nor is a value.

## Substitution

Weakening: unused assumptions may be added. Exchange: distinct assumptions may be reordered. Rename binders fresh before substitution.

$$
\boxed{
\Gamma,x:A\vdash e:B\quad\land\quad\Gamma\vdash s:A
\Rightarrow\Gamma\vdash e[x\mapsto s]:B.
}
$$

Proof: induction on the typing derivation of $e$.

- $e=x$: use the typing of $s$.
- Other variable or constant: unchanged.
- Application: apply IH to both parts; rebuild App.
- Lambda $\lambda y:C.e_0$: choose $y\ne x$, $y\notin\mathrm{FV}(s)$. Weaken $s$ into $\Gamma,y:C$; apply IH to the body; rebuild Abs.
- Addition and conditional: IH on subterms; rebuild rule.

The lemma works for terms; CBV uses its value instance.

## Preservation

$$
\boxed{\Gamma\vdash e:\tau\land e\to e'\Rightarrow\Gamma\vdash e':\tau.}
$$

Induction on the step derivation; invert the typing judgment.

Beta case:

$$
\Gamma\vdash(\lambda x:A.e)\,v:B
\Rightarrow
\Gamma,x:A\vdash e:B,\quad\Gamma\vdash v:A.
$$

Substitution gives $\Gamma\vdash e[x\mapsto v]:B$.

Context step: IH preserves the subterm's type; rebuild the surrounding typing rule. Arithmetic preserves $\mathsf{int}$; either conditional branch has the original result type.

## Type soundness

Progress + preservation:

$$
\vdash e:\tau\land e\to^*e'
\Rightarrow e'\text{ is a value or can step}.
$$

Well-typed closed programs never get stuck. Termination needs a [separate proof](11-termination-and-logical-relations.md).

Safe $\ne$ typable. Example:

$$
\mathsf{if}\ \mathsf{true}\ \mathsf{then}\ 1\ \mathsf{else}\ (\mathsf{true}+1)\to1.
$$

Safe execution, but the unused branch fails typing. The type system rejects some safe programs.

Products, sums, and their typing rules: [algebraic data types](10-algebraic-data-types.md).

Sources: `lec11-slides.pdf`, slides 9–14; `lec12-slides.pdf`, slides 8–12; `lec13-slides.pdf`, slides 5–8; Kozen, `kozen-cs6110-lec20-typed-lambda-calculus.pdf`, §§2–6, and `kozen-cs6110-lec22-type-soundness.pdf`, §§1–4; [Discussion 6](https://externalhom.com/3598e8b965c9563c/), §§2–4.
