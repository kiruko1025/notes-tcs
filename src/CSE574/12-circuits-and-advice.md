---
title: "Circuits and Advice"
author: ""
tags: [CSE574, circuits, advice, P-poly]
draft: false
---

# Circuits and Advice

## Boolean circuits

Directed acyclic graph with $n$ input vertices and one designated output.

- AND/OR: fan-in $2$. NOT: fan-in $1$. Constants $0,1$ allowed.
- Size $s$: number of vertices, including inputs.
- Depth: longest input-to-output path.
- Fan-out unrestricted: gates may reuse earlier outputs.
- Encoding length $O(s\log s)$: $O(s)$ wires, $O(\log s)$ bits per index.

Evaluate gates in topological order. Every Boolean function has a circuit, e.g. its DNF; size $O(n2^n)$ suffices.

$$
x\oplus y=(x\land\neg y)\lor(\neg x\land y).
$$

$n$-bit AND: size $O(n)$; depth $O(n)$ as a chain or $O(\log n)$ as a balanced tree. Binary addition: $O(n)$ gates using carries.

## Circuit families

$\{C_n\}_{n\ge1}$: one circuit per input length. No algorithm relating the circuits is required.

$$
L\in\mathrm{SIZE}(s(n))
\iff\exists\{C_n\},\quad
|C_n|\le s(n),\quad
C_n(x)=1\iff x\in L\quad(|x|=n).
$$

$$
\mathrm{P/poly}=\bigcup_{c>0}\mathrm{SIZE}(n^c).
$$

## P is contained in P/poly

Let $M$ decide $L$ in time $T(n)=\operatorname{poly}(n)$.

1. Encode a configuration using $O(T(n))$ bits.
2. Build a polynomial-size circuit for one deterministic transition.
3. Repeat it for $T(n)$ steps; read the final accept bit.

Initial input bits remain inputs; other initial bits are constants. Halting configurations persist. The resulting $C_n$ has polynomial size and computes $M(x)$ for every $|x|=n$.

For deterministic $M$, the tableau is determined by $x$; these gates compute it. A Cook–Levin CNF checks the tableau using auxiliary variables.

## Undecidable languages in P/poly

Every unary language $U\subseteq\{1\}^*$ has linear-size circuits:

$$
C_n(x)=
\begin{cases}
\bigwedge_{i=1}^n x_i&1^n\in U,\\
0&1^n\notin U.
\end{cases}
$$

Example: $U=\{1^n:\text{the }n\text{th TM halts on empty input}\}$.

No uniform algorithm must produce $C_n$. Hence even undecidable languages lie in $\mathrm{P/poly}$, and $\mathrm P\subsetneq\mathrm{P/poly}$.

## Uniformity

A single machine outputs $C_n$ on input $1^n$.

- P-uniform: polynomial time.
- L-uniform: logarithmic workspace; write-only output.

P-uniform polynomial-size circuits capture exactly P:

- P to circuits: generate the simulation above.
- Circuits to P: generate $C_{|x|}$, then evaluate it on $x$.

## Advice

$$
L\in\mathrm{DTIME}(T(n))/a(n)
$$

if some fixed machine $M$, running in $O(T(n))$ time, has advice strings $\alpha_n\in\{0,1\}^{a(n)}$ satisfying

$$
\forall x\in\{0,1\}^n,\qquad M(x,\alpha_n)=1\iff x\in L.
$$

- Advice depends only on $n$, shared by all length-$n$ inputs.
- No requirement that $n\mapsto\alpha_n$ be computable.
- NP witnesses may depend on the individual input.

Every unary language is in $\mathrm{DTIME}(n)/1$: advice says whether $1^n\in U$; accept iff that bit is $1$ and $x=1^n$.

## Polynomial advice equals polynomial circuits

$$
\mathrm{P/poly}=\bigcup_{c,d>0}\mathrm{DTIME}(n^c)/n^d.
$$

**Circuit to advice:** let $\alpha_n$ encode $C_n$. Its length is $O(|C_n|\log|C_n|)$; evaluation takes polynomial time.

**Advice to circuit:** simulate $M(x,\alpha)$ by a polynomial-size circuit, then hardwire the bits of $\alpha_n$ as constants.

Lower bounds and Karp–Lipton: [Circuit lower bounds](13-circuit-lower-bounds.md).

Sources: [Lecture 12](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture12/lecture12-Pathak-Anwesha.pdf>); [Chapter 6](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 06.pdf>).
