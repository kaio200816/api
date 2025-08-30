export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Use POST" });

  try {
    const body = req.body;
    const webhook = process.env.DISCORD_WEBHOOK;
    if (!webhook) throw new Error("Webhook do Discord não configurado");

    const discordResponse = await fetch(webhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!discordResponse.ok) {
      const errorText = await discordResponse.text();
      return res.status(discordResponse.status).json({ error: errorText });
    }

    res.status(200).json({ sucesso: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
