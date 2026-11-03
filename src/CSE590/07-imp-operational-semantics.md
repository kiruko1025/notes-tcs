---
title: "Operational Semantics of IMP"
author: ""
tags: [CSE590]
draft: false
---

# Operational Semantics of IMP

Small-step = one execution step. Big-step = complete evaluation. Both give the same terminating results.

Proof methods: [induction and inference rules](06-induction-and-proof-rules.md). Mathematical meanings: [denotational semantics](08-imp-denotational-semantics.md).

## Syntax and states

### Syntax

Integer literals $n\in\mathbb Z$; variable names $x\in\mathrm{Var}$.

$$
\begin{aligned}
\mathrm{AExp}:\quad a&::=n\mid x\mid a_1+a_2\mid a_1-a_2\mid a_1*a_2,\\
\mathrm{BExp}:\quad b&::=\mathsf{true}\mid\mathsf{false}
 \mid a_1=a_2\mid a_1\le a_2\\
 &\quad\mid\neg b\mid b_1\land b_2\mid b_1\lor b_2,\\
\mathrm{Com}:\quad c&::=\mathsf{skip}\mid x:=a\mid c_1;c_2\\
 &\quad\mid\mathsf{if}\ b\ \mathsf{then}\ c_1\ \mathsf{else}\ c_2\\
 &\quad\mid\mathsf{while}\ b\ \mathsf{do}\ c.
\end{aligned}
$$

- $=$ tests equality; $:=$ assigns.
- Assignments are commands, not expressions: `x := (y := 1)` invalid.
- Terminal forms have **no small steps**, including no self-step.

### States and configurations

**State:** total map $\sigma\in\Sigma=(\mathrm{Var}\to\mathbb Z)$.

- Every variable has a supplied value; no automatic zero initialization.
- Mathematical integers: no overflow.
- Expressions read state; only commands modify it.

**Update:** change one variable, preserve all others.

$$
\sigma[x\mapsto n](y)=
\begin{cases}
n & y=x,\\
\sigma(y) & y\ne x.
\end{cases}
$$

**Configuration:** $\langle\text{remaining phrase},\text{current state}\rangle$.

## Small-step semantics

### Arithmetic steps

Variable lookup:

$$
\frac{}{\langle x,\sigma\rangle\to_a\sigma(x)}.
$$

For $\odot\in\{+,-,*\}$: **left operand → right operand → compute**.

