class hash:
    def __init__(self, s: str):
        self.p1, self.m1 = 31, 10**9 + 7
        self.p2, self.m2 = 37, 10**9 + 9
        self.hash1, self.hash2 = 0, 0
        self.compute_hashes(s)
 
    def compute_hashes(self, s: str):
        pow1, pow2 = 1, 1
        hash1, hash2 = 0, 0
        for ch in s:
            seed = 1 + ord(ch) - ord('a')
            hash1 = (hash1 + seed * pow1) % self.m1
            hash2 = (hash2 + seed * pow2) % self.m2
            pow1 = (pow1 * self.p1) % self.m1
            pow2 = (pow2 * self.p2) % self.m2
        self.hash1, self.hash2 = hash1, hash2
 
    def __eq__(self, other):
        return self.hash1 == other.hash1 and self.hash2 == other.hash2
 
    def __str__(self):
        return str(f'{self.hash1}, {self.hash2}')