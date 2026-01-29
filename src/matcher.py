import sys
from typing import List, Tuple

def parse_input(filename: str) -> Tuple[int, List[List[int]], List[List[int]]]:
    filepath = "../tests/input/" + filename
    try:
        with open(filepath, 'r') as file:
            content = file.read().split("\n")

        if content == "":
            raise Exception("No content in input.")
            sys.exit(1)

        n = int(content[0])
        hospital_section = content[1:n+1]
        student_section = content[n+1:]

        if n != len(hospital_section) or n != len(student_section):
            raise Exception("Invalid number of students or hospitals.")
            sys.exit(1)

        # change to 2D array of ints
        hospital_prefs = []
        student_prefs = []

        for i in range(n):
            if n != len(hospital_section[i].split()) or n != len(student_section[i].split()):
                raise Exception("Invalid input in preferences.")
                sys.exit(1)
                
            hospital_prefs.append(list(map(int, hospital_section[i].split())))
            student_prefs.append(list(map(int, student_section[i].split())))
        
        print(f"n: {n}, hospital_prefs: {hospital_prefs}, student_prefs: {student_prefs}")

        return n, hospital_prefs, student_prefs
    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def gale_shapley(n: int, hospital_prefs: List[List[int]], student_prefs: List[List[int]]) -> Tuple[List[int], int]:
     # Initialize each person and hospital to be free
    h_isMatched = [False] * n
    s_matches = [-1] * n
    unmatched_count = n
    num_proposals = 0
    # while some hospital is free and hasn't been matched to every applicant
    while unmatched_count > 0:
        # choose such a hospital h
        h_index = next(i for i in range(n) if not h_isMatched[i]) # index = 0, 1, 2
        h_val = h_index + 1 # val = hospital #1, 2, 3
        for i in range(n):
            if h_isMatched[h_index]:
                break
            # a = 1st applicant on h's list to whom h has not been matched
            a_val = hospital_prefs[h_index][i]
            a_index = a_val - 1
            
            # h' is the hospital currently assigned to a
            h_prime_val = s_matches[a_index]
            h_prime_index = h_prime_val - 1

            # if a is free
            if h_prime_val == -1:
                # assign h and a
                h_isMatched[h_index] = True
                s_matches[a_index] = h_val
                unmatched_count -= 1
            # else if a prefers h to their current assignment h'
            elif h_prime_val > 0 and student_prefs[a_index].index(h_prime_val) > student_prefs[a_index].index(h_val):
                # assign a and h, and h' is free
                h_isMatched[h_index] = True
                s_matches[a_index] = h_val
                h_isMatched[h_prime_index] = False
            # else
            else:
                # a rejects h
                pass
            num_proposals += 1
    matching = []
    for i in range(n):
        matching.append([s_matches[i], i + 1]) # hospital, student
    return matching, num_proposals

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