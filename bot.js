require('dotenv').config();
const axios = require('axios');
const cheerio = require('cheerio');
const { Telegraf } = require('telegraf');

const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);
let lastSentLinks = new Set();

async function checkFreeMints() {
  try {
    const { data } = await axios.get('https://nfts2.me/');
    const $ = cheerio.load(data);

    $('div.card-drop').each(async (_, element) => {
      const price = $(element).find('.text-price').text().trim();
      const title = $(element).find('.title-drop').text().trim();
      const chain = $(element).find('.chain').text().trim();
      const href = $(element).find('a').attr('href');
      const link = "https://nfts2.me" + href;

      if (
        (price.toLowerCase().includes("free") || price.includes("0 ETH")) &&
        chain.toLowerCase().includes("ape")
      ) {
        if (!lastSentLinks.has(link)) {
          lastSentLinks.add(link);
          const message = `*FREE MINT on ApeChain!*

${title}
Chain: ${chain}
Price: ${price}

[View Drop](${link})`;
          await bot.telegram.sendMessage(process.env.TELEGRAM_CHAT_ID, message, { parse_mode: 'Markdown' });
        }
      }
    });
  } catch (err) {
    console.error("Error:", err.message);
  }
}

bot.launch();
console.log("Bot is running...");
setInterval(checkFreeMints, 60000); // setiap 60 detik