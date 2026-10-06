import re
import getpass


# Load common passwords from text file
def load_common_passwords():
    try:
        with open("common_passwords.txt", "r") as file:
            passwords = {
                line.strip().lower()
                for line in file
                if line.strip()
            }

        return passwords

    except FileNotFoundError:
        print("\nWarning: common_passwords.txt was not found.")
        return set()


# Check password strength
def check_password(password, common_passwords):

    score = 0
    suggestions = []

    # Check common password
    if password.lower() in common_passwords:
        return "Weak", 0, [
            "This is a common password and can be easily guessed."
        ]

    # Check password length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append(
            "Use at least 8 characters; 12 or more is better."
        )

    # Check uppercase letter
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append(
            "Add at least one uppercase letter (A-Z)."
        )

    # Check lowercase letter
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append(
            "Add at least one lowercase letter (a-z)."
        )

    # Check number
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append(
            "Add at least one number (0-9)."
        )

    # Check special character
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append(
            "Add at least one special character such as @, #, $, %, or !."
        )

    # Check repeated characters
    if re.search(r"(.)\1\1", password):
        score -= 1
        suggestions.append(
            "Avoid repeating the same character multiple times."
        )

    # Check predictable sequences
    common_sequences = [
        "1234",
        "abcd",
        "qwerty",
        "password"
    ]

    if any(sequence in password.lower()
           for sequence in common_sequences):

        score -= 1
        suggestions.append(
            "Avoid predictable sequences or common words."
        )

    # Prevent negative score
    score = max(score, 0)

    # Classify password
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    # Additional suggestion
    if strength != "Strong":
        suggestions.append(
            "Use a longer password with a mix of letters, "
            "numbers, and special characters."
        )

    return strength, score, suggestions


# Display password analysis
def display_result(password, common_passwords):

    strength, score, suggestions = check_password(
        password,
        common_passwords
    )

    print("\n" + "=" * 50)
    print("        PASSWORD STRENGTH ANALYSIS")
    print("=" * 50)

    print(f"\nPassword Length : {len(password)}")
    print(f"Security Score  : {score}/6")
    print(f"Strength        : {strength}")

    print("\nCriteria:")

    # Uppercase
    if re.search(r"[A-Z]", password):
        print("✓ Uppercase letter")
    else:
        print("✗ Uppercase letter")

    # Lowercase
    if re.search(r"[a-z]", password):
        print("✓ Lowercase letter")
    else:
        print("✗ Lowercase letter")

    # Number
    if re.search(r"[0-9]", password):
        print("✓ Number")
    else:
        print("✗ Number")

    # Special character
    if re.search(r"[^A-Za-z0-9]", password):
        print("✓ Special character")
    else:
        print("✗ Special character")

    # Length
    if len(password) >= 12:
        print("✓ Good password length")
    elif len(password) >= 8:
        print("✓ Acceptable password length")
    else:
        print("✗ Password is too short")

    # Suggestions
    if suggestions:

        print("\nSuggestions:")

        for suggestion in suggestions:
            print(f"- {suggestion}")

    else:
        print("\n✓ No major improvements needed.")

    print("\n" + "=" * 50)


# Main program
def main():

    print("=" * 50)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 50)

    # Load common password dictionary
    common_passwords = load_common_passwords()

    print("\nEnter a password to check its strength.")
    print("Your password will not be displayed while typing.")

    password = getpass.getpass("\nEnter password: ")

    # Check empty password
    if not password:
        print("\nError: Password cannot be empty.")
        return

    # Analyze password
    display_result(password, common_passwords)


# Start the program
if __name__ == "__main__":
    main()