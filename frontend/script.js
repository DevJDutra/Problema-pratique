const API_BASE =
  window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";

const machineSelect = document.getElementById("machine-select");
const machineButton = document.getElementById("machine-button");
const machineResult = document.getElementById("machine-result");
const noteMachineSelect = document.getElementById("note-machine-select");
const noteAuthor = document.getElementById("note-author");
const noteType = document.getElementById("note-type");
const noteMessage = document.getElementById("note-message");
const noteButton = document.getElementById("note-button");
const noteResult = document.getElementById("note-result");
const statusMachineSelect = document.getElementById("status-machine-select");
const machineAction = document.getElementById("machine-action");
const statusMachineGroup = document.getElementById("status-machine-group");
const newMachineGroup = document.getElementById("new-machine-group");
const newMachineName = document.getElementById("new-machine-name");
const statusSelect = document.getElementById("status-select");
const maintenanceDate = document.getElementById("maintenance-date");
const equipmentObservation = document.getElementById("equipment-observation");
const statusButton = document.getElementById("status-button");
const statusResult = document.getElementById("status-result");

const registrationInput = document.getElementById("registration-input");
const paymentButton = document.getElementById("payment-button");
const paymentResult = document.getElementById("payment-result");
const decreaseButton = document.getElementById("decrease-button");
const increaseButton = document.getElementById("increase-button");
const peopleCount = document.getElementById("people-count");
const counterMessage = document.getElementById("counter-message");

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.erro || "Erro ao processar a solicitacao.");
  }

  return data;
}

