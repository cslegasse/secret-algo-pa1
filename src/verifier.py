import sys
from typing import List, Tuple

def verify(input_file: str, matching_file: str) -> Tuple[bool, str]:
    return "HELLO WORLD!"


def main():
    if len(sys.argv) < 3:
        print("python/python3 verifier.py <input_file> <matching_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    matching_file = sys.argv[2]

    try:
        success, message = verify(input_file, matching_file)
        print(message)
        sys.exit(0 if success else 1)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()