const form = document.getElementById("concept-form");
const input = document.getElementById("concept-input");
const list = document.getElementById("concepts-list");

function createConceptElement(concept) {
  const li = document.createElement("li");
  li.className = "concept-shell";

  const termShell = 
    document.createElement("div");
  termShell.className = "term-shell"

  const termBtn =
    document.createElement("button");
  termBtn.className = "term-btn";
  termBtn.textContent = ">";

  const details = 
    document.createElement("div");
  details.className = "details";
  details.textContent = concept.description;
  details.textContent += "\n\n" + 
    concept.example;
  details.style.display = "none"
  
  termBtn.addEventListener(
    "click", () => {termBtnHandler(
      termBtn, details)
    }
  );

  const term = 
    document.createElement("div");
  term.className = "term";
  term.textContent = concept.term;

  termShell.appendChild(termBtn)
  termShell.appendChild(term);

  li.appendChild(termShell);
  li.appendChild(details);

  return li;
}

function termBtnHandler(termBtn, details) {
  const isHidden = 
    details.style.display === "none"
  if (isHidden) {
    details.style.display = "block";
    termBtn.textContent = "v";
  } else {
    details.style.display = "none";
    termBtn.textContent = ">";
  }
  
}

async function fetchConcepts() {
  const response = await fetch("/concepts");
  const concepts = await response.json();
  list.innerHTML = "";

  for (const concept of concepts) {
    const li = createConceptElement(concept);
    list.appendChild(li);
  }
}

fetchConcepts();