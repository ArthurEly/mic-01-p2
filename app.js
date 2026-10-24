// ============================================================================
// MIC 01 - Física de Dispositivos Semicondutores
// Simulador Interativo em JavaScript (HTML5 Canvas a 60 FPS)
// ============================================================================

// Navegação entre abas principais
function switchMainTab(tabId, btnEl) {
  document.querySelectorAll('.tab-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  const target = document.getElementById(tabId);
  if (target) target.classList.add('active');
  if (btnEl) btnEl.classList.add('active');
}

// Navegação entre os 4 Simuladores JS
let activeSimIndex = 1;
function switchSimTab(index, btnEl) {
  activeSimIndex = index;
  document.querySelectorAll('.sim-panel').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.sim-tab-btn').forEach(el => el.classList.remove('active'));
  const panel = document.getElementById('sim-panel-' + index);
  if (panel) panel.classList.add('active');
  if (btnEl) btnEl.classList.add('active');
}

// Atalho dos botões "Carregar no Simulador Interativo" dentro das resoluções das Listas 2 e 3
function jumpToPreset(simIdx, presetName) {
  const mainSimBtn = document.querySelector('.tab-btn[data-tab="tab-simuladores"]');
  switchMainTab('tab-simuladores', mainSimBtn);
  const simBtn = document.querySelector(`.sim-tab-btn[data-sim="${simIdx}"]`);
  switchSimTab(simIdx, simBtn);
  applyPreset(presetName);
  window.scrollTo({ top: 180, behavior: 'smooth' });
}

// ============================================================================
// ESTADO GLOBAL DOS 4 SIMULADORES E PARTÍCULAS ANIMADAS
// ============================================================================
const q_el = 1.6e-19;
const k_eV = 8.62e-5;
const eps_0_cm = 8.854e-14; // F/cm

// Partículas para animação de portadores (Simulador 1, 3 e 4)
const particlesPN = [];
for (let i = 0; i < 70; i++) {
  particlesPN.push({
    x: Math.random(),
    y: Math.random(),
    vx: (Math.random() - 0.5) * 0.006,
    vy: (Math.random() - 0.5) * 0.006,
    type: i < 35 ? 'hole' : 'elec'
  });
}

const particlesSchottky = [];
for (let i = 0; i < 45; i++) {
  particlesSchottky.push({
    x: Math.random(),
    y: Math.random(),
    speed: 0.004 + Math.random() * 0.006,
    energy: Math.random()
  });
}

const particlesMOS = [];
for (let i = 0; i < 80; i++) {
  particlesMOS.push({
    x: Math.random(),
    y: Math.random(),
    phase: Math.random() * Math.PI * 2,
    kind: i < 50 ? 'maj' : 'min'
  });
}

// Presets exatos das Questões da Lista 2 e Lista 3
function applyPreset(name) {
  if (name === 'L2Q1') {
    // Ge: ND = 1.74e15, NA = 3.68e16, ni = 2.5e13, Va = 0
    document.getElementById('s1-mat').value = 'Ge';
    document.getElementById('s1-logNA').value = Math.log10(3.6765e16).toFixed(2);
    document.getElementById('s1-logND').value = Math.log10(1.7361e15).toFixed(2);
    document.getElementById('s1-Va').value = 0.0;
  } else if (name === 'L2Q2d') {
    // Si n+p: ND = 1e18, NA = 1e16, Va = -0.5 V
    document.getElementById('s1-mat').value = 'Si';
    document.getElementById('s1-logNA').value = 16.0;
    document.getElementById('s1-logND').value = 18.0;
    document.getElementById('s1-Va').value = -0.50;
  } else if (name === 'L2Q3_eq') {
    // Questão 3 no equilíbrio: Vbi = 0.80 V, Va = 0 V -> Emax = -16 kV/cm, W = 1.0 um
    document.getElementById('s1-mat').value = 'Q3';
    document.getElementById('s1-Va').value = 0.0;
  } else if (name === 'L2Q3_bias') {
    // Questão 3 polarizado: Va = +0.60 V -> Emax = -8 kV/cm, W = 0.5 um
    document.getElementById('s1-mat').value = 'Q3';
    document.getElementById('s1-Va').value = 0.60;
  } else if (name === 'L2Q2_dir') {
    document.getElementById('s2-Va').value = 0.50;
    document.getElementById('s2-Va-cap').value = -0.55;
  } else if (name === 'L2Q2_rev') {
    document.getElementById('s2-Va').value = -0.50;
    document.getElementById('s2-Va-cap').value = -0.50;
  } else if (name === 'L2Q4_p1') {
    document.getElementById('s2-Va-cap').value = -4.30;
  } else if (name === 'L2Q4_p2') {
    document.getElementById('s2-Va-cap').value = -0.55;
  } else if (name === 'L3Q1_ini') {
    document.getElementById('s3-metal').value = 'Q12';
    document.getElementById('s3-ND').value = 15.0; // 10^15
    document.getElementById('s3-Va').value = 0.0;
    document.getElementById('s3-T').value = 300;
  } else if (name === 'L3Q1_fim') {
    document.getElementById('s3-metal').value = 'Q12';
    document.getElementById('s3-ND').value = Math.log10(4.8e15).toFixed(2); // 4.8x10^15
    document.getElementById('s3-Va').value = 0.0;
    document.getElementById('s3-T').value = 300;
  } else if (name === 'L3Q2a') {
    document.getElementById('s3-metal').value = 'Q12';
    document.getElementById('s3-ND').value = 15.0;
    document.getElementById('s3-Va').value = 0.20;
    document.getElementById('s3-T').value = 300;
  } else if (name === 'L3Q2b') {
    document.getElementById('s3-metal').value = 'Q12';
    document.getElementById('s3-ND').value = 15.0;
    document.getElementById('s3-Va').value = -5.00;
    document.getElementById('s3-T').value = 300;
  } else if (name === 'L3Q3_300') {
    document.getElementById('s3-metal').value = 'Cr';
    document.getElementById('s3-ND').value = 15.5;
    document.getElementById('s3-Va').value = 0.20;
    document.getElementById('s3-T').value = 300;
  } else if (name === 'L3Q3_358') {
    document.getElementById('s3-metal').value = 'Cr';
    document.getElementById('s3-ND').value = 15.5;
    document.getElementById('s3-Va').value = 0.141;
    document.getElementById('s3-T').value = 358;
  } else if (name === 'L3Q4') {
    document.getElementById('s4-sub').value = 'N';
    document.getElementById('s4-gate').value = 'Custom_VFB_minus1';
    document.getElementById('s4-VG').value = 0.0;
    document.getElementById('s4-tox').value = 5.0;
    document.getElementById('s4-logN').value = 16.0;
  } else if (name === 'L3Q5') {
    document.getElementById('s4-sub').value = 'P';
    document.getElementById('s4-gate').value = 'P+Si';
    document.getElementById('s4-VG').value = 0.0;
    document.getElementById('s4-tox').value = 15.0;
    document.getElementById('s4-logN').value = 16.0;
  } else if (name === 'L3Q6') {
    document.getElementById('s4-sub').value = 'P';
    document.getElementById('s4-gate').value = 'Q6_VT025';
    document.getElementById('s4-VG').value = 5.0;
    document.getElementById('s4-tox').value = 15.0;
    document.getElementById('s4-logN').value = 16.0;
  } else if (name === 'L3Q7_acc') {
    document.getElementById('s4-sub').value = 'P';
    document.getElementById('s4-gate').value = 'N+Si';
    document.getElementById('s4-VG').value = -2.0;
    document.getElementById('s4-tox').value = 3.84;
    document.getElementById('s4-logN').value = 17.0;
  } else if (name === 'L3Q7_inv') {
    document.getElementById('s4-sub').value = 'P';
    document.getElementById('s4-gate').value = 'N+Si';
    document.getElementById('s4-VG').value = 2.0;
    document.getElementById('s4-tox').value = 3.84;
    document.getElementById('s4-logN').value = 17.0;
  }
}

// ============================================================================
// SIMULADOR 1: JUNÇÃO PN & ELETROSTÁTICA (Aulas 8–10 | Lista 2 Q1, Q2d, Q3)
// ============================================================================
function renderSim1(ctx, W, H, time) {
  ctx.clearRect(0, 0, W, H);

  const mat = document.getElementById('s1-mat').value;
  const logNA = parseFloat(document.getElementById('s1-logNA').value);
  const logND = parseFloat(document.getElementById('s1-logND').value);
  const Va = parseFloat(document.getElementById('s1-Va').value);

  const NA = Math.pow(10, logNA);
  const ND = Math.pow(10, logND);

  document.getElementById('s1-logNA-val').textContent = `10^${logNA.toFixed(2)} cm⁻³`;
  document.getElementById('s1-logND-val').textContent = `10^${logND.toFixed(2)} cm⁻³`;
  document.getElementById('s1-Va-val').textContent = `${Va >= 0 ? '+' : ''}${Va.toFixed(2)} V`;

  const Vt = 0.02586; // kT/q a 300 K
  let ni = 1.0e10;
  let eps_r = 11.7;
  if (mat === 'Ge') {
    ni = 2.5e13;
    eps_r = 16.0;
  }

  let Vbi, Vj, W_um, xn_um, xp_um, Emax_kVcm;
  if (mat === 'Q3') {
    // Modo exato da Questão 3 da Lista 2 (Vbi = 0.80 V, W0 = 1.0 um, Emax0 = -16 kV/cm)
    Vbi = 0.80;
    Vj = Math.max(Vbi - Va, 0.02);
    const scale = Math.sqrt(Vj / Vbi);
    W_um = 1.0 * scale;
    xn_um = 0.96 * scale;
    xp_um = 0.04 * scale;
    Emax_kVcm = -16.0 * scale;
  } else {
    Vbi = Vt * Math.log((NA * ND) / (ni * ni));
    Vj = Math.max(Vbi - Va, 0.02);
    const eps_s = eps_r * eps_0_cm;
    const W_cm = Math.sqrt(((2 * eps_s) / q_el) * ((NA + ND) / (NA * ND)) * Vj);
    W_um = W_cm * 1e4;
    xp_um = W_um * (ND / (NA + ND));
    xn_um = W_um * (NA / (NA + ND));
    Emax_kVcm = -((q_el * ND * (xn_um * 1e-4)) / eps_s) * 1e-3;
  }

  // Atualiza cartões numéricos
  document.getElementById('r1-Vbi').textContent = `${Vbi.toFixed(4)} V`;
  document.getElementById('r1-Vj').textContent = `${Vj.toFixed(4)} V`;
  document.getElementById('r1-W').textContent = `${W_um.toFixed(4)} µm`;
  document.getElementById('r1-Emax').textContent = `${Emax_kVcm.toFixed(2)} kV/cm`;

  // Layout em 3 zonas: Topo = Estrutura Física Animada | Meio Esq = Campo Elétrico E(x) | Meio Dir = Bandas E(x)
  const pad = 35;
  const topH = 155;
  const botY = topH + 35;
  const botH = H - botY - 35;
  const halfW = (W - pad * 3) / 2;

  // 1) Desenha o bloco físico da Junção P-N com depleção e partículas móveis
  const bx = pad, by = 22, bw = W - pad * 2, bh = topH - 30;
  const midX = bx + bw * 0.45; // posição da junção metalúrgica x=0

  // Escala visual da zona de depleção no desenho
  const visScale = mat === 'Q3' ? 140 : Math.min(220, Math.max(45, W_um * 220));
  const fracP = Math.max(0.12, xp_um / (xp_um + xn_um));
  const fracN = 1.0 - fracP;
  const depLeft = Math.max(bx + 30, midX - visScale * fracP);
  const depRight = Math.min(bx + bw - 30, midX + visScale * fracN);

  // Lado P neutro
  ctx.fillStyle = '#1e3a8a';
  ctx.fillRect(bx, by, midX - bx, bh);
  // Lado N neutro
  ctx.fillStyle = '#7f1d1d';
  ctx.fillRect(midX, by, bx + bw - midX, bh);
  // Zona de depleção
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(depLeft, by, depRight - depLeft, bh);
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2;
  ctx.strokeRect(bx, by, bw, bh);

  // Linha tracejada da junção x=0 e bordas -xp, +xn
  ctx.setLineDash([5, 4]);
  ctx.strokeStyle = '#94a3b8';
  ctx.beginPath();
  ctx.moveTo(midX, by); ctx.lineTo(midX, by + bh);
  ctx.moveTo(depLeft, by); ctx.lineTo(depLeft, by + bh);
  ctx.moveTo(depRight, by); ctx.lineTo(depRight, by + bh);
  ctx.stroke();
  ctx.setLineDash([]);

  // Íons fixos na zona de depleção (- no lado P, + no lado N)
  ctx.font = 'bold 13px monospace';
  ctx.textAlign = 'center';
  for (let x = depLeft + 12; x < midX - 6; x += 22) {
    for (let y = by + 22; y < by + bh - 10; y += 26) {
      ctx.fillStyle = '#60a5fa';
      ctx.fillText('⊖', x, y);
    }
  }
  for (let x = midX + 12; x < depRight - 6; x += 22) {
    for (let y = by + 22; y < by + bh - 10; y += 26) {
      ctx.fillStyle = '#f87171';
      ctx.fillText('⊕', x, y);
    }
  }

  // Seta do Campo Elétrico Interno (aponta do lado N(+) para o lado P(-), sentido -x!)
  const arrowY = by + bh / 2;
  ctx.strokeStyle = '#facc15';
  ctx.fillStyle = '#facc15';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(depRight - 15, arrowY);
  ctx.lineTo(depLeft + 15, arrowY);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(depLeft + 15, arrowY);
  ctx.lineTo(depLeft + 26, arrowY - 6);
  ctx.lineTo(depLeft + 26, arrowY + 6);
  ctx.closePath();
  ctx.fill();
  ctx.font = 'bold 12px Inter, sans-serif';
  ctx.fillText(`Campo Elétrico ξ (N → P): E_max = ${Emax_kVcm.toFixed(1)} kV/cm`, (depLeft + depRight) / 2, arrowY - 10);

  // Animação das partículas (lacunas e elétrons móveis)
  const injectionBoost = Va > 0 ? Math.min(1, Va / 0.6) : 0;
  particlesPN.forEach(p => {
    p.x += p.vx * (1 + injectionBoost * 1.5);
    p.y += p.vy;
    if (p.y < 0.08 || p.y > 0.92) p.vy *= -1;

    if (p.type === 'hole') {
      // Lacunas no lado P (e injetadas no lado N se Va > 0)
      const maxX = Va > 0.1 ? 0.45 + 0.35 * injectionBoost : (depLeft - bx) / bw;
      if (p.x < 0.02) { p.x = 0.02; p.vx = Math.abs(p.vx); }
      if (p.x > maxX) { p.x = maxX; p.vx = -Math.abs(p.vx); }
      const px = bx + p.x * bw;
      const py = by + p.y * bh;
      ctx.fillStyle = '#f43f5e';
      ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI * 2); ctx.fill();
    } else {
      // Elétrons no lado N (e injetados no lado P se Va > 0)
      const minX = Va > 0.1 ? 0.45 - 0.35 * injectionBoost : (depRight - bx) / bw;
      if (p.x < minX) { p.x = minX; p.vx = Math.abs(p.vx); }
      if (p.x > 0.98) { p.x = 0.98; p.vx = -Math.abs(p.vx); }
      const px = bx + p.x * bw;
      const py = by + p.y * bh;
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI * 2); ctx.fill();
    }
  });

  // Rótulos da estrutura
  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 13px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('Região Tipo P (Lacunas + Íons Aceitadores ⊖)', bx + 10, by + 18);
  ctx.textAlign = 'right';
  ctx.fillText('Região Tipo N (Elétrons + Íons Doadores ⊕)', bx + bw - 10, by + 18);
  ctx.textAlign = 'center';
  ctx.fillStyle = '#38bdf8';
  ctx.fillText(`Zona de Depleção W = ${W_um.toFixed(3)} µm`, (depLeft + depRight) / 2, by + bh + 16);

  // 2) Gráfico Inferior Esquerdo: Perfil de Campo Elétrico E(x) e Área do Triângulo (Questão 3!)
  const g1x = pad, g1y = botY, g1w = halfW, g1h = botH;
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.lineWidth = 1;
  ctx.fillRect(g1x, g1y, g1w, g1h);
  ctx.strokeRect(g1x, g1y, g1w, g1h);

  const axisY = g1y + 38;
  const juncX1 = g1x + g1w * 0.38;
  ctx.strokeStyle = '#64748b';
  ctx.beginPath();
  ctx.moveTo(g1x + 15, axisY); ctx.lineTo(g1x + g1w - 15, axisY);
  ctx.moveTo(juncX1, g1y + 15); ctx.lineTo(juncX1, g1y + g1h - 15);
  ctx.stroke();

  // Triângulo de equilíbrio (sombra tracejada) vs Triângulo atual
  const scaleX1 = (g1w * 0.45);
  const peakH = Math.min(g1h - 65, Math.max(25, (Math.abs(Emax_kVcm) / 22.0) * (g1h - 65)));
  const xLeft1 = juncX1 - scaleX1 * fracP * Math.sqrt(Vj / Vbi) * 0.7;
  const xRight1 = juncX1 + scaleX1 * fracN * Math.sqrt(Vj / Vbi) * 0.7;

  // Triângulo preenchido
  ctx.fillStyle = 'rgba(244, 63, 94, 0.32)';
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(xLeft1, axisY);
  ctx.lineTo(juncX1, axisY + peakH);
  ctx.lineTo(xRight1, axisY);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 12.5px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('Perfil de Campo Elétrico ξ(x) [Aula 9 & Lista 2 Q3]', g1x + 12, g1y + 20);
  ctx.fillStyle = '#facc15';
  ctx.font = '12px monospace';
  ctx.fillText(`ξ_max = ${Emax_kVcm.toFixed(2)} kV/cm`, juncX1 + 10, axisY + peakH - 5);
  ctx.fillStyle = '#34d399';
  ctx.fillText(`Área = -∫ξ dx = V_bi - V_a = ${Vj.toFixed(3)} V`, g1x + 16, g1y + g1h - 14);

  // 3) Gráfico Inferior Direito: Diagrama de Bandas de Energia (EC, Ei, EFp, EFn, EV)
  const g2x = pad * 2 + halfW, g2y = botY, g2w = halfW, g2h = botH;
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.fillRect(g2x, g2y, g2w, g2h);
  ctx.strokeRect(g2x, g2y, g2w, g2h);

  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 12.5px Inter, sans-serif';
  ctx.fillText('Diagrama de Bandas e Barreira q(V_bi - V_a) [Aulas 9–10]', g2x + 12, g2y + 20);

  const bTopP = g2y + 52;
  const dropPx = Math.min(85, Math.max(12, Vj * 52));
  const gapPx = 68;
  const juncX2 = g2x + g2w * 0.45;
  const wPx = Math.min(g2w * 0.35, Math.max(25, 70 * Math.sqrt(Vj / Vbi)));

  function drawBandCurve(yStart, yEnd, color, dashed = false) {
    ctx.strokeStyle = color;
    ctx.lineWidth = dashed ? 1.5 : 2.5;
    if (dashed) ctx.setLineDash([4, 4]);
    ctx.beginPath();
    for (let i = 0; i <= 100; i++) {
      const t = i / 100;
      const px = g2x + 20 + t * (g2w - 40);
      let s = 0;
      if (px < juncX2 - wPx) s = 0;
      else if (px > juncX2 + wPx) s = 1;
      else {
        const u = (px - (juncX2 - wPx)) / (2 * wPx);
        s = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
      }
      const py = yStart + s * (yEnd - yStart);
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.stroke();
    ctx.setLineDash([]);
  }

  drawBandCurve(bTopP, bTopP + dropPx, '#38bdf8', false); // EC
  drawBandCurve(bTopP + gapPx / 2, bTopP + dropPx + gapPx / 2, '#94a3b8', true); // Ei
  drawBandCurve(bTopP + gapPx, bTopP + dropPx + gapPx, '#f472b6', false); // EV

  // Quasi-Fermi levels EFp e EFn
  const EFp_y = bTopP + gapPx - 12;
  const EFn_y = bTopP + dropPx + 14;
  ctx.strokeStyle = '#facc15';
  ctx.lineWidth = 2;
  ctx.setLineDash([6, 3]);
  ctx.beginPath();
  ctx.moveTo(g2x + 20, EFp_y); ctx.lineTo(juncX2, EFp_y);
  ctx.moveTo(juncX2, EFn_y); ctx.lineTo(g2x + g2w - 20, EFn_y);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 11.5px monospace';
  ctx.fillText('E_C', g2x + 24, bTopP - 6);
  ctx.fillStyle = '#f472b6';
  ctx.fillText('E_V', g2x + 24, bTopP + gapPx + 15);
  ctx.fillStyle = '#facc15';
  ctx.fillText(`Barreira = q(V_bi - V_a) = ${Vj.toFixed(3)} eV`, g2x + 20, g2y + g2h - 14);
}

