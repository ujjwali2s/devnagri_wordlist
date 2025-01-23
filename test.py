import os
import random
from hashlib import sha256
from bip_utils import Bip44, Bip44Coins, Bip44Changes

# Load your Devanagari wordlist
WORDLIST_FILE = "devnagri_script.txt"

def load_wordlist(file_path):
    """Load the custom Devanagari wordlist."""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def generate_valid_mnemonic(wordlist):
    """Generate a valid BIP-39 mnemonic using a custom wordlist."""
    # Generate 128 bits of entropy (16 bytes)
    entropy = os.urandom(16)
    
    # Convert entropy to binary string
    entropy_bits = "".join(f"{byte:08b}" for byte in entropy)

    # Calculate the checksum (first few bits of the hash)
    checksum_bits = sha256(entropy).hexdigest()
    checksum_bits = bin(int(checksum_bits, 16))[2:].zfill(256)
    checksum = checksum_bits[: len(entropy) * 8 // 32]

    # Combine entropy and checksum
    combined_bits = entropy_bits + checksum

    # Split into 11-bit chunks and map to the wordlist
    mnemonic_words = [
        wordlist[int(combined_bits[i:i+11], 2)] for i in range(0, len(combined_bits), 11)
    ]
    return " ".join(mnemonic_words)

def generate_btc_address(mnemonic, wordlist):
    """Generate a Bitcoin address from a mnemonic."""
    # Convert mnemonic to seed manually (simplified for BIP-39)
    seed = sha256(mnemonic.encode("utf-8")).digest()

    # Create a BIP44 Bitcoin context
    bip44_ctx = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)

    # Derive the first Bitcoin address
    bip44_acc = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    btc_address = bip44_acc.PublicKey().ToAddress()
    return btc_address

if __name__ == "__main__":
    # Load the Devanagari wordlist
    wordlist = load_wordlist(WORDLIST_FILE)

    # Generate a valid mnemonic
    mnemonic = generate_valid_mnemonic(wordlist)

    # Generate a Bitcoin address
    btc_address = generate_btc_address(mnemonic, wordlist)

    # Output the results
    print("\nGenerated Mnemonic (Devanagari):")
    print(mnemonic)

    print("\nGenerated Bitcoin Address:")
    print(btc_address)
