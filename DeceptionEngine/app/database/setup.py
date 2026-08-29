from .db import initialize_database
from .seed import seed_database


def setup():
    print("[+] Initializing deception database...")

    initialize_database()

    print("[+] Creating synthetic company data...")

    seed_database()

    print("[+] Database setup complete.")


if __name__ == "__main__":
    setup()