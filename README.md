# Highest Value Longest Common Subsequence (HVLCS)
**COP 4533 – Algorithm Abstraction and Design | Assignment 3 | Spring 2026**

---

## Student Information
| Name | UFID |
|------|------|
| Aicha Keita | 66149226 |

---

## Repository Structure
```
hvlcs/
├── src/
│   ├── hvlcs.py           #main hvlcs algorithm
│   ── generate_tests.py  #genGenerates 10 nontrivial test inputs
│   └── benchmark.py     #times each test and produces runtime_plot.png
├── data/
│   ├── example.in      #worked example from the assignment
│   └── test01.in … test10.in1 #10 nontrivial inputs (|A|,|B| ≥ 25)
├── runtime_plot.png     #graph frqm Question 1
└── README.md
```

---

## Dependencies
- Python 3.8+
- `matplotlib` (for the benchmark graph only)

Install matplotlib if needed:
```bash
pip install matplotlib
```

---

## How to Run

### Run on the example file
```bash
python src/hvlcs.py data/example.in
```
Expected output:
```
9
cb
```

### Run on any input file
```bash
python src/hvlcs.py data/test05.in
```

### Run from stdin
```bash
python src/hvlcs.py < data/example.in
```

### Generate the 10 test inputs
```bash
python src/generate_tests.py
```

### Run the benchmark and generate the runtime graph
```bash
python src/benchmark.py
```
This produces `runtime_plot.png`.

---

## Input Format
```
K
x1 v1
x2 v2
...
xK vK
A
B
```
- `K` – alphabet size  
- Each of the next `K` lines: a character and its nonnegative integer value  
- `A` – first string  
- `B` – second string  

## Output Format
```
<max value>
<one optimal common subsequence>
```

---

## Assumptions
- All character values are nonnegative integers (as stated in the problem).
- Characters not listed in the alphabet that appear in A or B are assigned value 0.
- If the maximum value is 0, the empty subsequence is printed (empty line).
- Strings consist only of characters from the given alphabet.

---

## Written Component

### Question 1 – Empirical Comparison

Ten nontrivial test files were generated (all with `|A|, |B| ≥ 25`).  
The runtimes below were measured on a single machine:

| File    | \|A\| | \|B\| | \|A\|×\|B\| | Time (ms) |
|---------|-------|-------|------------|-----------|
| test01  | 25    | 25    | 625        | 0.153     |
| test02  | 30    | 30    | 900        | 0.201     |
| test03  | 40    | 35    | 1 400      | 0.305     |
| test04  | 50    | 50    | 2 500      | 0.468     |
| test05  | 60    | 55    | 3 300      | 0.602     |
| test06  | 75    | 80    | 6 000      | 1.129     |
| test07  | 100   | 90    | 9 000      | 1.860     |
| test08  | 120   | 110   | 13 200     | 2.540     |
| test09  | 150   | 140   | 21 000     | 3.812     |
| test10  | 200   | 200   | 40 000     | 7.613     |

The runtime grows linearly with `|A| × |B|`, confirming the O(mn) theoretical bound.  
See `runtime_plot.png` for the graphs (bar chart + scatter plot).

---

### Question 2 – Recurrence Equation

Let `m = |A|`, `n = |B|`, and `v(c)` be the value of character `c`.

Define:

> **`dp[i][j]`** = the maximum value achievable by any common subsequence of `A[1..i]` and `B[1..j]`.

**Base cases:**

```
dp[0][j] = 0    for all j = 0, 1, ..., n
dp[i][0] = 0    for all i = 0, 1, ..., m
```

An empty prefix of either string has no characters to match, so the only common subsequence is the empty sequence with value 0.

**Recurrence (for i ≥ 1, j ≥ 1):**

```
         ⎧ max( dp[i-1][j-1] + v(A[i]), dp[i-1][j], dp[i][j-1] )   if A[i] = B[j]
dp[i][j] = ⎨
         ⎩ max( dp[i-1][j], dp[i][j-1] )                             if A[i] ≠ B[j]
```

**Why this is correct:**

- If `A[i] ≠ B[j]`, neither character can be the last element of an optimal common subsequence that uses both positions, so we take the best of ignoring `A[i]` (`dp[i-1][j]`) or ignoring `B[j]` (`dp[i][j-1]`).

- If `A[i] = B[j]`, we have three choices:
  1. **Include** this character as the last element of the subsequence. Its value is `v(A[i])` plus the best we can do on `A[1..i-1]` and `B[1..j-1]`, which is `dp[i-1][j-1]`.
  2. **Skip** `A[i]`: best on `A[1..i-1]` and `B[1..j]` → `dp[i-1][j]`.
  3. **Skip** `B[j]`: best on `A[1..i]` and `B[1..j-1]` → `dp[i][j-1]`.

  Because all values `v(c) ≥ 0`, option 1 is always at least as large as `dp[i-1][j-1]`, but options 2 and 3 could be larger (using a different alignment). Taking the maximum over all three options guarantees optimality.

The answer is `dp[m][n]`.

---

### Question 3 – Big-Oh and Pseudocode

**Pseudocode:**

```
HVLCS(A, B, v):
    m ← |A|,  n ← |B|
    // Allocate (m+1) × (n+1) table, initialised to 0
    dp[0..m][0..n] ← 0

    for i from 1 to m:
        for j from 1 to n:
            if A[i] = B[j]:
                dp[i][j] ← max(dp[i-1][j-1] + v(A[i]),
                               dp[i-1][j],
                               dp[i][j-1])
            else:
                dp[i][j] ← max(dp[i-1][j], dp[i][j-1])

    // Traceback to reconstruct the subsequence
    seq ← empty list
    i ← m,  j ← n
    while i > 0 and j > 0:
        if A[i] = B[j] and dp[i][j] = dp[i-1][j-1] + v(A[i])
                       and dp[i][j] ≥ dp[i-1][j]
                       and dp[i][j] ≥ dp[i][j-1]:
            prepend A[i] to seq
            i ← i - 1,  j ← j - 1
        else if dp[i-1][j] ≥ dp[i][j-1]:
            i ← i - 1
        else:
            j ← j - 1

    return dp[m][n], seq
```

**Runtime Analysis:**

| Phase | Work |
|-------|------|
| Table initialisation | O(mn) |
| Double loop (fill dp) | O(mn) – constant work per cell |
| Traceback | O(m + n) – at most m+n steps |
| **Total** | **O(mn)** |

**Space:** O(mn) for the table (can be reduced to O(min(m,n)) if only the value is needed, but reconstruction requires the full table or a path record).
