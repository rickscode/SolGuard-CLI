import { Connection } from "@solana/web3.js";
import { TOKEN_PROGRAM_ID } from "@solana/spl-token";

const rpcEndpoint = "";
const solanaConnection = new Connection(rpcEndpoint);

async function getTokenAccounts(wallet) {
  const filters = [
    {
      dataSize: 165,
    },
    {
      memcmp: {
        offset: 32,
        bytes: wallet,
      },
    },
  ];

  const accounts = await solanaConnection.getParsedProgramAccounts(
    TOKEN_PROGRAM_ID,
    { filters }
  );

  const tokenInfo = accounts.map((account) => {
    const parsed = account.account.data.parsed;
    const info = parsed.info;

    return {
      tokenAddress: account.pubkey.toString(),
      mintAddress: info.mint,
      tokenSymbol: info.mint.slice(0, 6).toUpperCase(),
      tokenBalance: info.tokenAmount.uiAmount,
    };
  });

  return tokenInfo;
}

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
