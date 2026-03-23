<template>
  <div class="page">
    <!-- PAGE HEADER -->
    <div class="page-header">
      <div class="page-header-left">
        <div class="page-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <rect x="2" y="5" width="20" height="14" rx="3"/>
            <line x1="2" y1="10" x2="22" y2="10"/>
            <line x1="6" y1="15" x2="10" y2="15"/>
            <line x1="14" y1="15" x2="16" y2="15"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Retraits</h1>
          <p class="page-subtitle">Opérations bancaires — CRUD complet</p>
        </div>
      </div>
      <button class="btn-new" @click="openModal('create')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:16px;height:16px">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Nouveau Retrait
      </button>
    </div>

    <!-- MESSAGE -->
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

    <!-- TABLE CARD -->
    <div class="table-card">
      <div class="table-toolbar">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input v-model="search" placeholder="Rechercher par compte, chèque..." class="search-input" />
        </div>
        <div class="count-badge">{{ retraits.length }} retrait(s)</div>
      </div>

      <div v-if="loading" class="state-box">
        <div class="spinner"></div><span>Chargement...</span>
      </div>

      <div v-else style="overflow-x:auto;">
        <table class="data-table">
          <thead>
            <tr>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                N° Retrait
              </div></th>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                N° Chèque
              </div></th>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
                N° Compte
              </div></th>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                Client
              </div></th>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                Montant
              </div></th>
              <th><div class="th-content">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="th-icon"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                Solde restant
              </div></th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in paginatedRetraits" :key="r.n_retrait" class="table-row">
              <td><span class="id-badge">#{{ r.n_retrait }}</span></td>
              <td><span class="cheque-badge">{{ r.n_cheque }}</span></td>
              <td><span class="account-badge">{{ r.n_compte }}</span></td>
              <td>
                <div class="client-cell">
                  <div class="avatar">{{ r.nomclient.charAt(0) }}</div>
                  {{ r.nomclient }}
                </div>
              </td>
              <td><span class="montant-value">− {{ formatMontant(r.montant) }} Ar</span></td>
              <td>
                <span class="solde-value" :class="r.solde < 0 ? 'solde-neg' : 'solde-pos'">
                  {{ formatMontant(r.solde) }} Ar
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="btn-edit" @click="openModal('edit', r)" title="Modifier">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:15px;height:15px">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                    Modifier
                  </button>
                  <button class="btn-delete" @click="confirmDelete(r)" title="Supprimer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:15px;height:15px">
                      <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                    </svg>
                    Supprimer
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredRetraits.length === 0">
              <td colspan="7" class="empty-row">Aucun retrait trouvé</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- PAGINATION -->
      <div class="pagination" v-if="totalPages > 1">
        <span class="page-info">Page {{ currentPage }} / {{ totalPages }} — {{ filteredRetraits.length }} résultat(s)</span>
        <div class="page-controls">
          <button class="page-btn" @click="currentPage=1" :disabled="currentPage===1">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
          </button>
          <button class="page-btn" @click="currentPage--" :disabled="currentPage===1">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <button v-for="p in visiblePages" :key="p" class="page-btn" :class="{ active: p===currentPage }" @click="currentPage=p">{{ p }}</button>
          <button class="page-btn" @click="currentPage++" :disabled="currentPage===totalPages">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
          <button class="page-btn" @click="currentPage=totalPages" :disabled="currentPage===totalPages">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL CREATE/EDIT -->
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
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            </div>
            <div>
              <div class="modal-title">{{ editMode ? 'Modifier le Retrait' : 'Nouveau Retrait' }}</div>
              <div class="modal-subtitle">{{ editMode ? 'Mise à jour du montant' : 'Enregistrer une opération' }}</div>
            </div>
          </div>

          <div v-if="formError" class="form-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;flex-shrink:0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            {{ formError }}
          </div>

          <template v-if="!editMode">
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
                N° Compte Client
              </label>
              <select v-model="form.n_compte" class="form-select">
                <option value="">— Sélectionner un compte —</option>
                <option v-for="c in clients" :key="c.n_compte" :value="c.n_compte">
                  {{ c.n_compte }} · {{ c.nomclient }} ({{ formatMontant(c.solde) }} Ar)
                </option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                N° Chèque
              </label>
              <input v-model="form.n_cheque" class="form-input" placeholder="Ex: CHQ-2024-001" />
            </div>
          </template>

          <div class="form-group">
            <label class="form-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="label-icon"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              Montant (Ar)
            </label>
            <input v-model.number="form.montant" type="number" min="1" class="form-input" placeholder="Ex: 50000" />
          </div>

          <div class="modal-actions">
            <button class="btn-cancel" @click="closeModal">Annuler</button>
            <button class="btn-confirm" :class="editMode ? 'btn-edit-confirm' : 'btn-create-confirm'" @click="saveRetrait" :disabled="saving">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:15px;height:15px"><polyline points="20 6 9 17 4 12"/></svg>
              <div v-else class="spinner-sm"></div>
              {{ saving ? 'Enregistrement...' : (editMode ? 'Modifier' : 'Créer le retrait') }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL DELETE -->
    <transition name="modal-fade">
      <div class="modal-overlay" v-if="showDeleteModal" @click.self="showDeleteModal=false">
        <div class="modal modal-danger">
          <div class="modal-header">
            <div class="modal-icon modal-icon-danger">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px">
                <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
              </svg>
            </div>
            <div>
              <div class="modal-title">Confirmer la suppression</div>
              <div class="modal-subtitle">Cette action est irréversible</div>
            </div>
          </div>
          <div class="delete-info">
            <div class="delete-row"><span>Retrait</span><strong>#{{ deleteTarget?.n_retrait }}</strong></div>
            <div class="delete-row"><span>Montant</span><strong class="montant-value">{{ formatMontant(deleteTarget?.montant) }} Ar</strong></div>
            <div class="delete-row"><span>Client</span><strong>{{ deleteTarget?.nomclient }}</strong></div>
            <p class="delete-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;flex-shrink:0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              Le montant sera automatiquement remboursé sur le compte client.
            </p>
          </div>
          <div class="modal-actions">
            <button class="btn-cancel" @click="showDeleteModal=false">Annuler</button>
            <button class="btn-confirm btn-delete-confirm" @click="doDelete" :disabled="saving">
              <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:15px;height:15px"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
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
import { retraitService, clientService } from '../services/api'

const retraits = ref([])
const clients = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const showDeleteModal = ref(false)
const editMode = ref(false)
const editId = ref(null)
const deleteTarget = ref(null)
const formError = ref('')
const msg = ref(null)
const search = ref('')
const currentPage = ref(1)
const perPage = 5
const form = ref({ n_compte: '', n_cheque: '', montant: '' })

const formatMontant = (v) => parseFloat(v || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2 })

