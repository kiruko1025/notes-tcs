---
title: "Reductions and NP-Completeness"
author: ""
tags: [CSE574, reductions, NP-completeness, Cook-Levin]
draft: false
---

# Reductions and NP-Completeness

## Karp reductions

$$
A\le_p B\iff\exists\text{ polynomial-time }f:\
\forall x,\ x\in A\iff f(x)\in B.
$$

One instance → one instance. Output length polynomially bounded.

- $A\le_p B$, $B\in\mathrm P$ $\Rightarrow$ $A\in\mathrm P$; same for NP.
- Transitive: compose the maps.
- Hardness: known hard problem → target problem.

**Clique → Independent Set:** $(G,k)\mapsto(\overline G,k)$. Complement edges between distinct vertices. Clique in $G$ ⇔ independent set in $\overline G$.

## Completeness

- $B$ NP-hard: every $A\in\mathrm{NP}$ satisfies $A\le_p B$.
- $B$ NP-complete: NP-hard and in NP.
- One NP-complete language in P $\Rightarrow$ P = NP.

Proof: give a verifier and a hardness reduction.

## TMSAT

Deterministic verifier $M$:

$$
\mathrm{TMSAT}=\{\langle M,x,1^m,1^t\rangle:
\exists u\in\{0,1\}^m,\ M(x,u)\text{ accepts within }t\text{ steps}\}.
$$

- In NP: guess $u$; simulate $t$ steps. Unary bounds make this polynomial in input length.
- NP-hard: for verifier $V$, witness bound $p$, time bound $q$,

$$
x\mapsto\langle V,x,1^{p(|x|)},1^{q(|x|)}\rangle.
$$

Thus TMSAT is NP-complete. Binary $t$ would allow exponentially long simulation.

## SAT

- Literal: $z$ or $\neg z$.
- Clause: OR of literals. CNF: AND of clauses.
- SAT: satisfiable CNFs. $k$-SAT: clause width at most $k$.
- In NP: certificate = satisfying assignment.

## Cook–Levin

**SAT is NP-complete.** Given an NP verifier $V$, construct

$$
\varphi_x\text{ satisfiable}\iff\exists u\;V(x,u)=1\iff x\in L.
$$

Runtime $T=\operatorname{poly}(|x|)$, including one-tape simulation. Tableau: $T+1$ rows, $O(T)$ cells per row. Cell symbol includes head/state when present.

$$
t_{i,j,\sigma}=1\iff\text{cell }j\text{ at time }i\text{ has symbol }\sigma.
$$

| CNF constraints | Requirement |
| --- | --- |
| Cell | Exactly one symbol per cell |
| Start | Input $x$, start state/head, blanks; free witness bits |
| Move | Legal local transitions and boundaries |
| Accept | Accepting final row; pad acceptance through time $T$ |

Exactly one:

$$
\left(\bigvee_\sigma t_{i,j,\sigma}\right)
\land\bigwedge_{\sigma\ne\tau}
(\neg t_{i,j,\sigma}\lor\neg t_{i,j,\tau}).
$$

Forbid each illegal constant-size neighborhood by a clause. Valid first row + local transitions $\Rightarrow$ legal computation.

- Witness → satisfying tableau: actual accepting computation.
- Satisfying tableau → witness: read initial witness bits; constraints force acceptance.
- Fixed alphabet, $O(T^2)$ cells $\Rightarrow$ polynomial size/construction time.

Variables include witness **and** tableau bits. The reduction need not find the witness.

$$
\mathrm{SAT}\le_p\mathrm{3SAT}\le_p\mathrm{INDSET}\le_p\mathrm{VC}.
$$

All targets are in NP, so all are NP-complete.

## SAT → 3SAT

Fresh $z$:

$$
\ell_1\lor\ell_2\lor\ell_3\lor\ell_4
\quad\rightsquigarrow\quad
(\ell_1\lor\ell_2\lor z)\land(\neg z\lor\ell_3\lor\ell_4).
$$

For each original assignment: old clause true ⇔ some $z$ satisfies both new clauses.

