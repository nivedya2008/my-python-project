#!/usr/bin/env python3
"""
Smart Contact Book
A simple, persistent, interactive command-line contact manager.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


# Store contacts in the same directory as this Python file.
DATA_FILE = Path(__file__).resolve().parent / "contacts.json"


class Colors:
    """ANSI color codes for a more pleasant terminal experience."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"

    @classmethod
    def disable(cls) -> None:
        """Disable colors when the terminal does not support ANSI codes."""
        for attribute in (
            "RESET",
            "BOLD",
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "CYAN",
            "MAGENTA",
        ):
            setattr(cls, attribute, "")


# Disable colors on terminals that are unlikely to support ANSI escape codes.
if os.name == "nt" and not os.environ.get("WT_SESSION"):
    Colors.disable()


def styled(text: str, color: str = "", bold: bool = False) -> str:
    """Return text with optional color and bold formatting."""
    prefix = f"{Colors.BOLD if bold else ''}{color}"
    return f"{prefix}{text}{Colors.RESET}"


def print_separator(character: str = "-", length: int = 72) -> None:
    """Print a visual separator line."""
    print(character * length)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print()
    print_separator("=")
    print(styled(f"  {title}", Colors.CYAN, bold=True))
    print_separator("=")


def load_contacts() -> list[dict[str, str]]:
    """Load contacts from the JSON file, creating it if necessary."""
    try:
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")
            return []

        raw_data = DATA_FILE.read_text(encoding="utf-8").strip()

        if not raw_data:
            return []

        data = json.loads(raw_data)

        if not isinstance(data, list):
            raise ValueError("The contacts file must contain a list.")

        valid_contacts: list[dict[str, str]] = []

        for contact in data:
            if isinstance(contact, dict):
                valid_contacts.append(
                    {
                        "name": str(contact.get("name", "")).strip(),
                        "phone": str(contact.get("phone", "")).strip(),
                        "email": str(contact.get("email", "")).strip(),
                    }
                )

        return valid_contacts

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(
            styled(
                f"\n⚠️  Could not load contacts.json: {error}",
                Colors.YELLOW,
            )
        )

        # Preserve the damaged file instead of overwriting it.
        try:
            backup_file = DATA_FILE.with_suffix(".json.backup")
            if DATA_FILE.exists():
                DATA_FILE.replace(backup_file)
                print(
                    styled(
                        f"📦 A backup was created at: {backup_file.name}",
                        Colors.YELLOW,
                    )
                )
            DATA_FILE.write_text("[]", encoding="utf-8")
        except OSError as backup_error:
            print(
                styled(
                    f"⚠️  Could not recreate the data file: {backup_error}",
                    Colors.RED,
                )
            )

        return []


def save_contacts(contacts: list[dict[str, str]]) -> bool:
    """Save contacts safely using a temporary file and atomic replacement."""
    temporary_path: Path | None = None

    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            prefix=".contacts_",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            json.dump(contacts, temporary_file, indent=4, ensure_ascii=False)
            temporary_file.write("\n")
            temporary_path = Path(temporary_file.name)

        temporary_path.replace(DATA_FILE)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(styled(f"\n❌ Could not save contacts: {error}", Colors.RED))
        return False

    finally:
        if temporary_path and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                pass


def get_non_empty_input(prompt: str) -> str:
    """Prompt until the user enters non-empty text."""
    while True:
        try:
            value = input(prompt).strip()

            if value:
                return value

            print(styled("⚠️  This field cannot be empty.", Colors.YELLOW))

        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n👋 Goodbye!", Colors.CYAN))
            raise SystemExit


def get_valid_phone() -> str:
    """Prompt until the user enters exactly ten numeric digits."""
    while True:
        try:
            phone = input("📞 Phone number (10 digits): ").strip()

            if re.fullmatch(r"\d{10}", phone):
                return phone

            print(
                styled(
                    "⚠️  Phone number must contain exactly 10 digits.",
                    Colors.YELLOW,
                )
            )

        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n👋 Goodbye!", Colors.CYAN))
            raise SystemExit


def get_valid_email() -> str:
    """Prompt until the user enters a basic valid email address."""
    while True:
        try:
            email = input("✉️  Email address: ").strip()

            # Basic validation: text before @, domain text, and a dot in domain.
            email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

            if re.fullmatch(email_pattern, email):
                return email

            print(
                styled(
                    "⚠️  Enter a valid email containing '@' and a dot.",
                    Colors.YELLOW,
                )
            )

        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n👋 Goodbye!", Colors.CYAN))
            raise SystemExit


def add_contact(contacts: list[dict[str, str]]) -> None:
    """Add a new contact to the contact list."""
    print_header("Add New Contact")

    name = get_non_empty_input("👤 Full name: ")
    phone = get_valid_phone()
    email = get_valid_email()

    if any(contact["phone"] == phone for contact in contacts):
        print(
            styled(
                "\n⚠️  A contact with this phone number already exists.",
                Colors.YELLOW,
            )
        )
        return

    new_contact = {
        "name": name,
        "phone": phone,
        "email": email,
    }

    contacts.append(new_contact)

    if save_contacts(contacts):
        print(styled("\n✅ Contact added successfully!", Colors.GREEN))