const showMsg = (text, type = 'success') => {
  msg.value = { text, type }
  setTimeout(() => msg.value = null, 4000)
}

const filteredRetraits = computed(() => {
  if (!search.value) return retraits.value
  const q = search.value.toLowerCase()
  return retraits.value.filter(r =>
    r.n_compte.toLowerCase().includes(q) ||
    r.n_cheque.toLowerCase().includes(q) ||
    r.nomclient.toLowerCase().includes(q)
  )
})

const totalPages = computed(() => Math.ceil(filteredRetraits.value.length / perPage))

const paginatedRetraits = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredRetraits.value.slice(start, start + perPage)
})

const visiblePages = computed(() => {
  const pages = []
  for (let i = Math.max(1, currentPage.value - 1); i <= Math.min(totalPages.value, currentPage.value + 1); i++) pages.push(i)
  return pages
})

watch(search, () => { currentPage.value = 1 })

const loadData = async () => {
  loading.value = true
  try {
    const [r, c] = await Promise.all([retraitService.getAll(), clientService.getAll()])
    retraits.value = r.data
    clients.value = c.data
  } catch(e) {
    showMsg('Erreur de chargement. Backend démarré ?', 'error')
  }
  loading.value = false
}

const openModal = (mode, retrait = null) => {
  formError.value = ''
  editMode.value = mode === 'edit'
  if (mode === 'edit') {
    editId.value = retrait.n_retrait
    form.value = { montant: retrait.montant }
  } else {
    form.value = { n_compte: '', n_cheque: '', montant: '' }
  }
  showModal.value = true
}

const closeModal = () => { showModal.value = false; formError.value = '' }

const saveRetrait = async () => {
  formError.value = ''
  if (!editMode.value && (!form.value.n_compte || !form.value.n_cheque)) {
    formError.value = 'Veuillez remplir tous les champs.'; return
  }
  if (!form.value.montant || form.value.montant <= 0) {
    formError.value = 'Le montant doit être supérieur à 0.'; return
  }
  saving.value = true
  try {
    if (editMode.value) {
      await retraitService.update(editId.value, { montant: form.value.montant })
      showMsg('Retrait modifié avec succès !')
    } else {
      await retraitService.create(form.value)
      showMsg('Retrait créé avec succès !')
    }
    closeModal()
    await loadData()
  } catch (e) {
    formError.value = e.response?.data?.error || 'Erreur lors de l\'enregistrement'
  }
  saving.value = false
}

const confirmDelete = (r) => { deleteTarget.value = r; showDeleteModal.value = true }

