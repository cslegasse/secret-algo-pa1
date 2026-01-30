import sys

def load(path):
    with open(path) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith('#')]

def match(inp):
    lines = load(inp) # Load input file
    n = int(lines[0]) if lines else 0
    if n == 0: return [], 0

    hp = [list(map(int, lines[i].split())) for i in range(1, n+1)] # hospital prefs
    sp = [list(map(int, lines[n+i].split())) for i in range(1, n+1)] # student prefs

    for i, p in enumerate(hp + sp):
        if sorted(p) != list(range(1, n+1)):
            t = "Hospital" if i < n else "Student"
            raise ValueError(f"{t} {(i % n) + 1} prefs not a permutation")

    sr = [{h: r for r, h in enumerate(p)} for p in sp] # student rankings

    free = list(range(n))  # free hospitals at 0 index
    ptr = [0] * n          # Pointer to next s to propose to h
    s2h = [-1] * n         # A student is matched or return -1 if free
    props = 0

    while free:
        h = free.pop()
        s = hp[h][ptr[h]] - 1  # denotes a 0-indexed student
        ptr[h] += 1
        props += 1

        if s2h[s] == -1:  # The student is free
            s2h[s] = h
        elif sr[s][h+1] < sr[s][s2h[s]+1]:  # A student prefers h
            free.append(s2h[s])
            s2h[s] = h
        else:  # A student rejects h
            free.append(h)

    return [(s2h[s]+1, s+1) for s in range(n)], props

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use as follows: python matcher.py <input> <output>", file=sys.stderr); sys.exit(1)

    try:
        M, props = match(sys.argv[1])
        out = '\n'.join(f"{h} {s}" for h, s in M)

        if len(sys.argv) > 2:
            with open(sys.argv[2], 'w') as f: f.write(out + '\n')
            print(f"Output is at {sys.argv[2]}, with # proposals: {props}")
        else:
            print(out)
            print(f"\n # proposals: {props}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)