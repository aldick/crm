const columnsContainer = document.querySelector(".columns");
const columns = columnsContainer.querySelectorAll(".column");

let currentTask = null;

//* functions

const handleDragover = (event) => {
  event.preventDefault(); // allow drop

  const draggedTask = document.querySelector(".dragging");
  const target = event.target.closest(".task, .tasks");

  if (!target || target === draggedTask) return;

  if (target.classList.contains("tasks")) {
    // target is the tasks element
    const lastTask = target.lastElementChild;
    if (!lastTask) {
      // tasks is empty
      target.appendChild(draggedTask);
    } else {
      const { bottom } = lastTask.getBoundingClientRect();
      event.clientY > bottom && target.appendChild(draggedTask);
    }
  } else {
    // target is another
    const { top, height } = target.getBoundingClientRect();
    const distance = top + height / 2;

    if (event.clientY < distance) {
      target.before(draggedTask);
    } else {
      target.after(draggedTask);
    }
  }
};

const handleDrop = (event) => {
  event.preventDefault();
};

const handleDragend = (event) => {
  event.target.classList.remove("dragging");
  var options = {
    method: 'GET',
    mode: 'same-origin',
  }
  let order_id = event.target.getAttribute('class').split(" ")[1]
  let order_stage = event.target.closest(".column").getAttribute('class').split(" ")[1][6]
  fetch(`/orders/column-update/${order_id}/${order_stage}/`, options)

  setTimeout(() => {
    location.reload();
  }, "300");
};

const handleDragstart = (event) => {
  event.dataTransfer.effectsAllowed = "move";
  event.dataTransfer.setData("text/plain", "");
  requestAnimationFrame(() => event.target.classList.add("dragging"));
};

const handleEdit = (event) => {
  const task = event.target.closest(".task");
  const input = createTaskInput(task.innerText);
  task.replaceWith(input);
  input.focus();

  // move cursor to the end
  const selection = window.getSelection();
  selection.selectAllChildren(input);
  selection.collapseToEnd();
};

const handleBlur = (event) => {
  const input = event.target;
  const content = input.innerText.trim() || "Untitled";
  const task = createTask(content.replace(/\n/g, "<br>"));
  input.replaceWith(task);
};

const handleAdd = (event) => {
  const tasksEl = event.target.closest(".column").lastElementChild;
  const input = createTaskInput();
  tasksEl.appendChild(input);
  input.focus();
};

const updateColumnPrice = (column) => {
  const tasks = column.querySelector(".tasks").children;
  let sum = 0
  for(let i=0; i<tasks.length; i++) {
    sum += +tasks[i].dataset.price
  }
  column.querySelector(".column-title h2").dataset.price = sum;
};

const observeTaskChanges = () => {
  for (const column of columns) {
    const observer = new MutationObserver(() => updateColumnPrice(column));
    observer.observe(column.querySelector(".tasks"), { childList: true });
  }
};

observeTaskChanges();

const createTask = (content) => {
  const task = document.createElement("div");
  task.className = "task";
  task.draggable = true;
  task.innerHTML = `
  <div>${content}</div>
  <menu>
      <button data-edit><i class="bi bi-pencil-square"></i></button>
      <button data-delete><i class="bi bi-trash"></i></button>
  </menu>`;
  task.addEventListener("dragstart", handleDragstart);
  task.addEventListener("dragend", handleDragend);
  return task;
};

const createTaskInput = (text = "") => {
  const input = document.createElement("div");
  input.className = "task-input";
  input.dataset.placeholder = "Task name";
  input.contentEditable = true;
  input.innerText = text;
  input.addEventListener("blur", handleBlur);
  return input;
};

//* event listeners

// dragover and drop
tasksElements = columnsContainer.querySelectorAll(".tasks");
for (const tasksEl of tasksElements) {
  tasksEl.addEventListener("dragover", handleDragover);
  tasksEl.addEventListener("drop", handleDrop);
}

// add, edit and delete task
columnsContainer.addEventListener("click", (event) => {
  if (event.target.closest("button[data-add]")) {
    handleAdd(event);
  } else if (event.target.closest("button[data-edit]")) {
    handleEdit(event);
  } else if (event.target.closest("button[data-delete]")) {
    handleDelete(event);
  }
});

// clear current task

//* placeholder tasks

let tasks = document.getElementsByClassName("task");
console.log(tasks.length)

for (let i=0; i<tasks.length; i++) {
	tasks[i].addEventListener("dragstart", handleDragstart);
  	tasks[i].addEventListener("dragend", handleDragend);
}
