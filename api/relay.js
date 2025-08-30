const fetch = require("node-fetch");

module.exports = async (req, res) => {
  // Configuração para CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método não permitido, use POST" });
  }

  try {
    // Corpo enviado pelo addon
    const body = req.body;

    if (!body) {
      return res.status(400).json({ error: "Corpo da requisição vazio" });
    }

    const DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1411224316816789515/OjR_249xbtPmkWkzN3Bn_OsNr-I-lNgzRFUDmhRXKX_ZICoYydVO9UM2GK4GsQXZyuqb";

    // Repassa o JSON exatamente como veio
    const discordResponse = await fetch(DISCORD_WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    // Se o Discord retornar erro
    if (!discordResponse.ok) {
      const errorText = await discordResponse.text();
      return res.status(discordResponse.status).json({
        error: "Falha ao enviar para o Discord",
        detalhes: errorText,
      });
    }

    // Sucesso
    res.status(200).json({
      sucesso: true,
      status: discordResponse.status,
    });
  } catch (error) {
    res.status(500).json({
      error: "Erro interno na API",
      detalhes: error.message,
    });
  }
};