- First pair true: choose $z=0$.
- Second pair true: choose $z=1$.
- All false: require $z$ and $\neg z$.

Repeat with fresh variables. Width $r\ge4$: $r-3$ new variables, $r-2$ clauses. Short clauses unchanged; empty clause → fixed contradiction. Total size linear in literal occurrences.

Equisatisfiable, not equivalent for every fixed auxiliary assignment. Fixed $k\ge3$: $k$-SAT NP-complete; 2SAT in P.

## 3SAT → Independent Set

For $m$ clauses:

1. Vertex per literal occurrence.
2. Clique within each clause.
3. Edge between complementary literals across clauses.
4. Threshold $k=m$.

Assignment → choose one true literal per clause. Choices are nonadjacent.

Independent set of size $m$ → one vertex per clause; no complementary choices. Set chosen literals true; satisfy all clauses.

At most $3m$ vertices, $O(m^2)$ edges. Empty clause → fixed no instance. Certificate: check size and nonadjacency.

## Independent Set → Vertex Cover

Cover: every edge has an endpoint in the set.

$$
S\text{ independent}\iff V\setminus S\text{ covers every edge}.
$$

For $v=|V|$:

$$
(G,k)\mapsto(G,v-k),\qquad
\alpha(G)+\tau(G)=v.
$$

$\alpha$: maximum independent-set size. $\tau$: minimum cover size. If $k>v$, output a fixed no instance. Verify a cover by checking all edges.

## 3SAT → Subset Sum

Input: indexed nonnegative integers $a_1,\ldots,a_r$, binary encoded; target $t$. Ask whether some selected indices sum to $t$. Equal numbers remain separate choices.

For $n$ variables, $m$ clauses, use $n+m$ decimal columns:

| Number | Variable columns | Clause column $j$ |
| --- | --- | --- |
| $a_i^T$ | $1$ at $i$, else $0$ | $1$ if $x_i$ occurs in $C_j$ |
| $a_i^F$ | $1$ at $i$, else $0$ | $1$ if $\neg x_i$ occurs in $C_j$ |
| Two fillers for $C_j$ | All $0$ | Each has $1$ at $j$, else $0$ |
| Target | All $1$ | All $3$ |

Unspecified digits are $0$. No carries: variable sums $\le2$; clause sums $\le5$.

- Variable target $1$ forces exactly one of $a_i^T,a_i^F$.
- Satisfied clause contributes $1$–$3$; fillers raise it to $3$.
- Unsatisfied clause contributes $0$; two fillers cannot reach $3$.

Thus satisfiability ⇔ subset sum. $2n+2m$ numbers, $O(n+m)$ bits each; polynomial construction. In NP: check selected sum. Hence NP-complete.

## coNP-completeness

In coNP + every coNP language reduces to it.

- **UNSAT:** for $A\in\mathrm{coNP}$, reduce $\overline A$ to SAT. The same map reduces $A$ to UNSAT.
- **TAUTOLOGY:** general Boolean formulas; $\varphi\in\mathrm{UNSAT}\iff\neg\varphi$ tautological.
- CNF tautology is in P: every clause must contain a complementary pair.

$$
\mathrm{NP}\ne\mathrm{coNP}\implies\mathrm P\ne\mathrm{NP}.
$$

## Nullstellensatz

Over an algebraically closed field:

$$
f_1,\ldots,f_m\text{ have no common zero}
\iff\exists g_1,\ldots,g_m:\ \sum_i g_if_i=1.
$$

A common zero would give $0=1$. Boolean constraints: $z_j^2-z_j=0$. Certificate polynomials may be huge; existence alone gives no NP certificate.

## Circuit satisfiability

Circuit definitions: [Circuits and advice](12-circuits-and-advice.md).

$$
\mathrm{CKT\text{-}SAT}=\{C:\exists x,\ C(x)=1\}.
$$

NP-complete:

- In NP: guess input and evaluate the circuit.
- NP-hard: a CNF is a circuit after replacing large AND/OR gates with binary trees.
