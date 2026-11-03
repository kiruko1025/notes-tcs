---
title: "Lambda Calculus"
author: ""
tags: [CSE590]
draft: false
---

# Lambda Calculus

## Lambda syntax

Countably infinite variable set $\mathrm{Var}$; finite terms:

$$
e::=x\mid\lambda x.e\mid e_1\,e_2.
$$

| Form | Meaning |
| --- | --- |
| $x$ | Variable reference. |
| $\lambda x.e$ | Function: parameter $x$, body $e$. |
| $e_1\,e_2$ | Apply $e_1$ to $e_2$. |

- $e,e_1,e_2$: metavariables ranging over terms.
- Untyped: no restrictions on application; $x\,x$ allowed.
- Numbers/booleans: later encodings, not primitive syntax.

### Parsing

$$
\begin{aligned}
e_1\,e_2\,e_3&=(e_1\,e_2)\,e_3
&&\text{application: left-associative},\\
\lambda x.e_1\,e_2&=\lambda x.(e_1\,e_2)
&&\text{body extends right},\\
\lambda x\,y.e&=\lambda x.\lambda y.e
&&\text{currying}.
\end{aligned}
$$

**Watch:** $\lambda x.x\,y\ne(\lambda x.x)\,y$.

**Currying:** take one argument; return a function for the next.

$$
(\lambda x.\lambda y.x)\,a\,b
\to_\beta(\lambda y.a)\,b\to_\beta a
\qquad(y\notin\mathrm{FV}(a)).
$$

### Common terms

| Name | Term |
| --- | --- |
| Identity $I$ | $\lambda x.x$ |
| First selector $K$ | $\lambda x.\lambda y.x$ |
| Second selector | $\lambda x.\lambda y.y$ |
| Application | $\lambda f.\lambda x.f\,x$ |
| Composition: $f$, then $g$ | $\lambda f.\lambda g.\lambda x.g\,(f\,x)$ |

## Binding and free variables

- **Binder:** $x$ in $\lambda x.e$.
- **Bound occurrence:** refers to nearest enclosing binder of the same name.
- **Free occurrence:** no enclosing matching binder.
- **Shadowing:** in $\lambda x.\lambda x.x$, the final $x$ refers to the inner binder.

$$
\begin{aligned}
\mathrm{FV}(x)&=\{x\},\\
\mathrm{FV}(e_1\,e_2)&=\mathrm{FV}(e_1)\cup\mathrm{FV}(e_2),\\
\mathrm{FV}(\lambda x.e)&=\mathrm{FV}(e)\setminus\{x\}.
\end{aligned}
$$

- **Closed term / combinator:** $\mathrm{FV}(e)=\varnothing$.
- **Open term:** at least one free variable.
- Example: $\mathrm{FV}(\lambda x.x\,y)=\{y\}$.

## Beta reduction

$$
(\lambda x.e)\,s\to_\beta e[x\mapsto s].
$$

Replace free occurrences of $x$ by $s$; **avoid capture**.

$$
(\lambda x.\lambda y.y)\,a\,b
\to_\beta(\lambda y.y)\,b
\to_\beta b.
$$

Reduction rules and strategies: [reduction and evaluation](03-reduction-and-evaluation.md).

## Capture: the main mistake

Expected result: first argument $y$.

$$
\begin{aligned}
(\lambda x.\lambda y.x)\,y\,z
&\equiv_\alpha(\lambda x.\lambda a.x)\,y\,z\\
&\to_\beta(\lambda a.y)\,z
\to_\beta y.
\end{aligned}
$$

**Wrong:** replacing $x$ directly gives $(\lambda y.y)\,z\to z$.

- Cause: inner $\lambda y$ captures the argument's free $y$.
- Fix: rename that binder to fresh $a$ before substitution.

## Freshness

- **Fresh for $e$:** not in $\mathrm{FV}(e)$.
- Safe implementation choice: new name absent everywhere in the relevant terms.
- Infinite names + finite terms $\Rightarrow$ always a fresh choice.
- **Support** of a term modulo alpha equivalence: its free-variable set.

## Swapping names

$e[x\leftrightarrow y]$: simultaneous exchange of **all** $x,y$ names, including binders.

$$
z[x\leftrightarrow y]=
\begin{cases}
y & z=x,\\
x & z=y,\\
z & \text{otherwise}.
\end{cases}
$$

$$
(e_1\,e_2)[x\leftrightarrow y]
=e_1[x\leftrightarrow y]\;e_2[x\leftrightarrow y],
$$

$$
(\lambda z.e)[x\leftrightarrow y]
=\lambda\bigl(z[x\leftrightarrow y]\bigr).e[x\leftrightarrow y].
$$

- Reversible: $(e[x\leftrightarrow y])[x\leftrightarrow y]=e$.
- Unlike substitution: also changes binding sites and free names.
- Arbitrary swap $\ne$ alpha renaming.

Example: $(\lambda x.x\,y)[x\leftrightarrow y]=\lambda y.y\,x$. Free name changes; not alpha-equivalent.

## Alpha equivalence

$e\equiv_\alpha e'$: same syntax/binding structure; same free names; bound names may differ.

$$
\lambda x.x\equiv_\alpha\lambda a.a,
\qquad
\lambda x.y\not\equiv_\alpha\lambda x.z\quad(y\ne z).
$$

Recursive comparison:

