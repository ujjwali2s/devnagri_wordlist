# Custom Devanagari Mnemonic Generator and Bitcoin Address Deriver

This repository contains a Python project that generates mnemonic phrases using a custom Devanagari wordlist and derives Bitcoin addresses from the generated mnemonics. The project leverages the BIP-39 and BIP-44 standards for mnemonic generation and address derivation.

---

## Features

- **Custom Wordlist Support**: Generates mnemonics from a user-provided Devanagari wordlist.
- **Checksum Validation**: Ensures generated mnemonics comply with BIP-39 checksum rules.
- **Bitcoin Address Derivation**: Uses BIP-44 standards to derive Bitcoin addresses from the mnemonic.

---

## Requirements

- Python 3.7+
- Dependencies:
  - `bip-utils`
  - `random`
  - `os`
  - `hashlib`

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ujjwali2s/devnagri_wordlist.git
   cd devnagri_wordlist
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Your Wordlist**:
   - Place your custom Devanagari wordlist in the root directory with the filename `out_wordlist.txt`.
   - Ensure the file contains exactly 2048 unique words, one word per line.

---

## Usage

1. **Run the Script**:
   ```bash
   python3 text.py
   ```

2. **Output**:
   - The script will generate a mnemonic phrase using the custom wordlist.
   - It will derive a Bitcoin address from the mnemonic.

3. **Example Output**:
   ```
   Generated Mnemonic (Devanagari):
   पावन ख्याति परिणाम अनुशासन दिशा साधना पर्वत नदी कला प्रेम

   Generated Bitcoin Address:
   bc1qexampleaddressxyz...
   ```

---

## File Structure

```
mnemonic-generator/
|
├── text.py               # Main Python script
├── out_wordlist.txt      # Custom Devanagari wordlist (must be provided by the user)
├── requirements.txt      # Required Python packages
└── README.md             # Project documentation
```

---

## Notes

- Ensure your wordlist file strictly adheres to BIP-39 formatting.
- For more information on BIP-39 and BIP-44, refer to:
  - [BIP-39 Specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
  - [BIP-44 Specification](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki)

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

