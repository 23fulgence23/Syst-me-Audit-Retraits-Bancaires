<template>
  <div id="app-wrapper">

    <!-- ═══════════ NAVBAR ═══════════ -->
    <nav class="navbar">

      <!-- BRAND / TITRE -->
      <div class="nav-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="width:22px;height:22px">
            <rect x="2" y="7" width="20" height="14" rx="2"/>
            <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
            <line x1="12" y1="12" x2="12" y2="16"/>
            <line x1="10" y1="14" x2="14" y2="14"/>
          </svg>
        </div>
        <div class="brand-text">
          <span class="brand-bank">Bank</span><span class="brand-audit">Audit</span>
          <span class="brand-dot">●</span>
        </div>
      </div>

      <!-- NAV LINKS -->
      <div class="nav-links">

        <!-- Clients -->
        <router-link to="/clients" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:17px;height:17px">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </div>
          <span>Clients</span>
          <div class="nav-underline"></div>
        </router-link>

        <!-- Retraits -->
        <router-link to="/retraits" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:17px;height:17px">
              <rect x="2" y="5" width="20" height="14" rx="3"/>
              <line x1="2" y1="10" x2="22" y2="10"/>
              <line x1="6" y1="15" x2="10" y2="15"/>
              <line x1="14" y1="15" x2="16" y2="15"/>
            </svg>
          </div>
          <span>Retraits</span>
          <div class="nav-underline"></div>
        </router-link>

        <!-- Audit -->
        <router-link to="/audit" class="nav-item">
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:17px;height:17px">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="16" y1="13" x2="8" y2="13"/>
              <line x1="16" y1="17" x2="8" y2="17"/>
              <polyline points="10 9 9 9 8 9"/>
            </svg>
          </div>
          <span>Audit</span>
          <div class="nav-underline"></div>
        </router-link>

      </div>
    </nav>

    <!-- PAGE CONTENT -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif;
  background: #f0f4f8;
  color: #2d3748;
}

#app-wrapper { min-height: 100vh; }

/* ══════════════════════════════════════
   NAVBAR
══════════════════════════════════════ */
.navbar {
  background: linear-gradient(135deg, #060e1f 0%, #0d2151 50%, #163a82 100%);
  color: white;
  padding: 0 2rem;
  height: 62px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(0,0,0,0.35);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

/* ── BRAND ── */
.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  text-decoration: none;
  user-select: none;
}

.brand-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  border-radius: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(99, 102, 241, 0.45);
  flex-shrink: 0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.nav-brand:hover .brand-icon {
  transform: rotate(-6deg) scale(1.08);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}

.brand-text {
  display: flex;
  align-items: baseline;
  gap: 0;
  line-height: 1;
}

/* "Bank" — blanc épais */
.brand-bank {
  font-size: 1.45rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.5px;
}

/* "Audit" — dégradé bleu→violet */
.brand-audit {
  font-size: 1.45rem;
  font-weight: 900;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Petit point décoratif animé */
.brand-dot {
  font-size: 0.45rem;
  color: #60a5fa;
  margin-left: 3px;
  margin-bottom: 6px;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1);   }
  50%       { opacity: 0.4; transform: scale(0.6); }
}

/* ── NAV LINKS ── */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  transition: all 0.2s ease;
  overflow: hidden;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.08);
  transition: all 0.25s ease;
  flex-shrink: 0;
}

/* Underline animé */
.nav-underline {
  position: absolute;
  bottom: 4px;
  left: 50%;
  transform: translateX(-50%) scaleX(0);
  width: 60%;
  height: 2px;
  border-radius: 99px;
  background: linear-gradient(90deg, #60a5fa, #a78bfa);
  transition: transform 0.25s cubic-bezier(.34,1.56,.64,1);
}

/* Hover */
.nav-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}
.nav-item:hover .nav-icon {
  background: rgba(96, 165, 250, 0.2);
  transform: translateY(-2px);
}
.nav-item:hover .nav-underline {
  transform: translateX(-50%) scaleX(1);
}

/* Active (route courante) */
.nav-item.router-link-active {
  color: white;
  background: rgba(255, 255, 255, 0.12);
}
.nav-item.router-link-active .nav-icon {
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  box-shadow: 0 3px 10px rgba(99,102,241,0.4);
}
.nav-item.router-link-active .nav-underline {
  transform: translateX(-50%) scaleX(1);
}

/* ══════════════════════════════════════
   MAIN CONTENT
══════════════════════════════════════ */
.main-content {
  padding: 1.8rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── SHARED STYLES (inchangés) ── */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  margin-bottom: 1.5rem;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.2rem;
}
.card-title { font-size: 1.2rem; font-weight: 700; color: #1a365d; }

table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
thead th {
  background: #ebf4ff; color: #2b6cb0; font-weight: 700;
  padding: 0.75rem 1rem; text-align: left; border-bottom: 2px solid #bee3f8;
}
tbody td { padding: 0.7rem 1rem; border-bottom: 1px solid #e2e8f0; }
tbody tr:hover { background: #f7fafc; }
tbody tr:last-child td { border-bottom: none; }

.btn {
  padding: 0.45rem 1rem; border: none; border-radius: 6px;
  cursor: pointer; font-size: 0.85rem; font-weight: 600; transition: all 0.2s;
}
.btn-primary { background: #2b6cb0; color: white; }
.btn-primary:hover { background: #2c5282; }
.btn-success { background: #38a169; color: white; }
.btn-success:hover { background: #276749; }
.btn-danger { background: #e53e3e; color: white; }
.btn-danger:hover { background: #c53030; }
.btn-warning { background: #d69e2e; color: white; }
.btn-warning:hover { background: #b7791f; }

.form-group { margin-bottom: 1rem; }
.form-group label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.85rem; color: #4a5568; }
.form-group input, .form-group select {
  width: 100%; padding: 0.6rem 0.8rem;
  border: 1.5px solid #e2e8f0; border-radius: 8px;
  font-size: 0.9rem; outline: none; transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus { border-color: #2b6cb0; }

.badge { padding: 0.25rem 0.6rem; border-radius: 20px; font-size: 0.78rem; font-weight: 700; }
.badge-insert { background: #c6f6d5; color: #276749; }
.badge-update { background: #fefcbf; color: #744210; }
.badge-delete { background: #fed7d7; color: #822727; }

.alert { padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.9rem; }
.alert-error { background: #fff5f5; color: #c53030; border: 1px solid #feb2b2; }
.alert-success { background: #f0fff4; color: #276749; border: 1px solid #9ae6b4; }

.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal {
  background: white; border-radius: 12px; padding: 2rem;
  width: 420px; max-width: 95vw; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.modal-title { font-size: 1.15rem; font-weight: 700; color: #1a365d; margin-bottom: 1.2rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.8rem; margin-top: 1.5rem; }
</style>