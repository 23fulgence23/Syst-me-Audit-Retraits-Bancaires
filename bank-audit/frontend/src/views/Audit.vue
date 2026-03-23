<template>
  <div class="page">

    <!-- PAGE HEADER -->
    <div class="page-header">
      <div class="page-header-left">
        <div class="page-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">Journal d'Audit</h1>
          <p class="page-subtitle">Supervision des opérations bancaires</p>
        </div>
      </div>
      <button class="btn-refresh" @click="loadData">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:13px;height:13px">
          <polyline points="23 4 23 10 17 10"/>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
        </svg>
        Actualiser
      </button>
    </div>

    <!-- STATS BOXES -->
    <div class="stats-grid" v-if="stats">

      <!-- INSERT -->
      <div class="stat-box box-insert">
        <div class="box-shine"></div>
        <div class="box-bg-anim"></div>
        <div class="box-left">
          <div class="box-icon-wrap icon-insert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:24px;height:24px">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
          </div>
          <div>
            <div class="box-num">{{ stats.nb_insertions }}</div>
            <div class="box-label">Insertions</div>
          </div>
        </div>
        <div class="box-right">
          <span class="box-pill pill-insert">INSERT</span>
          <div class="box-bar"><div class="box-bar-fill fill-insert" :style="{ width: getPercent(stats.nb_insertions) + '%' }"></div></div>
        </div>
      </div>

      <!-- UPDATE -->
      <div class="stat-box box-update">
        <div class="box-shine"></div>
        <div class="box-bg-anim"></div>
        <div class="box-left">
          <div class="box-icon-wrap icon-update">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:24px;height:24px">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </div>
          <div>
            <div class="box-num">{{ stats.nb_modifications }}</div>
            <div class="box-label">Modifications</div>
          </div>
        </div>
        <div class="box-right">
          <span class="box-pill pill-update">UPDATE</span>
          <div class="box-bar"><div class="box-bar-fill fill-update" :style="{ width: getPercent(stats.nb_modifications) + '%' }"></div></div>
        </div>
      </div>

      <!-- DELETE -->
      <div class="stat-box box-delete">
        <div class="box-shine"></div>
        <div class="box-bg-anim"></div>
        <div class="box-left">
          <div class="box-icon-wrap icon-delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:24px;height:24px">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
          </div>
          <div>
            <div class="box-num">{{ stats.nb_suppressions }}</div>
            <div class="box-label">Suppressions</div>
          </div>
        </div>
        <div class="box-right">
          <span class="box-pill pill-delete">DELETE</span>
          <div class="box-bar"><div class="box-bar-fill fill-delete" :style="{ width: getPercent(stats.nb_suppressions) + '%' }"></div></div>
        </div>
      </div>

      <!-- TOTAL -->
      <div class="stat-box box-total">
        <div class="box-shine"></div>
        <div class="box-bg-anim"></div>
        <div class="box-left">
          <div class="box-icon-wrap icon-total">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:24px;height:24px">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <div>
            <div class="box-num">{{ total }}</div>
            <div class="box-label">Total opérations</div>
          </div>
        </div>
        <div class="box-right">
          <span class="box-pill pill-total">TOTAL</span>
          <div class="box-bar"><div class="box-bar-fill fill-total" style="width:100%"></div></div>
        </div>
      </div>

    </div>

    <!-- TABLE CARD -->
    <div class="table-card">

      <div class="table-toolbar">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input v-model="search" placeholder="Rechercher compte, client..." class="search-input"/>
        </div>
        <div class="filter-group">
          <button v-for="f in filters" :key="f.val"
            class="filter-btn"
            :class="['fbtn-' + f.val.toLowerCase(), { 'filter-active': activeFilter === f.val }]"
            @click="setFilter(f.val)">
            <span class="fbtn-dot"></span>{{ f.label }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="state-box">
        <div class="spinner"></div><span>Chargement de l'audit...</span>
      </div>
      <div v-else-if="error" class="alert-error">{{ error }}</div>

      <div v-else style="overflow-x:auto;">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th><th>Action</th><th>Date &amp; Heure</th>
              <th>N° Retrait</th><th>N° Compte</th><th>Client</th>
              <th>Mnt. Ancien</th><th>Mnt. Nouveau</th><th>Utilisateur</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in paginatedAudit" :key="a.id" class="table-row">
              <td><span class="id-badge">#{{ a.id }}</span></td>
              <td><span :style="getBadgeStyle(a.type_action)">{{ a.type_action }}</span></td>
              <td>
                <div class="date-cell">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:11px;height:11px;color:#a0aec0;flex-shrink:0"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  {{ a.date_maj }}
                </div>
              </td>
              <td><span class="retrait-badge">#{{ a.n_retrait }}</span></td>
              <td><span class="account-badge">{{ a.n_compte }}</span></td>
              <td>
                <div class="client-cell">
                  <div class="avatar">{{ a.nomclient ? a.nomclient.charAt(0).toUpperCase() : '?' }}</div>
                  {{ a.nomclient }}
                </div>
              </td>
              <td><span class="montant-old">{{ a.montant_ancien > 0 ? formatMontant(a.montant_ancien) + ' Ar' : '—' }}</span></td>
              <td><span class="montant-new">{{ a.montant_nouv > 0 ? formatMontant(a.montant_nouv) + ' Ar' : '—' }}</span></td>
              <td>
                <div class="user-cell">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:11px;height:11px;color:#a0aec0;flex-shrink:0"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  {{ a.utilisateur }}
                </div>
              </td>
            </tr>
            <tr v-if="filteredAudit.length === 0">
              <td colspan="9" class="empty-row">Aucune opération trouvée</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- BOTTOM BAR -->
      <div class="bottom-bar">
        <div class="sum-chips">
          <span class="sum-chip chip-insert">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px;flex-shrink:0">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
            {{ stats ? stats.nb_insertions : 0 }} insertion(s)
          </span>
          <span class="sum-chip chip-update">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px;flex-shrink:0">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            {{ stats ? stats.nb_modifications : 0 }} modification(s)
          </span>
          <span class="sum-chip chip-delete">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px;flex-shrink:0">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>
            </svg>
            {{ stats ? stats.nb_suppressions : 0 }} suppression(s)
          </span>
          <span class="sum-chip chip-total">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px;flex-shrink:0">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            {{ total }} opération(s) au total
          </span>
        </div>
        <div class="pag-right">
          <span class="pag-info">
            <strong>{{ filteredAudit.length === 0 ? 0 : (currentPage - 1) * perPage + 1 }}–{{ Math.min(currentPage * perPage, filteredAudit.length) }}</strong>
            / {{ filteredAudit.length }}
          </span>
          <div class="pag-controls" v-if="totalPages >= 1">
            <button class="pag-btn" @click="currentPage=1" :disabled="currentPage===1">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
            </button>
            <button class="pag-btn" @click="currentPage--" :disabled="currentPage===1">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <button v-if="currentPage > 2" class="pag-btn pag-ellipsis" disabled>…</button>
            <button v-for="p in visiblePages" :key="p" class="pag-btn"
              :class="{ 'pag-active': p === currentPage }" @click="currentPage = p">{{ p }}</button>
            <button v-if="currentPage < totalPages - 1" class="pag-btn pag-ellipsis" disabled>…</button>
            <button class="pag-btn" @click="currentPage++" :disabled="currentPage===totalPages">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
            <button class="pag-btn" @click="currentPage=totalPages" :disabled="currentPage===totalPages">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="width:12px;height:12px"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { auditService } from '../services/api'

const audit        = ref([])
const stats        = ref(null)
const loading      = ref(true)
const error        = ref('')
const search       = ref('')
const activeFilter = ref('ALL')
const currentPage  = ref(1)
const perPage      = 3

const filters = [
  { val: 'ALL',    label: 'Tous'   },
  { val: 'INSERT', label: 'Insert' },
  { val: 'UPDATE', label: 'Update' },
  { val: 'DELETE', label: 'Delete' },
]

const formatMontant = (v) =>
  parseFloat(v || 0).toLocaleString('fr-FR', { minimumFractionDigits: 2 })

const total = computed(() =>
  stats.value
    ? stats.value.nb_insertions + stats.value.nb_modifications + stats.value.nb_suppressions
    : 0
)
const getPercent = (n) => (!total.value ? 0 : Math.round((n / total.value) * 100))

const getBadgeStyle = (action) => {
  const s = {
    INSERT: 'background:#dcfce7;color:#166534;padding:2px 9px;border-radius:20px;font-size:0.7rem;font-weight:800;display:inline-block;letter-spacing:.04em;',
    UPDATE: 'background:#fef9c3;color:#713f12;padding:2px 9px;border-radius:20px;font-size:0.7rem;font-weight:800;display:inline-block;letter-spacing:.04em;',
    DELETE: 'background:#fee2e2;color:#991b1b;padding:2px 9px;border-radius:20px;font-size:0.7rem;font-weight:800;display:inline-block;letter-spacing:.04em;',
  }
  return s[action] || 'background:#f1f5f9;color:#475569;padding:2px 9px;border-radius:20px;font-size:0.7rem;font-weight:800;display:inline-block;'
}

const setFilter = (f) => { activeFilter.value = f; currentPage.value = 1 }

const filteredAudit = computed(() => {
  let data = audit.value
  if (activeFilter.value !== 'ALL')
    data = data.filter(a => a.type_action === activeFilter.value)
  if (search.value) {
    const q = search.value.toLowerCase()
    data = data.filter(a =>
      (a.n_compte  || '').toLowerCase().includes(q) ||
      (a.nomclient || '').toLowerCase().includes(q)
    )
  }
  return data
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredAudit.value.length / perPage)))
const paginatedAudit = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredAudit.value.slice(start, start + perPage)
})
const visiblePages = computed(() => {
  const pages = []
  for (let i = Math.max(1, currentPage.value - 1); i <= Math.min(totalPages.value, currentPage.value + 1); i++)
    pages.push(i)
  return pages
})

