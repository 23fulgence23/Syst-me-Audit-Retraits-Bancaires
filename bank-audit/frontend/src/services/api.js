import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
})

// ── Clients ──────────────────────────────────────────
export const clientService = {
  getAll:  ()           => api.get('/clients'),
  getOne:  (n_compte)   => api.get(`/clients/${n_compte}`),
  create:  (data)       => api.post('/clients', data),
  update:  (n_compte, data) => api.put(`/clients/${n_compte}`, data),
  delete:  (n_compte)   => api.delete(`/clients/${n_compte}`)
}

// ── Retraits ─────────────────────────────────────────
export const retraitService = {
  getAll:  ()           => api.get('/retraits'),
  create:  (data)       => api.post('/retraits', data),
  update:  (id, data)   => api.put(`/retraits/${id}`, data),
  delete:  (id)         => api.delete(`/retraits/${id}`)
}

// ── Audit ─────────────────────────────────────────────
export const auditService = {
  getAll: () => api.get('/audit')
}