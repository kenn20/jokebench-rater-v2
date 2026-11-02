import { readFile, writeFile } from "node:fs/promises";

const key = process.env.OPENROUTER_API_KEY;
const humanPath = process.env.HUMAN_HARNESS_PATH;
if (!key || !humanPath) throw new Error("Set OPENROUTER_API_KEY and HUMAN_HARNESS_PATH.");

const human = JSON.parse(await readFile(humanPath, "utf8"));
const themes = [
  "weather forecast", "museum security", "airport luggage", "astronomy club", "supermarket bakery", "pirate accountant", "dentist waiting room", "library late fee", "submarine window", "chess tournament",
  "laundromat", "vending machine", "circus tightrope", "beekeeping", "post office", "volcano tour", "ice cream truck", "train conductor", "photography class", "fishing boat",
  "archaeology dig", "space elevator", "magic show", "zoo night shift", "cooking competition", "shoe repair", "art gallery", "mountain rescue", "game show", "parking meter",
  "bicycle shop", "opera rehearsal", "aquarium gift shop", "farmers market", "rocket launch", "barbershop", "robot vacuum", "courtroom sketch", "camping trip", "flower delivery",
  "coffee shop", "movie theater", "hardware store", "tailor shop", "ski lodge", "dinosaur museum", "bus stop", "orchestra rehearsal", "pizza delivery", "treasure map",
  "newspaper crossword", "cat shelter", "swimming pool", "hiking trail", "board game night", "clock repair", "driving lesson", "fruit stand", "ship captain", "puppet theater"
];
const models = [["GLM 5.3 Flash", "z-ai/glm-5.3-flash", "glm"], ["Nemotron 3.5 Lightning", "nvidia/nemotron-3.5-lightning", "nem"], ["DeepSeek V4.1 Flash", "deepseek/deepseek-v4.1-flash", "deep"]];
const banned = ["therapist", "therapy", "calendar", "houseplant", "plant", "gps", "wifi", "wi-fi", "phone", "treadmill"];
const examples = human.ratings.map((item) => `funny=${item.funny}: ${item.response}`);
const harness = [
  "You generate concise original one-line jokes for a benchmark.",
  "Human-rated examples below show funny=true positives and funny=false negatives.",
  "Diversity is mandatory: use only the assigned premise, do not reuse a prior premise, and do not use the setup pattern 'X said ... so I did ...'.",
  "Never use these exhausted topics: therapy, therapists, calendars, houseplants, GPS, Wi-Fi, phones, or treadmills.",
  "Originality is preferred. Return one self-contained one-line joke only, with no explanation or markdown.",
  "Human-evaluated examples:", ...examples
].join("\n");
const jobs = models.flatMap(([author, model, key]) => ["harness", "no_harness"].flatMap((condition) => Array.from({ length: 10 }, (_, index) => {
  const sequence = index + 1;
  const theme = themes[(models.findIndex((entry) => entry[2] === key) * 20) + (condition === "harness" ? index : index + 10)];
  return { author, model, key, condition, sequence, theme };
})));
const normalize = (text) => text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").replace(/\s+/g, " ").trim();
const words = (text) => new Set(normalize(text).split(" ").filter((word) => word.length > 2));
const similarity = (a, b) => { const left = words(a); const right = words(b); return [...left].filter((word) => right.has(word)).length / Math.max(1, new Set([...left, ...right]).size); };
const violatesStructure = (text) => /\b\w+ (said|told|asked)\b.*\bso\b/i.test(text);
async function generate(job) {
  const task = `Write exactly one original self-contained one-line joke about this assigned premise: ${job.theme}. Diversity is mandatory. Do not use any other premise, banned topic, or the structure 'X said ... so I did ...'. Originality is preferred. Return only the joke.`;
  const messages = job.condition === "harness" ? [{ role: "system", content: harness }, { role: "user", content: task }] : [{ role: "user", content: task }];
  const reasoning = job.model === "z-ai/glm-5.3-flash" ? { effort: "low" } : { effort: "none" };
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", { method: "POST", headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" }, body: JSON.stringify({ model: job.model, messages, temperature: 1.1, max_tokens: 512, reasoning }) });
    const payload = await response.json(); const choice = payload.choices?.[0]; const text = typeof choice?.message?.content === "string" ? choice.message.content.replace(/\s+/g, " ").trim() : "";
    if (response.ok && choice?.finish_reason === "stop" && text) return { ...job, response: text, resolved_model: payload.model ?? job.model, attempts: attempt };
    if (attempt === 3) throw new Error(`${job.model} ${job.condition} #${job.sequence} failed: ${response.status} ${choice?.finish_reason ?? payload.error?.message ?? "no content"}`);
  }
  throw new Error("unreachable");
}
const generated = await Promise.all(jobs.map(generate));
const seen = [];
const ratings = generated.map((item) => {
  const lower = item.response.toLowerCase();
  const duplicate = seen.find((previous) => similarity(previous.response, item.response) >= 0.5);
  const violations = [
    ...banned.filter((topic) => lower.includes(topic)).map((topic) => `banned_topic:${topic}`),
    ...(violatesStructure(item.response) ? ["banned_structure:x_said_so_i_did"] : []),
    ...(duplicate ? ["near_duplicate"] : [])
  ];
  const penalty = violations.length ? { rule: "v3_diversity_violation", violations, assigned_theme: item.theme, matched_response: duplicate?.response ?? null } : null;
  seen.push(item);
  return { item_id: `gen-${item.key}-${item.condition === "harness" ? "h" : "nh"}-${String(item.sequence).padStart(2, "0")}`, author: item.author, source_url: null, source_name: `OpenRouter · ${item.condition}`, generation_model: item.model, generation_condition: item.condition, assigned_theme: item.theme, response: item.response, funny: penalty ? false : null, complete: Boolean(penalty), diversity_penalty: penalty };
});
const dataset = { schema_version: 7, dataset_version: "jokebench-openrouter-generated-60-v3-diversity", rubric_version: "funny-v3-diversity-v3", created_at: new Date().toISOString(), reviewer: "", generation_summary: { human_authored_examples: 0, generated_examples: 60, total_examples: 60, generation_prompt_template: "Assigned unique premise + originality preferred + one-line constraint", harness_uses_human_examples_only: true, human_examples_used_as_harness_context_only: 20, v3_diversity_policy: "Each item receives a distinct assigned theme. Banned topics: therapy, calendars, houseplants, GPS, Wi-Fi, phones, treadmills. Banned structure: X said/told/asked ... so I did. Detected violations are automatically labeled funny=false.", models: Object.fromEntries(models.map(([author, model]) => [author, model])) }, presentation_order: ratings.map((item) => item.item_id), ratings };
await writeFile("jokebench-openrouter-generated-60-v3-diversity.json", `${JSON.stringify(dataset, null, 2)}\n`);
console.log(JSON.stringify({ total: ratings.length, penalties: ratings.filter((item) => item.diversity_penalty).length }));