watch([search, activeFilter], () => { currentPage.value = 1 })

const loadData = async () => {
  loading.value = true; error.value = ''
  try {
    const res = await auditService.getAll()
    audit.value = res.data.audit
    stats.value = res.data.stats
  } catch (e) {
    error.value = "Impossible de charger l'audit. Vérifiez que le backend Flask est démarré."
  }
  loading.value = false
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
  margin-bottom:0.85rem;
  background:linear-gradient(135deg,#0a1628 0%,#0f2e6e 60%,#1a4a8a 100%);
  border-radius:14px; padding:0.9rem 1.5rem; color:white;
  box-shadow:0 4px 20px rgba(10,22,40,0.2);
}
.page-header-left { display:flex; align-items:center; gap:0.85rem; }
.page-icon {
  width:42px; height:42px;
  background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.2);
  border-radius:11px; display:flex; align-items:center; justify-content:center;
}
.page-icon svg { width:21px; height:21px; color:white; }
.page-title    { font-size:1.2rem; font-weight:800; margin:0; }
.page-subtitle { font-size:0.74rem; opacity:0.65; margin:0; }
.btn-refresh {
  display:flex; align-items:center; gap:0.4rem;
  background:rgba(255,255,255,0.12); color:white;
  border:1px solid rgba(255,255,255,0.25);
  padding:0.48rem 1rem; border-radius:8px;
  font-weight:700; font-size:0.79rem; cursor:pointer;
  transition:all 0.2s; font-family:inherit;
}
.btn-refresh:hover { background:rgba(255,255,255,0.25); transform:translateY(-1px); }

