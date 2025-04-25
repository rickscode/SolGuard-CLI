import { Connection, GetProgramAccountsFilter } from "@solana/web3.js";
import { TOKEN_PROGRAM_ID } from "@solana/spl-token";

// Solana RPC Endpoint (Replace with your own endpoint or a public one)
const rpcEndpoint = 'https://api.mainnet-beta.solana.com';
const solanaConnection = new Connection(rpcEndpoint);

// The wallet address to query
const walletToQuery = process.argv[2];  // Get wallet address from command-line argument

async function getTokenAccounts(wallet: string, solanaConnection: Connection) {
    const filters: GetProgramAccountsFilter[] = [
        {
            dataSize: 165,  // size of token accounts
        },
        {
            memcmp: {
                offset: 32,  // search for the wallet address at offset 32
                bytes: wallet,  // wallet address to search for
            },
        }
    ];

    try {
        const accounts = await solanaConnection.getParsedProgramAccounts(
            TOKEN_PROGRAM_ID,  // The Solana SPL Token Program
            { filters: filters }
        );

        const tokens = accounts.map(account => {
            const parsedAccountInfo: any = account.account.data;
            const mintAddress: string = parsedAccountInfo["parsed"]["info"]["mint"];
            const tokenBalance: number = parsedAccountInfo["parsed"]["info"]["tokenAmount"]["uiAmount"];
            return {
                tokenAddress: account.pubkey.toString(),
                tokenSymbol: mintAddress,  // Placeholder for actual symbol
                tokenBalance: tokenBalance
            };
        });

        // Output tokens as JSON string for Python to parse
        console.log(JSON.stringify(tokens));
    } catch (e) {
        console.error("Error fetching token accounts:", e);
        process.exit(1);
    }
}

// Run the function with the provided wallet address
getTokenAccounts(walletToQuery, solanaConnection);
