import sys

def load(path):
    with open(path) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith('#')]

def verify(inp, out):
    lines = load(inp)
    n = int(lines[0]) if lines else 0
    if n == 0: return (True, "VALID STABLE") if not load(out) else (False, "INVALID: non-empty matching for n=0")

    hp = [list(map(int, lines[i].split())) for i in range(1, n+1)]
    sp = [list(map(int, lines[n+i].split())) for i in range(1, n+1)]

    # Validate the preferences
    for i, p in enumerate(hp + sp):
        if sorted(p) != list(range(1, n+1)):
            t = "Hospital" if i < n else "Student"
            return False, f"INVALID: {t} {(i % n) + 1} prefs not a permutation"

    # Parse each matching list
    M = [tuple(map(int, l.split()[:2])) for l in load(out)]
    H, S = zip(*M) if M else ([], [])

    # Check validity of matching
    if len(M) != n or set(H) != set(range(1,n+1)) or set(S) != set(range(1,n+1)):
        return False, f"INVALID: matching not a valid bijection"

    # Create a student ranking table
    sr = [{h: r for r, h in enumerate(sp[s])} for s in range(n)]

    # 0 indexed lookup
    h2s = {h-1: s-1 for h, s in M}
    s2h = {s-1: h-1 for h, s in M}

    # Check for stability
    for h in range(n):
        for s in hp[h]:
            s -= 1
            if s == h2s[h]: break  
            if sr[s][h] < sr[s][s2h[s]]: 
                return False, f"UNSTABLE: blocking pair H{h+1}-S{s+1}"

    return True, "VALID STABLE"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Use the command as follows: python verifier.py <input> <matching>", file=sys.stderr); sys.exit(1)
        
    try:
        ok, msg = verify(sys.argv[1], sys.argv[2])
        print(msg); sys.exit(0 if ok else 1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)