$$
\frac{\langle a_1,\sigma\rangle\to_a a_1'}
{\langle a_1\odot a_2,\sigma\rangle\to_a a_1'\odot a_2}
\quad(\text{A-Left})
$$

$$
\frac{\langle a_2,\sigma\rangle\to_a a_2'}
{\langle n_1\odot a_2,\sigma\rangle\to_a n_1\odot a_2'}
\quad(\text{A-Right})
$$

$$
\frac{}{\langle n_1\odot n_2,\sigma\rangle\to_a n_3}
\quad(\text{A-Compute}),
\qquad n_3=n_1\odot n_2\text{ in }\mathbb Z.
$$

### Boolean steps

$q,q_1,q_2\in\{\mathsf{true},\mathsf{false}\}$. Here: **strict, left-to-right** $\land,\lor$.

#### Comparison steps

For $\bowtie\in\{=,\le\}$:

$$
\frac{\langle a_1,\sigma\rangle\to_a a_1'}
{\langle a_1\bowtie a_2,\sigma\rangle\to_b a_1'\bowtie a_2}
\quad(\text{Compare-Left})
$$

$$
\frac{\langle a_2,\sigma\rangle\to_a a_2'}
{\langle n_1\bowtie a_2,\sigma\rangle\to_b n_1\bowtie a_2'}
\quad(\text{Compare-Right})
$$

$$
\frac{}{\langle n_1\bowtie n_2,\sigma\rangle\to_b q}
\quad(\text{Compare}).
$$

$q$ true exactly when the integer comparison holds; false otherwise.

#### Negation and Boolean operations

$$
\frac{\langle b,\sigma\rangle\to_b b'}
{\langle\neg b,\sigma\rangle\to_b\neg b'},
\qquad
\frac{}{\langle\neg q,\sigma\rangle\to_b\operatorname{not}(q)}.
$$

Here $\operatorname{not}$ flips the Boolean value. For $\diamond\in\{\land,\lor\}$:

$$
\frac{\langle b_1,\sigma\rangle\to_b b_1'}
{\langle b_1\diamond b_2,\sigma\rangle\to_b b_1'\diamond b_2}
\quad(\text{B-Left})
$$

$$
\frac{\langle b_2,\sigma\rangle\to_b b_2'}
{\langle q_1\diamond b_2,\sigma\rangle\to_b q_1\diamond b_2'}
\quad(\text{B-Right})
$$

$$
\frac{}{\langle q_1\diamond q_2,\sigma\rangle\to_b q}
\quad(\text{B-Compute}).
$$

Compute Boolean results by the usual truth tables.

Short-circuiting is another convention: skip unused operands. Same final values here, different traces.

### Command steps

#### Assignment steps

$$
\frac{\langle a,\sigma\rangle\to_a a'}
{\langle x:=a,\sigma\rangle\to\langle x:=a',\sigma\rangle}
\quad(\text{Assign-Step})
$$

$$
\frac{}{\langle x:=n,\sigma\rangle
\to\langle\mathsf{skip},\sigma[x\mapsto n]\rangle}
\quad(\text{Assign})
$$

For `x := x + 1`: read old `x`; update only after evaluating the right-hand side.

#### Sequence steps

$$
\frac{\langle c_1,\sigma\rangle\to\langle c_1',\sigma'\rangle}
{\langle c_1;c_2,\sigma\rangle\to\langle c_1';c_2,\sigma'\rangle}
\quad(\text{Seq-Step})
$$

$$
\frac{}{\langle\mathsf{skip};c_2,\sigma\rangle\to\langle c_2,\sigma\rangle}
\quad(\text{Seq-Skip})
$$

Second command uses the state produced by the first.

#### Conditional and loop steps

Compact notation for the ordinary IMP syntax:

$$
\begin{aligned}
\mathsf{If}(b,c_1,c_2)&\equiv\mathsf{if}\ b\ \mathsf{then}\ c_1\ \mathsf{else}\ c_2,\\
\mathsf{While}(b,c)&\equiv\mathsf{while}\ b\ \mathsf{do}\ c.
\end{aligned}
$$

$$
\frac{\langle b,\sigma\rangle\to_b b'}
{\langle\mathsf{If}(b,c_1,c_2),\sigma\rangle
\to\langle\mathsf{If}(b',c_1,c_2),\sigma\rangle}
\quad(\text{If-Step})
$$

$$
\frac{}{\langle\mathsf{If}(\mathsf{true},c_1,c_2),\sigma\rangle
\to\langle c_1,\sigma\rangle}
\quad(\text{If-True})
$$

$$
\frac{}{\langle\mathsf{If}(\mathsf{false},c_1,c_2),\sigma\rangle
\to\langle c_2,\sigma\rangle}
\quad(\text{If-False})
$$

Unroll once; write $W=\mathsf{While}(b,c)$:

$$
\frac{}{\langle W,\sigma\rangle
\to\langle\mathsf{If}(b,c;W,\mathsf{skip}),\sigma\rangle}
\quad(\text{While})
$$

- Only the selected branch executes.
- Unrolling leaves state unchanged.
- $W$ keeps the **original guard expression** $b$: reevaluate it after the body changes state.

### Finite runs

For configurations $C,C',C''$:

$$
\frac{}{C\to^*C}\quad(\text{Refl}),
\qquad
\frac{C\to C'\qquad C'\to^*C''}{C\to^*C''}\quad(\text{Step}).
$$

Zero or more steps. Concatenation requires matching command and state. Termination: $\langle c,\sigma\rangle\to^*\langle\mathsf{skip},\tau\rangle$.

$C\to^*C$ alone proves no loop: zero steps allowed.

### Execution examples

#### Two assignments

Distinct $x,y$; $\sigma_1=\sigma[x\mapsto1]$, $\sigma_2=\sigma_1[y\mapsto3]$.

$$
\begin{aligned}
\langle x:=1;\ y:=x+2,\sigma\rangle
&\to\langle\mathsf{skip};\ y:=x+2,\sigma_1\rangle\\
&\to\langle y:=x+2,\sigma_1\rangle\\
&\to\langle y:=1+2,\sigma_1\rangle\\
&\to\langle y:=3,\sigma_1\rangle\\
&\to\langle\mathsf{skip},\sigma_2\rangle.
\end{aligned}
$$

#### Euclid's subtraction algorithm

```text
while not (m = n) do
    if m <= n then n := n - m
    else m := m - n
```

For **positive** inputs:

$$
(m,n):\quad(6,4)\mapsto(2,4)\mapsto(2,2).
$$

Each arrow = one loop iteration. GCD preserved; positive $m+n$ decreases. Final common value = GCD. Zero inputs may loop.

#### An infinite cycle

Let $W=\mathsf{While}(\mathsf{true},\mathsf{skip})$:

$$
\begin{aligned}
\langle W,\sigma\rangle
&\to\langle\mathsf{If}(\mathsf{true},\mathsf{skip};W,\mathsf{skip}),\sigma\rangle\\
&\to\langle\mathsf{skip};W,\sigma\rangle
\to\langle W,\sigma\rangle.
\end{aligned}
$$

Positive-length cycle: three actual steps, repeat forever. Rules deterministic; expressions always terminate, commands may diverge.

## Big-step semantics

### Result judgments

| Judgment | Result |
| --- | --- |
| $\langle a,\sigma\rangle\Downarrow_a n$ | Arithmetic expression → integer |
| $\langle b,\sigma\rangle\Downarrow_b q$ | Boolean expression → truth value |
| $\langle c,\sigma\rangle\Downarrow\tau$ | Command → final state |

Big-step = complete evaluation, also called natural semantics. Derivations are finite trees. Commands return final states; expressions preserve state.

### Expression results

#### Arithmetic results

$$
\frac{}{\langle n,\sigma\rangle\Downarrow_a n}
\quad(\text{A-Num}),
\qquad
\frac{}{\langle x,\sigma\rangle\Downarrow_a\sigma(x)}
\quad(\text{A-Var}).
$$

For $\odot\in\{+,-,*\}$:

$$
\frac{
\langle a_1,\sigma\rangle\Downarrow_a n_1
\qquad\langle a_2,\sigma\rangle\Downarrow_a n_2
}{\langle a_1\odot a_2,\sigma\rangle\Downarrow_a n_3}
\quad(\text{A-Op}),
$$

where $n_3=n_1\odot n_2$ in $\mathbb Z$.

Both premises use the same state. Example: $\sigma(x)=4$ gives $\langle x+2,\sigma\rangle\Downarrow_a6$.

#### Boolean results

$q,q_1,q_2\in\{\mathsf{true},\mathsf{false}\}$; $\bowtie\in\{=,\le\}$; $\diamond\in\{\land,\lor\}$.

$$
\frac{}{\langle q,\sigma\rangle\Downarrow_b q}
\quad(\text{B-Bool})
$$

$$
\frac{
\langle a_1,\sigma\rangle\Downarrow_a n_1
\qquad\langle a_2,\sigma\rangle\Downarrow_a n_2
}{\langle a_1\bowtie a_2,\sigma\rangle\Downarrow_b q}
\quad(\text{B-Compare})
$$

$q$ true exactly when the integer comparison holds; false otherwise.

$$
\frac{\langle b,\sigma\rangle\Downarrow_b q}
{\langle\neg b,\sigma\rangle\Downarrow_b\operatorname{not}(q)}
\quad(\text{B-Not})
$$

$$
\frac{
\langle b_1,\sigma\rangle\Downarrow_b q_1
\qquad\langle b_2,\sigma\rangle\Downarrow_b q_2
}{\langle b_1\diamond b_2,\sigma\rangle\Downarrow_b q}
\quad(\text{B-Op})
$$

Boolean operations use the usual truth tables; strict evaluation, matching the small-step rules.

All IMP expressions terminate with unique results: finite syntax, total states, total operations.

### Command results

#### Skip and assignment results

$$
\frac{}{\langle\mathsf{skip},\sigma\rangle\Downarrow\sigma}
\quad(\text{Skip})
$$

$$
\frac{\langle a,\sigma\rangle\Downarrow_a n}
{\langle x:=a,\sigma\rangle\Downarrow\sigma[x\mapsto n]}
\quad(\text{Assign})
$$

Skip: unchanged state. Assignment: evaluate right-hand side in **old** state, then update.

#### Sequence results

$$
\frac{
\langle c_1,\sigma\rangle\Downarrow\rho
\qquad\langle c_2,\rho\rangle\Downarrow\tau
}{\langle c_1;c_2,\sigma\rangle\Downarrow\tau}
\quad(\text{Seq})
$$

#### Conditional results

$$
\frac{
\langle b,\sigma\rangle\Downarrow_b\mathsf{true}
\qquad\langle c_1,\sigma\rangle\Downarrow\tau
}{\langle\mathsf{If}(b,c_1,c_2),\sigma\rangle\Downarrow\tau}
\quad(\text{If-True})
$$

$$
\frac{
\langle b,\sigma\rangle\Downarrow_b\mathsf{false}
\qquad\langle c_2,\sigma\rangle\Downarrow\tau
}{\langle\mathsf{If}(b,c_1,c_2),\sigma\rangle\Downarrow\tau}
\quad(\text{If-False})
$$

Only the selected branch needs a derivation; starts in $\sigma$.

#### While results

Let $W=\mathsf{while}\ b\ \mathsf{do}\ c$.

$$
\frac{\langle b,\sigma\rangle\Downarrow_b\mathsf{false}}
{\langle W,\sigma\rangle\Downarrow\sigma}
\quad(\text{While-False})
$$

$$
\frac{
\begin{gathered}
\langle b,\sigma\rangle\Downarrow_b\mathsf{true}
\qquad\langle c,\sigma\rangle\Downarrow\rho\\
\langle W,\rho\rangle\Downarrow\tau
\end{gathered}
}{\langle W,\sigma\rangle\Downarrow\tau}
\quad(\text{While-True})
$$

Loop premise needs a finite derivation. Repeated syntax allowed; circular proofs excluded.

### Euclid's evaluation tree

$$
B=\mathsf{If}(m\le n,\ n:=n-m,\ m:=m-n),
\qquad
W=\mathsf{while}\ \neg(m=n)\ \mathsf{do}\ B.
$$

Initial state: $\sigma_0(m)=6$, $\sigma_0(n)=4$; other variables $0$ in this example.

$$
\sigma_1=\sigma_0[m\mapsto2],
\qquad\sigma_2=\sigma_1[n\mapsto2].
$$

**First body:** variable lookup + subtraction + assignment + If-False.

$$
\frac{
\langle m\le n,\sigma_0\rangle\Downarrow_b\mathsf{false}
\qquad
\displaystyle\frac{\langle m-n,\sigma_0\rangle\Downarrow_a2}
{\langle m:=m-n,\sigma_0\rangle\Downarrow\sigma_1}
}{\langle B,\sigma_0\rangle\Downarrow\sigma_1}.
$$

Second body similarly: If-True gives $\langle B,\sigma_1\rangle\Downarrow\sigma_2$.

**Build the loop proof from its stopping case upward:**

| Judgment proved | Final rule | Required loop subtree |
| --- | --- | --- |
| $\langle W,\sigma_2\rangle\Downarrow\sigma_2$ | While-False | None |
| $\langle W,\sigma_1\rangle\Downarrow\sigma_2$ | While-True | Previous row |
| $\langle W,\sigma_0\rangle\Downarrow\sigma_2$ | While-True | Previous row |

Top-level rule instance:

$$
\frac{
\begin{gathered}
\langle\neg(m=n),\sigma_0\rangle\Downarrow_b\mathsf{true}
\qquad\langle B,\sigma_0\rangle\Downarrow\sigma_1\\
\langle W,\sigma_1\rangle\Downarrow\sigma_2
\end{gathered}
}{\langle W,\sigma_0\rangle\Downarrow\sigma_2}.
$$

Final state $\sigma_2$: $m=n=2$; other variables unchanged. Positive-input termination: [Euclid's algorithm](#euclids_subtraction_algorithm).

### Divergence and determinism

$W_\infty=\mathsf{while}\ \mathsf{true}\ \mathsf{do}\ \mathsf{skip}$ has **no finite big-step derivation**.

Proof by contradiction:

1. Choose a derivation of $\langle W_\infty,\sigma\rangle\Downarrow\tau$ with minimum height.
2. Last rule must be While-True; skip leaves state $\sigma$.
3. Recursive premise proves the same judgment with smaller height: contradiction.

Small-step shows an infinite run. IMP has no stuck nonterminal configurations; no big-step result means divergence.

**Determinism:**

$$
\langle c,\sigma\rangle\Downarrow\tau_1
\land\langle c,\sigma\rangle\Downarrow\tau_2
\Longrightarrow\tau_1=\tau_2.
$$

Rule induction on first derivation; second result arbitrary. Expression results fix branches; IHs identify intermediate/final states.

$$
\operatorname{eval}:\mathrm{Com}\times\Sigma\rightharpoonup\Sigma.
$$

**Partial function:** at most one result; loops may prevent any result. Determinism does not imply termination.

## Equivalence proof

$$
\boxed{
\langle c,\sigma\rangle\Downarrow\tau
\iff
\langle c,\sigma\rangle\to^*\langle\mathsf{skip},\tau\rangle.
}
$$

| Direction | Main tools |
| --- | --- |
| Big-step → small-step run | Rule induction, lifting, transitivity |
| Small-step run → big-step | Inversion, anti-reduction, induction on run |

Same terminating programs and final states. Only finite runs to skip appear; divergent runs have no finite big-step derivation.

### Proof tools

**Rule induction:** case per last rule; IH per premise derivation. While repeats syntax, but its proof subtree is smaller.

**Expression correspondence:** prove arithmetic first, then Booleans, then commands.

$$
\begin{aligned}
\langle a,\sigma\rangle\Downarrow_a n
&\iff\langle a,\sigma\rangle\to_a^*n,\\
\langle b,\sigma\rangle\Downarrow_b q
&\iff\langle b,\sigma\rangle\to_b^*q.
\end{aligned}
$$

Expression chains below keep $\sigma$ fixed. Command IHs do not replace these separate expression lemmas.

**Transitivity:** matching finite runs concatenate. Proof: induction on the first run.

**Lifting:** a subrun becomes a run in its evaluation position.

$$
\langle a_1,\sigma\rangle\to_a^*a_1'
\Longrightarrow
\langle a_1+a_2,\sigma\rangle\to_a^*a_1'+a_2.
$$

$$
\langle c_1,\sigma\rangle\to^*\langle c_1',\rho\rangle
\Longrightarrow
\langle c_1;c_2,\sigma\rangle\to^*\langle c_1';c_2,\rho\rangle.
$$

Also lift assignment expressions and guards. Right-operand lifting needs a numeral on the left. Proof: induction on subrun.

### Forward: big-step to small-step

Induct on the **big-step derivation**; join runs from IHs.

#### Forward arithmetic and assignment

Given operand results $n_1,n_2$:

$$
a_1+a_2\to_a^*n_1+a_2\to_a^*n_1+n_2\to_a n_3,
\qquad n_3=n_1+n_2.
$$

Literals: zero steps. Variables: one lookup. Operators: evaluate operands, then compute.

Given $\langle a,\sigma\rangle\Downarrow_a n$:

$$
\langle x:=a,\sigma\rangle
\to^*\langle x:=n,\sigma\rangle
\to\langle\mathsf{skip},\sigma[x\mapsto n]\rangle.
$$

#### Forward sequence

Premises: $\langle c_1,\sigma\rangle\Downarrow\rho$, $\langle c_2,\rho\rangle\Downarrow\tau$.

$$
\begin{aligned}
\langle c_1;c_2,\sigma\rangle
&\to^*\langle\mathsf{skip};c_2,\rho\rangle\\
&\to\langle c_2,\rho\rangle
\to^*\langle\mathsf{skip},\tau\rangle.
\end{aligned}
$$

Second command starts in updated state $\rho$.

#### Forward While-True

Let $W=\mathsf{while}\ b\ \mathsf{do}\ c$; abbreviate conditional syntax as $\mathsf{If}(b,c_1,c_2)$.

Premises: guard true in $\sigma$; body takes $\sigma$ to $\rho$; remaining loop takes $\rho$ to $\tau$.

$$
\begin{aligned}
\langle W,\sigma\rangle
&\to\langle\mathsf{If}(b,c;W,\mathsf{skip}),\sigma\rangle\\
&\to^*\langle\mathsf{If}(\mathsf{true},c;W,\mathsf{skip}),\sigma\rangle\\
&\to\langle c;W,\sigma\rangle\\
&\to^*\langle\mathsf{skip};W,\rho\rangle\\
&\to\langle W,\rho\rangle
\to^*\langle\mathsf{skip},\tau\rangle.
\end{aligned}
$$

Guard: Boolean lemma. Body and remaining loop: command IHs.

| Other case | Small-step construction |
| --- | --- |
| Skip | Zero steps |
| If | Evaluate guard; select branch; run branch |
| While-False | Unroll; evaluate guard; select skip |

### Reverse: small-step to big-step

#### Inversion

Read a derivation backward: its conclusion determines possible last rules and required premises.

| Known result | Recovered information |
| --- | --- |
| $\langle\mathsf{skip},\sigma\rangle\Downarrow\tau$ | $\tau=\sigma$ |
| $\langle x:=a,\sigma\rangle\Downarrow\tau$ | Some $n$: $\langle a,\sigma\rangle\Downarrow_a n$, $\tau=\sigma[x\mapsto n]$ |
| $\langle c_1;c_2,\sigma\rangle\Downarrow\tau$ | Some $\rho$: $\langle c_1,\sigma\rangle\Downarrow\rho$, $\langle c_2,\rho\rangle\Downarrow\tau$ |

#### Anti-reduction

Reconstruct a big-step result **before** one small step:

$$
\frac{
\langle c,\sigma\rangle\to\langle c',\sigma'\rangle
\qquad\langle c',\sigma'\rangle\Downarrow\tau
}{\langle c,\sigma\rangle\Downarrow\tau}.
$$

Induct on one-step derivation; invert result; use IH/expression lemma; rebuild. Quantify over **all final states**.

Expression version, proved first:

$$
\langle a,\sigma\rangle\to_a a'
\land\langle a',\sigma\rangle\Downarrow_a n
\Longrightarrow\langle a,\sigma\rangle\Downarrow_a n.
$$

Boolean version analogous.

**Assignment-Step case:**

1. Invert result for `x := a'`: obtain value $n$ and $\tau=\sigma[x\mapsto n]$.
2. Arithmetic anti-reduction: $a$ also evaluates to $n$.
3. Reapply Assign: `x := a` evaluates to $\tau$.

**Seq-Step:** invert the result to get intermediate $\rho$. IH restores $\langle c_1,\sigma\rangle\Downarrow\rho$; retain $\langle c_2,\rho\rangle\Downarrow\tau$; rebuild Seq. IH must apply to $\rho$, not just $\tau$.

**While-unrolling:** invert conditional. False: rebuild While-False. True: invert sequence into body/loop results; rebuild While-True.

#### Induction on the terminating run

| Run case | Big-step proof |
| --- | --- |
| Zero steps to $\langle\mathsf{skip},\tau\rangle$ | Source already skip in state $\tau$; apply Skip |
| First step, then remaining run | IH gives result after first step; anti-reduction restores result before it |

Reverse expression proofs: same pattern, ending at a numeral or Boolean value.