/* ═══════════════════════════════════════
   STATS BOXES — grandes + animation hover
   ═══════════════════════════════════════ */
.stats-grid {
  display:grid; grid-template-columns:repeat(4,1fr);
  gap:0.85rem; margin-bottom:0.85rem;
}

.stat-box {
  position:relative; overflow:hidden; background:white;
  border-radius:16px;
  padding:2.5rem 1.9rem;           /* ↑ hauteur augmentée */
  box-shadow:0 3px 14px rgba(0,0,0,0.08);
  display:flex; align-items:center; justify-content:space-between;
  gap:0.9rem;
  cursor:default;

  /* transition complète pour l'animation hover */
  transition:
    transform 0.3s cubic-bezier(.34,1.56,.64,1),
    box-shadow 0.3s ease,
    background 0.4s ease,
    border-color 0.3s ease;
}

/* Décoration : effet lumière en sweep */
.box-shine {
  position:absolute; top:0; left:-100%;
  width:60%; height:100%;
  background:linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent);
  transform:skewX(-20deg);
  transition:left 0.5s ease;
  pointer-events:none; z-index:2;
}
.stat-box:hover .box-shine { left:150%; }

/* Fond animé en dégradé couleur au hover */
.box-bg-anim {
  position:absolute; inset:0; border-radius:inherit;
  opacity:0; transition:opacity 0.35s ease;
  pointer-events:none; z-index:0;
}
.box-insert .box-bg-anim { background:linear-gradient(135deg,#dcfce7 0%,#bbf7d0 100%); }
.box-update .box-bg-anim { background:linear-gradient(135deg,#fef9c3 0%,#fde68a 100%); }
.box-delete .box-bg-anim { background:linear-gradient(135deg,#fee2e2 0%,#fecaca 100%); }
.box-total  .box-bg-anim { background:linear-gradient(135deg,#dbeafe 0%,#bfdbfe 100%); }

.stat-box:hover .box-bg-anim { opacity:1; }

/* Bordure gauche colorée + effet hover renforcé */
.box-insert {
  border-left:4px solid #16a34a;
}
.box-update {
  border-left:4px solid #d97706;
}
.box-delete {
  border-left:4px solid #dc2626;
}
.box-total {
  border-left:4px solid #2563eb;
}

/* Hover : remontée + ombre dramatique + scale léger */
.box-insert:hover {
  transform:translateY(-6px) scale(1.02);
  box-shadow:0 16px 36px rgba(22,163,74,0.22), 0 4px 12px rgba(0,0,0,0.08);
  border-left-color:#15803d;
}
.box-update:hover {
  transform:translateY(-6px) scale(1.02);
  box-shadow:0 16px 36px rgba(217,119,6,0.22), 0 4px 12px rgba(0,0,0,0.08);
  border-left-color:#b45309;
}
.box-delete:hover {
  transform:translateY(-6px) scale(1.02);
  box-shadow:0 16px 36px rgba(220,38,38,0.22), 0 4px 12px rgba(0,0,0,0.08);
  border-left-color:#b91c1c;
}
.box-total:hover {
  transform:translateY(-6px) scale(1.02);
  box-shadow:0 16px 36px rgba(37,99,235,0.22), 0 4px 12px rgba(0,0,0,0.08);
  border-left-color:#1d4ed8;
}

/* Icône grandit au hover */
.box-icon-wrap {
  width:46px; height:46px; border-radius:13px;          /* ↑ plus grand */
  display:flex; align-items:center; justify-content:center;
  flex-shrink:0; position:relative; z-index:1;
  transition:transform 0.35s cubic-bezier(.34,1.56,.64,1);
}
.stat-box:hover .box-icon-wrap { transform:scale(1.18) rotate(-5deg); }

.icon-insert { background:#dcfce7; color:#16a34a; }
.icon-update { background:#fef9c3; color:#d97706; }
.icon-delete { background:#fee2e2; color:#dc2626; }
.icon-total  { background:#dbeafe; color:#2563eb; }

.box-left  { display:flex; align-items:center; gap:0.8rem; flex-shrink:0; position:relative; z-index:1; }
.box-right { display:flex; flex-direction:column; align-items:flex-end; gap:0.5rem; flex:1; min-width:0; position:relative; z-index:1; }

.box-num {
  font-size:2.1rem; font-weight:800; color:#0f172a; line-height:1;  /* ↑ plus grand */
  transition:color 0.3s ease, transform 0.3s ease;
}
.stat-box:hover .box-num { transform:scale(1.08); }
.box-insert:hover .box-num { color:#15803d; }
.box-update:hover .box-num { color:#92400e; }
.box-delete:hover .box-num { color:#991b1b; }
.box-total:hover  .box-num { color:#1d4ed8; }

.box-label {
  font-size:0.72rem; color:#94a3b8; font-weight:600;
  text-transform:uppercase; letter-spacing:0.05em; margin-top:2px;
  transition:color 0.3s ease;
}
.box-insert:hover .box-label { color:#16a34a; }
.box-update:hover .box-label { color:#d97706; }
.box-delete:hover .box-label { color:#dc2626; }
.box-total:hover  .box-label { color:#2563eb; }

.box-pill {
  font-size:0.63rem; font-weight:800; letter-spacing:0.07em;
  padding:0.2rem 0.65rem; border-radius:20px; white-space:nowrap;
  transition:transform 0.3s ease;
}
.stat-box:hover .box-pill { transform:scale(1.08); }
.pill-insert { background:#dcfce7; color:#166534; }
.pill-update { background:#fef9c3; color:#713f12; }
.pill-delete { background:#fee2e2; color:#991b1b; }
.pill-total  { background:#dbeafe; color:#1d4ed8; }

.box-bar { width:100%; height:5px; background:rgba(0,0,0,0.07); border-radius:99px; overflow:hidden; }
.box-bar-fill {
  height:100%; border-radius:99px;
  transition:width 0.6s cubic-bezier(.4,0,.2,1);
}
.fill-insert { background:linear-gradient(90deg,#16a34a,#4ade80); }
.fill-update { background:linear-gradient(90deg,#d97706,#fbbf24); }
.fill-delete { background:linear-gradient(90deg,#dc2626,#f87171); }
.fill-total  { background:linear-gradient(90deg,#2563eb,#60a5fa); }

/* TABLE CARD */
.table-card { background:white; border-radius:14px; box-shadow:0 2px 14px rgba(0,0,0,0.07); overflow:hidden; }

.table-toolbar {
  display:flex; align-items:center; justify-content:space-between;
  padding:0.65rem 1rem; border-bottom:1px solid #f0f4f8; gap:0.8rem; flex-wrap:wrap;
}
.search-box { position:relative; flex:1; max-width:260px; }
.search-icon { position:absolute; left:0.65rem; top:50%; transform:translateY(-50%); width:13px; height:13px; color:#a0aec0; }
.search-input {
  width:100%; padding:0.42rem 0.65rem 0.42rem 1.9rem;
  border:1.5px solid #e2e8f0; border-radius:8px;
  font-size:0.8rem; outline:none; font-family:inherit; transition:border-color 0.2s;
}
.search-input:focus { border-color:#2b6cb0; box-shadow:0 0 0 2px rgba(43,108,176,0.1); }

.filter-group { display:flex; gap:0.25rem; }
.filter-btn {
  display:flex; align-items:center; gap:0.35rem;
  padding:0.32rem 0.7rem; border:1.5px solid #e2e8f0;
  background:white; border-radius:7px; font-size:0.75rem; font-weight:700;
  cursor:pointer; color:#64748b; transition:all 0.15s; font-family:inherit;
}
.filter-btn:hover { border-color:#2b6cb0; color:#2b6cb0; background:#ebf4ff; }
.fbtn-dot { width:6px; height:6px; border-radius:50%; background:currentColor; flex-shrink:0; opacity:0.7; }
.fbtn-all.filter-active    { background:#1e3a5f; color:white; border-color:#1e3a5f; }
.fbtn-insert.filter-active { background:#dcfce7; color:#166534; border-color:#16a34a; }
.fbtn-update.filter-active { background:#fef9c3; color:#713f12; border-color:#d97706; }
.fbtn-delete.filter-active { background:#fee2e2; color:#991b1b; border-color:#dc2626; }

.state-box { display:flex; align-items:center; justify-content:center; gap:0.7rem; padding:2rem; color:#718096; font-size:0.85rem; }
.spinner { width:18px; height:18px; border:2.5px solid #e2e8f0; border-top-color:#2b6cb0; border-radius:50%; animation:spin .8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.alert-error { display:flex; align-items:center; gap:0.7rem; background:#fff5f5; color:#c53030; border:1.5px solid #feb2b2; padding:0.7rem 1rem; margin:0.75rem; border-radius:10px; font-size:0.84rem; }

.data-table { width:100%; border-collapse:collapse; }
.data-table thead th {
  padding:0.5rem 0.75rem; text-align:left;
  font-size:0.67rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em;
  color:#64748b; background:#f8fafc; border-bottom:1.5px solid #e2e8f0; white-space:nowrap;
}
.table-row:hover { background:#f8fafc; }
.data-table tbody td { padding:0.55rem 0.75rem; border-bottom:1px solid #f0f4f8; font-size:0.82rem; color:#2d3748; }
.data-table tbody tr:last-child td { border-bottom:none; }

.id-badge      { background:#f1f5f9; color:#64748b; padding:0.12rem 0.45rem; border-radius:5px; font-size:0.72rem; font-weight:700; border:1px solid #e2e8f0; }
.retrait-badge { background:#ede9fe; color:#5b21b6; padding:0.12rem 0.5rem; border-radius:6px; font-size:0.72rem; font-weight:700; }
.account-badge { background:#ebf4ff; color:#2b6cb0; padding:0.12rem 0.55rem; border-radius:6px; font-size:0.72rem; font-weight:700; font-family:monospace; }
.date-cell     { display:flex; align-items:center; gap:0.3rem; font-size:0.75rem; color:#64748b; white-space:nowrap; }
.client-cell   { display:flex; align-items:center; gap:0.45rem; }
.avatar        { width:24px; height:24px; border-radius:6px; background:linear-gradient(135deg,#667eea,#764ba2); color:white; font-weight:800; font-size:0.65rem; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.montant-old   { color:#94a3b8; font-size:0.78rem; }
.montant-new   { color:#2563eb; font-weight:700; font-size:0.8rem; }
.user-cell     { display:flex; align-items:center; gap:0.3rem; font-size:0.74rem; color:#94a3b8; font-family:monospace; }
.empty-row     { text-align:center; padding:2rem !important; color:#a0aec0; font-size:0.85rem; }

/* BOTTOM BAR */
.bottom-bar {
  display:flex; align-items:center; justify-content:space-between;
  padding:0.6rem 1rem; border-top:1px solid #f0f4f8;
  background:#fafbfc; gap:0.5rem; flex-wrap:wrap;
}
.sum-chips { display:flex; align-items:center; gap:0.45rem; flex-wrap:wrap; }
.sum-chip {
  display:inline-flex; align-items:center; gap:0.35rem;
  padding:0.25rem 0.7rem; border-radius:20px;
  font-weight:700; font-size:0.77rem; white-space:nowrap;
}
.chip-insert { background:#dcfce7; color:#166534; border:1px solid #bbf7d0; }
.chip-update { background:#fef9c3; color:#713f12; border:1px solid #fde68a; }
.chip-delete { background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }
.chip-total  { background:#dbeafe; color:#1d4ed8; border:1px solid #bfdbfe; }

.pag-right  { display:flex; align-items:center; gap:0.5rem; }
.pag-info   { font-size:0.78rem; color:#718096; white-space:nowrap; }
.pag-info strong { color:#2d3748; }
.pag-controls { display:flex; align-items:center; gap:0.2rem; }
.pag-btn {
  min-width:30px; height:30px; border:1.5px solid #e2e8f0; background:white;
  border-radius:7px; cursor:pointer; font-size:0.82rem; font-weight:700; color:#4a5568;
  display:flex; align-items:center; justify-content:center;
  transition:all 0.15s; font-family:inherit;
}
.pag-btn:hover:not(:disabled) { border-color:#2b6cb0; color:#2b6cb0; background:#ebf4ff; }
.pag-btn:disabled { opacity:0.3; cursor:not-allowed; }
.pag-active {
  background:linear-gradient(135deg,#1e3a5f,#2b6cb0) !important;
  border-color:#2b6cb0 !important; color:white !important;
  box-shadow:0 2px 8px rgba(43,108,176,0.3);
}
.pag-ellipsis { border:none; background:none; color:#a0aec0; cursor:default !important; min-width:20px; }
.pag-ellipsis:hover { background:none !important; border-color:transparent !important; color:#a0aec0 !important; }

@media (max-width:900px) { .stats-grid { grid-template-columns:repeat(2,1fr); } }
@media (max-width:540px) {
  .stats-grid { grid-template-columns:1fr 1fr; }
  .table-toolbar { flex-direction:column; align-items:flex-start; }
  .bottom-bar { flex-direction:column; align-items:flex-start; }
}
</style>