import { readFile, writeFile } from "node:fs/promises";

const humanPath = process.env.HUMAN_HARNESS_PATH;
const outputPath = "jokebench-openrouter-80-v2.json";
const key = process.env.OPENROUTER_API_KEY;

if (!key) throw new Error("OPENROUTER_API_KEY is required.");
if (!humanPath) throw new Error("HUMAN_HARNESS_PATH must point to the 20-item human-rating JSON used as harness context.");

const human = JSON.parse(await readFile(humanPath, "utf8"));
const prompt = "Make exactly one original, self-contained, one-line joke. Originality is preferred: do not use a familiar stock joke, a common setup, or a joke from the examples. Return only the joke.";
const harness = [
  "You generate original standalone one-line jokes for a benchmark.",
  "The human-rated examples below show funny=true positives and funny=false negatives.",
  "Originality is preferred. Do not copy, quote, lightly rephrase, or reuse a setup or punchline from any example.",
  "Return exactly one original, self-contained, one-line joke and nothing else.",
  "Human-evaluated examples:",
  ...human.ratings.map((item) => `funny=${item.funny}: ${item.response}`),
].join("\n");
const models = [
  ["GLM 5.3 Flash", "z-ai/glm-5.3-flash"],
  ["Nemotron 3.5 Lightning", "nvidia/nemotron-3.5-lightning"],
  ["DeepSeek V4.1 Flash", "deepseek/deepseek-v4.1-flash"],
];
const jobs = models.flatMap(([author, model]) => ["harness", "no_harness"].flatMap((condition) =>
  Array.from({ length: 10 }, (_, index) => ({ author, model, condition, sequence: index + 1 }))));
const normalize = (text) => text.toLowerCase().replace(/[^a-z0-9\s]/g, " ").replace(/\s+/g, " ").trim();
const words = (text) => new Set(normalize(text).split(" ").filter((word) => word.length > 2));
const similarity = (a, b) => {
  const left = words(a);
  const right = words(b);
  const overlap = [...left].filter((word) => right.has(word)).length;
  return overlap / Math.max(1, new Set([...left, ...right]).size);
};
const sharesPhrase = (a, b) => {
  const phrases = (text) => normalize(text).split(" ").filter(Boolean).flatMap((_, index, items) => index + 8 <= items.length ? [items.slice(index, index + 8).join(" ")] : []);
  const right = new Set(phrases(b));
  return phrases(a).some((phrase) => right.has(phrase));
};
async function generate(job) {
  const messages = job.condition === "harness"
    ? [{ role: "system", content: harness }, { role: "user", content: prompt }]
    : [{ role: "user", content: prompt }];
  const reasoning = job.model === "z-ai/glm-5.3-flash" ? { effort: "low" } : { effort: "none" };
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: job.model, messages, temperature: 1.05, max_tokens: 512, reasoning }),
    });
    const payload = await response.json();
    const choice = payload.choices?.[0];
    const responseText = typeof choice?.message?.content === "string" ? choice.message.content.replace(/\s+/g, " ").trim() : "";
    if (response.ok && choice?.finish_reason === "stop" && responseText) return { ...job, responseText, resolvedModel: payload.model ?? job.model, attempts: attempt };
    if (attempt === 3) throw new Error(`${job.model} ${job.condition} #${job.sequence}: ${response.status} ${choice?.finish_reason ?? payload.error?.message ?? "no content"}`);
  }
  throw new Error("unreachable");
}
const generated = await Promise.all(jobs.map(generate));
const priorTexts = human.ratings.map((item) => item.response);
const seen = [...priorTexts];
const ratings = generated.map((item) => {
  const match = seen.find((previous) => normalize(previous) === normalize(item.responseText) || similarity(previous, item.responseText) >= 0.5 || sharesPhrase(previous, item.responseText));
  const penalty = match ? { rule: "duplicate_or_near_duplicate", matched_response: match, threshold: 0.5 } : null;
  seen.push(item.responseText);
  return {
    item_id: `gen-${item.model.includes("glm") ? "glm" : item.model.includes("nemotron") ? "nem" : "deep"}-${item.condition === "harness" ? "h" : "nh"}-${String(item.sequence).padStart(2, "0")}`,
    author: item.author,
    source_url: null,
    source_name: `OpenRouter · ${item.condition}`,
    generation_model: item.model,
    generation_condition: item.condition,
    response: item.responseText,
    funny: penalty ? false : null,
    complete: Boolean(penalty),
    originality_penalty: penalty,
  };
});
const all = [...human.ratings.map((item) => ({ ...item })), ...ratings];
const output = {
  schema_version: 6,
  dataset_version: "jokebench-openrouter-80-v2",
  rubric_version: "funny-v3-originality-v2",
  created_at: new Date().toISOString(),
  reviewer: "",
  generation_summary: {
    human_authored_examples: 20,
    generated_examples: 60,
    total_examples: 80,
    generation_prompt: prompt,
    harness_uses_human_examples_only: true,
    duplicate_penalty: "Exact or near-duplicate generated responses are automatically labeled funny=false and complete=true. Near duplicate rules: Jaccard word similarity >= 0.50 or a shared eight-word phrase.",
    models: Object.fromEntries(models.map(([author, model]) => [author, model])),
  },
  presentation_order: all.map((item) => item.item_id),
  ratings: all,
};
await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(JSON.stringify({ outputPath, total: all.length, penalties: ratings.filter((item) => item.originality_penalty).length }));