def view_all_contacts(contacts: list[dict[str, str]]) -> None:
    """Display every saved contact."""
    print_header("All Contacts")

    if not contacts:
        print(styled("📭 No contacts found.", Colors.YELLOW))
        return

    sorted_contacts = sorted(contacts, key=lambda contact: contact["name"].lower())

    for index, contact in enumerate(sorted_contacts, start=1):
        print(styled(f"\n{index}. {contact['name']}", Colors.GREEN, bold=True))
        print(f"   📞 {contact['phone']}")
        print(f"   ✉️  {contact['email']}")

    print()
    print_separator()
    print(styled(f"Total contacts: {len(contacts)}", Colors.CYAN))


def search_contacts(contacts: list[dict[str, str]]) -> None:
    """Search contacts by name, phone number, or email address."""
    print_header("Search Contacts")

    if not contacts:
        print(styled("📭 No contacts found.", Colors.YELLOW))
        return

    query = get_non_empty_input("🔎 Search for a name, phone, or email: ").lower()

    matches = [
        contact
        for contact in contacts
        if query in contact["name"].lower()
        or query in contact["phone"].lower()
        or query in contact["email"].lower()
    ]

    if not matches:
        print(styled("\n❌ No matching contacts found.", Colors.YELLOW))
        return

    print(styled(f"\n✅ Found {len(matches)} matching contact(s):", Colors.GREEN))

    for index, contact in enumerate(matches, start=1):
        print(styled(f"\n{index}. {contact['name']}", Colors.GREEN, bold=True))
        print(f"   📞 {contact['phone']}")
        print(f"   ✉️  {contact['email']}")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    """Delete a selected contact after confirmation."""
    print_header("Delete Contact")

    if not contacts:
        print(styled("📭 No contacts found.", Colors.YELLOW))
        return

    sorted_contacts = sorted(contacts, key=lambda contact: contact["name"].lower())

    for index, contact in enumerate(sorted_contacts, start=1):
        print(f"{index}. {contact['name']} — {contact['phone']}")

    while True:
        try:
            choice = input(
                "\nEnter the contact number to delete, or 'q' to cancel: "
            ).strip().lower()

            if choice == "q":
                print(styled("↩️  Deletion cancelled.", Colors.CYAN))
                return

            selected_index = int(choice)

            if 1 <= selected_index <= len(sorted_contacts):
                selected_contact = sorted_contacts[selected_index - 1]
                break

            print(
                styled(
                    f"⚠️  Enter a number from 1 to {len(sorted_contacts)}.",
                    Colors.YELLOW,
                )
            )

        except ValueError:
            print(styled("⚠️  Please enter a valid number.", Colors.YELLOW))
        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n👋 Goodbye!", Colors.CYAN))
            raise SystemExit

    print(
        f"\nYou selected: {styled(selected_contact['name'], Colors.GREEN, bold=True)}"
    )

    while True:
        try:
            confirmation = input("Delete this contact? (y/n): ").strip().lower()

            if confirmation in {"y", "yes"}:
                contacts.remove(selected_contact)

                if save_contacts(contacts):
                    print(styled("✅ Contact deleted successfully!", Colors.GREEN))
                return

            if confirmation in {"n", "no"}:
                print(styled("↩️  Deletion cancelled.", Colors.CYAN))
                return

            print(styled("⚠️  Please enter 'y' or 'n'.", Colors.YELLOW))

        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n👋 Goodbye!", Colors.CYAN))
            raise SystemExit


def display_menu() -> None:
    """Display the main application menu."""
    print()
    print_separator("=")
    print(styled("📒 SMART CONTACT BOOK", Colors.CYAN, bold=True))
    print_separator("=")
    print("1. ➕ Add Contact")
    print("2. 📋 View All Contacts")
    print("3. 🔎 Search Contact")
    print("4. 🗑️  Delete Contact")
    print("5. 🚪 Exit")
    print_separator("-")


def main() -> None:
    """Run the contact book application."""
    contacts = load_contacts()

    print(styled("\n✨ Welcome to Smart Contact Book! ✨", Colors.MAGENTA, bold=True))
    print(styled(f"📁 Data file: {DATA_FILE}", Colors.CYAN))

    while True:
        display_menu()

        try:
            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                add_contact(contacts)
            elif choice == "2":
                view_all_contacts(contacts)
            elif choice == "3":
                search_contacts(contacts)
            elif choice == "4":
                delete_contact(contacts)
            elif choice == "5":
                print(styled("\n💾 Saving contacts...", Colors.CYAN))
                if save_contacts(contacts):
                    print(styled("✅ All contacts saved successfully.", Colors.GREEN))
                print(styled("👋 Thank you for using Smart Contact Book!", Colors.MAGENTA))
                break
            else:
                print(styled("⚠️  Invalid option. Please choose 1-5.", Colors.YELLOW))

        except (EOFError, KeyboardInterrupt):
            print(styled("\n\n💾 Saving contacts before exit...", Colors.CYAN))
            save_contacts(contacts)
            print(styled("👋 Goodbye!", Colors.MAGENTA))
            break
        except Exception as error:
            # Final safety net to prevent unexpected crashes.
            print(
                styled(
                    f"\n❌ An unexpected error occurred: {error}",
                    Colors.RED,
                )
            )


if __name__ == "__main__":
    main()
