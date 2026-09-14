import random
import string

# -----------------------------------------
# 🔗 Link Shortener + 📱 QR Code Generator
# -----------------------------------------

def make_short_link():
    """Create a fun simulated short link."""
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"short.ly/{code}"


def make_ascii_qr(link):
    """Create a simple simulated ASCII QR code."""
    random.seed(link)

    size = 21
    qr = []

    # Create random QR-like pattern
    for _ in range(size):
        row = ""
        for _ in range(size):
            row += "██" if random.choice([True, False]) else "  "
        qr.append(row)

    # Add simple QR-style corner markers
    def add_marker(grid, start_row, start_col):
        pattern = [
            "1111111",
            "1000001",
            "1011101",
            "1011101",
            "1011101",
            "1000001",
            "1111111"
        ]

        for r in range(7):
            for c in range(7):
                if start_row + r < len(grid) and start_col + c < len(grid[0]):
                    grid[start_row + r][start_col + c] = pattern[r][c]

    # Convert rows into editable character grids
    grid = []
    for row in qr:
        grid.append(list(row))

    add_marker(grid, 0, 0)
    add_marker(grid, 0, size - 7)
    add_marker(grid, size - 7, 0)

    print("\n📱 YOUR FUN ASCII QR CODE")
    print("┌" + "─" * (size * 2) + "┐")

    for row in grid:
        print("│", end="")
        for char in row:
            if char == "1":
                print("██", end="")
            else:
                print(char * 1, end="")
        print("│")

    print("└" + "─" * (size * 2) + "┘")
    print("\n💡 This is a fun simulated QR-style design for your short link!")


def main():
    print("=" * 50)
    print("       🔗 LINK SHORTENER + 📱 QR GENERATOR")
    print("=" * 50)

    name = input("\n👋 Hey there! What's your name? ").strip()

    if not name:
        name = "Friend"

    print(f"\nWelcome, {name}! 🎉")
    print("Paste a long website URL and I'll make it shorter!")
    print("Type 'exit' anytime to quit.\n")

    while True:
        url = input("🌐 Enter a long website URL: ").strip()

        if url.lower() == "exit":
            print(f"\n👋 See you later, {name}! Stay awesome! 🚀")
            break

        if not url:
            print("⚠️ Please enter a URL.\n")
            continue

        if not (url.startswith("http://") or url.startswith("https://")):
            print("⚠️ Please enter a URL starting with http:// or https://\n")
            continue

        # Generate simulated short link
        short_link = make_short_link()

        print("\n✨ Shortening your link...")
        print("🔗 Original :", url)
        print("🚀 Short Link:", short_link)

        # Generate ASCII QR
        make_ascii_qr(short_link)

        print("\n🎊 Done! Your link is ready to share!")
        print("💻 Tip: This program creates simulated short links.")
        print("🔄 Enter another URL, or type 'exit' to quit.\n")


if __name__ == "__main__":
    main()
