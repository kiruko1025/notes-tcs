---
title: "Programming Language Foundations"
author: ""
tags: [CSE590]
draft: false
---

# Programming Language Foundations

PL = languages + precise reasoning about programs.

## Main questions

- Syntax: which programs are valid expressions?
- Semantics: what do they mean?
- Types: which errors can we rule out before execution?
- Verification: does a program satisfy its specification?

## Applications

| Area | Examples |
| --- | --- |
| Language design | TypeScript: gradual types; Rust: ownership; Swift: protocols |
| Static analysis | Detect errors without running the program |
| Synthesis | Construct programs from specifications/examples |
| Proof assistants | Lean, Rocq, Isabelle |
| Verified systems | CompCert: C compiler; seL4: OS kernel |
| Separation logic | Reason about heap updates and concurrent programs |

Same methods across software, hardware, security, and mathematics.

## Syntax and semantics

Syntax = program structure. Semantics = meaning.

| Concept | Meaning |
| --- | --- |
| Syntax | Program structure; legal expressions. |
| Operational semantics | Execution steps or evaluation rules. |
| Denotational semantics | Meaning as a mathematical object. |
| Axiomatic semantics | Properties before/after execution. |
| Static semantics | Scope, typing, other pre-execution checks. |
| Dynamic semantics | Runtime behavior. |

## Functions

- **Relation:** $R\subseteq A\times B$.
- **Total function:** exactly one output per input.

$$
f:A\to B
\qquad
\forall a\in A,\;\exists!b\in B.\;(a,b)\in f.
$$

- **Partial function** $f:A\rightharpoonup B$: at most one output; possibly undefined.
- **Graph / extension:** $\{(a,f(a))\mid a\in\operatorname{dom}(f)\}$; domain = inputs where $f$ is defined.
- **Extensional view:** input-output behavior.
- **Intensional view:** expression or algorithm computing it.
- Example: $n+n$ and $2n$ — different descriptions, same integer function.
- Programs may diverge; their computed functions need not be total.
