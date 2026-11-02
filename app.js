const DATASET_PATH = "jokebench-openrouter-generated-60-v3-diversity.json";
const STORAGE_KEY = "jokebench-rater-feedback-generated-60-v3-diversity";

const state = { dataset: null, ratings: JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}") };
const elements = {
  datasetLabel: document.querySelector("#datasetLabel"), progressText: document.querySelector("#progressText"), progressFill: document.querySelector("#progressFill"), remainingText: document.querySelector("#remainingText"), itemType: document.querySelector("#itemType"), sourceInfo: document.querySelector("#sourceInfo"), itemNumber: document.querySelector("#itemNumber"), jokeText: document.querySelector("#jokeText"), funny: document.querySelector("#funnyButton"), notFunny: document.querySelector("#notFunnyButton"), exportJson: document.querySelector("#exportJson"), exportCsv: document.querySelector("#exportCsv"), reset: document.querySelector("#resetRatings"), complete: document.querySelector("#completeCard"), announcer: document.querySelector("#announcer")
};

const currentItem = () => state.dataset.presentation_order.map((id) => state.dataset.ratings.find((item) => item.item_id === id)).find((item) => !state.ratings[item.item_id]);
const completed = () => Object.keys(state.ratings).length;
const save = () => localStorage.setItem(STORAGE_KEY, JSON.stringify(state.ratings));
const announce = (message) => { elements.announcer.textContent = message; };

function render() {
  const total = state.dataset.ratings.length;
  const rated = completed();
  const item = currentItem();
  elements.datasetLabel.textContent = state.dataset.dataset_version;
  elements.progressText.textContent = `${rated} of ${total} rated`;
  elements.progressFill.style.width = `${(rated / total) * 100}%`;
  elements.remainingText.textContent = rated === total ? "Collection complete" : `${total - rated} decisions remaining`;
  elements.exportJson.disabled = rated === 0;
  elements.exportCsv.disabled = rated === 0;
  elements.complete.hidden = rated !== total;
  if (!item) {
    elements.jokeText.textContent = "You’ve rated every joke.";
    elements.itemType.textContent = "Complete";
    elements.sourceInfo.textContent = "Export your feedback when ready";
    elements.itemNumber.textContent = `${total} / ${total}`;
    elements.funny.disabled = true;
    elements.notFunny.disabled = true;
    return;
  }
  const index = state.dataset.presentation_order.indexOf(item.item_id) + 1;
  elements.itemType.textContent = item.generation_condition ? `${item.generation_condition.replace("_", " ")} · ${item.author}` : "Human reference";
  elements.sourceInfo.textContent = item.source_name;
  elements.itemNumber.textContent = `${index} / ${total}`;
  elements.jokeText.textContent = item.response;
  elements.funny.disabled = false;
  elements.notFunny.disabled = false;
}

function rate(funny) {
  const item = currentItem();
  if (!item) return;
  state.ratings[item.item_id] = { funny, rated_at: new Date().toISOString() };
  save();
  announce(`${funny ? "Funny" : "Not funny"} recorded. Moving to the next joke.`);
  window.setTimeout(render, window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 220);
}

function exportData(format) {
  const exportObject = { ...state.dataset, reviewer: "", exported_at: new Date().toISOString(), ratings: state.dataset.ratings.map((item) => ({ ...item, ...(state.ratings[item.item_id] || {}) })) };
  let content;
  let type;
  let extension;
  if (format === "json") {
    content = JSON.stringify(exportObject, null, 2);
    type = "application/json";
    extension = "json";
  } else {
    const fields = ["item_id", "author", "source_name", "generation_model", "generation_condition", "response", "funny", "rated_at"];
    const quote = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
    content = [fields.join(","), ...exportObject.ratings.map((item) => fields.map((field) => quote(item[field])).join(","))].join("\n");
    type = "text/csv";
    extension = "csv";
  }
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = Object.assign(document.createElement("a"), { href: url, download: `jokebench-feedback-${new Date().toISOString().slice(0, 10)}.${extension}` });
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  announce(`${format.toUpperCase()} export downloaded.`);
}

async function initialize() {
  const response = await fetch(DATASET_PATH);
  if (!response.ok) throw new Error("Dataset could not be loaded.");
  state.dataset = await response.json();
  render();
}

elements.funny.addEventListener("click", () => rate(true));
elements.notFunny.addEventListener("click", () => rate(false));
elements.exportJson.addEventListener("click", () => exportData("json"));
elements.exportCsv.addEventListener("click", () => exportData("csv"));
elements.reset.addEventListener("click", () => { if (window.confirm("Reset all ratings saved in this browser?")) { state.ratings = {}; save(); announce("Local ratings reset."); render(); } });
window.addEventListener("keydown", (event) => { if (event.key.toLowerCase() === "f") rate(true); if (event.key.toLowerCase() === "n") rate(false); });
initialize().catch((error) => { elements.jokeText.textContent = error.message; announce(error.message); });
