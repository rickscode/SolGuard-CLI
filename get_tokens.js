// get_tokens.js
import { Connection } from "@solana/web3.js";
import { TOKEN_PROGRAM_ID } from "@solana/spl-token";

const rpcEndpoint = "https://api.mainnet-beta.solana.com"; // Or your preferred RPC
const solanaConnection = new Connection(rpcEndpoint);

async function getTokenAccounts(wallet) {
  const filters = [
    {
      dataSize: 165, // size of token account data
    },
    {
      memcmp: {
        offset: 32, // offset where wallet address starts
        bytes: wallet, // wallet address (base58)
      },
    },
  ];

  const accounts = await solanaConnection.getParsedProgramAccounts(
    TOKEN_PROGRAM_ID,
    { filters }
  );

  const tokenInfo = accounts.map((account) => {
    const parsedAccountInfo = account.account.data;
    const mintAddress = parsedAccountInfo.parsed.info.mint;
    const tokenBalance = parsedAccountInfo.parsed.info.tokenAmount.uiAmount;

    return {
      tokenAddress: account.pubkey.toString(),
      mintAddress,
      tokenBalance,
    };
  });

  return tokenInfo;
}

// Read wallet from command line
const wallet = process.argv[2];
if (!wallet) {
  console.error("❌ Please provide a wallet address");
  process.exit(1);
}

getTokenAccounts(wallet)
  .then((tokens) => {
    console.log(JSON.stringify(tokens));
  })
  .catch((error) => {
    console.error("Error fetching tokens:", error.message);
    process.exit(1);
  });
