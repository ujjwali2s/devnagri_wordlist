from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

def generate_mnemonic():
    # Generate a 12-word mnemonic using the BIP39 wordlist
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)  # 128 bits = 12 words

def derive_wallet_address(mnemonic):
    # Generate the seed from the mnemonic
    seed = Bip39SeedGenerator(mnemonic).Generate()
    
    # Use BIP44 to derive the Bitcoin address (mainnet)
    bip44_ctx = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    wallet = bip44_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    
    return wallet.PublicKey().ToAddress()  # Returns the address

def main():
    # Generate mnemonic and wallet address
    mnemonic = generate_mnemonic()
    address = derive_wallet_address(mnemonic)
    
    # Print results
    print("--- Wallet Details ---")
    print(f"Mnemonic: {mnemonic}")
    print(f"Derived Wallet Address: {address}")

if __name__ == "__main__":
    main()
