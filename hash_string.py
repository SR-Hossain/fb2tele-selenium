def compute_hashes(s):
    p1, m1 = 31, 10**9 + 7
    p2, m2 = 37, 10**9 + 9
    hash1, hash2 = 0, 0
    pow1, pow2 = 1, 1

    for ch in s:
        seed = 1 + ord(ch) - ord('a')
        hash1 = (hash1 + seed * pow1) % m1
        hash2 = (hash2 + seed * pow2) % m2
        pow1 = (pow1 * p1) % m1
        pow2 = (pow2 * p2) % m2

    return hash1, hash2

def hash(s):
    hash1, hash2 = compute_hashes(s)
    return f'{hash1}, {hash2}'
