import time, random, tempfile, os
from matcher import match
from verifier import verify
import matplotlib.pyplot as plt

def write_input(path, n, hp, sp):
    with open(path, 'w') as f:
        f.write(f"{n}\n")
        for p in hp: f.write(' '.join(map(str, p)) + '\n')
        for p in sp: f.write(' '.join(map(str, p)) + '\n')

def write_matching(path, M):
    with open(path, 'w') as f:
        for h, s in M: f.write(f"{h} {s}\n")

def gen(n):
    hp = [random.sample(range(1, n+1), n) for _ in range(n)]
    sp = [random.sample(range(1, n+1), n) for _ in range(n)]
    return hp, sp

def bench():
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    results = []

    print(f"{'n':>6} {'match_ms':>10} {'verify_ms':>10} {'props':>10}")
    print("-" * 40)

    for n in sizes:
        hp, sp = gen(n)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.in', delete=False) as f:
            inp = f.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.out', delete=False) as f:
            out = f.name

        write_input(inp, n, hp, sp)

        t0 = time.perf_counter()
        M, props = match(inp)
        t_match = (time.perf_counter() - t0) * 1000

        write_matching(out, M)

        t0 = time.perf_counter()
        _, _ = verify(inp, out)
        t_verify = (time.perf_counter() - t0) * 1000

        results.append((n, t_match, t_verify, props))
        print(f"{n:>6} {t_match:>10.3f} {t_verify:>10.3f} {props:>10}")

        os.unlink(inp); os.unlink(out)

    return results

def plot(results):
    try:
        ns = [r[0] for r in results]
        t_m = [r[1] for r in results]
        t_v = [r[2] for r in results]

        plt.figure(figsize=(10, 6))
        plt.plot(ns, t_m, 'o-', label='Matcher')
        plt.plot(ns, t_v, 's-', label='Verifier')
        plt.xlabel('n (hospitals/students)')
        plt.ylabel('Time (ms)')
        plt.title('GS Benchmark Tests')
        plt.legend()
        plt.grid(True)
        plt.savefig('../benchmark.png', dpi=150)
    except ImportError:
        print("\npip install matplotlib")

if __name__ == "__main__":
    print("Use python benchmark.py, do not use 'RUN' in IDE.\n")
    results = bench()
    plot(results)