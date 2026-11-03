---
title: "Logspace and NL"
author: ""
tags: [CSE574, logspace, NL, reachability]
draft: false
---

# Logspace and NL

## L and NL

$$
\mathrm L=\mathrm{SPACE}(\log n),
\qquad
\mathrm{NL}=\mathrm{NSPACE}(\log n).
$$

Space model and configuration graphs: [Space complexity](08-space-complexity.md).

- $\mathrm{EVEN}\in\mathrm L$: one parity bit; actually constant space.
- $\mathrm{MULT}=\{\langle a,b,c\rangle:c=ab\}\in\mathrm L$: grade-school multiplication, one column at a time. Store indices, column sum, carry; rescan input. Each needs $O(\log n)$ bits for total input length $n$.

## Logspace functions

A logspace transducer has:

- Read-only input.
- $O(\log n)$ work space.
- Write-only output, moving right after each written bit.

Output is not workspace. A halting deterministic transducer has polynomially many internal configurations, hence polynomial output length.

Equivalent bitwise definition: $|f(x)|\le\operatorname{poly}(|x|)$ and

$$
\begin{aligned}
L_f&=\{\langle x,i\rangle:1\le i\le|f(x)|,\ f(x)_i=1\}\in\mathrm L,\\
L_f'&=\{\langle x,i\rangle:1\le i\le|f(x)|\}\in\mathrm L.
\end{aligned}
$$

$i$ is binary. $L_f'$ distinguishes a zero bit from the end of output.

- Transducer to bitwise: rerun it; count outputs until position $i$ or halt.
- Bitwise to transducer: test successive positions; compute and print each bit.

## Logspace reductions

$$
A\le_\ell B
\iff\exists\text{ logspace }f,\quad x\in A\iff f(x)\in B.
$$

$B$ is NL-complete if $B\in\mathrm{NL}$ and every $A\in\mathrm{NL}$ reduces to it by $\le_\ell$.

Logspace functions compose. Simulate $g$ on a virtual input $f(x)$; recompute each requested bit. Store its index, not the whole output.

Thus $\le_\ell$ is transitive; $A\le_\ell B\in\mathrm L$ implies $A\in\mathrm L$.
Polynomial-time reductions would be too strong here: $\mathrm{NL}\subseteq\mathrm P$.

## PATH is NL-complete

$$
\mathrm{PATH}=\{\langle G,s,t\rangle:s\leadsto t\text{ in directed }G\}.
$$

**Membership:** guess at most $N-1$ edges in an $N$-vertex graph. Store current vertex and step counter: $O(\log N)$ bits.

**Hardness:** for a nondeterministic logspace machine $M$,

$$
x\mapsto\langle G_{M,x},c_{\mathrm{start}},c_{\mathrm{accept}}\rangle.
$$

- Configuration length $O(\log n)$; graph has $n^{O(1)}$ vertices.
- Output its adjacency matrix one bit at a time.
- Each bit checks one legal transition between two configurations.
- Invalid encodings have no edges. Length and endpoint indices are logspace computable.

$$
x\in L(M)\iff c_{\mathrm{start}}\leadsto c_{\mathrm{accept}}.
$$

Consequently, $\mathrm{PATH}\in\mathrm L\iff\mathrm L=\mathrm{NL}$.

Undirected reachability is in L: Reingold's theorem.

## Read-once certificates

$L\in\mathrm{NL}$ iff some deterministic logspace verifier $V$ satisfies

$$
x\in L\iff\exists u\in\{0,1\}^{p(|x|)},\quad V(x,u)=1,
$$

for a polynomial $p$. Input read-only; certificate read-only and read-once.

- Nondeterminism to certificate: record the choices on an accepting path.
- Certificate to nondeterminism: guess each next bit when needed.
- A polynomial bound suffices: remove cycles from an accepting configuration path.

Two-way access lets a logspace verifier check a SAT assignment clause by clause. Repeating assignments on a read-once tape does not ensure the copies agree.

## Inductive counting

**Immerman–Szelepcsényi:** $\mathrm{NL}=\mathrm{coNL}$.

Since [PATH is NL-complete](#path_is_nl-complete), suffice to show $\overline{\mathrm{PATH}}\in\mathrm{NL}$.
Let $G$ have $N$ vertices. Define

$$
R_i=\{v:s\leadsto v\text{ in at most }i\text{ edges}\},
\qquad c_i=|R_i|.
$$

$R_0=\{s\}$, $c_0=1$, and $R_N$ contains every reachable vertex.

### Enumerating a set from its count

Assume the correct $c_i$ is known. Certificate:

1. List $c_i$ distinct vertices in increasing order.
2. For each, give a path from $s$ of length at most $i$.
3. Reject any bad order, count, or path.

Every listed vertex is in $R_i$. Correct count means none is missing.
Only the previous label, path position, and counters are stored.

### Computing the next count

$$
v\in R_{i+1}\iff v\in R_i
\ \lor\ \exists u\in R_i:(u,v)\in E.
$$

For each vertex $v$, in label order:

1. Read a fresh certified enumeration of $R_i$.
2. Set a flag if some listed $u$ equals $v$ or has edge $u\to v$.
3. Add the flag to a new counter.

The result is exactly $c_{i+1}$. Every successful enumeration is the same true set; copies need not be compared directly.

Start with $c_0=1$, compute through $c_N$, then enumerate $R_N$ and accept iff $t$ is absent.

- Soundness: correct counts force complete lists; an accepting certificate cannot omit $t$.
- Completeness: supply true lists and paths when $t$ is unreachable.
- Space: constantly many $O(\log N)$-bit counters and labels.
- Certificate length: polynomial; at most $O(N^4\log N)$ bits with this implementation.

Thus $\overline{\mathrm{PATH}}\in\mathrm{NL}$. Logspace reductions transfer this to complements of all NL languages.

Sources: [Lecture 9, Nie](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture09/lecture09-Nie-Zinnia.pdf>); [Lecture 9, Menacho Ordonez](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture09/lecture09-MenachoOrdonez-Daniel.pdf>); [Lecture 10](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture10/lecture10-Chae-Yeonu.pdf>); [Lecture 11](</home/everett/Desktop/Umich-EECS/CSE574/scribes/lecture11/lecture11-Frieler-Nicholas.pdf>); [Chapter 4](</home/everett/Desktop/Umich-EECS/CSE574/handouts/Chapter 04.pdf>).
