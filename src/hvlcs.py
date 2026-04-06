import sys


def parse_input(file_path=None):
    #parse input
    if file_path:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    else:
        lines = [line.strip() for line in sys.stdin if line.strip()]

    idx = 0
    K = int(lines[idx]); idx += 1

    values = {}
    for _ in range(K):
        parts = lines[idx].split(); idx += 1
        char, val = parts[0], int(parts[1])
        values[char] = val

    A = lines[idx]; idx += 1
    B = lines[idx]; idx += 1

    return values, A, B


def hvlcs(A, B, values):
    """
    compute the highest value common subsequence of A and B.

    recurrence:
      Let dp[i][j] = max value of a common subsequence of A[0..i-1] and B[0..j-1].

      base cases:
        dp[0][j] = 0  for all j  (empty prefix of A -> no common subsequence)
        dp[i][0] = 0  for all i  (empty prefix of B -> no common subsequence)

      recurrence (for i >= 1, j >= 1):
        If A[i-1] == B[j-1]:
          dp[i][j] = dp[i-1][j-1] + v(A[i-1])
            - we can always extend a common subsequence by the matching character;
               since v >= 0, this is always as good as not taking it at all.
            - we also compare with dp[i-1][j] and dp[i][j-1] in case
               skipping this match (and using a different alignment) is better.
          dp[i][j] = max(dp[i-1][j-1] + v(A[i-1]), dp[i-1][j], dp[i][j-1])
        Else:
          dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    runtime: O(m * n) where m = |A|, n = |B|.
    """
    m, n = len(A), len(B)

    #build dp table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i - 1] == B[j - 1]:
                char_val = values.get(A[i - 1], 0)
                take = dp[i - 1][j - 1] + char_val
                dp[i][j] = max(take, dp[i - 1][j], dp[i][j - 1])
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    #reconstruct the optimal subsequence
    seq = []
    i, j = m, n
    while i > 0 and j > 0:
        if A[i - 1] == B[j - 1]:
            char_val = values.get(A[i - 1], 0)
            take = dp[i - 1][j - 1] + char_val
            if dp[i][j] == take and dp[i][j] >= dp[i - 1][j] and dp[i][j] >= dp[i][j - 1]:
                seq.append(A[i - 1])
                i -= 1
                j -= 1
            elif dp[i][j] == dp[i - 1][j]:
                i -= 1
            else:
                j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    seq.reverse()
    return dp[m][n], ''.join(seq)


def main():
    if len(sys.argv) > 1:
        values, A, B = parse_input(sys.argv[1])
    else:
        values, A, B = parse_input()

    max_val, subseq = hvlcs(A, B, values)
    print(max_val)
    print(subseq)


if __name__ == '__main__':
    main()
