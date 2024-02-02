const taskInput = document.querySelector(".task-input input"),
  filters = document.querySelectorAll(".filters span"),
  clearAll = document.querySelector(".clear-btn"),
  taskBox = document.querySelector(".task-box");

let editId,
  isEditTask = false,
  todos = JSON.parse(localStorage.getItem("todo-list"));

filters.forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelector("span.active").classList.remove("active");
    btn.classList.add("active");
    showTodo(btn.id);
  });
});

showTodo("all");

function showTodo(filter) {
  let liTag = "";
  if (todos) {
    todos.forEach((todo, id) => {
      let completed = todo.status == "completed" ? "checked" : "";
      if (filter == todo.status || filter == "all") {
        liTag += `<li class="task">
        <label for="${id}">
          <input onclick="updateStatus(this)" type="checkbox" id="${id}" ${completed}>
          <p class="${completed}">${todo.name} (Target: ${todo.target})</p>
        </label>
        <div class="settings">
          <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
          <ul class="task-menu">
            <li onclick='editTask(${id}, "${todo.name}", "${todo.target}")'><i class="uil uil-pen"></i>Edit</li>
            <li onclick='deleteTask(${id}, "${filter}")'><i class="uil uil-trash"></i>Delete</li>
          </ul>
        </div>
      </li>`;
      }
    });
  }
  taskBox.innerHTML = liTag || `<span>You don't have any task here</span>`;
  let checkTask = taskBox.querySelectorAll(".task");
  !checkTask.length
    ? clearAll.classList.remove("active")
    : clearAll.classList.add("active");
  taskBox.offsetHeight >= 300
    ? taskBox.classList.add("overflow")
    : taskBox.classList.remove("overflow");
}

function showMenu(selectedTask) {
  let menuDiv = selectedTask.parentElement.lastElementChild;
  menuDiv.classList.add("show");
  document.addEventListener("click", (e) => {
    if (e.target.tagName != "I" || e.target != selectedTask) {
      menuDiv.classList.remove("show");
    }
  });
}

function updateStatus(selectedTask) {
  let taskName = selectedTask.parentElement.lastElementChild;
  if (selectedTask.checked) {
    taskName.classList.add("checked");
    todos[selectedTask.id].status = "completed";
  } else {
    taskName.classList.remove("checked");
    todos[selectedTask.id].status = "pending";
  }
  localStorage.setItem("todo-list", JSON.stringify(todos));
}

function editTask(taskId, textName) {
  editId = taskId;
  isEditTask = true;
  taskInput.value = textName;
  taskInput.focus();
  taskInput.classList.add("active");
}

function deleteTask(deleteId, filter) {
  isEditTask = false;
  todos.splice(deleteId, 1);
  localStorage.setItem("todo-list", JSON.stringify(todos));
  showTodo(filter);
}

clearAll.addEventListener("click", () => {
  isEditTask = false;
  todos.splice(0, todos.length);
  localStorage.setItem("todo-list", JSON.stringify(todos));
  showTodo();
});

const targetInput = document.getElementById("targetInput");

targetInput.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    // When Enter key is pressed in the target input
    taskInput.focus(); // Move focus to the stock input
  }
});



taskInput.addEventListener("keyup", (e) => {
    let stockName = taskInput.value.trim();
    let stockTarget = taskInput.nextElementSibling.value.trim(); // Get the value of the second input
  
    if (e.key == "Enter" && stockName && stockTarget) { // Check if both inputs are filled
      if (!isEditTask) {
        todos = !todos ? [] : todos;
        let taskInfo = { name: stockName, target: stockTarget, status: "pending" }; // Store both stock name and target
        todos.push(taskInfo);
      } else {
        isEditTask = false;
        todos[editId].name = stockName;
        todos[editId].target = stockTarget; // Update the target
      }
      taskInput.value = "";
      taskInput.nextElementSibling.value = ""; // Clear the second input
      localStorage.setItem("todo-list", JSON.stringify(todos));
      showTodo(document.querySelector("span.active").id);
    }
  });


// ... Your existing JavaScript code ...

// Call this function at the start to load existing data from CSV
async function loadInitialData() {
  const initialData = await eel.load_from_csv()();
  if (initialData && initialData.length > 0) {
    todos = initialData;
    showTodo(document.querySelector("span.active").id);
  }
}

// Call the loadInitialData function when the DOM content is loaded
document.addEventListener("DOMContentLoaded", () => {
  loadInitialData();
});

// Save the todos to CSV whenever there is an update
function saveTodoToCSV() {
  eel.save_to_csv(todos)(function(response) {
    console.log(response); // Log the response from Python
  });
}























/*
 
  function saveDataToCSV() {
    var stockName = document.getElementById('stockNameInput').value.trim();
    var target = document.getElementById('targetInput').value.trim();
    
      todos.push({
      name: stockName,
      target: stockTarget,
      status: "pending"
    });

    eel.save_to_csv(stockName, target)(function(response) {
      console.log(response); // Log the response from Python (e.g., 'Data saved successfully')
      showTodo(document.querySelector("span.active").id); // Refresh the task list
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    eel.load_from_csv()(function(response) {
      if (response.length > 0) {
        todos = response.map(item => ({
          name: item[0],
          target: item[1],
          status: "pending"
        }));
        showTodo(document.querySelector("span.active").id);
      }
    });
  });
  

  function deleteTask(deleteId, filter) {
    isEditTask = false;
    todos.splice(deleteId, 1);
    eel.delete_from_csv(deleteId)();
    showTodo(filter);
  }



  


  
  


// The HTML element where the chart will be displayed
*/