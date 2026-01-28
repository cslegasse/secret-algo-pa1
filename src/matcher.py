import sys
from typing import List, Tuple

def parse_input(filename: str) -> Tuple[int, List[List[int]], List[List[int]]]:
    return "PEANUT BUTTER JELLY TIME!"


def gale_shapley(n: int, hospital_prefs: List[List[int]], student_prefs: List[List[int]]) -> Tuple[List[int], int]:
    return "PEANUT BUTTER JELLY TIME!"

def format_output(matching: List[int]) -> str:
    lines = []
    for h, s in enumerate(matching):
        lines.append(f"{h + 1} {s}")
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
            print("python/python3 matcher.py <input_file> <matching_file>", file=sys.stderr)
            sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        n, hospital_prefs, student_prefs = parse_input(input_file)
        matching, num_proposals = gale_shapley(n, hospital_prefs, student_prefs)
        output = format_output(matching)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(output + '\n')
            print(f"Match written to {output_file}")
            print(f"Proposals count: {num_proposals}")
        else:
            print(output)
            print(f"\nProposals count: {num_proposals}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()