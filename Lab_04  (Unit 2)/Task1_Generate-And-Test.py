"""
Generate and Test — SEND + MORE = MONEY Cryptarithmetic Puzzle

Each letter (S, E, N, D, M, O, R, Y) represents a unique digit (0-9).
Constraints:
    - S and M cannot be 0 (no leading zero in a number).
    - SEND + MORE = MONEY must hold numerically.

Approach: GENERATE all possible digit assignments (permutations),
          TEST each one against the constraints until a valid one is found.
"""

from itertools import permutations


def word_to_number(word, mapping):
    """Convert a word to its numeric value using a letter-to-digit mapping."""
    return int("".join(str(mapping[letter]) for letter in word))


def is_valid_assignment(mapping):
    """Test whether a given letter-to-digit mapping solves the puzzle."""
    if mapping["S"] == 0 or mapping["M"] == 0:
        return False  # No leading zeros

    send = word_to_number("SEND", mapping)
    more = word_to_number("MORE", mapping)
    money = word_to_number("MONEY", mapping)

    return send + more == money


def generate_and_test():
    """
    GENERATE: produce every possible assignment of digits 0-9 to the
              8 distinct letters in SEND, MORE, MONEY.
    TEST:     check each candidate against the puzzle's constraints.
    """
    letters = "SENDMORY"  # 8 unique letters used across all three words
    digits = range(10)
    candidates_tested = 0

    for perm in permutations(digits, len(letters)):
        candidates_tested += 1
        mapping = dict(zip(letters, perm))

        if is_valid_assignment(mapping):
            return mapping, candidates_tested

    return None, candidates_tested


def print_solution(mapping):
    """Print the solved puzzle in a readable format."""
    send = word_to_number("SEND", mapping)
    more = word_to_number("MORE", mapping)
    money = word_to_number("MONEY", mapping)

    print("\n--- Solution Found ---\n")
    for letter in sorted(mapping):
        print(f"{letter} = {mapping[letter]}")

    print(f"\n  {send}")
    print(f"+ {more}")
    print(f"-------")
    print(f" {money}")


def main():
    """Run the Generate and Test algorithm on SEND + MORE = MONEY."""
    try:
        mapping, candidates_tested = generate_and_test()

        if mapping is None:
            print("No solution found.")
            return

        print_solution(mapping)

        print("\n--- Performance Summary ---")
        print(f"Candidates tested: {candidates_tested}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()