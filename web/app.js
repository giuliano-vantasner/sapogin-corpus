/* sapogin-corpus explorer — cluster/claim graph. No framework, vendored libs only. */
"use strict";
const D = window.SAPOGIN;
const byId = Object.fromEntries(D.claims.map(c => [c.id, c]));
const PALETTE = {
  "transmutation-nuclear": "#e06c75", "catalysis": "#56b6c2",
  "evo-charge-clusters": "#e5a54d", "electrical-devices": "#61afef",
  "discharge-plasma": "#c678dd", "emden-gravity-cosmic": "#98c379",
  "foundations-canonical": "#d19a66", "general": "#7f8790",
};
const bucketColor = b => PALETTE[b] || "#888";

/* ---------- search ---------- */
const mini = new MiniSearch({
  fields: ["statement", "quote", "tags", "id", "title"],
  storeFields: ["id"],
  searchOptions: { fuzzy: 0.2, prefix: true, boost: { id: 4, tags: 2 } },
});
mini.addAll(D.claims);
const $ = sel => document.querySelector(sel);
const esc = s => String(s ?? "").replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));

/* ---------- graph ---------- */
const container = $("#graph");
const graph = new vis.Network(container, { nodes: [], edges: [] }, {
  layout: { improvedLayout: true },
  physics: { solver: "barnesHut", barnesHut: { gravitationalConstant: -5200, springLength: 95 } },
  interaction: { hover: true, tooltipDelay: 120 },
  nodes: { shape: "dot", font: { color: "#d7dae0", size: 13 } },
  edges: { color: { color: "#3a4048", highlight: "#4da3ff" } },
});
let mode = "clusters";          // clusters | cluster
let bucketFilter = null;        // null = all buckets
let selectedCluster = null;

function overviewData() {
  const nodes = [], edges = [];
  if (!bucketFilter)
    for (const b of D.buckets)
      nodes.push({
        id: "B:" + b.name, label: `${b.name}\n${b.size}`,
        value: Math.sqrt(b.size) * 3, color: bucketColor(b.name),
        shape: "box", font: { size: 15, color: "#fff" }, physics: false,
      });
  for (const c of D.clusters) {
    if (bucketFilter && c.bucket !== bucketFilter) continue;
    nodes.push({
      id: "C:" + c.id, label: `${c.id}\n${c.size}`,
      value: 2 + Math.sqrt(c.size) * 1.6, color: bucketColor(c.bucket),
      title: `${c.id} — ${c.size} claims, ${c.core} core\nkeywords: ${c.keywords.slice(0, 6).join(", ")}`,
    });
    if (!bucketFilter) edges.push({ from: "B:" + c.bucket, to: "C:" + c.id });
  }
  return { nodes, edges };
}

function claimData(clusterId) {
  const members = D.claims.filter(c => c.cluster === clusterId);
  const nodes = members.map(c => ({
    id: "S:" + c.id, label: c.id + (c.priority === "core" ? " ★" : ""),
    value: 2 + (c.priority === "core" ? 2 : 0) + Math.min(c.tags.length, 4) * 0.5,
    color: c.priority === "core" ? "#ffb84d" : "#6b7684",
    title: c.statement.slice(0, 220), font: { size: 11 },
  }));
  const ids = new Set(members.map(c => c.id));
  const edges = [];
  for (const e of D.edges)
    if (ids.has(e.from) && ids.has(e.to))
      edges.push({ from: "S:" + e.from, to: "S:" + e.to, label: e.kind, font: { size: 9, color: "#8a919c" } });
  for (let i = 0; i < members.length; i++)
    for (let j = i + 1; j < members.length; j++) {
      const a = members[i], b = members[j];
      const shared = a.tags.filter(t => b.tags.includes(t));
      if (shared.length >= 3 && a.doc === b.doc)
        edges.push({ from: "S:" + a.id, to: "S:" + b.id, color: { color: "#333a44" } });
    }
  return { nodes, edges };
}

function render() {
  const { nodes, edges } = selectedCluster ? claimData(selectedCluster) : overviewData();
  graph.setData({ nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) });
  $("#modeBtn").textContent = selectedCluster
    ? `view: ${selectedCluster} (back)` : "view: clusters";
  renderLegend();
}

graph.on("click", p => {
  if (!p.nodes.length) return;
  const id = p.nodes[0];
  if (id.startsWith("C:")) { selectedCluster = id.slice(2); render(); showCluster(selectedCluster); }
  else if (id.startsWith("S:")) showClaim(id.slice(2));
  else if (id.startsWith("B:")) { bucketFilter = id.slice(2); render(); }
});
$("#modeBtn").onclick = () => {
  if (selectedCluster) { selectedCluster = null; render(); defaultSide(); }
  else { bucketFilter = null; render(); }
};

