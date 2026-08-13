// ─── Config ───────────────────────────────────────────────────────────────────
// En producción (Railway) el frontend y el backend están en el mismo servidor
const API = window.location.hostname === 'localhost' ? 'http://localhost:8000' : window.location.origin;

// ─── Tab navigation ───────────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  event.target.classList.add('active');

  if (name === 'team') loadTeam();
  if (name === 'market') loadMarket();
}

// ─── Toast ────────────────────────────────────────────────────────────────────
function toast(msg, type = 'ok') {
  const el = document.getElementById('toast');
  el.textContent = (type === 'ok' ? '✅ ' : '❌ ') + msg;
  el.className = 'toast ' + type + ' show';
  setTimeout(() => el.classList.remove('show'), 3500);
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function fmtMoney(v) {
  if (!v) return '—';
  if (v >= 1000000) return (v / 1000000).toFixed(1) + 'M€';
  if (v >= 1000) return (v / 1000).toFixed(0) + 'K€';
  return v + '€';
}

function posLabel(p) {
  if (!p) return '?';
  const m = { 1: 'POR', 2: 'DEF', 3: 'MED', 4: 'DEL', por: 'POR', def: 'DEF', med: 'MED', del: 'DEL' };
  return m[String(p).toLowerCase()] || String(p).toUpperCase().substring(0, 3);
}

function urgencyBadge(u) {
  if (!u) return '';
  const map = { alta: 'br', media: 'by', baja: 'bb' };
  return `<span class="badge ${map[u] || 'bb'}">${u}</span>`;
}

function alertIcon(tipo) {
  const m = { lesion: '🤕', sancion: '🟥', precio: '📈', rendimiento: '⬇️' };
  return m[tipo] || '⚠️';
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
async function loadDashboard() {
  show('dload'); hide('dcont'); hide('derr');
  try {
    const data = await api('/api/team');
    hide('dload');

    const team = data.team || {};
    const round = data.current_round || {};

    // Stats
    const stats = [
      { v: team.points || team.totalPoints || '—', l: 'Puntos totales' },
      { v: fmtMoney(team.budget || team.money), l: 'Presupuesto' },
      { v: fmtMoney(team.teamValue || team.value), l: 'Valor plantilla' },
      { v: (team.players || team.squad || []).length || '—', l: 'Jugadores' }
    ];
    document.getElementById('sgrid').innerHTML = stats.map(s =>
      `<div class="sbox"><div class="sv">${s.v}</div><div class="sl">${s.l}</div></div>`
    ).join('');

    // Jornada
    const rinfo = document.getElementById('rinfo');
    if (round.round || round.id) {
      rinfo.innerHTML = `<strong>Jornada ${round.round || round.id}</strong> · Estado: ${round.status || round.state || '?'}`;
    } else {
      rinfo.textContent = 'No disponible';
    }

    show('dcont');
  } catch (e) {
    hide('dload');
    document.getElementById('derrmsg').textContent = 'No se pudo conectar con el servidor. ¿Está ejecutándose el backend?';
    show('derr');
  }
}

// ─── AI Analysis ─────────────────────────────────────────────────────────────
async function runAnalysis() {
  const btn = document.getElementById('btnA');
  btn.disabled = true;
  btn.textContent = '⏳ Analizando...';
  show('aload');
  document.getElementById('acont').innerHTML = '';
  document.getElementById('ats').textContent = '';

  try {
    const result = await api('/api/analyze');
    hide('aload');

    if (!result.success) {
      document.getElementById('acont').innerHTML = `<div class="es"><div class="ei">❌</div><p>${result.error || 'Error al analizar'}</p></div>`;
      return;
    }

    const a = result.analysis || {};
    let html = '';

    // Situación general
    if (a.resumen_situacion) {
      html += `<div class="tbox"><div class="tl">📊 Situación actual</div><p>${a.resumen_situacion}</p></div>`;
    }

    // Consejo experto
    if (a.consejo_experto) {
      html += `<div class="tbox"><div class="tl">💡 Consejo del experto</div><p>${a.consejo_experto}</p></div>`;
    }

    html += '<div class="agrid">';

    // Alineación óptima
    if (a.alineacion_optima) {
      const al = a.alineacion_optima;
      html += `<div class="card"><div class="ctitle">📋 Alineación óptima</div>`;
      if (al.formacion) html += `<p style="font-size:12px;color:var(--t2);margin-bottom:10px">Formación: <strong>${al.formacion}</strong></p>`;
      if (al.capitan) {
        html += `<div class="lp"><span>👑 Capitán</span><span style="font-weight:600;color:var(--y)">${al.capitan.nombre}</span></div>`;
      }
      (al.titulares || []).forEach(p => {
        const pos = p.posicion || '?';
        html += `<div class="lp"><div style="display:flex;align-items:center;gap:8px"><div class="pp ${pos}">${pos}</div><span style="font-size:13px">${p.nombre}</span></div><span class="badge bg">Titular</span></div>`;
      });
      (al.suplentes || []).forEach(p => {
        html += `<div class="lp"><div style="display:flex;align-items:center;gap:8px"><div class="pp">?</div><span style="font-size:13px">${p.nombre}</span></div><span class="badge bb">Suplente</span></div>`;
      });
      html += `</div>`;
    }

    // Mercado recomendaciones
    if (a.mercado) {
      html += `<div>`;
      if ((a.mercado.vender || []).length > 0) {
        html += `<div class="card"><div class="ctitle">📤 Vender</div>`;
        a.mercado.vender.forEach(p => {
          html += `<div class="ri"><div class="rco">🔴</div><div><div class="rn">${p.nombre} ${urgencyBadge(p.urgencia)}</div><div class="rr">${p.razon}</div>${p.precio_recomendado ? `<div class="rp">Precio: ${fmtMoney(p.precio_recomendado)}</div>` : ''}</div></div>`;
        });
        html += `</div>`;
      }
      if ((a.mercado.fichar || []).length > 0) {
        html += `<div class="card"><div class="ctitle">📥 Fichar</div>`;
        a.mercado.fichar.forEach(p => {
          html += `<div class="ri"><div class="rco">🟢</div><div><div class="rn">${p.nombre} ${urgencyBadge(p.prioridad)}</div><div class="rr">${p.razon}</div>${p.precio_estimado ? `<div class="rp">Precio est.: ${fmtMoney(p.precio_estimado)}</div>` : ''}</div></div>`;
        });
        html += `</div>`;
      }
      html += `</div>`;
    }

    html += '</div>'; // end agrid

    // Estrategia jornada
    if (a.estrategia_jornada) {
      html += `<div class="card"><div class="ctitle">🎯 Estrategia de jornada</div><p style="font-size:13px;line-height:1.6">${a.estrategia_jornada}</p>`;
      if (a.puntuacion_estimada) html += `<p style="margin-top:10px;font-size:12px;color:var(--t2)">Puntuación estimada: <strong>${a.puntuacion_estimada}</strong></p>`;
      html += `</div>`;
    }

    // Alertas
    if ((a.alertas || []).length > 0) {
      html += `<div class="card"><div class="ctitle">⚠️ Alertas</div>`;
      a.alertas.forEach(al => {
        html += `<div class="ai"><div class="aico">${alertIcon(al.tipo)}</div><div class="atx"><div class="ath">${al.jugador}</div>${al.mensaje}</div></div>`;
      });
      html += `</div>`;
    }

    // Texto libre si no hay JSON estructurado
    if (a.texto_libre) {
      html += `<div class="card"><div class="ctitle">🤖 Análisis IA</div><p style="font-size:13px;line-height:1.7;white-space:pre-wrap">${a.texto_libre}</p></div>`;
    }

    document.getElementById('acont').innerHTML = html || '<div class="es"><div class="ei">🤔</div><p>No se obtuvieron recomendaciones</p></div>';
    document.getElementById('ats').textContent = 'Último análisis: ' + new Date().toLocaleTimeString('es-ES');

    // También actualizar alertas en dashboard
    if ((a.alertas || []).length > 0) renderAlerts(a.alertas);

  } catch (e) {
    hide('aload');
    document.getElementById('acont').innerHTML = `<div class="es"><div class="ei">❌</div><p>Error: ${e.message}</p></div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = '🤖 Analizar equipo';
  }
}

function renderAlerts(alertas) {
  const el = document.getElementById('alerts');
  if (!el) return;
  el.innerHTML = alertas.map(a =>
    `<div class="ai"><div class="aico">${alertIcon(a.tipo)}</div><div class="atx"><div class="ath">${a.jugador}</div>${a.mensaje}</div></div>`
  ).join('');
}

// ─── Team ─────────────────────────────────────────────────────────────────────
async function loadTeam() {
  show('tload'); hide('tcont');
  try {
    const data = await api('/api/team');
    hide('tload');
    const team = data.team || {};
    const players = team.players || team.squad || team.lineup || [];

    if (team.name || team.teamName) {
      document.getElementById('ttitle').textContent = '⚽ ' + (team.name || team.teamName);
    }

    if (!players.length) {
      document.getElementById('tplayers').innerHTML = '<p style="color:var(--t2);font-size:13px">No se encontraron jugadores. Verifica la conexión con LaLiga Fantasy.</p>';
    } else {
      document.getElementById('tplayers').innerHTML = players.map(p => {
        const pl = p.player || p;
        const pos = posLabel(pl.position || pl.positionId);
        const name = pl.name || pl.playerName || '?';
        const pts = pl.points || pl.totalPoints || 0;
        const price = fmtMoney(pl.marketValue || pl.price);
        const status = pl.status || pl.playerStatus || '';
        const statusBadge = status && status !== 'ok' ? `<span class="badge br">${status}</span>` : '';
        return `<div class="pi">
          <div class="pl">
            <div class="pp ${pos}">${pos}</div>
            <div><div class="pn">${name} ${statusBadge}</div><div class="pm">${pts} pts · ${price}</div></div>
          </div>
          <button class="btn bs bsm" onclick="analyzePlayer('${name}')">Analizar</button>
        </div>`;
      }).join('');
    }
    show('tcont');
  } catch (e) {
    hide('tload');
    document.getElementById('tcont').innerHTML = `<div class="es"><div class="ei">❌</div><p>${e.message}</p></div>`;
    show('tcont');
  }
}

// ─── Market ───────────────────────────────────────────────────────────────────
async function loadMarket() {
  show('mload'); hide('mcont');
  try {
    const data = await api('/api/market');
    hide('mload');
    const players = data.players_stats || [];

    if (!players.length) {
      document.getElementById('mplayers').innerHTML = '<p style="color:var(--t2);font-size:13px">No se encontraron datos de mercado.</p>';
    } else {
      document.getElementById('mplayers').innerHTML = players.slice(0, 30).map(p => {
        const name = p.name || p.playerName || p.nickname || '?';
        const pos = posLabel(p.position || p.positionId);
        const price = fmtMoney(p.marketValue || p.price || p.value);
        const pts = p.points || p.totalPoints || p.fantasyPoints || 0;
        const trend = p.marketValueChange > 0 ? '📈' : p.marketValueChange < 0 ? '📉' : '➡️';
        return `<div class="pi">
          <div class="pl">
            <div class="pp ${pos}">${pos}</div>
            <div><div class="pn">${name}</div><div class="pm">${pts} pts · ${price} ${trend}</div></div>
          </div>
          <button class="btn bs bsm" onclick="analyzePlayer('${name}')">Analizar</button>
        </div>`;
      }).join('');
    }
    show('mcont');
  } catch (e) {
    hide('mload');
    show('mcont');
  }
}

// ─── Player analysis ──────────────────────────────────────────────────────────
async function analyzePlayer(name) {
  try {
    toast('Analizando a ' + name + '...');
    const result = await fetch(`${API}/api/player/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player_name: name })
    });
    const data = await result.json();
    if (data.success && data.analysis) {
      const a = data.analysis;
      const recMap = { comprar: '🟢', mantener: '🟡', vender: '🔴' };
      const icon = recMap[a.recomendacion] || '⚪';
      alert(`${icon} ${a.jugador}\n\nRecomendación: ${a.recomendacion?.toUpperCase()}\nForma: ${a.forma_actual}\nRival: ${a.proximo_rival} (dificultad ${a.dificultad_rival})\nTendencia precio: ${a.tendencia_precio}\n\n${a.razon_detallada}`);
    }
  } catch (e) {
    toast('Error al analizar jugador', 'err');
  }
}

