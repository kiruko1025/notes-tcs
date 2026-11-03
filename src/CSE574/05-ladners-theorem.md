---
title: "Ladner's Theorem"
author: ""
tags: [CSE574, Ladner, NP-intermediate]
draft: false
---

# Ladner's Theorem

$$
\mathrm P\ne\mathrm{NP}
\implies\exists L\in\mathrm{NP}\setminus\mathrm P
\text{ that is not NP-complete}.
$$

Such $L$ is **NP-intermediate**.

### Delayed padding

Use an unambiguous encoding:

$$
\mathrm{SAT}_H=
\{\varphi\,0\,1^{n^{H(n)}}:
\varphi\in\mathrm{SAT},\ n=|\varphi|\}.
$$

Length $N=n+1+n^{H(n)}$. Fixed bounded $H$ gives polynomial padding.

Construct slowly growing, integer-valued $H$, computable in $\operatorname{poly}(n)$ time:

1. Use a padded enumeration. At stage $n$, test its first $\lfloor\log\log n\rfloor$ machines.
2. Test all inputs $y$ of length $\le\lfloor\log n\rfloor$; clock $M_i(y)$ at $i(1+|y|)^i$ steps.
3. $H(n)$ = least index correct on every test; use the cap if none. Fix small stages separately.

Testing membership uses earlier $H$ values and brute-force SAT on short cores. The cutoffs keep total work polynomial in $n$.

- Correct polynomial-time decider $\Rightarrow$ some permanent passing index $\Rightarrow$ bounded $H$.
- Every incorrect machine has a fixed counterexample $\Rightarrow$ eventually eliminated.
- No polynomial-time decider $\Rightarrow$ $H(n)\to\infty$.

### Three properties

Assume P ≠ NP.

1. **In NP:** validate padding; guess and check a satisfying assignment.
2. **Outside P:** a decider would bound $H$. Then SAT reduces by polynomial padding to a language in P: contradiction.
3. **Not NP-complete:** suppose $f$ reduces SAT to $\mathrm{SAT}_H$, with $|f(\varphi)|\le n^d$ eventually.

For a valid output with core length $m$, sufficiently large $m$ gives $H(m)>2d$, hence

$$
m^{2d}<m^{H(m)}\le|f(\varphi)|\le n^d,
\qquad m<\sqrt n.
$$

Invalid padding → reject. Otherwise recurse on the smaller core; brute-force below a fixed threshold. $O(\log\log n)$ rounds, polynomial total time $\Rightarrow$ SAT in P: contradiction.

The constructed $H$ matters; arbitrary padding does not prove Ladner.

Sources: [Lecture 5, Lee](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture05/lecture05-Lee-Amy.pdf>); [Lecture 5, Wanner](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture05/lecture05-Wanner-Alice.pdf>).