/* ---------- side panel ---------- */
function defaultSide() {
  $("#side").innerHTML = `<h2>sapogin-corpus</h2>
    <p class="meta">${D.claims.length} source claims · 65 documents · ${D.clusters.length} clusters · ${D.buckets.length} buckets.
    Click a cluster node to open it; a claim node to inspect it.
    Search matches ids, English statements, tags, and Russian quotes.</p>
    <h3>Data model</h3>
    <p class="meta">SC-* = source claim (verbatim-faithful, provenance-pinned,
    data not doctrine). Clusters are PROPOSALS pending Dan's campaign split.
    <span class="pri-core">core</span> = transmutation / catalysis / EVO /
    electrical path (Tiziano priority).</p>`;
}
function pdfLink(c) {
  return c.pdf ? `<a href="${esc(c.pdf)}#page=${c.page || 1}" target="_blank" style="color:var(--accent);font-size:12px">source PDF${c.page ? " p." + c.page : ""}</a>` : "";
}
function claimCard(c, sel) {
  return `<div class="claim ${sel ? "sel" : ""}" data-id="${c.id}">
    <span class="cid">${c.id}</span> ${c.priority === "core" ? '<span class="pri-core">core</span>' : ""}
    <div>${esc(c.statement)}</div>
    ${c.quote ? `<div class="quote">${esc(c.quote.slice(0, 240))}${c.quote.length > 240 ? "…" : ""}</div>` : ""}
    <div class="meta">${c.doc} · ${c.section} · ${c.type}/${c.facet}${c.page ? " · p." + c.page : ""} · ${pdfLink(c)}</div>
  </div>`;
}
function showCluster(id) {
  const meta = D.clusters.find(c => c.id === id);
  const members = D.claims.filter(c => c.cluster === id);
  const syn = D.synthesis[meta.bucket];
  $("#side").innerHTML = `<h2>${esc(id)}</h2>
    <p class="meta">${meta.bucket} · ${meta.size} claims · ${meta.core} core</p>
    <p class="meta">keywords: ${esc(meta.keywords.join(", "))}</p>
    ${syn ? `<div class="md">${marked.parse(syn)}</div>` : `<p class="meta">no synthesis yet for ${esc(meta.bucket)}</p>`}
    <h3>Claims (${members.length})</h3>
    ${members.map(c => claimCard(c)).join("")}`;
  bindCards();
  $("#side").scrollTop = 0;
}
function showClaim(id) {
  const c = byId[id];
  if (!c) return;
  document.querySelectorAll(".claim").forEach(el => el.classList.toggle("sel", el.dataset.id === id));
  const kv = (label, arr) => arr?.length ? `<div class="kv"><b>${label}:</b> ${esc([].concat(arr).join(" · "))}</div>` : "";
  $("#side").innerHTML = `<h2>${esc(c.id)}</h2>
    <div>${esc(c.statement)}</div>
    ${c.quote ? `<div class="quote">${esc(c.quote)}</div>` : ""}
    <div class="meta">${c.doc} — ${esc(c.title)} · ${c.section}${c.page ? " · p." + c.page : ""} · ${pdfLink(c)}</div>
    <div class="kv"><b>cluster:</b> <span style="cursor:pointer;color:var(--accent)" onclick="openCluster('${c.cluster}')">${esc(c.cluster)}</span></div>
    <div class="kv"><b>type/facet:</b> ${esc(c.type)} / ${esc(c.facet)} · <b>priority:</b> ${esc(c.priority)}</div>
    ${kv("tags", c.tags)}${kv("quantities", c.quantities)}${kv("materials", c.materials)}
    <h3>Cluster context</h3>
    <p class="meta">open the full cluster via its name above or the view button.</p>`;
  $("#side").scrollTop = 0;
}
window.openCluster = id => { selectedCluster = id; render(); showCluster(id); };
function bindCards() {
  document.querySelectorAll(".claim").forEach(el =>
    el.onclick = () => { showClaim(el.dataset.id); focusClaim(el.dataset.id); });
}
function focusClaim(id) {
  try { graph.selectNodes(["S:" + id]); graph.focus("S:" + id, { scale: 1.1, animation: true }); } catch {}
}

/* ---------- chips + legend ---------- */
const chips = $("#chips");
for (const b of D.buckets) {
  const el = document.createElement("span");
  el.className = "chip"; el.textContent = b.name; el.style.borderColor = bucketColor(b.name);
  el.onclick = () => {
    bucketFilter = bucketFilter === b.name ? null : b.name;
    selectedCluster = null;
    document.querySelectorAll(".chip").forEach(x => x.classList.remove("on"));
    if (bucketFilter) el.classList.add("on");
    render();
  };
  chips.appendChild(el);
}
function renderLegend() {
  $("#legend").innerHTML = selectedCluster
    ? `<span><span class="sw" style="background:#ffb84d"></span>core claim ★</span>
       <span><span class="sw" style="background:#6b7684"></span>normal claim</span>
       <span>edges: extracted relations + same-document shared tags (≥3)</span>`
    : `<span>node size ∝ claims; click a bucket hub to filter, a cluster to open</span>`;
}

/* ---------- search box ---------- */
let searchTimer;
$("#search").addEventListener("input", e => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    const q = e.target.value.trim();
    if (q.length < 2) return;
    const hits = mini.search(q).slice(0, 25);
    $("#side").innerHTML = `<h2>Search — ${hits.length} hits</h2>` +
      (hits.map(h => claimCard(byId[h.id])).join("") || `<p class="meta">no matches</p>`);
    bindCards();
  }, 180);
});

defaultSide();
render();
