const sortBtn = 
  document.getElementById("sort-btn");
const sortSelect = 
  document.getElementById("sort-select");

const searchBtn = 
  document.getElementById("search-btn");
const searchInput = 
  document.getElementById("search-input");

const filterBtn = 
  document.getElementById("filter-btn");
const filterSelect = 
  document.getElementById("filter-select");

const list = 
  document.getElementById("concepts-list");

const sortCtlShell = 
  document.getElementById(
    "sort-ctl-shell");
const searchCtlShell = 
  document.getElementById(
    "search-ctl-shell");
const filterCtlShell = 
  document.getElementById(
    "filter-ctl-shell");

function createConceptElement(concept) {
  const li = document.createElement("li");
  li.className = "concept-shell";

  const termShell = 
    document.createElement("div");
  termShell.className = "term-shell";

  const termBtn = 
    document.createElement("button");
  termBtn.className = "term-btn";
  termBtn.textContent = ">";

  const details = 
    document.createElement("div");
  details.className = "details";
  details.textContent = 
    concept.description;
  details.textContent +=
    "\n\n" + concept.example;

  termBtn.addEventListener("click", () => {
    termBtnHandler(termBtn, details);
  });

  const term = 
    document.createElement("div");
  term.className = "term";
  term.textContent = concept.term;

  termShell.appendChild(termBtn);
  termShell.appendChild(term);

  li.appendChild(termShell);
  li.appendChild(details);

  return li;
}

function termBtnHandler(termBtn, details) {
  const isHidden = 
    !details.classList.contains(
      "open-details");

  if (isHidden) {
    details.classList.add("open-details");
    termBtn.textContent = "v";
  } else {
    details.classList.remove(
      "open-details")
    termBtn.textContent = ">";
  }
}
function hideAllControls() {
  sortSelect.classList.remove(
    "open-panel");
  searchInput.classList.remove(
    "open-panel");
  filterSelect.classList.remove(
    "open-panel");

  sortBtn.classList.remove("open-btn");
  searchBtn.classList.remove("open-btn");
  filterBtn.classList.remove("open-btn");
}
function toggleControl(btn, panel) {
  const isHidden = 
    !panel.classList.contains(
      "open-panel");

  hideAllControls();

  if (isHidden) {
    btn.classList.add("open-btn");
    panel.classList.add("open-panel");
  }
}
function setControls() {
  sortBtn.addEventListener("click", () => {
    toggleControl(
      sortBtn, sortSelect);
  });
      
  searchBtn.addEventListener(
    "click", () => {
    toggleControl(
      searchBtn, searchInput);
  });

  filterBtn.addEventListener(
    "click", () => {
    toggleControl(
      filterBtn, filterSelect);
  });
}

async function fetchConcepts() {
  const response = 
    await fetch("/concepts");
  const concepts = await response.json();
  list.innerHTML = "";

  for (const concept of concepts) {
    const li = 
      createConceptElement(concept);
    list.appendChild(li);
  }
}

document.addEventListener(
  "click", (event) => {
  const clickedInsideSort = 
    sortCtlShell.contains(event.target);
  const clickedInsideSearch = 
    searchCtlShell.contains(event.target);
  const clickedInsideFilter = 
    filterCtlShell.contains(event.target);

  if (!clickedInsideSort && 
      !clickedInsideSearch && 
      !clickedInsideFilter) {
    hideAllControls();
  }
});

setControls();
fetchConcepts();