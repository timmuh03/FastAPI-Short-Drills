const form = document.getElementById("note-form");
const input = document.getElementById("note-input");
const list = document.getElementById("notes-list")

function createNoteElement(note) {
  const li = document.createElement("li");
  li.textContent = note.text;

  const deleteArea = document.createElement(
    "div"
  );
  deleteArea.className = "note-delete-area";

  const button = document.createElement(
    "button"
  );
  button.className = "note-delete-btn";
  button.textContent = "Delete";

  button.addEventListener(
    "click", 
    async () => {
      const response = await fetch(
        `/notes/${note.id}`, {
          method: "DELETE",
        }
      );
      if (!response.ok) {
        alert("Failed to delete note");
        return;
      }

      await fetchNotes();
    }
  );
  li.appendChild(deleteArea)
  deleteArea.appendChild(button);

  const card = document.createElement(
    "div"
  );
  card.className = "note-card";
  card.textContent = note.text

  let startX = 0;
  let currentX = 0;
  let open = false;

  card.addEventListener(
    "touchstart", 
    (event) => {
      startX = event.touches[0].clientX;
    }
  );
  card.addEventListener(
    "touchmove",
    (event) => {
      currentX = event.touches[0].clientX;
      const deltaX = currentX - startX;
      
      if (deltaX < 0) {
        const clamped = Math.max(
          deltaX, -100
        );
        card.style.transform = 
          `translateX(${clamped}px)`;
      }
    }
  );

  card.addEventListener(
    "touchend",
    () => {
      const deltaX = currentX - startX;
      
      if (deltaX < -50) {
        card.style.transform = 
          "translateX(-100px)";
        open = true;
      } else {
        card.style.transform = 
          "translateX(0)";
        open = false;
      }

      startX = 0;
      currentX = 0;
    }
  );
  card.addEventListener(
    "click",
    () => {
      if (open) {
        card.style.transform = 
          "translateX(0)";
        open = false
      }
    }
  );
  li.appendChild(deleteArea);
  li.appendChild(card);
  deleteArea.appendChild(button)

  return li;
}

async function fetchNotes() {
   const response = await fetch("/notes");
   const notes = await response.json();
   list.innerHTML = "";

   for (const note of notes) {
      const li = createNoteElement(note);
      list.appendChild(li);
   }
}
form.addEventListener(
  "submit", 
  async (event) => {
    event.preventDefault();
  
    const text = input.value.trim();
    if (!text) return;
  
    const response = await fetch(
      "/notes", {
        method: "POST",
        headers: {
          "Content-Type": 
            "application/json",
        },
      body: JSON.stringify({ text }),
      }
    );
  
    if (!response.ok) {
       alert("Failed to add note");
       return;
     }
     input.value = "";
     await fetchNotes();
  }
);

fetchNotes()