function escapeHtml(value) {
  return String(value).replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function buildStatusBadge(type, label) {
  return `<span class="status ${type}">${label}</span>`;
}

function getMachineStatusBadge(status) {
  if (status === "operando") {
    return buildStatusBadge("success", "Operando");
  }

  if (status === "fora de servico") {
    return buildStatusBadge("danger", "Fora de servico");
  }

  return buildStatusBadge("warning", "Com problema");
}

function buildNoteTypeBadge(type) {
  return type === "defeito"
    ? buildStatusBadge("danger", "Defeito relatado")
    : buildStatusBadge("success", "Anotacao");
}

function renderMachineNotes(notes) {
  if (!notes.length) {
    return "<p>Nenhuma anotacao registrada para esta maquina.</p>";
  }

  const items = notes
    .map(
      (note) => `
        <div class="note-item">
          <button
            type="button"
            class="note-delete"
            data-note-id="${note.id}"
            data-machine-id="${note.machine_id}"
            aria-label="Remover anotacao"
            title="Remover anotacao"
          >
            X
          </button>
          <div class="note-meta">
            <span class="note-author">${escapeHtml(note.autor)}</span>
            ${buildNoteTypeBadge(note.tipo)}
            <span class="note-date">${escapeHtml(note.criado_em)}</span>
          </div>
          <p>${escapeHtml(note.mensagem)}</p>
        </div>
      `
    )
    .join("");

  return `<div class="notes-list">${items}</div>`;
}

function renderMachine(machine) {
  const notes = Array.isArray(machine.anotacoes) ? machine.anotacoes : [];
  const badge = getMachineStatusBadge(machine.status);
  const maintenance = escapeHtml(machine.ultima_manutencao || "Nao informada");
  const observation = escapeHtml(machine.observacao || "Sem observacoes.");

  machineResult.classList.remove("muted");
  machineResult.innerHTML = `
    <strong>${machine.nome}</strong>
    <div>${badge}</div>
    <p><b>Localizacao:</b> ${machine.localizacao}</p>
    <p><b>Ultima manutencao:</b> ${maintenance}</p>
    <p><b>Observacao:</b> ${observation}</p>
    <p><b>Relatos registrados:</b> ${notes.length}</p>
    ${renderMachineNotes(notes)}
  `;
}

function renderPayment(student) {
  const isPaid = student.mensalidade === "paga";
  const badge = isPaid
    ? buildStatusBadge("success", "Mensalidade paga")
    : buildStatusBadge("danger", "Mensalidade em atraso");

  paymentResult.classList.remove("muted");
  paymentResult.innerHTML = `
    <strong>${student.nome}</strong>
    <p><b>Matricula:</b> ${student.matricula}</p>
    <div>${badge}</div>
    <p><b>Referencia:</b> ${student.referencia}</p>
    <p><b>Vencimento:</b> ${student.vencimento}</p>
  `;
}

async function loadMachines() {
  try {
    const machines = await apiRequest("/api/maquinas");
    const selectedMachineId = machineSelect.value;
    const selectedNoteMachineId = noteMachineSelect.value;
    const selectedStatusMachineId = statusMachineSelect.value;

    machineSelect.innerHTML =
      '<option value="">Selecione uma maquina</option>';
    noteMachineSelect.innerHTML =
      '<option value="">Selecione uma maquina</option>';
    statusMachineSelect.innerHTML =
      '<option value="">Selecione uma maquina</option>';

    for (const machine of machines) {
      const option = document.createElement("option");
      option.value = machine.id;
      option.textContent = `${machine.id} - ${machine.nome}`;
      machineSelect.appendChild(option);

      const noteOption = document.createElement("option");
      noteOption.value = machine.id;
      noteOption.textContent = `${machine.id} - ${machine.nome}`;
      noteMachineSelect.appendChild(noteOption);

      const statusOption = document.createElement("option");
      statusOption.value = machine.id;
      statusOption.textContent = `${machine.id} - ${machine.nome}`;
      statusMachineSelect.appendChild(statusOption);
    }

    if (selectedMachineId) {
      machineSelect.value = selectedMachineId;
    }
    if (selectedNoteMachineId) {
      noteMachineSelect.value = selectedNoteMachineId;
    }
    if (selectedStatusMachineId) {
      statusMachineSelect.value = selectedStatusMachineId;
    }
  } catch (error) {
    machineSelect.innerHTML =
      '<option value="">Erro ao carregar maquinas</option>';
    noteMachineSelect.innerHTML =
      '<option value="">Erro ao carregar maquinas</option>';
    statusMachineSelect.innerHTML =
      '<option value="">Erro ao carregar maquinas</option>';
  }
}

function syncMachineActionForm() {
  const action = machineAction.value;
  const isCreate = action === "create";
  const isDelete = action === "delete";

  statusMachineGroup.classList.toggle("hidden", isCreate);
  newMachineGroup.classList.toggle("hidden", !isCreate);

  statusSelect.disabled = isDelete;
  maintenanceDate.disabled = isDelete;
  equipmentObservation.disabled = isDelete;

  statusButton.classList.toggle("button-danger", isDelete);

  if (isCreate) {
    statusButton.textContent = "Catalogar maquina";
    statusResult.classList.add("muted");
    statusResult.textContent = "Preencha os campos da nova maquina para cadastrar no catalogo.";
    return;
  }

  if (isDelete) {
    statusButton.textContent = "Remover maquina";
    statusResult.classList.add("muted");
    statusResult.textContent = "Selecione a maquina que deseja remover do catalogo.";
    return;
  }

  statusButton.textContent = "Salvar status";
  statusResult.classList.add("muted");
  statusResult.textContent = "Escolha uma maquina e os dados que deseja atualizar.";
}

machineButton.addEventListener("click", async () => {
  if (!machineSelect.value) {
    machineResult.classList.add("muted");
    machineResult.textContent = "Selecione uma maquina antes de consultar.";
    return;
  }

  try {
    const machine = await apiRequest(`/api/maquinas/${machineSelect.value}`);
    renderMachine(machine);
  } catch (error) {
    machineResult.classList.add("muted");
    machineResult.textContent = error.message;
  }
});

paymentButton.addEventListener("click", async () => {
  const registration = registrationInput.value.trim();

  if (!registration) {
    paymentResult.classList.add("muted");
    paymentResult.textContent = "Digite uma matricula para consultar.";
    return;
  }

  try {
    const student = await apiRequest(`/api/mensalidades/${registration}`);
    renderPayment(student);
  } catch (error) {
    paymentResult.classList.add("muted");
    paymentResult.textContent = error.message;
  }
});

noteButton.addEventListener("click", async () => {
  const machineId = noteMachineSelect.value;
  const author = noteAuthor.value.trim();
  const type = noteType.value;
  const message = noteMessage.value.trim();

  if (!machineId) {
    noteResult.classList.add("muted");
    noteResult.textContent = "Selecione a maquina do relato.";
    return;
  }

  if (!author) {
    noteResult.classList.add("muted");
    noteResult.textContent = "Digite o nome do aluno.";
    return;
  }

  if (!message) {
    noteResult.classList.add("muted");
    noteResult.textContent = "Descreva a anotacao ou defeito encontrado.";
    return;
  }

  try {
    noteButton.disabled = true;

    const note = await apiRequest(`/api/maquinas/${machineId}/anotacoes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        autor: author,
        tipo: type,
        mensagem: message,
      }),
    });

    noteResult.classList.remove("muted");
    noteResult.innerHTML = `
      <strong>Relato salvo com sucesso</strong>
      <p>${escapeHtml(note.autor)} registrou um(a) ${escapeHtml(note.tipo)} em ${escapeHtml(note.criado_em)}.</p>
    `;

    noteAuthor.value = "";
    noteType.value = "anotacao";
    noteMessage.value = "";

    if (machineSelect.value === machineId) {
      const machine = await apiRequest(`/api/maquinas/${machineId}`);
      renderMachine(machine);
    }
  } catch (error) {
    noteResult.classList.add("muted");
    noteResult.textContent = error.message;
  } finally {
    noteButton.disabled = false;
  }
});

statusButton.addEventListener("click", async () => {
  const action = machineAction.value;
  const machineId = statusMachineSelect.value;
  const status = statusSelect.value;
  const selectedMaintenanceDate = maintenanceDate.value;
  const observation = equipmentObservation.value.trim();
  const machineName = newMachineName.value.trim();

  if (action !== "create" && !machineId) {
    statusResult.classList.add("muted");
    statusResult.textContent = "Selecione a maquina que deseja atualizar.";
    return;
  }

  if (action === "delete") {
    try {
      statusButton.disabled = true;

      await apiRequest(`/api/maquinas/${machineId}`, {
        method: "DELETE",
      });

      statusResult.classList.remove("muted");
      statusResult.innerHTML = `
        <strong>Maquina removida</strong>
        <p>A maquina foi removida do catalogo com sucesso.</p>
      `;

      if (machineSelect.value === machineId) {
        machineSelect.value = "";
        machineResult.classList.add("muted");
        machineResult.textContent = "A maquina consultada foi removida do catalogo.";
      }

      if (noteMachineSelect.value === machineId) {
        noteMachineSelect.value = "";
      }

      statusMachineSelect.value = "";
      await loadMachines();
    } catch (error) {
      statusResult.classList.add("muted");
      statusResult.textContent = error.message;
    } finally {
      statusButton.disabled = false;
    }
    return;
  }

  if (!selectedMaintenanceDate) {
    statusResult.classList.add("muted");
    statusResult.textContent = "Informe a data da manutencao.";
    return;
  }

  if (!observation) {
    statusResult.classList.add("muted");
    statusResult.textContent = "Informe a observacao do equipamento.";
    return;
  }

  if (action === "create" && !machineName) {
    statusResult.classList.add("muted");
    statusResult.textContent = "Informe o nome da nova maquina.";
    return;
  }

  try {
    statusButton.disabled = true;

    const machine = action === "create"
      ? await apiRequest("/api/maquinas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nome: machineName,
          status,
          ultima_manutencao: selectedMaintenanceDate,
          observacao: observation,
        }),
      })
      : await apiRequest(`/api/maquinas/${machineId}/status`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          status,
          ultima_manutencao: selectedMaintenanceDate,
          observacao: observation,
        }),
      });

    statusResult.classList.remove("muted");
    statusResult.innerHTML = `
      <strong>${action === "create" ? "Maquina catalogada" : "Status atualizado"}</strong>
      <p>A maquina <b>${escapeHtml(machine.nome)}</b> agora esta com status <b>${escapeHtml(machine.status)}</b>.</p>
      <p>Manutencao: <b>${escapeHtml(machine.ultima_manutencao)}</b>.</p>
    `;

    newMachineName.value = "";
    await loadMachines();

    if (action === "create") {
      machineAction.value = "update";
      syncMachineActionForm();
      statusMachineSelect.value = String(machine.id);
    }

    if (machineSelect.value === machineId || action === "create") {
      machineSelect.value = String(machine.id);
      renderMachine(machine);
    }
  } catch (error) {
    statusResult.classList.add("muted");
    statusResult.textContent = error.message;
  } finally {
    statusButton.disabled = false;
  }
});

statusMachineSelect.addEventListener("change", async () => {
  if (!statusMachineSelect.value) {
    return;
  }

  try {
    const machine = await apiRequest(`/api/maquinas/${statusMachineSelect.value}`);
    if (machine.status) {
      statusSelect.value = machine.status;
    }
    maintenanceDate.value = machine.ultima_manutencao || "";
    equipmentObservation.value = machine.observacao || "";
  } catch (error) {
    statusResult.classList.add("muted");
    statusResult.textContent = error.message;
  }
});

machineAction.addEventListener("change", () => {
  syncMachineActionForm();
});

machineResult.addEventListener("click", async (event) => {
  const deleteButton = event.target.closest(".note-delete");
  if (!deleteButton) {
    return;
  }

  const noteId = deleteButton.dataset.noteId;
  const machineId = deleteButton.dataset.machineId;

  try {
    await apiRequest(`/api/maquinas/${machineId}/anotacoes/${noteId}`, {
      method: "DELETE",
    });

    const machine = await apiRequest(`/api/maquinas/${machineId}`);
    renderMachine(machine);
  } catch (error) {
    machineResult.classList.add("muted");
    machineResult.textContent = error.message;
  }
});

function updateCounterMessage(count) {
  counterMessage.classList.remove("muted");
  counterMessage.innerHTML = `
    <strong>Contagem atualizada</strong>
    <p>No momento ha <b>${count}</b> pessoa(s) registrada(s) na academia.</p>
  `;
}

function renderCounter(count) {
  peopleCount.textContent = count;
  updateCounterMessage(count);
}

async function loadPeopleCount() {
  try {
    const data = await apiRequest("/api/pessoas");
    renderCounter(data.people_count);
  } catch (error) {
    counterMessage.classList.add("muted");
    counterMessage.textContent = error.message;
  }
}

async function updatePeopleCount(action) {
  try {
    increaseButton.disabled = true;
    decreaseButton.disabled = true;

    const data = await apiRequest(`/api/pessoas/${action}`, {
      method: "POST",
    });

    renderCounter(data.people_count);
  } catch (error) {
    counterMessage.classList.add("muted");
    counterMessage.textContent = error.message;
  } finally {
    increaseButton.disabled = false;
    decreaseButton.disabled = false;
  }
}

increaseButton.addEventListener("click", () => {
  updatePeopleCount("entrada");
});

decreaseButton.addEventListener("click", () => {
  updatePeopleCount("saida");
});

loadMachines();
loadPeopleCount();
syncMachineActionForm();