// ============================================================================
// SIMULADOR 2: INJEÇÃO DE MINORITÁRIOS, CORRENTE & CAPACITÂNCIA (Lista 2 Q2, Q4)
// ============================================================================
function renderSim2(ctx, W, H) {
  ctx.clearRect(0, 0, W, H);

  const Va_iv = parseFloat(document.getElementById('s2-Va').value);
  const Va_cap = parseFloat(document.getElementById('s2-Va-cap').value);

  document.getElementById('s2-Va-val').textContent = `${Va_iv >= 0 ? '+' : ''}${Va_iv.toFixed(2)} V`;
  document.getElementById('s2-Va-cap-val').textContent = `${Va_cap >= 0 ? '+' : ''}${Va_cap.toFixed(2)} V`;

  // Dados exatos da Questão 2 da Lista 2:
  // ND = 1e18, NA = 1e16, A = 1.2e-4 cm^2, Dn = 34, Dp = 13, tau = 1 us -> Ln = 58.31 um, Lp = 36.06 um
  const Is_q2 = 1.1265e-15; // A
  const Vt = 0.02586;
  const I_q2 = Is_q2 * (Math.exp(Va_iv / Vt) - 1.0);
  const Vbi_q2 = Vt * Math.log((1e18 * 1e16) / 1e20); // 0.8336 V
  const eps_s_q2 = 11.7 * eps_0_cm;
  const W_q2_um = Math.sqrt(((2 * eps_s_q2) / q_el) * ((1e16 + 1e18) / (1e16 * 1e18)) * Math.max(0.05, Vbi_q2 - Va_iv)) * 1e4;

  // Dados exatos da Questão 4 da Lista 2:
  // Vbi = 0.70 V, ND = 6.033e13 cm^-3, A = 2e-2 cm^2, Cj(-4.3V) = 20 pF, Cj(-0.55V) = 40 pF
  const Vbi_q4 = 0.70;
  const k_cap = 40.0 * Math.sqrt(0.70 - (-0.55)); // 44.72136 pF * V^0.5
  const Cj_q4 = k_cap / Math.sqrt(Math.max(0.05, Vbi_q4 - Va_cap));

  document.getElementById('r2-Is').textContent = `${Is_q2.toExponential(3)} A`;
  document.getElementById('r2-Id').textContent = `${I_q2.toExponential(3)} A`;
  document.getElementById('r2-W2').textContent = `${W_q2_um.toFixed(4)} µm`;
  document.getElementById('r2-Cj').textContent = `${Cj_q4.toFixed(2)} pF`;

  const pad = 35;
  const halfW = (W - pad * 3) / 2;
  const boxH = H - 55;
  const boxY = 25;

  // Painel Esquerdo: Perfil de Minoritários e Corrente (Questão 2 da Lista 2)
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.fillRect(pad, boxY, halfW, boxH);
  ctx.strokeRect(pad, boxY, halfW, boxH);

  ctx.fillStyle = '#38bdf8';
  ctx.font = 'bold 13px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('Lista 2 Q2: Injeção de Minoritários no Diodo n⁺p (300 K)', pad + 14, boxY + 24);

  const midX = pad + halfW * 0.52;
  const baseY = boxY + boxH * 0.62;
  ctx.strokeStyle = '#475569';
  ctx.beginPath();
  ctx.moveTo(pad + 20, baseY); ctx.lineTo(pad + halfW - 20, baseY);
  ctx.moveTo(midX - 18, boxY + 45); ctx.lineTo(midX - 18, boxY + boxH - 25);
  ctx.moveTo(midX + 18, boxY + 45); ctx.lineTo(midX + 18, boxY + boxH - 25);
  ctx.stroke();

  ctx.fillStyle = 'rgba(71, 85, 105, 0.35)';
  ctx.fillRect(midX - 18, boxY + 45, 36, boxH - 70);

  // Exponenciais de decaimento L_n (no lado P, esquerda) e L_p (no lado N+, direita)
  const factor = Math.tanh(Va_iv / 0.18);
  // Lado P (esquerda): elétrons injetados n'(x)
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.8;
  ctx.beginPath();
  for (let i = 0; i <= 80; i++) {
    const u = i / 80; // 0 (longe) -> 1 (borda da depleção)
    const px = (pad + 22) + u * (midX - 18 - (pad + 22));
    const amp = 115 * factor * Math.exp(-(1 - u) * 2.6);
    const py = baseY - 25 - amp;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Lado N+ (direita): lacunas injetadas p'(x') (muito menor pois ND = 100 * NA!)
  ctx.strokeStyle = '#f43f5e';
  ctx.lineWidth = 2.8;
  ctx.beginPath();
  for (let i = 0; i <= 80; i++) {
    const u = i / 80; // 0 (borda) -> 1 (longe)
    const px = (midX + 18) + u * (pad + halfW - 22 - (midX + 18));
    const amp = 35 * factor * Math.exp(-u * 3.8);
    const py = baseY - 10 - amp;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '12px monospace';
  ctx.fillText(`Lado P (N_A=10¹⁶): L_n = 58,31 µm`, pad + 20, boxY + 52);
  ctx.fillText(`Lado N⁺ (N_D=10¹⁸): L_p = 36,06 µm`, midX + 24, boxY + 52);
  ctx.fillStyle = '#facc15';
  ctx.fillText(`Em V_a = ${Va_iv >= 0 ? '+' : ''}${Va_iv.toFixed(2)} V → I = ${I_q2.toExponential(4)} A`, pad + 20, boxY + boxH - 16);

  // Painel Direito: Curva C_j(V_a) e 1/C_j^2 da Questão 4 da Lista 2
  const rX = pad * 2 + halfW;
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.fillRect(rX, boxY, halfW, boxH);
  ctx.strokeRect(rX, boxY, halfW, boxH);

  ctx.fillStyle = '#f472b6';
  ctx.font = 'bold 13px Inter, sans-serif';
  ctx.fillText('Lista 2 Q4: Capacitância C_j(V_a) [V_bi = 0,70 V, N_D = 6,03×10¹³]', rX + 14, boxY + 24);

  const gx0 = rX + 48, gy0 = boxY + boxH - 42, gw = halfW - 75, gh = boxH - 85;
  ctx.strokeStyle = '#64748b';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(gx0, boxY + 42); ctx.lineTo(gx0, gy0); ctx.lineTo(gx0 + gw, gy0);
  ctx.stroke();

  // Mapeia Va de -5.0 V a +0.5 V e Cj de 0 a 70 pF
  const mapX = v => gx0 + ((v - (-5.0)) / 5.5) * gw;
  const mapY = c => gy0 - (c / 70.0) * gh;

  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.6;
  ctx.beginPath();
  for (let i = 0; i <= 120; i++) {
    const v = -5.0 + (i / 120) * 5.4;
    const c = k_cap / Math.sqrt(Vbi_q4 - v);
    const px = mapX(v), py = mapY(c);
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Destaca os 2 pontos do enunciado da Questão 4: (-4.3 V, 20 pF) e (-0.55 V, 40 pF)
  const pts = [
    { v: -4.3, c: 20, lbl: '(-4,3V; 20pF)' },
    { v: -0.55, c: 40, lbl: '(-0,55V; 40pF)' }
  ];
  pts.forEach(pt => {
    const px = mapX(pt.v), py = mapY(pt.c);
    ctx.fillStyle = '#10b981';
    ctx.beginPath(); ctx.arc(px, py, 6, 0, Math.PI * 2); ctx.fill();
    ctx.font = 'bold 11px monospace';
    ctx.fillText(pt.lbl, px - 35, py - 10);
  });

  // Ponto ativo selecionado pelo usuário
  const curX = mapX(Va_cap), curY = mapY(Math.min(68, Cj_q4));
  ctx.fillStyle = '#facc15';
  ctx.beginPath(); ctx.arc(curX, curY, 7, 0, Math.PI * 2); ctx.fill();
  ctx.font = 'bold 12px monospace';
  ctx.fillText(`C_j(${Va_cap.toFixed(2)}V) = ${Cj_q4.toFixed(2)} pF`, rX + 55, boxY + boxH - 14);
}

// ============================================================================
// SIMULADOR 3: DIODO SCHOTTKY METAL-SEMICONDUTOR (Aula 14 | Lista 3 Q1, Q2, Q3)
// ============================================================================
function renderSim3(ctx, W, H) {
  ctx.clearRect(0, 0, W, H);

  const metalKey = document.getElementById('s3-metal').value;
  const logND = parseFloat(document.getElementById('s3-ND').value);
  const Va = parseFloat(document.getElementById('s3-Va').value);
  const T = parseFloat(document.getElementById('s3-T').value);

  const ND = Math.pow(10, logND);
  document.getElementById('s3-ND-val').textContent = `${(ND / 1e15).toFixed(2)}×10¹⁵ cm⁻³`;
  document.getElementById('s3-Va-val').textContent = `${Va >= 0 ? '+' : ''}${Va.toFixed(3)} V`;
  document.getElementById('s3-T-val').textContent = `${T.toFixed(0)} K (${(T - 273).toFixed(0)} °C)`;

  // Funções trabalho da Aula 14 Slide 19
  const metals = {
    'Q12': { name: 'Metal Q1/Q2 (φ_B = 0,65 V)', phi_m: 4.70 },
    'Cr':  { name: 'Cromo - Cr (4,50 eV - Q3)', phi_m: 4.50 },
    'Al':  { name: 'Alumínio - Al (4,10 eV)', phi_m: 4.10 },
    'Ni':  { name: 'Níquel - Ni (5,15 eV)', phi_m: 5.15 },
    'PtSi':{ name: 'PtSi (5,40 eV)', phi_m: 5.40 },
    'Pt':  { name: 'Platina - Pt (5,70 eV)', phi_m: 5.70 }
  };

  const chi_s = 4.05; // eV (Silício)
  const phi_m = metals[metalKey].phi_m;
  const phi_B = phi_m - chi_s; // Barreira metal -> semicondutor (CONSTANTE!)

  const kT = k_eV * T;
  // Para reproduzir exatamente Vbi = 0.40 V quando ND = 10^15 cm^-3 e phi_B = 0.65 V (Questão 1 e 2 da Lista 3):
  // Sabemos que Ec - EF = 0.25 eV em ND = 10^15 cm^-3, e diminui como kT * ln(ND / 10^15)
  const Ec_minus_EF = Math.max(0.02, 0.25 - kT * Math.log(ND / 1e15));
  const Vbi = Math.max(0.02, phi_B - Ec_minus_EF);
  const V_semi_to_metal = Math.max(0.0, Vbi - Va); // Barreira semicondutor -> metal: q(Vbi - Va)

  // Cálculo da corrente para a área da Questão 3 (A = 1.4631e-4 cm^2, A* = 120 A/cm^2K^2)
  const Area_q3 = 1.4631e-4;
  const IS = Area_q3 * 120.0 * T * T * Math.exp(-phi_B / kT);
  const ID = IS * (Math.exp(Math.min(25, Va / kT)) - 1.0);

  document.getElementById('r3-phiB').textContent = `${phi_B.toFixed(3)} eV (Constante!)`;
  document.getElementById('r3-Vbi').textContent = `${Vbi.toFixed(4)} V`;
  document.getElementById('r3-qVd').textContent = `${V_semi_to_metal.toFixed(3)} eV`;
  document.getElementById('r3-ID').textContent = `${(ID * 1e3).toFixed(2)} mA`;

  const pad = 35;
  const boxY = 25, boxH = H - 50;
  const juncX = W * 0.42;

  // Fundo Metal (esquerda) e Semicondutor Tipo N (direita)
  ctx.fillStyle = 'rgba(245, 158, 11, 0.14)';
  ctx.fillRect(pad, boxY, juncX - pad, boxH);
  ctx.fillStyle = '#111827';
  ctx.fillRect(juncX, boxY, W - pad - juncX, boxH);
  ctx.strokeStyle = '#475569';
  ctx.strokeRect(pad, boxY, W - pad * 2, boxH);

  // Interface Metal / Semicondutor
  ctx.strokeStyle = '#facc15';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(juncX, boxY); ctx.lineTo(juncX, boxY + boxH);
  ctx.stroke();

  // Referência de energia: Nível de Fermi do Metal EF_m fixo no meio
  const EFm_y = boxY + boxH * 0.62;
  const scaleE = 150; // pixels por eV

  // Desenha EF_m no Metal
  ctx.strokeStyle = '#facc15';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(pad + 20, EFm_y); ctx.lineTo(juncX, EFm_y);
  ctx.stroke();

  // Topo da barreira na interface (sempre EFm_y - phi_B * scaleE!)
  const peakY = EFm_y - phi_B * scaleE;

  // Nível de Fermi no Semicondutor EF_s = EF_m + q*Va (em polarização direta sobe, em reversa desce)
  const EFs_y = EFm_y - Math.max(-1.1, Math.min(0.45, Va)) * scaleE;
  const Ec_bulk_y = EFs_y - Ec_minus_EF * scaleE;
  const depW = Math.min(W - pad - juncX - 60, Math.max(45, 130 * Math.sqrt(Math.max(0.05, V_semi_to_metal) / 0.40)));

  // Curva da Banda de Condução EC(x) no Semicondutor Tipo N
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 3;
  ctx.beginPath();
  for (let x = juncX; x <= W - pad - 20; x += 4) {
    let py = Ec_bulk_y;
    if (x < juncX + depW) {
      const u = 1.0 - (x - juncX) / depW;
      py = Ec_bulk_y + (peakY - Ec_bulk_y) * u * u;
    }
    if (x === juncX) ctx.moveTo(x, py); else ctx.lineTo(x, py);
  }
  ctx.stroke();

  // Nível de Fermi EFs no Semicondutor
  ctx.strokeStyle = '#10b981';
  ctx.lineWidth = 2;
  ctx.setLineDash([6, 4]);
  ctx.beginPath();
  ctx.moveTo(juncX, EFs_y); ctx.lineTo(W - pad - 20, EFs_y);
  ctx.stroke();
  ctx.setLineDash([]);

  // Animação de emissão termiônica de elétrons sobre a barreira!
  const netFlow = Va >= 0 ? Math.min(1, Va / 0.2) : -0.25;
  particlesSchottky.forEach(p => {
    p.x += p.speed * (netFlow >= 0 ? -(0.6 + netFlow * 1.5) : 0.4);
    if (p.x < 0.08) p.x = 0.95;
    if (p.x > 0.95) p.x = 0.08;
    const px = pad + p.x * (W - pad * 2);
    const py = peakY - 8 - p.energy * 30;
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill();
  });

  // Setas indicadoras das duas barreiras (Questões 1 e 2 da Lista 3!)
  ctx.fillStyle = '#facc15';
  ctx.font = 'bold 13px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(`METAL: ${metals[metalKey].name}`, pad + 18, boxY + 26);
  ctx.fillText(`E_Fm (Metal)`, pad + 24, EFm_y - 10);
  ctx.fillText(`Barreira Metal → Semicondutor: qφ_B = ${phi_B.toFixed(2)} eV (NÃO muda com N_D nem com V_a!)`, pad + 18, boxY + boxH - 16);

  ctx.fillStyle = '#38bdf8';
  ctx.fillText(`SEMICONDUTOR TIPO N (Silício: qχ_s = 4,05 eV)`, juncX + 18, boxY + 26);
  ctx.fillText(`Barreira Semicondutor → Metal: q(V_bi - V_a) = ${V_semi_to_metal.toFixed(3)} eV`, juncX + 18, boxY + 50);
  ctx.fillStyle = '#10b981';
  ctx.fillText(`E_Fs (E_C - E_F = ${Ec_minus_EF.toFixed(3)} eV)`, W - pad - 230, EFs_y + 18);
}

// ============================================================================
// SIMULADOR 4: CAPACITOR MOS COMPLETO (Aula 14 | Lista 3 Q4, Q5, Q6, Q7)
// ============================================================================
function renderSim4(ctx, W, H, time) {
  ctx.clearRect(0, 0, W, H);

  const subType = document.getElementById('s4-sub').value; // 'P' ou 'N'
  const gateKey = document.getElementById('s4-gate').value;
  const VG = parseFloat(document.getElementById('s4-VG').value);
  const tox_nm = parseFloat(document.getElementById('s4-tox').value);
  const logN = parseFloat(document.getElementById('s4-logN').value);

  const N_dop = Math.pow(10, logN);
  document.getElementById('s4-VG-val').textContent = `${VG >= 0 ? '+' : ''}${VG.toFixed(2)} V`;
  document.getElementById('s4-tox-val').textContent = `${tox_nm.toFixed(2)} nm`;
  document.getElementById('s4-logN-val').textContent = `10^${logN.toFixed(1)} cm⁻³`;

  // Constantes da Lista 3 e Aula 14 Slide 18/19
  const Vt = 0.02586; // kT/q
  const ni = 1.02e10;
  const eps_ox = 3.4515e-11; // F/m (3.9 * 8.85e-12 F/m)
  const eps_s = 1.0443e-10;  // F/m (11.8 * 8.85e-12 F/m)
  const tox_m = tox_nm * 1e-9;
  const Cox = eps_ox / tox_m; // F/m^2

  // Potencial de Fermi phi_F e função trabalho do substrato phi_s_work
  const phi_F_mag = Vt * Math.log(N_dop / ni);
  const phi_F = subType === 'P' ? phi_F_mag : -phi_F_mag;
  const q_phi_s = 4.05 + 0.56 + phi_F; // eV

  const gateWork = {
    'P+Si': 5.17,
    'N+Si': 4.05,
    'Al': 4.10,
    'Cr': 4.50,
    'Custom_VFB_minus1': q_phi_s - 1.0,
    'Q6_VT025': q_phi_s
  };
  const q_phi_m = gateWork[gateKey] || 4.05;
  const phi_ms = q_phi_m - q_phi_s;

  let V_FB = phi_ms;
  if (gateKey === 'Custom_VFB_minus1') V_FB = -1.0;

  // Largura de depleção máxima na inversão forte w_d-inv (Tabela da Lista 3 pág. 2)
  const wd_inv_m = Math.sqrt((2 * eps_s * (2 * phi_F_mag)) / (q_el * (N_dop * 1e6)));
  const Qd_max = q_el * (N_dop * 1e6) * wd_inv_m; // C/m^2

  let V_T = subType === 'P'
    ? V_FB + 2 * phi_F_mag + (Qd_max / Cox)
    : V_FB - 2 * phi_F_mag - (Qd_max / Cox);
  if (gateKey === 'Q6_VT025' && subType === 'P') {
    V_T = 0.25; // Preset exato da Questão 6 da Lista 3!
  }

  // Determina o regime de operação pela tabela da Lista 3 (página 2)!
  let regime = '';
  let phi_s = 0;
  let C_hf = Cox;
  let Q_surf = 0;
  let carrierLabel = '';

  if (subType === 'P') {
    if (VG < V_FB) {
      regime = 'ACUMULAÇÃO (Tipo P: V_G < V_FB)';
      phi_s = 0;
      C_hf = Cox;
      Q_surf = Math.abs(V_FB - VG) * Cox;
      carrierLabel = 'Lacunas (Acumulação)';
    } else if (VG <= V_T) {
      regime = 'DEPLEÇÃO (Tipo P: V_FB ≤ V_G ≤ V_T)';
      const frac = (VG - V_FB) / Math.max(0.05, V_T - V_FB);
      phi_s = frac * (2 * phi_F_mag);
      const wd = Math.sqrt((2 * eps_s * Math.max(0.001, phi_s)) / (q_el * N_dop * 1e6));
      C_hf = 1.0 / ((1.0 / Cox) + (wd / eps_s));
      Q_surf = q_el * (N_dop * 1e6) * wd;
      carrierLabel = 'Íons Aceitadores Fixos (-qN_A)';
    } else {
      regime = 'INVERSÃO FORTE (Tipo P: V_G > V_T)';
      phi_s = 2 * phi_F_mag;
      C_hf = 1.0 / ((1.0 / Cox) + (wd_inv_m / eps_s));
      Q_surf = Math.abs(VG - V_T) * Cox;
      carrierLabel = 'ELÉTRONS (Camada de Inversão!)';
    }
  } else {
    // Substrato Tipo N
    if (VG > V_FB) {
      regime = 'ACUMULAÇÃO (Tipo N: V_G > V_FB)';
      phi_s = 0;
      C_hf = Cox;
      Q_surf = Math.abs(VG - V_FB) * Cox;
      carrierLabel = 'Elétrons (Acumulação)';
    } else if (VG >= V_T) {
      regime = 'DEPLEÇÃO (Tipo N: V_T ≤ V_G ≤ V_FB)';
      const frac = (V_FB - VG) / Math.max(0.05, V_FB - V_T);
      phi_s = -frac * (2 * phi_F_mag);
      const wd = Math.sqrt((2 * eps_s * Math.max(0.001, Math.abs(phi_s))) / (q_el * N_dop * 1e6));
      C_hf = 1.0 / ((1.0 / Cox) + (wd / eps_s));
      Q_surf = q_el * (N_dop * 1e6) * wd;
      carrierLabel = 'Íons Doadores Fixos (+qN_D)';
    } else {
      regime = 'INVERSÃO FORTE (Tipo N: V_G < V_T)';
      phi_s = -2 * phi_F_mag;
      C_hf = 1.0 / ((1.0 / Cox) + (wd_inv_m / eps_s));
      Q_surf = Math.abs(VG - V_T) * Cox;
      carrierLabel = 'LACUNAS (Camada de Inversão!)';
    }
  }

  // Campo elétrico no óxido: V_ox = VG - V_FB - phi_s
  const V_ox = (VG - V_FB) - phi_s;
  const E_ox_MVcm = (Math.abs(V_ox) / tox_m) * 1e-8; // MV/cm (10^8 V/m = 10^6 V/cm = 1 MV/cm)
  const sentido_Eox = V_ox >= 0 ? 'Óxido → Semicondutor' : 'Semicondutor → Óxido';
  const ns_cm2 = (Q_surf / q_el) * 1e-4;

  document.getElementById('r4-regime').textContent = regime;
  document.getElementById('r4-phims').textContent = `${phi_ms >= 0 ? '+' : ''}${phi_ms.toFixed(4)} eV`;
  document.getElementById('r4-Eox').textContent = `${E_ox_MVcm.toFixed(2)} MV/cm (${sentido_Eox})`;
  document.getElementById('r4-ns').textContent = `${ns_cm2.toExponential(3)} cm⁻² (${carrierLabel})`;
  document.getElementById('r4-Cox').textContent = `${(Cox * 1e3).toFixed(2)} mF/m² | C_HF = ${(C_hf * 1e3).toFixed(2)} mF/m²`;

  const pad = 32;
  const halfW = (W - pad * 3) / 2;
  const boxY = 24, boxH = H - 48;

  // 1) Painel Esquerdo: Corte Físico Animado do Capacitor MOS (Porta | Óxido SiO2 | Substrato Si)
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.fillRect(pad, boxY, halfW, boxH);
  ctx.strokeRect(pad, boxY, halfW, boxH);

  const gateX = pad + 20, gateW = 75;
  const oxX = gateX + gateW, oxW = 65;
  const siX = oxX + oxW, siW = halfW - (siX - pad) - 20;
  const structY = boxY + 48, structH = boxH - 85;

  // Porta (Gate)
  ctx.fillStyle = '#334155';
  ctx.fillRect(gateX, structY, gateW, structH);
  // Óxido SiO2
  ctx.fillStyle = 'rgba(245, 158, 11, 0.25)';
  ctx.fillRect(oxX, structY, oxW, structH);
  // Substrato de Silício
  ctx.fillStyle = subType === 'P' ? 'rgba(30, 58, 138, 0.55)' : 'rgba(127, 29, 29, 0.55)';
  ctx.fillRect(siX, structY, siW, structH);
  ctx.strokeStyle = '#94a3b8';
  ctx.strokeRect(gateX, structY, gateW + oxW + siW, structH);

  // Setas do Campo Elétrico no Óxido E_ox (Questão 4 da Lista 3!)
  if (Math.abs(V_ox) > 0.02) {
    ctx.strokeStyle = '#facc15';
    ctx.fillStyle = '#facc15';
    ctx.lineWidth = 2.2;
    for (let y = structY + 28; y < structY + structH - 20; y += 38) {
      ctx.beginPath();
      if (V_ox > 0) {
        // Óxido -> Semicondutor (direita)
        ctx.moveTo(oxX + 8, y); ctx.lineTo(oxX + oxW - 8, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(oxX + oxW - 8, y);
        ctx.lineTo(oxX + oxW - 16, y - 5);
        ctx.lineTo(oxX + oxW - 16, y + 5);
        ctx.closePath(); ctx.fill();
      } else {
        // Semicondutor -> Óxido (esquerda)
        ctx.moveTo(oxX + oxW - 8, y); ctx.lineTo(oxX + 8, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(oxX + 8, y);
        ctx.lineTo(oxX + 16, y - 5);
        ctx.lineTo(oxX + 16, y + 5);
        ctx.closePath(); ctx.fill();
      }
    }
  }

  // Anima portadores na superfície do silício conforme o regime (Acumulação, Depleção ou Inversão Forte)
  const isAcc = (subType === 'P' && VG < V_FB) || (subType === 'N' && VG > V_FB);
  const isInv = (subType === 'P' && VG > V_T) || (subType === 'N' && VG < V_T);

  particlesMOS.forEach((p, idx) => {
    const py = structY + 14 + p.y * (structH - 28);
    let px;
    if (isAcc) {
      // Portadores majoritários encostados na interface SiO2/Si!
      px = siX + 8 + Math.abs(Math.sin(time * 0.003 + p.phase)) * (idx < 35 ? 24 : siW - 20);
      ctx.fillStyle = subType === 'P' ? '#f43f5e' : '#38bdf8';
      ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI * 2); ctx.fill();
    } else if (isInv) {
      if (idx < 35) {
        // Camada de inversão de minoritários colada na interface SiO2/Si!
        px = siX + 6 + Math.abs(Math.sin(time * 0.004 + p.phase)) * 18;
        ctx.fillStyle = subType === 'P' ? '#38bdf8' : '#f43f5e';
        ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();
      } else {
        // Majoritários afastados além da zona de depleção
        px = siX + 95 + (p.x * (siW - 105));
        ctx.fillStyle = subType === 'P' ? '#f43f5e' : '#38bdf8';
        ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill();
      }
    } else {
      // Depleção: região próxima à interface vazia de móveis, apenas íons fixos
      px = siX + 80 + (p.x * (siW - 90));
      ctx.fillStyle = subType === 'P' ? '#f43f5e' : '#38bdf8';
      ctx.beginPath(); ctx.arc(px, py, 4, 0, Math.PI * 2); ctx.fill();
    }
  });

  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 12.5px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText(`Estrutura Física MOS (Substrato Tipo ${subType})`, pad + 14, boxY + 24);
  ctx.textAlign = 'center';
  ctx.fillText('Porta', gateX + gateW / 2, structY - 8);
  ctx.fillStyle = '#facc15';
  ctx.fillText('SiO₂', oxX + oxW / 2, structY - 8);
  ctx.fillStyle = '#38bdf8';
  ctx.fillText(`Silício Tipo ${subType}`, siX + siW / 2, structY - 8);
  ctx.fillStyle = '#34d399';
  ctx.fillText(`${sentido_Eox} (E_ox = ${E_ox_MVcm.toFixed(2)} MV/cm)`, pad + halfW / 2, boxY + boxH - 14);

  // 2) Painel Direito: Curva C-V (LF & HF) + Ponto de Operação (Questão 7 da Lista 3!)
  const rX = pad * 2 + halfW;
  ctx.fillStyle = '#111827';
  ctx.strokeStyle = '#334155';
  ctx.fillRect(rX, boxY, halfW, boxH);
  ctx.strokeRect(rX, boxY, halfW, boxH);

  ctx.fillStyle = '#10b981';
  ctx.font = 'bold 12.5px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('Curva Capacitância × Tensão de Porta (LF vs HF) [Lista 3 Q7]', rX + 14, boxY + 24);

  const gx0 = rX + 48, gy0 = boxY + boxH - 42, gw = halfW - 72, gh = boxH - 85;
  ctx.strokeStyle = '#64748b';
  ctx.beginPath();
  ctx.moveTo(gx0, boxY + 42); ctx.lineTo(gx0, gy0); ctx.lineTo(gx0 + gw, gy0);
  ctx.stroke();

  const mapX = v => gx0 + ((v - (-3.0)) / 8.5) * gw;
  const mapY = ratio => gy0 - ratio * (gh - 15);

  // Desenha curvas normalizadas C / C_ox (HF em verde sólido, LF em azul tracejado)
  function evalC(vg, isLF) {
    if (subType === 'P') {
      if (vg <= V_FB) return 1.0;
      if (vg <= V_T) {
        const f = (vg - V_FB) / Math.max(0.05, V_T - V_FB);
        const w = wd_inv_m * Math.sqrt(f);
        return 1.0 / (1.0 + (Cox * w) / eps_s);
      }
      const cmin = 1.0 / (1.0 + (Cox * wd_inv_m) / eps_s);
      return isLF ? cmin + (1.0 - cmin) * (1.0 - Math.exp(-(vg - V_T) / 0.25)) : cmin;
    } else {
      if (vg >= V_FB) return 1.0;
      if (vg >= V_T) {
        const f = (V_FB - vg) / Math.max(0.05, V_FB - V_T);
        const w = wd_inv_m * Math.sqrt(f);
        return 1.0 / (1.0 + (Cox * w) / eps_s);
      }
      const cmin = 1.0 / (1.0 + (Cox * wd_inv_m) / eps_s);
      return isLF ? cmin + (1.0 - cmin) * (1.0 - Math.exp(-(V_T - vg) / 0.25)) : cmin;
    }
  }

  // LF
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 4]);
  ctx.beginPath();
  for (let i = 0; i <= 140; i++) {
    const v = -3.0 + (i / 140) * 8.5;
    const px = mapX(v), py = mapY(evalC(v, true));
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();
  ctx.setLineDash([]);

  // HF
  ctx.strokeStyle = '#10b981';
  ctx.lineWidth = 2.8;
  ctx.beginPath();
  for (let i = 0; i <= 140; i++) {
    const v = -3.0 + (i / 140) * 8.5;
    const px = mapX(v), py = mapY(evalC(v, false));
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();

  // Ponto atual
  const curRatio = evalC(VG, false);
  const cx = mapX(VG), cy = mapY(curRatio);
  ctx.fillStyle = '#facc15';
  ctx.beginPath(); ctx.arc(cx, cy, 7, 0, Math.PI * 2); ctx.fill();

  ctx.fillStyle = '#facc15';
  ctx.font = 'bold 11.5px monospace';
  ctx.fillText(`V_FB = ${V_FB.toFixed(2)}V | V_T = ${V_T.toFixed(2)}V | C_ox = ${(Cox*1e3).toFixed(2)} mF/m²`, rX + 48, boxY + boxH - 14);
}

// Loop de animação principal a 60 FPS
function animateAll(timestamp) {
  const c1 = document.getElementById('canvas-sim-1');
  const c2 = document.getElementById('canvas-sim-2');
  const c3 = document.getElementById('canvas-sim-3');
  const c4 = document.getElementById('canvas-sim-4');

  if (activeSimIndex === 1 && c1) renderSim1(c1.getContext('2d'), c1.width, c1.height, timestamp);
  if (activeSimIndex === 2 && c2) renderSim2(c2.getContext('2d'), c2.width, c2.height);
  if (activeSimIndex === 3 && c3) renderSim3(c3.getContext('2d'), c3.width, c3.height);
  if (activeSimIndex === 4 && c4) renderSim4(c4.getContext('2d'), c4.width, c4.height, timestamp);

  requestAnimationFrame(animateAll);
}

window.addEventListener('DOMContentLoaded', () => {
  requestAnimationFrame(animateAll);
});
