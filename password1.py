import secrets
import string
import math
import re


def generate_password(length=16, use_upper=True, use_lower=True,
                      use_digits=True, use_symbols=True):
    """Generate a cryptographically secure random password."""

    character_sets = []

    if use_upper:
        character_sets.append(string.ascii_uppercase)
    if use_lower:
        character_sets.append(string.ascii_lowercase)
    if use_digits:
        character_sets.append(string.digits)
    if use_symbols:
        character_sets.append("!@#$%^&*()-_=+[]{};:,.?/")

    if not character_sets:
        raise ValueError("At least one character type must be selected.")

    if length < len(character_sets):
        raise ValueError(
            f"Password length must be at least {len(character_sets)}."
        )

    # Ensure the password contains at least one character from each selected set
    password_characters = [
        secrets.choice(characters) for characters in character_sets
    ]

    all_characters = "".join(character_sets)

    # Fill the remaining length with random characters
    password_characters += [
        secrets.choice(all_characters)
        for _ in range(length - len(password_characters))
    ]

    # Securely shuffle the password characters
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)


def check_strength(password):
    """Evaluate password strength and return feedback."""

    score = 0
    feedback = []

    length = len(password)

    if length >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")

    if length >= 12:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[^\w\s]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # Check for common weak patterns
    common_passwords = {
        "password", "123456", "12345678", "qwerty",
        "admin", "letmein", "welcome"
    }

    if password.lower() in common_passwords:
        return "Very weak", ["Avoid common passwords."]

    if re.search(r"(.)\1{2,}", password):
        feedback.append("Avoid repeating the same character multiple times.")

    if re.search(r"(123|abc|qwerty)", password.lower()):
        feedback.append("Avoid predictable sequences.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score == 5:
        strength = "Strong"
    else:
        strength = "Very strong"

    return strength, feedback


def main():
    print("Password Generator and Strength Checker")
    print("---------------------------------------")

    try:
        length = int(input("Enter password length [16]: ") or 16)

        password = generate_password(length)
        print(f"\nGenerated password: {password}")

        strength, feedback = check_strength(password)
        print(f"Strength: {strength}")

        if feedback:
            print("Suggestions:")
            for suggestion in feedback:
                print(f"- {suggestion}")

        print("\nYou can also check your own password.")
        user_password = input("Enter a password to check, or press Enter to exit: ")

        if user_password:
            strength, feedback = check_strength(user_password)
            print(f"\nStrength: {strength}")

            if feedback:
                print("Suggestions:")
                for suggestion in feedback:
                    print(f"- {suggestion}")
            else:
                print("No obvious weaknesses detected.")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
