<template>
  <div class="page">

    <!-- PAGE HEADER -->
    <div class="page-header">
      <div class="page-header-left">
        <div class="page-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Clients</h1>
          <p class="page-subtitle">Gestion des comptes bancaires</p>
        </div>
      </div>
      <button class="btn-new" @click="openModal('create')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:16px;height:16px">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nouveau Client
      </button>
    </div>

    <!-- TOAST MESSAGE -->
    <transition name="slide-down">
      <div v-if="msg" :class="`toast toast-${msg.type}`">
        <svg v-if="msg.type==='success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="toast-icon">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="toast-icon">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ msg.text }}
      </div>
    </transition>

    <!-- LOADING -->
    <div v-if="loading" class="state-box">
      <div class="spinner"></div>
      <span>Chargement des clients...</span>
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="alert-error">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="alert-icon">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      {{ error }}
    </div>

    <!-- TABLE CARD -->
    <div v-else class="table-card">

      <!-- TOOLBAR -->
      <div class="table-toolbar">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input v-model="search" placeholder="Rechercher un client..." class="search-input" />
        </div>
        <div class="count-badge">{{ clients.length }} compte(s)</div>
      </div>

      <!-- TABLE -->
      <div style="overflow-x:auto;">
        <table class="data-table">
          <thead>
            <tr>
              <th>
                <div class="th-content">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon">
                    <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
                  </svg>
                  N° Compte
                </div>
              </th>
              <th>
                <div class="th-content">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                  </svg>
                  Nom Client
                </div>
              </th>
              <th>
                <div class="th-content">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon">
                    <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                  </svg>
                  Solde (Ar)
                </div>
              </th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in paginatedClients" :key="c.n_compte" class="table-row">
              <td>
                <span class="account-badge">{{ c.n_compte }}</span>
              </td>
              <td>
                <div class="client-name-cell">
                  <div class="avatar">{{ c.nomclient.charAt(0).toUpperCase() }}</div>
                  <span>{{ c.nomclient }}</span>
                </div>
              </td>
              <td>
                <span class="solde-value" :class="c.solde < 0 ? 'solde-neg' : 'solde-pos'">
                  {{ formatMontant(c.solde) }} Ar
                </span>
              </td>
              <td>
                <span class="status-badge" :class="c.solde >= 0 ? 'status-ok' : 'status-warn'">
                  <span class="status-dot"></span>
                  {{ c.solde >= 0 ? 'Actif' : 'Débiteur' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="btn-edit" @click="openModal('edit', c)" title="Modifier">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                    Modifier
                  </button>
                  <button class="btn-delete" @click="confirmDelete(c)" title="Supprimer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px">
                      <polyline points="3 6 5 6 21 6"/>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                    </svg>
                    Supprimer
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredClients.length === 0">
              <td colspan="5" class="empty-row">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width:2.2rem;height:2.2rem;opacity:0.3;margin-bottom:0.5rem;">
                  <circle cx="12" cy="12" r="10"/><line x1="8" y1="15" x2="16" y2="15"/>
                  <line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>
                </svg>
                <div>Aucun client trouvé</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div class="pagination" v-if="totalPages > 1">
        <span class="page-info">
          Page {{ currentPage }} / {{ totalPages }} — {{ filteredClients.length }} résultat(s)
        </span>
        <div class="page-controls">
          <button class="page-btn" @click="currentPage=1" :disabled="currentPage===1" title="Première">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
          </button>
          <button class="page-btn" @click="currentPage--" :disabled="currentPage===1" title="Précédent">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <button v-for="p in visiblePages" :key="p" class="page-btn" :class="{ active: p === currentPage }" @click="currentPage=p">{{ p }}</button>
          <button class="page-btn" @click="currentPage++" :disabled="currentPage===totalPages" title="Suivant">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
          <button class="page-btn" @click="currentPage=totalPages" :disabled="currentPage===totalPages" title="Dernière">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- ===== MODAL CREATE / EDIT ===== -->
    <transition name="modal-fade">
      <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <div class="modal-icon" :class="editMode ? 'modal-icon-edit' : 'modal-icon-create'">
              <svg v-if="editMode" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div>
              <div class="modal-title">{{ editMode ? 'Modifier le Client' : 'Nouveau Client' }}</div>
              <div class="modal-subtitle">{{ editMode ? 'Mise à jour des informations' : 'Créer un nouveau compte bancaire' }}</div>
            </div>
          </div>

          <div v-if="formError" class="form-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;flex-shrink:0">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ formError }}
          </div>

          <!-- N° Compte : seulement en création -->
          <div class="form-group" v-if="!editMode">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
                <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
              </svg>
              N° Compte
            </label>
            <input v-model="form.n_compte" class="form-input" placeholder="Ex: CPT-001" maxlength="20" />
            <div class="form-hint">Identifiant unique du compte (max 20 caractères)</div>
          </div>

          <!-- Nom Client -->
          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              Nom Complet
            </label>
            <input v-model="form.nomclient" class="form-input" placeholder="Ex: Jean Dupont" maxlength="100" />
          </div>

          <!-- Solde -->
          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon">
                <line x1="12" y1="1" x2="12" y2="23"/>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
              </svg>
              Solde initial (Ar)
            </label>
            <input v-model.number="form.solde" type="number" min="0" step="0.01" class="form-input" placeholder="Ex: 500000" />
          </div>

          <div class="modal-actions">
            <button class="btn-cancel" @click="closeModal">Annuler</button>
            <button class="btn-confirm"
              :class="editMode ? 'btn-edit-confirm' : 'btn-create-confirm'"
              @click="saveClient"
              :disabled="saving">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:15px;height:15px">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <div v-else class="spinner-sm"></div>
              {{ saving ? 'Enregistrement...' : (editMode ? 'Modifier' : 'Créer le compte') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- ===== MODAL CONFIRM DELETE ===== -->
    <transition name="modal-fade">
      <div class="modal-overlay" v-if="showDeleteModal" @click.self="showDeleteModal=false">
        <div class="modal">
          <div class="modal-header">
            <div class="modal-icon modal-icon-danger">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
            </div>
            <div>
              <div class="modal-title">Confirmer la suppression</div>
              <div class="modal-subtitle">Cette action est irréversible</div>
            </div>
          </div>

          <div class="delete-info">
            <div class="delete-row">
              <span>N° Compte</span>
              <strong class="account-badge">{{ deleteTarget?.n_compte }}</strong>
            </div>
            <div class="delete-row">
              <span>Nom Client</span>
              <strong>{{ deleteTarget?.nomclient }}</strong>
            </div>
            <div class="delete-row">
              <span>Solde</span>
              <strong :class="deleteTarget?.solde >= 0 ? 'solde-pos' : 'solde-neg'">
                {{ formatMontant(deleteTarget?.solde) }} Ar
              </strong>
            </div>
            <div class="delete-warn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:15px;height:15px;flex-shrink:0">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              Tous les retraits associés à ce compte seront également supprimés.
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn-cancel" @click="showDeleteModal=false">Annuler</button>
            <button class="btn-confirm btn-delete-confirm" @click="doDelete" :disabled="saving">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:15px;height:15px">
                <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
              </svg>
              <div v-else class="spinner-sm"></div>
              {{ saving ? 'Suppression...' : 'Confirmer la suppression' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { clientService } from '../services/api'

const clients        = ref([])
const loading        = ref(true)
const saving         = ref(false)
const error          = ref('')
const search         = ref('')
const currentPage    = ref(1)
const perPage        = 5

const showModal      = ref(false)
const showDeleteModal= ref(false)
const editMode       = ref(false)
const editId         = ref(null)
const deleteTarget   = ref(null)
const formError      = ref('')
const msg            = ref(null)

const form = ref({ n_compte: '', nomclient: '', solde: 0 })

const formatMontant = (v) => parseFloat(v || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2 })

const showMsg = (text, type = 'success') => {
  msg.value = { text, type }
  setTimeout(() => msg.value = null, 4000)
}

/* ---- Filtering & Pagination ---- */
const filteredClients = computed(() => {
  if (!search.value) return clients.value
  const q = search.value.toLowerCase()
  return clients.value.filter(c =>
    c.n_compte.toLowerCase().includes(q) || c.nomclient.toLowerCase().includes(q)
  )
})
const totalPages = computed(() => Math.max(1, Math.ceil(filteredClients.value.length / perPage)))
const paginatedClients = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredClients.value.slice(start, start + perPage)
})
const visiblePages = computed(() => {
  const pages = []
  for (let i = Math.max(1, currentPage.value - 1); i <= Math.min(totalPages.value, currentPage.value + 1); i++)
    pages.push(i)
  return pages
})
watch(search, () => { currentPage.value = 1 })

/* ---- Load ---- */
const loadData = async () => {
  loading.value = true; error.value = ''
  try {
    const res = await clientService.getAll()
    clients.value = res.data
  } catch (e) {
    error.value = 'Impossible de charger les clients. Vérifiez que le backend Flask est démarré.'
  } finally {
    loading.value = false
  }
}

/* ---- Modal helpers ---- */
const openModal = (mode, client = null) => {
  formError.value = ''
  editMode.value = mode === 'edit'
  if (mode === 'edit') {
    editId.value = client.n_compte
    form.value = { n_compte: client.n_compte, nomclient: client.nomclient, solde: parseFloat(client.solde) }
  } else {
    form.value = { n_compte: '', nomclient: '', solde: 0 }
  }
  showModal.value = true
}
const closeModal = () => { showModal.value = false; formError.value = '' }

/* ---- Save (create or update) ---- */
const saveClient = async () => {
  formError.value = ''
  if (!editMode.value && !form.value.n_compte.trim()) {
    formError.value = 'Le numéro de compte est obligatoire.'; return
  }
  if (!form.value.nomclient.trim()) {
    formError.value = 'Le nom du client est obligatoire.'; return
  }
  if (form.value.solde === '' || form.value.solde === null || isNaN(form.value.solde)) {
    formError.value = 'Le solde doit être un nombre valide.'; return
  }

  saving.value = true
  try {
    if (editMode.value) {
      await clientService.update(editId.value, {
        nomclient: form.value.nomclient,
        solde: form.value.solde
      })
      showMsg('Client modifié avec succès !')
    } else {
      await clientService.create({
        n_compte:  form.value.n_compte.trim(),
        nomclient: form.value.nomclient.trim(),
        solde:     form.value.solde
      })
      showMsg('Client créé avec succès !')
    }
    closeModal()
    await loadData()
  } catch (e) {
    formError.value = e.response?.data?.error || 'Erreur lors de l\'enregistrement'
  }
  saving.value = false
}

/* ---- Delete ---- */
const confirmDelete = (c) => { deleteTarget.value = c; showDeleteModal.value = true }
const doDelete = async () => {
  saving.value = true
  try {
    await clientService.delete(deleteTarget.value.n_compte)
    showMsg('Client supprimé avec succès !')
    showDeleteModal.value = false
    await loadData()
  } catch (e) {
    showMsg(e.response?.data?.error || 'Erreur lors de la suppression', 'error')
    showDeleteModal.value = false
  }
  saving.value = false
}

onMounted(loadData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* { box-sizing: border-box; }
.page { font-family: 'Plus Jakarta Sans', sans-serif; }

/* PAGE HEADER */
.page-header {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:1.5rem;
  background:linear-gradient(135deg,#0f2544 0%,#1a4a8a 100%);
  border-radius:16px; padding:1.5rem 2rem; color:white;
  box-shadow:0 6px 24px rgba(10,22,40,0.2);
}
.page-header-left { display:flex; align-items:center; gap:1rem; }
.page-icon {
  width:52px; height:52px;
  background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.2);
  border-radius:14px; display:flex; align-items:center; justify-content:center;
}
.page-icon svg { width:26px; height:26px; color:white; }
.page-title  { font-size:1.5rem; font-weight:800; margin:0; }
.page-subtitle { font-size:0.82rem; opacity:0.7; margin:0; }
.btn-new {
  display:flex; align-items:center; gap:0.5rem;
  background:white; color:#1a4a8a; border:none;
  padding:0.65rem 1.2rem; border-radius:10px;
  font-weight:700; font-size:0.88rem; cursor:pointer;
  transition:all 0.2s; font-family:inherit;
}
.btn-new:hover { background:#ebf4ff; transform:translateY(-1px); box-shadow:0 4px 12px rgba(0,0,0,0.15); }

/* TOAST */
.toast {
  display:flex; align-items:center; gap:0.7rem;
  padding:0.9rem 1.2rem; border-radius:12px; margin-bottom:1rem;
  font-size:0.9rem; font-weight:600;
}
.toast-success { background:#f0fff4; color:#276749; border:1.5px solid #9ae6b4; }
.toast-error   { background:#fff5f5; color:#c53030; border:1.5px solid #feb2b2; }
.toast-icon    { width:18px; height:18px; flex-shrink:0; }
.slide-down-enter-active, .slide-down-leave-active { transition:all 0.3s; }
.slide-down-enter-from, .slide-down-leave-to { opacity:0; transform:translateY(-10px); }

/* STATES */
.state-box {
  display:flex; align-items:center; justify-content:center;
  gap:0.8rem; padding:3rem; color:#718096;
  background:white; border-radius:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
}
.spinner {
  width:22px; height:22px; border:3px solid #e2e8f0;
  border-top-color:#2b6cb0; border-radius:50%;
  animation:spin 0.8s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
.alert-error {
  display:flex; align-items:center; gap:0.8rem;
  background:#fff5f5; color:#c53030; border:1.5px solid #feb2b2;
  padding:1rem 1.2rem; border-radius:12px; margin-bottom:1rem;
}
.alert-icon { width:20px; height:20px; flex-shrink:0; }

/* TABLE CARD */
.table-card { background:white; border-radius:16px; box-shadow:0 2px 16px rgba(0,0,0,0.07); overflow:hidden; }

.table-toolbar {
  display:flex; align-items:center; justify-content:space-between;
  padding:1.2rem 1.5rem; border-bottom:1px solid #f0f4f8; gap:1rem;
}
.search-box { position:relative; flex:1; max-width:320px; }
.search-icon { position:absolute; left:0.75rem; top:50%; transform:translateY(-50%); width:16px; height:16px; color:#a0aec0; pointer-events:none; }
.search-input {
  width:100%; padding:0.55rem 0.75rem 0.55rem 2.2rem;
  border:1.5px solid #e2e8f0; border-radius:10px;
  font-size:0.875rem; outline:none; transition:border-color 0.2s; font-family:inherit;
}
.search-input:focus { border-color:#2b6cb0; box-shadow:0 0 0 3px rgba(43,108,176,0.1); }
.count-badge {
  background:#ebf4ff; color:#2b6cb0;
  padding:0.3rem 0.8rem; border-radius:20px; font-size:0.8rem; font-weight:700; white-space:nowrap;
}

/* TABLE */
.data-table { width:100%; border-collapse:collapse; }
.data-table thead th {
  padding:0.85rem 1.2rem; text-align:left;
  font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;
  color:#64748b; background:#f8fafc; border-bottom:1.5px solid #e2e8f0; white-space:nowrap;
}
.th-content { display:flex; align-items:center; gap:0.4rem; }
.th-icon { width:13px; height:13px; }
.table-row { transition:background 0.15s; }
.table-row:hover { background:#f8fafc; }
.data-table tbody td { padding:0.9rem 1.2rem; border-bottom:1px solid #f0f4f8; font-size:0.9rem; color:#2d3748; }
.data-table tbody tr:last-child td { border-bottom:none; }

.account-badge { background:#ebf4ff; color:#2b6cb0; padding:0.25rem 0.7rem; border-radius:8px; font-size:0.82rem; font-weight:700; font-family:monospace; }
.client-name-cell { display:flex; align-items:center; gap:0.7rem; }
.avatar { width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,#667eea,#764ba2); color:white; font-weight:700; font-size:0.85rem; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.solde-value { font-weight:700; font-size:0.92rem; }
.solde-pos { color:#276749; }
.solde-neg { color:#c53030; }
.status-badge { display:inline-flex; align-items:center; gap:0.4rem; padding:0.28rem 0.75rem; border-radius:20px; font-size:0.78rem; font-weight:700; }
.status-ok   { background:#f0fff4; color:#276749; }
.status-warn { background:#fff5f5; color:#c53030; }
.status-dot  { width:6px; height:6px; border-radius:50%; background:currentColor; }

/* ACTION BUTTONS */
.action-buttons { display:flex; gap:0.4rem; }
.btn-edit {
  display:flex; align-items:center; gap:0.35rem;
  background:#fffbeb; color:#92400e; border:1.5px solid #fcd34d;
  padding:0.38rem 0.7rem; border-radius:8px; font-size:0.78rem; font-weight:700;
  cursor:pointer; transition:all 0.15s; font-family:inherit;
}
.btn-edit:hover { background:#fcd34d; }
.btn-delete {
  display:flex; align-items:center; gap:0.35rem;
  background:#fff5f5; color:#c53030; border:1.5px solid #feb2b2;
  padding:0.38rem 0.7rem; border-radius:8px; font-size:0.78rem; font-weight:700;
  cursor:pointer; transition:all 0.15s; font-family:inherit;
}
.btn-delete:hover { background:#fed7d7; }

.empty-row { text-align:center; padding:3rem !important; color:#a0aec0; display:flex; flex-direction:column; align-items:center; }

/* PAGINATION */
.pagination { display:flex; align-items:center; justify-content:space-between; padding:1rem 1.5rem; border-top:1px solid #f0f4f8; flex-wrap:wrap; gap:0.5rem; }
.page-info   { font-size:0.82rem; color:#718096; }
.page-controls { display:flex; align-items:center; gap:0.3rem; }
.page-btn {
  min-width:34px; height:34px; border:1.5px solid #e2e8f0;
  background:white; border-radius:8px; cursor:pointer;
  font-size:0.85rem; font-weight:600; color:#4a5568;
  display:flex; align-items:center; justify-content:center;
  transition:all 0.15s; font-family:inherit;
}
.page-btn:hover:not(:disabled) { border-color:#2b6cb0; color:#2b6cb0; background:#ebf4ff; }
.page-btn:disabled { opacity:0.35; cursor:not-allowed; }
.page-btn.active { background:#2b6cb0; border-color:#2b6cb0; color:white; }

/* MODAL */
.modal-fade-enter-active, .modal-fade-leave-active { transition:all 0.2s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity:0; }
.modal-overlay {
  position:fixed; inset:0; background:rgba(15,37,68,0.55);
  display:flex; align-items:center; justify-content:center;
  z-index:1000; backdrop-filter:blur(4px);
}
.modal {
  background:white; border-radius:20px; padding:2rem;
  width:460px; max-width:95vw; box-shadow:0 25px 60px rgba(0,0,0,0.25);
}
.modal-header { display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem; }
.modal-icon { width:46px; height:46px; border-radius:12px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.modal-icon-create { background:#ebf4ff; color:#2b6cb0; }
.modal-icon-edit   { background:#fffbeb; color:#92400e; }
.modal-icon-danger { background:#fff5f5; color:#c53030; }
.modal-title    { font-size:1.1rem; font-weight:800; color:#0f2544; margin:0; }
.modal-subtitle { font-size:0.8rem; color:#718096; margin:0; }

.form-error {
  display:flex; align-items:center; gap:0.6rem;
  background:#fff5f5; color:#c53030; border:1.5px solid #feb2b2;
  padding:0.75rem 1rem; border-radius:10px; margin-bottom:1rem; font-size:0.85rem;
}
.form-group { margin-bottom:1rem; }
.form-label { display:flex; align-items:center; gap:0.4rem; margin-bottom:0.4rem; font-size:0.83rem; font-weight:700; color:#374151; }
.label-icon { width:14px; height:14px; color:#6b7280; }
.form-input {
  width:100%; padding:0.65rem 0.9rem; border:1.5px solid #e2e8f0;
  border-radius:10px; font-size:0.9rem; outline:none;
  transition:border-color 0.2s; font-family:inherit; color:#2d3748;
}
.form-input:focus { border-color:#2b6cb0; box-shadow:0 0 0 3px rgba(43,108,176,0.1); }
.form-hint { font-size:0.75rem; color:#94a3b8; margin-top:0.3rem; }

/* DELETE INFO BOX */
.delete-info { background:#f8fafc; border-radius:12px; padding:1rem; margin-bottom:1.5rem; }
.delete-row {
  display:flex; justify-content:space-between; align-items:center;
  padding:0.45rem 0; border-bottom:1px solid #e2e8f0; font-size:0.88rem;
}
.delete-row:last-of-type { border-bottom:none; }
.delete-row span { color:#718096; }
.delete-warn {
  display:flex; align-items:flex-start; gap:0.5rem;
  margin-top:0.85rem; padding:0.65rem 0.75rem;
  background:#fffbeb; border:1.5px solid #fcd34d; border-radius:8px;
  font-size:0.8rem; color:#92400e; font-weight:600; line-height:1.4;
}

.modal-actions { display:flex; justify-content:flex-end; gap:0.75rem; margin-top:1.5rem; }
.btn-cancel {
  background:#f1f5f9; color:#64748b; border:none;
  padding:0.65rem 1.2rem; border-radius:10px; font-weight:700; font-size:0.88rem;
  cursor:pointer; font-family:inherit; transition:background 0.15s;
}
.btn-cancel:hover { background:#e2e8f0; }
.btn-confirm {
  display:flex; align-items:center; gap:0.5rem; border:none;
  padding:0.65rem 1.3rem; border-radius:10px; font-weight:700; font-size:0.88rem;
  cursor:pointer; font-family:inherit; transition:all 0.2s;
}
.btn-create-confirm { background:#2b6cb0; color:white; }
.btn-create-confirm:hover:not(:disabled) { background:#2c5282; }
.btn-edit-confirm   { background:#d97706; color:white; }
.btn-edit-confirm:hover:not(:disabled)   { background:#b45309; }
.btn-delete-confirm { background:#e53e3e; color:white; }
.btn-delete-confirm:hover:not(:disabled) { background:#c53030; }
.btn-confirm:disabled { opacity:0.6; cursor:not-allowed; }
.spinner-sm { width:14px; height:14px; border:2px solid rgba(255,255,255,0.4); border-top-color:white; border-radius:50%; animation:spin 0.7s linear infinite; }
</style>