// ─── Chat ─────────────────────────────────────────────────────────────────────
async function sendChat() {
  const input = document.getElementById('cinput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  addChatMsg(msg, 'user');
  const btn = document.getElementById('btnChat');
  btn.disabled = true;
  addChatMsg('...', 'ai', 'typing');
  try {
    const result = await fetch(`${API}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, include_team_context: true })
    });
    const data = await result.json();
    removeTyping();
    addChatMsg(data.response || 'Sin respuesta', 'ai');
  } catch (e) {
    removeTyping();
    addChatMsg('Error de conexión. ¿Está el servidor activo?', 'ai');
  } finally {
    btn.disabled = false;
  }
}

function quickChat(msg) {
  document.getElementById('cinput').value = msg;
  sendChat();
}

function addChatMsg(text, who, id) {
  const box = document.getElementById('cmsgs');
  const div = document.createElement('div');
  div.className = `msg ${who === 'user' ? 'mu' : 'ma'}`;
  if (id) div.id = id;
  div.innerHTML = `<div class="mb">${text}</div>`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

// ─── Refresh & utils ──────────────────────────────────────────────────────────
async function refreshData() {
  toast('Actualizando datos...');
  await fetch(`${API}/api/cache`, { method: 'DELETE' });
  loadDashboard();
  toast('Datos actualizados');
}

async function api(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function show(id) { const el = document.getElementById(id); if (el) el.style.display = 'flex'; }
function hide(id) { const el = document.getElementById(id); if (el) el.style.display = 'none'; }

// ─── Token LaLiga Fantasy ──────────────────────────────────────────────────────
async function saveToken() {
  const token = document.getElementById('token-input').value.trim();
  const userId = document.getElementById('userid-input').value.trim();
  if (!token) { toast('Pega el token primero', 'err'); return; }

  try {
    const btn = document.querySelector('#token-modal .bp');
    btn.disabled = true;
    btn.textContent = 'Guardando...';

    const res = await fetch(`${API}/api/token/set`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, user_id: userId })
    });
    const data = await res.json();

    if (data.success) {
      document.getElementById('token-modal').style.display = 'none';
      // Actualizar botón del header
      const btnC = document.getElementById('btn-connect');
      if (btnC) { btnC.textContent = '✅ Conectado'; btnC.style.borderColor = 'var(--p)'; btnC.style.color = 'var(--p)'; }
      toast('¡Cuenta conectada! Cargando tu equipo...');
      // Recargar datos
      await refreshData();
      loadDashboard();
    } else {
      toast('Error: ' + (data.error || 'No se pudo guardar'), 'err');
    }
  } catch (e) {
    toast('Error de conexión: ' + e.message, 'err');
  } finally {
    const btn = document.querySelector('#token-modal .bp');
    if (btn) { btn.disabled = false; btn.textContent = 'Guardar y conectar'; }
  }
}

async function checkTokenStatus() {
  try {
    const data = await api('/api/token/status');
    const btnC = document.getElementById('btn-connect');
    if (data.has_token && btnC) {
      btnC.textContent = '✅ Conectado';
      btnC.style.borderColor = 'var(--p)';
      btnC.style.color = 'var(--p)';
    }
  } catch (e) {}
}

// ─── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  loadDashboard();
  checkTokenStatus();
  // Registrar Service Worker para PWA
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/app/sw.js')
      .then(() => console.log('✅ Service Worker registrado'))
      .catch(e => console.log('SW error:', e));
  }
});
