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
  if (!bucketFilter) {
    const R = 620;
    D.buckets.forEach((b, i) => {
      const a = (2 * Math.PI * i) / D.buckets.length - Math.PI / 2;
      nodes.push({
        id: "B:" + b.name, label: `${b.name}\n${b.size} claims · ${b.clusters} clusters`,
        value: Math.sqrt(b.size) * 3, color: bucketColor(b.name),
        shape: "box", font: { size: 15, color: "#fff" }, physics: false,
        x: Math.round(R * Math.cos(a)), y: Math.round(R * Math.sin(a)),
      });
    });
  }
  for (const c of D.clusters) {
    if (bucketFilter && c.bucket !== bucketFilter) continue;
    nodes.push({
      id: "C:" + c.id,
      label: c.size >= 8 ? `${c.id}\n${c.size}` : "",
      value: 2 + Math.sqrt(c.size) * 1.6, color: bucketColor(c.bucket),
      title: `${c.id} — ${c.size} claims, ${c.core} core\nkeywords: ${c.keywords.slice(0, 6).join(", ")}\n(click to open)`,
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

function fitSoon() {
  setTimeout(() => { try { graph.fit({ animation: { duration: 400, easingFunction: "easeOutQuad" } }); } catch {} }, 350);
  // freeze the layout once it has spread — physics otherwise keeps pushing
  // nodes outward and every fit zooms further out (blank-looking canvas)
  setTimeout(() => {
    try { graph.setOptions({ physics: { enabled: false } }); graph.fit({ animation: { duration: 500 } }); } catch {}
  }, 2600);
}

function render() {
  const { nodes, edges } = selectedCluster ? claimData(selectedCluster) : overviewData();
  graph.setData({ nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) });
  $("#modeBtn").textContent = selectedCluster
    ? `◀ back to browse (${selectedCluster})` : "view: graph";
  renderLegend();
  fitSoon();
}
graph.on("stabilizationIterationsDone", () => { try { graph.fit({ animation: false }); } catch {} });

graph.on("click", p => {
  if (!p.nodes.length) return;
  const id = p.nodes[0];
  if (id.startsWith("C:")) { selectedCluster = id.slice(2); render(); showCluster(selectedCluster); }
  else if (id.startsWith("S:")) showClaim(id.slice(2));
  else if (id.startsWith("B:")) { bucketFilter = id.slice(2); render(); showBucketInSide(id.slice(2)); }
});
$("#modeBtn").onclick = () => {
  selectedCluster = null; bucketFilter = null; render(); browseSide();
};

/* ---------- side panel ---------- */
function browseSide() {
  const rows = D.buckets.map(b => {
    const cls = D.clusters.filter(c => c.bucket === b.name).sort((a, z) => z.size - a.size);
    const items = cls.map(c =>
      `<div class="crow" onclick="openCluster('${c.id}')"><span>${esc(c.id)}</span><span>${c.size} claims${c.core ? ` · ${c.core} core` : ""}</span></div>`).join("");
    return `<details open>
      <summary><span class="sw" style="background:${bucketColor(b.name)}"></span>${esc(b.name)} — ${b.size} claims, ${b.clusters} clusters</summary>
      ${items}</details>`;
  }).join("");
  $("#side").innerHTML = `<h2>Browse the corpus</h2>
    <p class="meta">${D.claims.length} source claims · 65 documents · ${D.clusters.length} clusters · ${D.buckets.length} buckets.
    Pick a cluster below, click a node in the graph, or search.
    <span class="pri-core">core</span> = transmutation / catalysis / EVO / electrical path (Tiziano priority).
    Clusters are PROPOSALS pending Dan's campaign split.</p>
    <h3>By bucket</h3>
    ${rows}`;
}
function showBucketInSide(name) {
  const cls = D.clusters.filter(c => c.bucket === name).sort((a, z) => z.size - a.size);
  $("#side").innerHTML = `<h2>${esc(name)}</h2>
    <p class="meta">${cls.length} clusters — click to open (also in the graph).</p>
    ${cls.map(c => `<div class="brow" onclick="openCluster('${c.id}')"><span class="cid">${esc(c.id)}</span><span class="meta">${c.size} claims · ${c.core} core</span></div>`).join("")}`;
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
    ${kv("geometry", c.geometry)}${kv("procedure", c.steps)}${kv("measurements", c.meas)}${kv("schematics", c.schematics)}
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

/* ---------- dragbar: resize the results panel ---------- */
const dragbar = $("#dragbar"), side = $("#side");
const savedW = parseInt(localStorage.getItem("sideWidth") || "480", 10);
if (savedW >= 320) side.style.width = savedW + "px";
let dragging = false;
dragbar.addEventListener("pointerdown", e => {
  dragging = true; dragbar.classList.add("active");
  dragbar.setPointerCapture(e.pointerId);
  document.body.style.cursor = "col-resize";
});
dragbar.addEventListener("pointermove", e => {
  if (!dragging) return;
  const w = Math.min(Math.max(window.innerWidth - e.clientX, 320), Math.floor(window.innerWidth * 0.85));
  side.style.width = w + "px";
});
dragbar.addEventListener("pointerup", e => {
  dragging = false; dragbar.classList.remove("active");
  document.body.style.cursor = "";
  localStorage.setItem("sideWidth", String(parseInt(side.style.width, 10) || 480));
  try { graph.redraw(); } catch {}
});

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
    bucketFilter ? showBucketInSide(b.name) : browseSide();
  };
  chips.appendChild(el);
}
function renderLegend() {
  $("#legend").innerHTML = selectedCluster
    ? `<span><span class="sw" style="background:#ffb84d"></span>core claim ★</span>
       <span><span class="sw" style="background:#6b7684"></span>normal claim</span>
       <span>edges: extracted relations + same-document shared tags (≥3)</span>`
    : `<span>node size ∝ claims · hover a dot for keywords · click to open · or use the Browse panel</span>`;
}

/* ---------- search box ---------- */
let searchTimer;
$("#search").addEventListener("input", e => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    const q = e.target.value.trim();
    if (q.length < 2) return;
    const hits = mini.search(q).slice(0, 25);
    $("#side").innerHTML = `<h2>Search — ${hits.length} hits</h2>
      <p class="meta">top 25 · drag the blue handle to widen this panel</p>` +
      (hits.map(h => claimCard(byId[h.id])).join("") || `<p class="meta">no matches</p>`);
    bindCards();
  }, 180);
});