const doDelete = async () => {
  saving.value = true
  try {
    await retraitService.delete(deleteTarget.value.n_retrait)
    showMsg('Retrait supprimé avec succès !')
    showDeleteModal.value = false
    await loadData()
  } catch (e) {
    showMsg(e.response?.data?.error || 'Erreur lors de la suppression', 'error')
  }
  saving.value = false
}

onMounted(loadData)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
.page { font-family: 'Plus Jakarta Sans', sans-serif; }

.page-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #0f2544 0%, #1a4a8a 100%);
  border-radius: 16px; padding: 1.5rem 2rem; color: white;
}
.page-header-left { display: flex; align-items: center; gap: 1rem; }
.page-icon {
  width: 52px; height: 52px; background: rgba(255,255,255,0.15);
  border-radius: 14px; display: flex; align-items: center; justify-content: center;
}
.page-icon svg { width: 26px; height: 26px; color: white; }
.page-title { font-size: 1.5rem; font-weight: 800; margin: 0; }
.page-subtitle { font-size: 0.82rem; opacity: 0.7; margin: 0; }

.btn-new {
  display: flex; align-items: center; gap: 0.5rem;
  background: white; color: #1a4a8a; border: none;
  padding: 0.65rem 1.2rem; border-radius: 10px;
  font-weight: 700; font-size: 0.88rem; cursor: pointer;
  transition: all 0.2s; font-family: inherit;
}
.btn-new:hover { background: #ebf4ff; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }

.toast {
  display: flex; align-items: center; gap: 0.7rem;
  padding: 0.9rem 1.2rem; border-radius: 12px; margin-bottom: 1rem;
  font-size: 0.9rem; font-weight: 600;
}
.toast-success { background: #f0fff4; color: #276749; border: 1.5px solid #9ae6b4; }
.toast-error { background: #fff5f5; color: #c53030; border: 1.5px solid #feb2b2; }
.toast-icon { width: 18px; height: 18px; flex-shrink: 0; }

.slide-down-enter-active, .slide-down-leave-active { transition: all 0.3s; }
.slide-down-enter-from { opacity: 0; transform: translateY(-10px); }
.slide-down-leave-to { opacity: 0; transform: translateY(-10px); }

.table-card { background: white; border-radius: 16px; box-shadow: 0 2px 16px rgba(0,0,0,0.07); overflow: hidden; }

.table-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 1.5rem; border-bottom: 1px solid #f0f4f8; gap: 1rem;
}
.search-box { position: relative; flex: 1; max-width: 340px; }
.search-icon { position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: #a0aec0; }
.search-input {
  width: 100%; padding: 0.55rem 0.75rem 0.55rem 2.2rem;
  border: 1.5px solid #e2e8f0; border-radius: 10px;
  font-size: 0.875rem; outline: none; font-family: inherit; transition: border-color 0.2s;
}
.search-input:focus { border-color: #2b6cb0; }
.count-badge {
  background: #ebf4ff; color: #2b6cb0;
  padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; white-space: nowrap;
}

.state-box { display: flex; align-items: center; justify-content: center; gap: 0.8rem; padding: 3rem; color: #718096; }
.spinner { width: 20px; height: 20px; border: 3px solid #e2e8f0; border-top-color: #2b6cb0; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th {
  padding: 0.85rem 1.2rem; text-align: left;
  font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
  color: #64748b; background: #f8fafc; border-bottom: 1.5px solid #e2e8f0; white-space: nowrap;
}
.th-content { display: flex; align-items: center; gap: 0.4rem; }
.th-icon { width: 13px; height: 13px; }
.table-row:hover { background: #f8fafc; }
.data-table tbody td { padding: 0.85rem 1.2rem; border-bottom: 1px solid #f0f4f8; font-size: 0.88rem; color: #2d3748; }
.data-table tbody tr:last-child td { border-bottom: none; }

.id-badge { background: #f7fafc; color: #718096; padding: 0.2rem 0.5rem; border-radius: 6px; font-size: 0.8rem; font-weight: 700; border: 1px solid #e2e8f0; }
.cheque-badge { background: #fef9e7; color: #7d6608; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; font-family: monospace; }
.account-badge { background: #ebf4ff; color: #2b6cb0; padding: 0.22rem 0.65rem; border-radius: 8px; font-size: 0.8rem; font-weight: 700; font-family: monospace; }
.client-cell { display: flex; align-items: center; gap: 0.6rem; }
.avatar { width: 30px; height: 30px; border-radius: 8px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; font-weight: 700; font-size: 0.8rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.montant-value { color: #c53030; font-weight: 700; }
.solde-pos { color: #276749; font-weight: 700; }
.solde-neg { color: #c53030; font-weight: 700; }

.action-buttons { display: flex; gap: 0.4rem; }
.btn-edit {
  display: flex; align-items: center; gap: 0.35rem;
  background: #fffbeb; color: #92400e; border: 1.5px solid #fcd34d;
  padding: 0.38rem 0.7rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700;
  cursor: pointer; transition: all 0.15s; font-family: inherit;
}
.btn-edit:hover { background: #fcd34d; }
.btn-delete {
  display: flex; align-items: center; gap: 0.35rem;
  background: #fff5f5; color: #c53030; border: 1.5px solid #feb2b2;
  padding: 0.38rem 0.7rem; border-radius: 8px; font-size: 0.78rem; font-weight: 700;
  cursor: pointer; transition: all 0.15s; font-family: inherit;
}
.btn-delete:hover { background: #fed7d7; }

.empty-row { text-align: center; padding: 3rem !important; color: #a0aec0; }

/* PAGINATION */
.pagination { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.5rem; border-top: 1px solid #f0f4f8; flex-wrap: wrap; gap: 0.5rem; }
.page-info { font-size: 0.82rem; color: #718096; }
.page-controls { display: flex; gap: 0.3rem; }
.page-btn { min-width: 34px; height: 34px; border: 1.5px solid #e2e8f0; background: white; border-radius: 8px; cursor: pointer; font-size: 0.85rem; font-weight: 600; color: #4a5568; display: flex; align-items: center; justify-content: center; transition: all 0.15s; font-family: inherit; }
.page-btn:hover:not(:disabled) { border-color: #2b6cb0; color: #2b6cb0; background: #ebf4ff; }
.page-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.page-btn.active { background: #2b6cb0; border-color: #2b6cb0; color: white; }

/* MODAL */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.2s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.modal-overlay { position: fixed; inset: 0; background: rgba(15,37,68,0.55); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal { background: white; border-radius: 20px; padding: 2rem; width: 460px; max-width: 95vw; box-shadow: 0 25px 60px rgba(0,0,0,0.25); }
.modal-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; }
.modal-icon { width: 46px; height: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.modal-icon-create { background: #ebf4ff; color: #2b6cb0; }
.modal-icon-edit { background: #fffbeb; color: #92400e; }
.modal-icon-danger { background: #fff5f5; color: #c53030; }
.modal-title { font-size: 1.1rem; font-weight: 800; color: #0f2544; margin: 0; }
.modal-subtitle { font-size: 0.8rem; color: #718096; margin: 0; }

.form-error { display: flex; align-items: center; gap: 0.6rem; background: #fff5f5; color: #c53030; border: 1.5px solid #feb2b2; padding: 0.75rem 1rem; border-radius: 10px; margin-bottom: 1rem; font-size: 0.85rem; }
.form-group { margin-bottom: 1rem; }
.form-label { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.4rem; font-size: 0.83rem; font-weight: 700; color: #374151; }
.label-icon { width: 14px; height: 14px; color: #6b7280; }
.form-input, .form-select { width: 100%; padding: 0.65rem 0.9rem; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 0.9rem; outline: none; transition: border-color 0.2s; font-family: inherit; color: #2d3748; }
.form-input:focus, .form-select:focus { border-color: #2b6cb0; box-shadow: 0 0 0 3px rgba(43,108,176,0.1); }

.delete-info { background: #f8fafc; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; }
.delete-row { display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0; border-bottom: 1px solid #e2e8f0; font-size: 0.88rem; }
.delete-row:last-of-type { border-bottom: none; }
.delete-row span { color: #718096; }
.delete-note { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.75rem; margin-bottom: 0; font-size: 0.8rem; color: #718096; }

.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }
.btn-cancel { background: #f1f5f9; color: #64748b; border: none; padding: 0.65rem 1.2rem; border-radius: 10px; font-weight: 700; font-size: 0.88rem; cursor: pointer; font-family: inherit; transition: background 0.15s; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-confirm { display: flex; align-items: center; gap: 0.5rem; border: none; padding: 0.65rem 1.3rem; border-radius: 10px; font-weight: 700; font-size: 0.88rem; cursor: pointer; font-family: inherit; transition: all 0.2s; }
.btn-create-confirm { background: #2b6cb0; color: white; }
.btn-create-confirm:hover:not(:disabled) { background: #2c5282; }
.btn-edit-confirm { background: #d97706; color: white; }
.btn-edit-confirm:hover:not(:disabled) { background: #b45309; }
.btn-delete-confirm { background: #e53e3e; color: white; }
.btn-delete-confirm:hover:not(:disabled) { background: #c53030; }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }
.spinner-sm { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.4); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
</style>