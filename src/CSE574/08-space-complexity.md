---
title: "Space Complexity"
author: ""
tags: [CSE574, space, Savitch, PSPACE]
draft: false
---

# Space Complexity

## Space model

Count maximum work-tape cells used. Read-only input and write-only output do not count. Reusing cells is free.

- $\mathrm{SPACE}(s)$: deterministic $O(s(n))$ space.
- $\mathrm{NSPACE}(s)$: nondeterministic; bound holds on every branch.

Assume $s(n)\ge\log n$ and space-constructible: computable in $O(s(n))$ space.

$$
\mathrm{DTIME}(t(n))\subseteq\mathrm{SPACE}(t(n)).
$$

But $s$ counter bits can support $2^s$ steps.

## Polynomial space

$$
\mathrm{PSPACE}=\bigcup_{c>0}\mathrm{SPACE}(n^c),
\qquad
\mathrm{NPSPACE}=\bigcup_{c>0}\mathrm{NSPACE}(n^c).
$$

$\mathrm{3SAT}\in\mathrm{PSPACE}$: enumerate assignments; reuse memory. Thus $\mathrm{NP}\subseteq\mathrm{PSPACE}$.

## Configuration graphs

Fix $M,x$. A configuration stores state, work tapes, and head positions; $x$ stays on the input tape.

$$
\text{configuration size}=O(s(n)+\log n)=O(s(n)),
\qquad N\le2^{O(s(n))}.
$$

$G_{M,x}$: configurations as vertices; legal steps as edges. Check an edge directly from the transition rules.

A polynomial-size CNF can encode this check, with auxiliary bits:

$$
C\to C'\iff\exists z\;\Phi_{M,x}(C,C',z)=1.
$$

Normalize acceptance: erase work tapes and reset heads before entering a unique accepting configuration. Then

$$
M\text{ accepts }x\iff C_{\mathrm{start}}\leadsto C_{\mathrm{accept}}.
$$

- Deterministic decider: cannot repeat a configuration.
- Nondeterministic acceptance: a simple accepting path has fewer than $N$ edges.

Enumerate the graph and search it:

$$
N^2\operatorname{poly}(n+s(n))=2^{O(s(n))}.
$$

Therefore

$$
\mathrm{SPACE}(s(n))\subseteq\mathrm{NSPACE}(s(n))
\subseteq\mathrm{DTIME}(2^{O(s(n))}).
$$

Explicit graph storage may be exponential. Savitch uses implicit search with $O(s^2)$ space.

## Savitch's theorem

For space-constructible $s(n)\ge\log n$,

$$
\mathrm{NSPACE}(s(n))\subseteq\mathrm{SPACE}(s(n)^2).
$$

Use a configuration graph with $N\le2^{O(s(n))}$ vertices. Define

$$
\mathrm{Reach}(u,v,i)\iff
u\leadsto v\text{ by a path of length at most }2^i.
$$

Base: $\mathrm{Reach}(u,v,0)$ iff $u=v$ or $u\to v$.

$$
\mathrm{Reach}(u,v,i)
=\bigvee_z\bigl(
\mathrm{Reach}(u,z,i-1)\land\mathrm{Reach}(z,v,i-1)\bigr).
$$

Enumerate $z$; run the two recursive calls sequentially. Generate vertices and edges on demand.

Top call: $\mathrm{Reach}(C_{\mathrm{start}},C_{\mathrm{accept}},\lceil\log_2N\rceil)$.

Each stack frame stores $u,v,z,i$: $O(\log N)$ bits. Depth: $O(\log N)$. Sibling calls reuse space:

$$
S(N,i)\le S(N,i-1)+O(\log N),
\qquad S=O(\log^2N)=O(s(n)^2).
$$

Consequences:

$$
\mathrm{NL}\subseteq\mathrm{SPACE}(\log^2n),
\qquad\mathrm{PSPACE}=\mathrm{NPSPACE}.
$$

Squaring preserves polynomial space, not logarithmic space. This does not settle L versus NL.

## Closure under complement

For space-constructible $s(n)\ge\log n$,

$$
\mathrm{NSPACE}(s(n))=\mathrm{coNSPACE}(s(n)).
$$

Apply [inductive counting](10-logspace-and-nl.md#inductive_counting) to the configuration graph, with $2^{O(s(n))}$ vertices. Each label and counter uses $O(s(n))$ bits.

## Known containments

$$
\mathrm L\subseteq\mathrm{NL}\subseteq\mathrm P
\subseteq\mathrm{NP}\subseteq\mathrm{PH}
\subseteq\mathrm{PSPACE}=\mathrm{NPSPACE}\subseteq\mathrm{EXP}.
$$

Hierarchy theorems give $\mathrm L\ne\mathrm{PSPACE}$ and $\mathrm P\ne\mathrm{EXP}$. They do not identify an adjacent strict inclusion in this chain.