browseSide();
render();

/* ---------- WebMCP: register explorer tools for MCP-capable clients ---------- */
if (typeof WebMCP !== "undefined") {
  const mcp = new WebMCP({ color: "#4da3ff", position: "bottom-right", size: "36px" });
  const out = fn => async a => ({ content: [{ type: "text", text: JSON.stringify(fn(a ?? {}), null, 1) }] });
  const brief = c => ({ id: c.id, statement: c.statement.slice(0, 220), doc: c.doc,
    page: c.page, priority: c.priority, bucket: c.bucket, cluster: c.cluster, pdf: c.pdf });

  mcp.registerTool("search_claims",
    "Full-text search over the 1,641 Sapogin 'Canonical Physics' corpus claims (English statements, Russian quotes, tags, SC-* ids). Optional filters: bucket, priority (core/normal), facet (theory/phenomenology/experiment/measurement/recipe/material/process/procedure/schematic/geometry).",
    { q: { type: "string", description: "search terms" },
      bucket: { type: "string", description: "optional bucket filter" },
      priority: { type: "string", description: "optional priority filter (core|normal)" },
      facet: { type: "string", description: "optional facet filter" },
      limit: { type: "string", description: "max results (default 15, max 50)" } },
    out(a => {
      let hits = a.q ? mini.search(a.q, { fuzzy: 0.2, prefix: true }).map(h => byId[h.id]) : D.claims.slice();
      if (a.bucket) hits = hits.filter(c => c.bucket === a.bucket);
      if (a.priority) hits = hits.filter(c => c.priority === a.priority);
      if (a.facet) hits = hits.filter(c => c.facet === a.facet);
      return { total: hits.length, results: hits.slice(0, parseInt(a.limit || "15", 10)).map(brief) };
    }));

  mcp.registerTool("get_claim",
    "Get the full record of one source claim by SC-* id: English statement, verbatim Russian quote, quantities, materials, geometry, procedure steps, measurements, schematic refs, and source-PDF path+page.",
    { id: { type: "string", description: "claim id, e.g. SC-AR04-005" } },
    out(a => byId[String(a.id).toUpperCase()] || { error: `unknown id ${a.id}` }));

  mcp.registerTool("list_clusters",
    "List the 145 proposal clusters, optionally filtered by bucket, with sizes and top keywords.",
    { bucket: { type: "string", description: "optional bucket filter" } },
    out(a => D.clusters.filter(c => !a.bucket || c.bucket === a.bucket)
      .map(c => ({ cluster: c.id, bucket: c.bucket, size: c.size, core: c.core, keywords: c.keywords.slice(0, 5) }))));

  mcp.registerTool("get_cluster",
    "Get one cluster's meta and member claim ids.",
    { id: { type: "string", description: "cluster id, e.g. evo-charge-clusters-04" } },
    out(a => {
      const c = D.clusters.find(x => x.id === a.id);
      return c ? { ...c, members: D.claims.filter(x => x.cluster === a.id).map(brief) }
               : { error: `unknown cluster ${a.id}` };
    }));

  mcp.registerTool("get_synthesis",
    "Get the practical-first synthesis markdown for a bucket (the art before the theory).",
    { bucket: { type: "string", description: "bucket name, e.g. catalysis" } },
    out(a => D.synthesis[a.bucket] !== undefined
      ? { bucket: a.bucket, markdown: D.synthesis[a.bucket] }
      : { error: "no synthesis", available: Object.keys(D.synthesis) }));

  mcp.registerTool("corpus_stats",
    "Corpus overview: claim/cluster/bucket counts, core counts, available syntheses.",
    {}, out(() => ({
      claims: D.claims.length, clusters: D.clusters.length, buckets: D.buckets,
      core: D.claims.filter(c => c.priority === "core").length,
      syntheses: Object.keys(D.synthesis),
      endpoints: ["http://127.0.0.1:8420/api/search?q=", "/api/claim/<id>", "/api/clusters",
        "/api/cluster/<id>", "/api/buckets", "/api/synthesis/<bucket>", "/api/random?n=", "/api/stats"],
    })));
}