$$
x\equiv_\alpha y\iff x=y,
$$

$$
e_1\,e_2\equiv_\alpha e_1'\,e_2'
\iff(e_1\equiv_\alpha e_1')\land(e_2\equiv_\alpha e_2'),
$$

$$
\lambda x.e\equiv_\alpha\lambda y.e'
\iff e[x\leftrightarrow z]\equiv_\alpha e'[y\leftrightarrow z].
$$

Choose common $z$ absent everywhere in $e,e',x,y$. Different outer constructors: never alpha-equivalent.

**Shadowing:**

$$
\lambda x.\lambda x.x\equiv_\alpha\lambda x.\lambda y.y
\not\equiv_\alpha\lambda x.\lambda y.x.
$$

First two: return inner parameter. Last: return outer parameter.

**Barendregt convention:** bound names distinct from each other and relevant free names. Rename again after duplication.

## Capture-avoiding substitution

$e[x\mapsto s]$: replace only **free** occurrences of $x$.

$$
y[x\mapsto s]=
\begin{cases}
s & y=x,\\
y & y\ne x,
\end{cases}
$$

$$
(e_1\,e_2)[x\mapsto s]
=(e_1[x\mapsto s])\,(e_2[x\mapsto s]).
$$

$$
\begin{aligned}
(\lambda x.e)[x\mapsto s]&=\lambda x.e,\\
(\lambda y.e)[x\mapsto s]&=\lambda y.(e[x\mapsto s])
&&\text{if }y\ne x,\ y\notin\mathrm{FV}(s),\\
(\lambda y.e)[x\mapsto s]&=\lambda z.((e[y\mapsto z])[x\mapsto s])
&&\text{if }y\ne x,\ y\in\mathrm{FV}(s).
\end{aligned}
$$

Last case: $z$ absent everywhere in $e,s,x,y$. Fresh choices give alpha-equivalent results.

Examples:

$$
\begin{aligned}
(x\,(\lambda x.x))[x\mapsto y]&=y\,(\lambda x.x),\\
(\lambda y.x\,y)[x\mapsto y]&\equiv_\alpha\lambda a.y\,a.
\end{aligned}
$$

Useful facts:

$$
x\notin\mathrm{FV}(e)\Rightarrow e[x\mapsto s]\equiv_\alpha e,
$$

$$
\mathrm{FV}(e[x\mapsto s])
\subseteq(\mathrm{FV}(e)\setminus\{x\})\cup\mathrm{FV}(s).
$$

Equality in the second formula when $x\in\mathrm{FV}(e)$. Inclusion proof: [substitution bounds free variables](06-induction-and-proof-rules.md#proof_1_substitution_bounds_free_variables).

## Nameless representations

Example: $\lambda f.\lambda x.\lambda y.(f\,x)\,(f\,y)$.

| Representation | Numbering | Result |
| --- | --- | --- |
| De Bruijn indices | Nearest binder = $0$; count outward. | $\lambda.\lambda.\lambda.(2\;1)\,(2\;0)$ |
| De Bruijn levels | Outermost binder = $0$; count inward. | $\lambda.\lambda.\lambda.(0\;1)\,(0\;2)$ |

At binder depth $d$:

$$
\text{index}=d-1-\text{level}.
$$

- Numbers here: binder references, not Church numerals.
- Alpha-equivalent closed terms: identical nameless representation.
- Open terms: require an external context or separate free names.
- Moving terms across binders: may require index shifting.

## De Bruijn substitution

Zero-based indices; fixed context for free variables.

In context $[y]$:

$$
(\lambda x.\lambda z.x)\,y
\quad\leftrightarrow\quad
(\lambda.\lambda.1)\;0
\to_\beta\lambda.1.
$$

$\lambda.1$ refers to free $y$; $\lambda.0$ would mean identity.

### Shift

$\uparrow_c^d t$: add $d$ to indices at least cutoff $c$.

$$
\uparrow_c^d k=
\begin{cases}k&k<c,\\k+d&k\ge c,\end{cases}
$$

$$
\begin{aligned}
\uparrow_c^d(t_1\,t_2)&=(\uparrow_c^dt_1)\,(\uparrow_c^dt_2),\\
\uparrow_c^d(\lambda.t)&=\lambda.(\uparrow_{c+1}^dt).
\end{aligned}
$$

Examples: $\uparrow_0^1(\lambda.1)=\lambda.2$; $\uparrow_0^1(\lambda.0)=\lambda.0$.

### Substitute index $j$

$$
\operatorname{sub}_j(k,s)=
\begin{cases}s&k=j,\\k&k\ne j,\end{cases}
$$

$$
\begin{aligned}
\operatorname{sub}_j(t_1\,t_2,s)
&=\operatorname{sub}_j(t_1,s)\;\operatorname{sub}_j(t_2,s),\\
\operatorname{sub}_j(\lambda.t,s)
&=\lambda.\operatorname{sub}_{j+1}(t,\uparrow_0^1s).
\end{aligned}
$$

Full beta rule:

$$
(\lambda.t)\,s\to_\beta
\uparrow_0^{-1}\bigl(\operatorname{sub}_0(t,\uparrow_0^1s)\bigr).
$$

1. Shift argument into binder's context.
2. Substitute, shifting again under nested binders.
3. Shift down to remove the contracted binder; no negative indices allowed.
