/* Responsive explorer view state. Kept separate from graph/search domain logic. */
(function () {
  "use strict";

  const media = window.matchMedia("(max-width: 720px)");
  const body = document.body;
  const graph = document.querySelector("#graph");
  const side = document.querySelector("#side");
  const contextButton = document.querySelector("#modeBtn");
  const viewButton = document.querySelector("#mobileViewBtn");

  if (!graph || !side || !contextButton || !viewButton) return;

  let view = "results";

  function updateContextAction() {
    const hasContext = contextButton.textContent.includes("back to browse");
    body.dataset.contextAction = String(hasContext);
  }

  function setView(nextView, focusResults) {
    view = nextView === "graph" ? "graph" : "results";
    const graphVisible = media.matches && view === "graph";

    body.classList.toggle("mobile-graph", graphVisible);
    viewButton.textContent = graphVisible ? "View results" : "View graph";
    viewButton.setAttribute("aria-pressed", String(graphVisible));
    viewButton.setAttribute("aria-label", graphVisible ? "Show corpus results" : "Show corpus graph");

    if (graphVisible) {
      requestAnimationFrame(() => {
        window.dispatchEvent(new Event("resize"));
        window.dispatchEvent(new CustomEvent("sapogin:graph-visible"));
      });
    } else if (focusResults && media.matches) {
      side.focus({ preventScroll: true });
    }
  }

  viewButton.addEventListener("click", () => {
    setView(view === "graph" ? "results" : "graph", true);
  });

  new MutationObserver(() => {
    if (media.matches && view === "graph") setView("results", false);
  }).observe(side, { childList: true });

  new MutationObserver(updateContextAction).observe(contextButton, { childList: true });

  media.addEventListener("change", () => setView(view, false));
  updateContextAction();
  setView("results", false);
})();
