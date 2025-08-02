# SolGuard-CLI

SolGuard-CLI is a command-line tool that analyzes a Solana wallet and provides a risk assessment for the SPL tokens it holds. It uses the rugcheck.xyz API to generate a "rug score" for each token, helping users identify potentially risky assets.

## Features

- Fetches all SPL tokens from a given Solana wallet address.
- Provides a risk score and detailed analysis for each token.
- Displays a clear and concise risk report in the terminal.
- Easy-to-use and interactive command-line interface.

## How It Works

The tool consists of a main Python script that orchestrates the process and a Node.js script responsible for fetching token data from the Solana blockchain.

1.  The user is prompted to enter a Solana wallet address.
2.  The Python script calls the Node.js script to get a list of all SPL tokens in the wallet.
3.  For each token, the Python script queries the rugcheck.xyz API to get a detailed risk analysis.
4.  Finally, a report is generated and displayed in the terminal, showing the risk level for each token.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Node.js and npm
- Git

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/rickscode/SolGuard-CLI.git
    cd SolGuard-CLI
    ```

2.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  Install the required Node.js packages:

    ```bash
    npm install
    ```

## Usage

To run the tool, execute the following command in your terminal:

```bash
python app.py
```

You will then be prompted to enter your Solana wallet address. The tool will fetch the token data and display the risk report.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This tool uses the [rugcheck.xyz](https://rugcheck.xyz/) API for token risk analysis.
- The user interface is enhanced with the [Rich](https://github.com/Textualize/rich) library for Python.
