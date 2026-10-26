// AgriSensa BioFertilizer Studio - SPA Application Logic

let availableMaterials = [];
let solidNPKChart = null;
let solidCNDecayChart = null;
let economicsChart = null;

// Initialize on DOM Loaded
document.addEventListener('DOMContentLoaded', () => {
 initNavigation();
 initSolidMaterials();
 initSolidPresets();
 initLiquidModule();
 initEconomicsModule();
});

// 1. Navigation & Tab Switcher
function initNavigation() {
 const mainTabs = document.querySelectorAll('.master-tabs .tab-btn');
 const tabPanels = document.querySelectorAll('.tab-panel');

 mainTabs.forEach(btn => {
 btn.addEventListener('click', () => {
 mainTabs.forEach(b => b.classList.remove('active'));
 tabPanels.forEach(p => p.classList.remove('active'));

 btn.classList.add('active');
 const target = btn.getAttribute('data-target');
 const panel = document.getElementById(target);
 if (panel) panel.classList.add('active');
 });
 });

 // Sub tabs inside Solid Fertilizer
 initSubTabs('solid-sub-tabs', 'solid-sub-panel');
 initSubTabs('liquid-sub-tabs', 'liquid-sub-panel');
}

function initSubTabs(btnContainerClass, panelClass) {
 const buttons = document.querySelectorAll(`.${btnContainerClass} .sub-tab-btn`);
 buttons.forEach(btn => {
 btn.addEventListener('click', () => {
 const parent = btn.closest('.glass-card') || document;
 parent.querySelectorAll(`.${btnContainerClass} .sub-tab-btn`).forEach(b => b.classList.remove('active'));
 parent.querySelectorAll(`.${panelClass}`).forEach(p => p.style.display = 'none');

 btn.classList.add('active');
 const targetId = btn.getAttribute('data-subtarget');
 const targetPanel = document.getElementById(targetId);
 if (targetPanel) targetPanel.style.display = 'block';
 });
 });
}

// 2. Solid Fertilizer Module (Fitur 1: Pupuk Padat)
async function initSolidMaterials() {
 const container = document.getElementById('solid-materials-list');
 if (!container) return;

 try {
 const res = await fetch('/api/solid/materials');
 const data = await res.json();
 availableMaterials = data.materials || [];

 container.innerHTML = '';
 availableMaterials.forEach((mat, idx) => {
 // Default select Kotoran Sapi (500kg), Sekam (200kg), Dedak (30kg)
 let defaultVal = 0;
 if (mat.name === 'Kotoran Sapi') defaultVal = 500;
 else if (mat.name === 'Sekam Padi Mentah') defaultVal = 200;
 else if (mat.name === 'Dedak Padi Halus (Katul)') defaultVal = 30;
 else if (mat.name === 'Dolomit (Kapur Pertanian)') defaultVal = 50;

 const row = document.createElement('div');
 row.className = 'material-row';
 row.innerHTML = `
 <div class="material-info">
 <div class="material-name">${mat.name}</div>
 <div class="material-tag">${mat.category} | C/N: ${mat.c_n_ratio} | N: ${mat.n_pct}% P: ${mat.p_pct}% K: ${mat.k_pct}%</div>
 </div>
 <div class="material-input-wrap">
 <input type="number" min="0" step="5" value="${defaultVal}" 
 data-name="${mat.name}" class="mat-weight-input" id="mat-input-${idx}">
 <span style="font-size:0.8rem; color:var(--text-muted);">kg</span>
 </div>
 `;
 container.appendChild(row);
 });

 // Trigger first calculation
 calculateSolidFormula();

 // Listen for changes
 container.querySelectorAll('.mat-weight-input').forEach(input => {
 input.addEventListener('input', debounce(calculateSolidFormula, 350));
 });

 // Day slider listener
 const daySlider = document.getElementById('solid-days-input');
 const dayDisplay = document.getElementById('solid-days-display');
 if (daySlider) {
 daySlider.addEventListener('input', (e) => {
 if (dayDisplay) dayDisplay.textContent = `Hari ke-${e.target.value}`;
 calculateSolidFormula();
 });
 }

 } catch (err) {
 console.error('Failed loading solid materials:', err);
 container.innerHTML = '<p style="color:var(--danger);">Gagal memuat bahan baku dari server.</p>';
 }
}

async function calculateSolidFormula() {
 const inputs = document.querySelectorAll('.mat-weight-input');
 const materials = [];

 inputs.forEach(inp => {
 const val = parseFloat(inp.value) || 0;
 if (val > 0) {
 materials.push({
 name: inp.getAttribute('data-name'),
 weight_kg: val
 });
 }
 });

 if (materials.length === 0) {
 document.getElementById('solid-weight-metric').textContent = '0 kg';
 return;
 }

 const days = parseInt(document.getElementById('solid-days-input')?.value || '0');

 try {
 const res = await fetch('/api/solid/calculate', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({
 materials: materials,
 fermentation_days: days
 })
 });

 if (!res.ok) throw new Error('Calculation error');
 const result = await res.json();
 renderSolidCalculation(result);

 } catch (err) {
 console.error('Solid calculation error:', err);
 }
}

function renderSolidCalculation(data) {
 // 1. Metric Cards
 document.getElementById('solid-weight-metric').textContent = `${data.total_wet_weight_kg.toLocaleString()} kg`;
    const weightSub = document.getElementById('solid-weight-sub');
    if (weightSub) weightSub.textContent = `Basis Kering: ${data.total_dry_weight_kg.toLocaleString()} kg (Kadar Air: ${data.initial_moisture_pct}%)`;
 document.getElementById('solid-npk-metric').textContent = `${data.dry_basis_n_pct}% - ${data.dry_basis_p2o5_pct}% - ${data.dry_basis_k2o_pct}%`;
 document.getElementById('solid-cn-metric').textContent = `${data.estimated_current_c_n_ratio}:1`;
 document.getElementById('solid-cn-sub').textContent = `Awal: ${data.initial_c_n_ratio}:1`;
 document.getElementById('solid-phase-metric').textContent = data.temperature_range;
 document.getElementById('solid-phase-sub').textContent = data.fermentation_phase;

 // 2. Suitability note
 const suitElem = document.getElementById('solid-suitability-note');
 if (suitElem) suitElem.innerHTML = `<strong>Karakter Pupuk:</strong> ${data.suitability}`;

 // 3. SNI Table
 const sniTbody = document.getElementById('solid-sni-tbody');
 if (sniTbody) {
 sniTbody.innerHTML = '';
 data.sni_evaluation.forEach(item => {
 const badgeClass = item.status.includes('Lolos') ? 'pass' : (item.status.includes('Kurang') ? 'fail' : 'warning');
 const tr = document.createElement('tr');
 tr.innerHTML = `
 <td><strong>${item.parameter}</strong></td>
 <td>${item.measured_value} ${item.unit}</td>
 <td>${item.standard_range} ${item.unit}</td>
 <td><span class="status-badge ${badgeClass}">${item.status}</span></td>
 `;
 sniTbody.appendChild(tr);
 });
 }

 // 4. Update NPK Bar Chart
 renderSolidNPKChart(data.dry_basis_n_pct, data.dry_basis_p2o5_pct, data.dry_basis_k2o_pct, data.dry_basis_c_pct);

 // 5. Update C/N Decay Curve
 renderSolidCNDecayChart(data.initial_c_n_ratio, parseInt(document.getElementById('solid-days-input')?.value || '0'));
}

function renderSolidNPKChart(n, p, k, c) {
 const ctx = document.getElementById('solid-npk-canvas');
 if (!ctx) return;

 if (solidNPKChart) solidNPKChart.destroy();

 solidNPKChart = new Chart(ctx, {
 type: 'bar',
 data: {
 labels: ['Nitrogen (N)', 'Fosfat (P₂O₅)', 'Kalium (K₂O)', 'C-Organik (%)'],
 datasets: [{
 label: 'Kandungan Hara Terhitung (%)',
 data: [n, p, k, c],
 backgroundColor: [
 'rgba(16, 185, 129, 0.8)',
 'rgba(59, 130, 246, 0.8)',
 'rgba(245, 158, 11, 0.8)',
 'rgba(148, 163, 184, 0.8)'
 ],
 borderRadius: 6
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 plugins: {
 legend: { display: false }
 },
 scales: {
 y: {
 beginAtZero: true,
 grid: { color: 'rgba(0, 0, 0, 0.06)' },
 ticks: { color: '#475569' }
 },
 x: {
 grid: { display: false },
 ticks: { color: '#0f172a' }
 }
 }
 }
 });
}

function renderSolidCNDecayChart(initialCN, currentDay) {
 const ctx = document.getElementById('solid-cn-canvas');
 if (!ctx) return;

 if (solidCNDecayChart) solidCNDecayChart.destroy();

 const days = [0, 3, 7, 10, 14, 18, 21, 28];
 const targetStable = 12.5;
 const cnValues = days.map(d => {
 const decay = Math.exp(-0.035 * d);
 return Math.max(10.0, targetStable + (initialCN - targetStable) * decay);
 });

 solidCNDecayChart = new Chart(ctx, {
 type: 'line',
 data: {
 labels: days.map(d => `H-${d}`),
 datasets: [
 {
 label: 'Proyeksi Rasio C/N',
 data: cnValues,
 borderColor: '#38bdf8',
 backgroundColor: 'rgba(56, 189, 248, 0.1)',
 fill: true,
 tension: 0.35,
 borderWidth: 2
 },
 {
 label: 'Batas Ideal SNI (10-20)',
 data: days.map(() => 20),
 borderColor: 'rgba(16, 185, 129, 0.6)',
 borderDash: [5, 5],
 fill: false,
 pointRadius: 0
 }
 ]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 plugins: {
 legend: {
 labels: { color: '#334155' }
 }
 },
 scales: {
 y: {
 min: 5,
 max: Math.max(40, initialCN + 5),
 grid: { color: 'rgba(0, 0, 0, 0.06)' },
 ticks: { color: '#475569' }
 },
 x: {
 grid: { display: false },
 ticks: { color: '#0f172a' }
 }
 }
 }
 });
}

// Solid AI Optimizer Handler
async function runSolidOptimizer() {
 const targetWeight = parseFloat(document.getElementById('opt-target-weight')?.value || '1000');
 const targetCN = parseFloat(document.getElementById('opt-target-cn')?.value || '28');
 const priority = document.getElementById('opt-priority')?.value || 'balanced';

 // Get checked materials for optimizer
 const checked = [];
 document.querySelectorAll('.opt-mat-checkbox:checked').forEach(cb => {
 checked.push(cb.value);
 });

 if (checked.length < 2) {
 alert('Pilih minimal 2 bahan baku untuk dioptimasi oleh AI!');
 return;
 }

 const btn = document.getElementById('btn-run-optimizer');
 if (btn) btn.innerHTML = '️ Mengoptimasi Formula...';

 try {
 const res = await fetch('/api/solid/optimize', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({
 target_total_weight_kg: targetWeight,
 target_c_n_ratio: targetCN,
 available_materials: checked,
 priority: priority
 })
 });

 const data = await res.json();
 renderOptimizationResult(data);

 } catch (err) {
 console.error('Optimizer error:', err);
 } finally {
 if (btn) btn.innerHTML = ' Jalankan AI Optimizer';
 }
}

function renderOptimizationResult(data) {
 const resBox = document.getElementById('opt-results-box');
 if (!resBox) return;

 resBox.style.display = 'block';
 resBox.innerHTML = `
 <div style="background:rgba(16, 185, 129, 0.1); border:1px solid var(--border-accent); border-radius:var(--radius-md); padding:16px; margin-bottom:14px;">
 <h4 style="color:#34d399; margin-bottom:6px;"> Formula AI Berhasil Dihitung</h4>
 <p style="font-size:0.9rem; color:var(--text-muted);">Target C/N: <strong>${data.target_c_n_ratio}:1</strong> | Tercapai: <strong>${data.estimated_achieved_c_n}:1</strong> | Estimasi NPK: <strong>${data.estimated_npk}</strong></p>
 </div>
 <table class="sni-table" style="margin-bottom:14px;">
 <thead>
 <tr>
 <th>Bahan Baku Rekomendasi</th>
 <th>Takaran Optimal</th>
 <th>Proporsi</th>
 <th>Peran Agroteknis</th>
 </tr>
 </thead>
 <tbody>
 ${data.materials.map(m => `
 <tr>
 <td><strong>${m.name}</strong></td>
 <td style="color:#34d399; font-weight:700;">${m.recommended_wet_kg} kg</td>
 <td>${m.percentage}%</td>
 <td style="font-size:0.8rem; color:var(--text-muted);">${m.role}</td>
 </tr>
 `).join('')}
 </tbody>
 </table>
 <button class="btn btn-secondary btn-sm" id="btn-apply-opt-formula">
 Terapkan Takaran Ini ke Formulator Utama
 </button>
 `;

 document.getElementById('btn-apply-opt-formula')?.addEventListener('click', () => {
 applyOptimizedToInputs(data.materials);
 });
}

function applyOptimizedToInputs(materials) {
 // Reset all inputs to 0
 document.querySelectorAll('.mat-weight-input').forEach(inp => inp.value = 0);

 // Apply new values
 materials.forEach(m => {
 const inp = document.querySelector(`.mat-weight-input[data-name="${m.name}"]`);
 if (inp) inp.value = m.recommended_wet_kg;
 });

 // Switch to first subtab
 const firstSubTab = document.querySelector('.solid-sub-tabs .sub-tab-btn[data-subtarget="solid-sub-calc"]');
 if (firstSubTab) firstSubTab.click();

 calculateSolidFormula();
}

// Preset Solid Recipes
async function initSolidPresets() {
 const listContainer = document.getElementById('solid-recipes-container');
 if (!listContainer) return;

 try {
 const res = await fetch('/api/solid/recipes');
 const data = await res.json();
 const recipes = data.recipes || [];

 listContainer.innerHTML = '';
 recipes.forEach(rc => {
 const card = document.createElement('div');
 card.className = 'recipe-card';
 card.innerHTML = `
 <div class="recipe-header">
 <div class="recipe-title">${rc.title}</div>
 <span class="recipe-tag">Waktu: ${rc.fermentation_time}</span>
 </div>
 <div class="recipe-summary">${rc.summary}</div>
 <div style="font-size:0.85rem; font-weight:600; color:#38bdf8; margin-bottom:8px;"> Komposisi Bahan:</div>
 <div class="ingredient-pills">
 ${rc.materials.map(m => `<span class="pill"><strong>${m.name}:</strong> ${m.qty}</span>`).join('')}
 </div>
 <div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:8px;"> Tahapan Pembuatan:</div>
 <ol class="step-list">
 ${rc.steps.map(s => `<li>${s}</li>`).join('')}
 </ol>
 `;
 listContainer.appendChild(card);
 });

 } catch (err) {
 console.error('Failed loading solid recipes:', err);
 }

 // Attach optimizer trigger button
 document.getElementById('btn-run-optimizer')?.addEventListener('click', runSolidOptimizer);
}

// Global states for POC
let allPocRecipes = [];
let allMols = [];
let troubleshootData = [];
let tankMixData = [];
let currentGlobalRecipeVol = 20;

// 3. Enriched Liquid Fertilizer Module (Fitur 2: Pupuk Organik Cair)
function initLiquidModule() {
  initPOCBatchBrewModule();
  initPOCFieldScheduleModule();
  initPOCRecipesModule();
  initMOLModule();
  initPOCTroubleshootModule();

  // SNI Check
  document.getElementById('btn-check-liquid-sni')?.addEventListener('click', checkLiquidSNI);
}

// 3.1 Smart POC Batch Brew Formulator
function initPOCBatchBrewModule() {
  const volInput = document.getElementById('brew-vol-input');
  const purposeSelect = document.getElementById('brew-purpose-select');
  const ftypeSelect = document.getElementById('brew-ftype-select');
  const calcBtn = document.getElementById('btn-calc-batch-brew');

  // Quick Preset Chips for Drum Volume
  const volChips = document.querySelectorAll('#brew-vol-chips .chip-btn');
  volChips.forEach(chip => {
    chip.addEventListener('click', () => {
      volChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const vol = chip.getAttribute('data-vol');
      if (volInput) {
        volInput.value = vol;
        calculatePOCBatchBrew();
      }
    });
  });

  calcBtn?.addEventListener('click', calculatePOCBatchBrew);
  purposeSelect?.addEventListener('change', calculatePOCBatchBrew);
  ftypeSelect?.addEventListener('change', calculatePOCBatchBrew);

  // Initial calculation
  calculatePOCBatchBrew();
}

async function calculatePOCBatchBrew() {
  const vol = parseFloat(document.getElementById('brew-vol-input')?.value || '100');
  const purpose = document.getElementById('brew-purpose-select')?.value || 'all_purpose';
  const ftype = document.getElementById('brew-ftype-select')?.value || 'anaerob';

  const btn = document.getElementById('btn-calc-batch-brew');
  if (btn) btn.innerHTML = '🧪 Menghitung Formulasi Batch...';

  try {
    const res = await fetch('/api/liquid/batch-brew', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        drum_volume_liters: vol,
        purpose: purpose,
        fermentation_type: ftype
      })
    });

    if (!res.ok) throw new Error('Failed to calculate batch brew');
    const data = await res.json();
    renderPOCBatchBrewResult(data);
  } catch (err) {
    console.error('Batch brew error:', err);
  } finally {
    if (btn) btn.innerHTML = 'Hitung Takaran Batch & Panduan Fermentasi';
  }
}

function renderPOCBatchBrewResult(data) {
  const placeholder = document.getElementById('brew-placeholder');
  const resultsBox = document.getElementById('brew-results-box');
  const badgePurpose = document.getElementById('brew-badge-purpose');

  if (placeholder) placeholder.style.display = 'none';
  if (resultsBox) resultsBox.style.display = 'block';
  if (badgePurpose) badgePurpose.textContent = data.fermentation_type;

  // 1. Metrics
  document.getElementById('brew-metric-eff').textContent = `${data.effective_liquid_liters} L`;
  document.getElementById('brew-metric-headspace').textContent = `${data.headspace_liters} L (15%)`;
  document.getElementById('brew-metric-npk').textContent = data.estimated_npk;
  document.getElementById('brew-metric-cost').textContent = `Rp ${data.estimated_cost_per_liter.toLocaleString()} / L`;

  // 2. Ingredients Table
  const tbody = document.getElementById('brew-ingredients-tbody');
  if (tbody) {
    tbody.innerHTML = '';
    data.ingredients.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${item.name}</strong></td>
        <td style="color:#059669; font-weight:700;">${item.amount} ${item.unit}</td>
        <td><span class="status-badge pass">${item.category}</span></td>
        <td style="font-size:0.8rem; color:var(--text-muted);">${item.role}</td>
        <td style="font-size:0.85rem; color:#475569;">Rp ${item.cost_est.toLocaleString()}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  // 3. Degas text
  const degasText = document.getElementById('brew-degas-text');
  if (degasText) degasText.textContent = data.degassing_protocol;

  // 4. Preparation steps
  const stepsList = document.getElementById('brew-steps-list');
  if (stepsList) {
    stepsList.innerHTML = '';
    data.preparation_steps.forEach(step => {
      const li = document.createElement('li');
      li.textContent = step;
      stepsList.appendChild(li);
    });
  }

  // 5. Indicators
  const indList = document.getElementById('brew-indicators-list');
  if (indList) {
    indList.innerHTML = '';
    data.maturation_indicators.forEach(ind => {
      const li = document.createElement('li');
      li.style.marginBottom = '4px';
      li.textContent = ind;
      indList.appendChild(li);
    });
  }
}

// 3.2 Field Scale Scheduler & Dosing
function initPOCFieldScheduleModule() {
  const modeBtnField = document.getElementById('mode-btn-field');
  const modeBtnTank = document.getElementById('mode-btn-tank');
  const fieldInputs = document.getElementById('schedule-field-inputs');
  const tankInputs = document.getElementById('schedule-tank-inputs');
  const fieldResults = document.getElementById('field-schedule-results');
  const tankResults = document.getElementById('dose-result-box');
  const placeholder = document.getElementById('schedule-placeholder');

  // Mode Toggle
  modeBtnField?.addEventListener('click', () => {
    modeBtnField.className = 'btn btn-sm btn-primary';
    modeBtnTank.className = 'btn btn-sm btn-secondary';
    if (fieldInputs) fieldInputs.style.display = 'block';
    if (tankInputs) tankInputs.style.display = 'none';
    if (tankResults) tankResults.style.display = 'none';
    calculateFieldSchedule();
  });

  modeBtnTank?.addEventListener('click', () => {
    modeBtnTank.className = 'btn btn-sm btn-primary';
    modeBtnField.className = 'btn btn-sm btn-secondary';
    if (fieldInputs) fieldInputs.style.display = 'none';
    if (tankInputs) tankInputs.style.display = 'block';
    if (fieldResults) fieldResults.style.display = 'none';
    if (placeholder) placeholder.style.display = 'block';
  });

  // Area chips
  const areaChips = document.querySelectorAll('#field-area-chips .chip-btn');
  const areaInput = document.getElementById('field-area-input');
  areaChips.forEach(chip => {
    chip.addEventListener('click', () => {
      areaChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const area = chip.getAttribute('data-area');
      if (areaInput) {
        areaInput.value = area;
        calculateFieldSchedule();
      }
    });
  });

  document.getElementById('btn-calc-field-schedule')?.addEventListener('click', calculateFieldSchedule);
  document.getElementById('field-crop-select')?.addEventListener('change', calculateFieldSchedule);
  document.getElementById('field-tank-cap-select')?.addEventListener('change', calculateFieldSchedule);

  // Tank calc button
  document.getElementById('btn-calc-dose')?.addEventListener('click', calculateLiquidDose);

  // Initial field schedule run
  calculateFieldSchedule();
}

async function calculateFieldSchedule() {
  const crop = document.getElementById('field-crop-select')?.value || 'Padi Sawah';
  const area = parseFloat(document.getElementById('field-area-input')?.value || '1000');
  const tankCap = parseFloat(document.getElementById('field-tank-cap-select')?.value || '16');

  const btn = document.getElementById('btn-calc-field-schedule');
  if (btn) btn.innerHTML = '📅 Menyusun Jadwal...';

  try {
    const res = await fetch('/api/liquid/field-schedule', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        crop_name: crop,
        land_area_sqm: area,
        tank_capacity_liters: tankCap
      })
    });

    if (!res.ok) throw new Error('Failed to generate schedule');
    const data = await res.json();
    renderFieldScheduleResult(data);
  } catch (err) {
    console.error('Schedule error:', err);
  } finally {
    if (btn) btn.innerHTML = 'Susun Kalender Aplikasi & Kebutuhan Musim';
  }
}

function renderFieldScheduleResult(data) {
  const placeholder = document.getElementById('schedule-placeholder');
  const resultsBox = document.getElementById('field-schedule-results');
  const badge = document.getElementById('schedule-output-badge');

  if (placeholder) placeholder.style.display = 'none';
  if (resultsBox) resultsBox.style.display = 'block';
  if (badge) badge.textContent = `${data.crop_name} (${data.land_area_desc})`;

  // Metrics
  document.getElementById('field-metric-poc').textContent = `${data.total_seasonal_poc_liters} L`;
  document.getElementById('field-metric-poc-sub').textContent = `Lahan ${data.land_area_desc}`;
  document.getElementById('field-metric-water').textContent = `${data.total_seasonal_water_liters} L`;
  document.getElementById('field-metric-water-sub').textContent = `± ${Math.round(data.total_seasonal_water_liters / data.tank_capacity_liters)} Tangki Total`;
  document.getElementById('field-metric-rounds').textContent = `${data.total_spraying_rounds} Fase`;

  // Savings
  const savingsText = document.getElementById('field-savings-text');
  if (savingsText) savingsText.textContent = data.economic_savings_est;

  // Timeline
  const container = document.getElementById('field-timeline-container');
  if (container) {
    container.innerHTML = '';
    data.stages.forEach(st => {
      const item = document.createElement('div');
      item.className = 'timeline-item';
      item.innerHTML = `
        <div class="timeline-header">
          <div class="timeline-stage-title">${st.stage_name}</div>
          <span class="timeline-timing">${st.timing}</span>
        </div>
        <p style="font-size:0.83rem; color:var(--text-muted); margin-bottom:6px;"><strong>🎯 Target Fokus:</strong> ${st.target_focus}</p>
        <div style="display:flex; flex-wrap:wrap; gap:10px; font-size:0.82rem; background:#f8fafc; padding:8px 10px; border-radius:6px; margin-bottom:6px;">
          <span>💧 <strong>Dosis per Tangki:</strong> <span style="color:#047857; font-weight:700;">${st.dose_per_tank}</span></span>
          <span>🚜 <strong>Metode:</strong> ${st.method}</span>
          <span>⚡ <strong>Volume Musim Ini:</strong> ${st.poc_volume_est} L POC / ${st.water_volume_est} L Air</span>
        </div>
        <div style="font-size:0.8rem; color:#64748b;">💡 <em>Catatan: ${st.notes}</em></div>
      `;
      container.appendChild(item);
    });
  }

  // Rules list
  const rulesList = document.getElementById('field-rules-list');
  if (rulesList) {
    rulesList.innerHTML = '';
    data.application_rules.forEach(rule => {
      const li = document.createElement('li');
      li.style.marginBottom = '4px';
      li.textContent = rule;
      rulesList.appendChild(li);
    });
  }
}

// 3.3 Enriched POC Recipes with Filtering, Search & Dynamic Volume Scaling
async function initPOCRecipesModule() {
  const container = document.getElementById('liquid-recipes-container');
  const searchInput = document.getElementById('recipe-search-input');
  const filterChips = document.querySelectorAll('#recipe-filter-chips .chip-btn');
  const scaleChips = document.querySelectorAll('#recipe-global-scale-chips .chip-btn');
  const scaleInput = document.getElementById('recipe-global-scale-input');

  // Scale chips listener
  scaleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      scaleChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const val = parseFloat(chip.getAttribute('data-rvol') || '20');
      currentGlobalRecipeVol = val;
      if (scaleInput) scaleInput.value = val;
      filterPOCRecipes();
    });
  });

  // Scale input listener
  scaleInput?.addEventListener('input', () => {
    const val = parseFloat(scaleInput.value);
    if (!isNaN(val) && val > 0) {
      currentGlobalRecipeVol = val;
      scaleChips.forEach(c => {
        if (parseFloat(c.getAttribute('data-rvol')) === val) {
          c.classList.add('active');
        } else {
          c.classList.remove('active');
        }
      });
      filterPOCRecipes();
    }
  });

  try {
    const res = await fetch('/api/liquid/recipes');
    const data = await res.json();
    allPocRecipes = data.poc_recipes || [];
    allMols = data.mol_collection || [];

    renderPOCRecipes(allPocRecipes);
    renderMOLCollection(allMols);
  } catch (err) {
    console.error('Failed to load POC recipes:', err);
    if (container) container.innerHTML = '<p style="color:var(--danger);">Gagal memuat resep POC dari server.</p>';
  }

  // Search filter
  searchInput?.addEventListener('input', () => {
    filterPOCRecipes();
  });

  // Category chip filter
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      filterPOCRecipes();
    });
  });
}

function filterPOCRecipes() {
  const query = document.getElementById('recipe-search-input')?.value.toLowerCase().trim() || '';
  const activeChip = document.querySelector('#recipe-filter-chips .chip-btn.active');
  const category = activeChip?.getAttribute('data-filter') || 'all';

  const filtered = allPocRecipes.filter(r => {
    const matchQuery = !query || r.title.toLowerCase().includes(query) || r.materials.some(m => m.toLowerCase().includes(query)) || r.highlights.toLowerCase().includes(query);
    let matchCat = true;
    if (category === 'vegetatif') matchCat = r.category.toLowerCase().includes('vegetatif') || r.title.toLowerCase().includes('vegetatif') || r.title.toLowerCase().includes('urine') || r.title.toLowerCase().includes('amino');
    else if (category === 'generatif') matchCat = r.category.toLowerCase().includes('generatif') || r.category.toLowerCase().includes('bunga') || r.title.toLowerCase().includes('kalium');
    else if (category === 'proteksi') matchCat = r.category.toLowerCase().includes('proteksi') || r.category.toLowerCase().includes('imun') || r.title.toLowerCase().includes('empon') || r.title.toLowerCase().includes('silika');
    else if (category === 'spesialis') matchCat = r.title.toLowerCase().includes('psb') || r.title.toLowerCase().includes('eco enzyme') || r.title.toLowerCase().includes('jakaba') || r.category.toLowerCase().includes('enzim');

    return matchQuery && matchCat;
  });

  renderPOCRecipes(filtered);
}

function renderPOCRecipes(recipes) {
  const container = document.getElementById('liquid-recipes-container');
  if (!container) return;

  if (recipes.length === 0) {
    container.innerHTML = '<p style="text-align:center; padding:30px; color:var(--text-muted);">Tidak ada resep POC yang cocok dengan filter pencarian.</p>';
    return;
  }

  container.innerHTML = '';
  recipes.forEach(poc => {
    const baseLiters = poc.base_batch_liters || 10.0;
    const scaleFactor = currentGlobalRecipeVol / baseLiters;
    const isScaled = Math.abs(scaleFactor - 1.0) > 0.001;

    // Render scaled ingredients if structured data is available
    let ingredientsHtml = '';
    if (poc.ingredients_structured && poc.ingredients_structured.length > 0) {
      ingredientsHtml = poc.ingredients_structured.map(ing => {
        const scaledQty = ing.amount * scaleFactor;
        let formattedQty;
        if (scaledQty >= 10) {
          formattedQty = Number.isInteger(scaledQty) ? scaledQty : scaledQty.toFixed(1);
        } else if (scaledQty >= 1) {
          formattedQty = Number.isInteger(scaledQty) ? scaledQty : scaledQty.toFixed(2).replace(/\.?0+$/, '');
        } else {
          formattedQty = scaledQty.toFixed(2).replace(/\.?0+$/, '');
        }
        return `<span class="pill" style="background:#ecfdf5; border-color:#a7f3d0; color:#064e3b; font-size:0.83rem; padding:4px 10px;"><strong>${ing.name}:</strong> <span style="font-weight:700; color:#047857;">${formattedQty}</span> ${ing.unit}</span>`;
      }).join('');
    } else {
      // Fallback
      ingredientsHtml = poc.materials.map(m => `<span class="pill">${m}</span>`).join('');
    }

    const card = document.createElement('div');
    card.className = 'recipe-card';
    card.innerHTML = `
      <div class="recipe-header">
        <div class="recipe-title">${poc.title}</div>
        <span class="recipe-tag">⏱️ Fermentasi: ${poc.fermentation_days}</span>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
        <span style="color:#d97706; font-size:0.85rem; font-weight:600;">🏷️ Kategori: ${poc.category}</span>
        <span style="background:${isScaled ? '#fef3c7' : '#e0f2fe'}; color:${isScaled ? '#92400e' : '#0369a1'}; border:1px solid ${isScaled ? '#fde68a' : '#bae6fd'}; border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:700;">
          📏 Skala: ${currentGlobalRecipeVol} L (${isScaled ? scaleFactor.toFixed(2) + 'x Resep Acuan ' + baseLiters + 'L' : 'Formula Acuan'})
        </span>
      </div>
      <p style="color:var(--text-muted); font-size:0.88rem; margin-bottom:12px;">${poc.highlights}</p>
      
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="font-size:0.85rem; font-weight:700; color:#059669;">🌿 Takaran Bahan Dinamis (${currentGlobalRecipeVol} Liter):</div>
        <span style="font-size:0.75rem; color:#64748b; font-style:italic;">Proporsional otomatis</span>
      </div>
      <div class="ingredient-pills" style="margin-bottom:12px;">
        ${ingredientsHtml}
      </div>

      <div style="font-size:0.85rem; font-weight:600; color:#334155; margin-bottom:6px;">🛠️ Cara Pembuatan:</div>
      <ol class="step-list">
        ${poc.steps.map(s => `<li>${s}</li>`).join('')}
      </ol>

      ${poc.upgrade_zpt ? `
        <div style="margin-top:12px; padding:10px; background:#ecfdf5; border-left:3px solid #059669; border-radius:4px; font-size:0.85rem; color:#064e3b;">
          <strong>⚡ Panduan Upgrade ZPT & Dosis:</strong><br>
          ${poc.upgrade_zpt.vegetatif ? `• Vegetatif: ${poc.upgrade_zpt.vegetatif}<br>` : ''}
          ${poc.upgrade_zpt.generatif ? `• Generatif: ${poc.upgrade_zpt.generatif}<br>` : ''}
          ${poc.upgrade_zpt.all_purpose ? `• Dosis Umum: ${poc.upgrade_zpt.all_purpose}` : ''}
        </div>
      ` : ''}

      <div style="margin-top:14px; padding-top:12px; border-top:1px dashed #cbd5e1; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <span style="font-size:0.82rem; color:#64748b;">Ingin meracik formula ini dalam drum besar?</span>
        <button type="button" class="btn btn-sm btn-secondary btn-load-to-brew" 
          data-recipe-title="${poc.title}" 
          data-recipe-cat="${poc.category}" 
          style="font-size:0.8rem; padding:5px 12px; font-weight:600;">
          🚀 Muat ke Formulator Drum (${currentGlobalRecipeVol} L)
        </button>
      </div>
    `;

    // Add listener to the "Muat ke Formulator Drum" button
    const loadBtn = card.querySelector('.btn-load-to-brew');
    loadBtn?.addEventListener('click', () => {
      loadRecipeToDrumFormulator(poc, currentGlobalRecipeVol);
    });

    container.appendChild(card);
  });
}

function loadRecipeToDrumFormulator(poc, vol) {
  // 1. Switch to sub-tab 1 (liquid-sub-brew)
  const brewSubTabBtn = document.querySelector('.liquid-sub-tabs .sub-tab-btn[data-subtarget="liquid-sub-brew"]');
  if (brewSubTabBtn) {
    brewSubTabBtn.click();
  }

  // 2. Set drum volume input and sync preset chips
  const volInput = document.getElementById('brew-vol-input');
  if (volInput) {
    volInput.value = vol;
  }
  const volChips = document.querySelectorAll('#brew-vol-chips .chip-btn');
  volChips.forEach(c => {
    if (parseFloat(c.getAttribute('data-vol')) === vol) {
      c.classList.add('active');
    } else {
      c.classList.remove('active');
    }
  });

  // 3. Set purpose select based on recipe category
  const purposeSelect = document.getElementById('brew-purpose-select');
  if (purposeSelect) {
    const cat = (poc.category || '').toLowerCase();
    const title = (poc.title || '').toLowerCase();
    if (cat.includes('vegetatif') || title.includes('urine') || title.includes('amino') || title.includes('daun')) {
      purposeSelect.value = 'vegetatif';
    } else if (cat.includes('generatif') || cat.includes('bunga') || title.includes('kalium') || title.includes('buah')) {
      purposeSelect.value = 'generatif';
    } else if (cat.includes('proteksi') || cat.includes('imun') || title.includes('silika') || title.includes('empon')) {
      purposeSelect.value = 'proteksi';
    } else {
      purposeSelect.value = 'all_purpose';
    }
  }

  // 4. Trigger calculation
  calculatePOCBatchBrew();

  // 5. Smooth scroll to formulator
  document.getElementById('liquid-sub-brew')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// 3.4 MOL Collection & ZPT Bank
function initMOLModule() {
  const molFilterChips = document.querySelectorAll('#mol-filter-chips .chip-btn');
  molFilterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      molFilterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const cat = chip.getAttribute('data-molfilter') || 'all';

      const filtered = allMols.filter(m => {
        if (cat === 'all') return true;
        if (cat === 'sitokinin') return m.hormone.toLowerCase().includes('sitokinin');
        if (cat === 'giberelin') return m.hormone.toLowerCase().includes('giberelin');
        if (cat === 'kalium') return m.hormone.toLowerCase().includes('kalium');
        if (cat === 'nitrogen') return m.hormone.toLowerCase().includes('nitrogen') || m.hormone.toLowerCase().includes('amino');
        if (cat === 'proteksi') return m.hormone.toLowerCase().includes('fungisida') || m.hormone.toLowerCase().includes('enzim') || (m.category && m.category.toLowerCase().includes('proteksi'));
        return true;
      });

      renderMOLCollection(filtered);
    });
  });
}

function renderMOLCollection(mols) {
  const molContainer = document.getElementById('mol-collection-container');
  if (!molContainer) return;

  molContainer.innerHTML = '';
  mols.forEach(mol => {
    const div = document.createElement('div');
    div.className = 'recipe-card';
    div.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <strong style="color:#059669; font-size:1.05rem;">${mol.name}</strong>
        <span class="status-badge pass">${mol.hormone}</span>
      </div>
      <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:10px;">${mol.function}</p>
      <div style="font-size:0.85rem; color:#1e293b; background:#f8fafc; border:1px solid #e2e8f0; padding:10px 12px; border-radius:6px;">
        <strong style="color:#047857;">🧪 Resep & Cara Biakan:</strong><br>
        ${mol.recipe}
      </div>
    `;
    molContainer.appendChild(div);
  });
}

// 3.5 Doctor POC & Tank-Mix Module
async function initPOCTroubleshootModule() {
  const symptomSelect = document.getElementById('trouble-symptom-select');
  const mixContainer = document.getElementById('tank-mix-container');

  try {
    // 1. Fetch troubleshooting data
    const resT = await fetch('/api/liquid/troubleshooting');
    troubleshootData = await resT.json();

    symptomSelect?.addEventListener('change', () => {
      displayTroubleshootDetail(symptomSelect.value);
    });

    if (troubleshootData.length > 0) {
      displayTroubleshootDetail(troubleshootData[0].id);
    }

    // 2. Fetch tank-mix data
    const resM = await fetch('/api/liquid/tank-mix-guide');
    tankMixData = await resM.json();

    if (mixContainer) {
      mixContainer.innerHTML = '';
      tankMixData.forEach(item => {
        let badgeClass = 'risk-safe';
        if (item.status.includes('DILARANG')) badgeClass = 'risk-danger';
        else if (item.status.includes('Syarat')) badgeClass = 'risk-warning';

        const card = document.createElement('div');
        card.style.cssText = 'background:#ffffff; border:1px solid #e2e8f0; border-radius:var(--radius-sm); padding:12px; margin-bottom:8px;';
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="font-size:0.9rem; color:#0f172a;">${item.partner_material}</strong>
            <span class="risk-badge ${badgeClass}">${item.status}</span>
          </div>
          <div style="font-size:0.82rem; color:#047857; font-weight:600; margin-bottom:4px;">📋 Aturan: ${item.rule}</div>
          <div style="font-size:0.8rem; color:#64748b;">🔬 <em>Alasan Sains: ${item.scientific_reason}</em></div>
        `;
        mixContainer.appendChild(card);
      });
    }

  } catch (err) {
    console.error('Failed to load troubleshooting data:', err);
  }
}

function displayTroubleshootDetail(id) {
  const item = troubleshootData.find(t => t.id === id);
  if (!item) return;

  document.getElementById('trouble-title').textContent = item.symptom;
  const badge = document.getElementById('trouble-risk-badge');
  if (badge) {
    badge.textContent = `Tingkat Bahaya: ${item.risk_level}`;
    badge.className = 'risk-badge ' + (item.risk_level.includes('Aman') ? 'risk-safe' : (item.risk_level.includes('Waspada') ? 'risk-warning' : 'risk-danger'));
  }

  document.getElementById('trouble-cause-text').textContent = item.cause;

  const solList = document.getElementById('trouble-solutions-list');
  if (solList) {
    solList.innerHTML = '';
    item.solution.forEach(s => {
      const li = document.createElement('li');
      li.style.marginBottom = '4px';
      li.textContent = s;
      solList.appendChild(li);
    });
  }

  document.getElementById('trouble-prevention-text').textContent = item.prevention;
}

// 3.6 Quick Tank Dosing & SNI Check
async function calculateLiquidDose() {
  const pocType = document.getElementById('dose-poc-type')?.value || 'POC ROTAN Premium';
  const crop = document.getElementById('dose-crop')?.value || 'Sayuran Daun';
  const method = document.getElementById('dose-method')?.value || 'Semprot Daun (Spraying)';
  const vol = parseFloat(document.getElementById('dose-vol')?.value || '16');

  try {
    const res = await fetch('/api/liquid/calculate-dose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        poc_type: pocType,
        crop_category: crop,
        application_method: method,
        volume_liters: vol
      })
    });

    const data = await res.json();
    renderDoseResult(data);
  } catch (err) {
    console.error('Dose calc error:', err);
  }
}

function renderDoseResult(data) {
  const resBox = document.getElementById('dose-result-box');
  const placeholder = document.getElementById('schedule-placeholder');
  if (!resBox) return;

  if (placeholder) placeholder.style.display = 'none';
  resBox.style.display = 'block';
  resBox.innerHTML = `
    <div class="grid-3" style="margin-bottom:14px;">
      <div class="metric-box">
        <div class="metric-label">Kebutuhan POC</div>
        <div class="metric-value" style="color:#059669;">${data.recommended_poc_cc} cc/ml</div>
        <div class="metric-sub info">Untuk ${data.water_volume_liters} Liter Air</div>
      </div>
      <div class="metric-box">
        <div class="metric-label">Rasio Pengenceran</div>
        <div class="metric-value" style="color:#2563eb;">${data.dilution_ratio}</div>
        <div class="metric-sub">Standar Aman Daun</div>
      </div>
      <div class="metric-box">
        <div class="metric-label">Waktu Optimal</div>
        <div class="metric-value" style="font-size:1.0rem; color:#d97706;">Pagi / Sore</div>
        <div class="metric-sub">Stomata Terbuka</div>
      </div>
    </div>
    <div style="background:#f8fafc; padding:14px; border-radius:var(--radius-sm); border:1px solid #e2e8f0;">
      <p style="margin-bottom:6px;"><strong>⏱️ Frekuensi Aplikasi:</strong> ${data.application_frequency}</p>
      <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px;"><strong>💡 Petunjuk Teknis:</strong></p>
      <ul style="padding-left:18px; font-size:0.85rem; color:#334155;">
        ${data.special_tips.map(t => `<li style="margin-bottom:4px;">${t}</li>`).join('')}
      </ul>
    </div>
  `;
}

async function checkLiquidSNI() {
  const cOrg = parseFloat(document.getElementById('sni-c-organic')?.value || '12.5');
  const npk = parseFloat(document.getElementById('sni-npk')?.value || '3.5');
  const ph = parseFloat(document.getElementById('sni-ph')?.value || '6.8');
  const salm = document.getElementById('sni-salmonella')?.value || 'Negatif';
  const ecoli = parseFloat(document.getElementById('sni-ecoli')?.value || '10');

  try {
    const res = await fetch('/api/liquid/sni-check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        c_organic_pct: cOrg,
        total_npk_pct: npk,
        ph: ph,
        pathogen_salmonella: salm,
        pathogen_ecoli_cfu: ecoli
      })
    });

    const data = await res.json();
    renderLiquidSNIResult(data);
  } catch (err) {
    console.error('SNI Check error:', err);
  }
}

function renderLiquidSNIResult(data) {
  const resBox = document.getElementById('liquid-sni-result-box');
  const placeholder = document.getElementById('liquid-sni-placeholder');
  if (!resBox) return;

  if (placeholder) placeholder.style.display = 'none';
  resBox.style.display = 'block';
  const isPass = data.overall_status.includes('Memenuhi');

  resBox.innerHTML = `
    <div style="padding:14px; border-radius:var(--radius-md); background:${isPass ? 'rgba(5,150,105,0.08)' : 'rgba(220,38,38,0.08)'}; border:1px solid ${isPass ? '#059669' : '#dc2626'}; margin-bottom:14px;">
      <h4 style="color:${isPass ? '#047857' : '#b91c1c'};">${isPass ? '✅' : '⚠️'} ${data.overall_status}</h4>
    </div>
    <table class="sni-table" style="margin-bottom:14px;">
      <thead>
        <tr>
          <th>Parameter Mutu POC</th>
          <th>Hasil Uji</th>
          <th>Baku Mutu (Permentan 261/2019)</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        ${data.details.map(d => `
          <tr>
            <td><strong>${d.parameter}</strong></td>
            <td>${d.measured_value} ${d.unit}</td>
            <td>${d.standard_range} ${d.unit}</td>
            <td><span class="status-badge ${d.status.includes('Lolos') ? 'pass' : 'fail'}">${d.status}</span></td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <div style="font-size:0.85rem; color:#334155; background:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:6px;">
      <strong style="color:#064e3b;">📌 Catatan & Saran Perbaikan Formula:</strong><br>
      ${data.improvement_advice.map(a => `• ${a}`).join('<br>')}
    </div>
  `;
}


// 4. Economics & HPP Module
function initEconomicsModule() {
 document.getElementById('btn-calc-economics')?.addEventListener('click', calculateEconomics);
}

async function calculateEconomics() {
 const type = document.getElementById('eco-type')?.value || 'Padat (kg)';
 const vol = parseFloat(document.getElementById('eco-volume')?.value || '1000');
 const rawCost = parseFloat(document.getElementById('eco-raw-cost')?.value || '250000');
 const bioCost = parseFloat(document.getElementById('eco-bio-cost')?.value || '80000');
 const labor = parseFloat(document.getElementById('eco-labor-cost')?.value || '300000');
 const packCost = parseFloat(document.getElementById('eco-pack-cost')?.value || '150000');
 const capex = parseFloat(document.getElementById('eco-capex')?.value || '10000000');
 const depMonths = parseInt(document.getElementById('eco-dep-months')?.value || '36');
 const sellPrice = parseFloat(document.getElementById('eco-price')?.value || '2500');

 try {
 const res = await fetch('/api/economics/calculate', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({
 fertilizer_type: type,
 batch_volume: vol,
 raw_material_cost: rawCost,
 bioactivator_cost: bioCost,
 labor_cost: labor,
 energy_packaging_cost: packCost,
 capex_equipment: capex,
 depreciation_months: depMonths,
 target_selling_price: sellPrice
 })
 });

 const data = await res.json();
 renderEconomicsResult(data);

 } catch (err) {
 console.error('Economics calc error:', err);
 }
}

function renderEconomicsResult(data) {
 const resBox = document.getElementById('eco-results-box');
 if (!resBox) return;

 resBox.style.display = 'block';
 const unitName = data.fertilizer_type.includes('Padat') ? 'kg' : 'Liter/Botol';

 document.getElementById('eco-hpp-val').textContent = `Rp ${Math.round(data.unit_cost_hpp).toLocaleString('id-ID')}`;
 document.getElementById('eco-profit-val').textContent = `Rp ${Math.round(data.net_profit).toLocaleString('id-ID')}`;
 document.getElementById('eco-margin-val').textContent = `${data.profit_margin_pct}%`;
 document.getElementById('eco-bep-val').textContent = `${data.break_even_units.toLocaleString('id-ID')} ${unitName}`;

 // Insights
 const insightElem = document.getElementById('eco-insights-list');
 if (insightElem) {
 insightElem.innerHTML = data.insights.map(i => `<li>${i}</li>`).join('');
 }

 // Chart
 renderEconomicsChart(data);
}

function renderEconomicsChart(data) {
 const ctx = document.getElementById('eco-chart-canvas');
 if (!ctx) return;

 if (economicsChart) economicsChart.destroy();

 economicsChart = new Chart(ctx, {
 type: 'doughnut',
 data: {
 labels: ['Total Biaya Produksi (HPP)', 'Keuntungan Bersih (Laba)'],
 datasets: [{
 data: [data.total_production_cost, Math.max(0, data.net_profit)],
 backgroundColor: [
 'rgba(239, 68, 68, 0.8)',
 'rgba(16, 185, 129, 0.8)'
 ],
 borderColor: '#ffffff',
 borderWidth: 2
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 plugins: {
 legend: {
 position: 'bottom',
 labels: { color: '#334155' }
 }
 }
 }
 });
}

// Utility: Debounce function for live reactive inputs
function debounce(func, wait) {
 let timeout;
 return function executedFunction(...args) {
 const later = () => {
 clearTimeout(timeout);
 func(...args);
 };
 clearTimeout(timeout);
 timeout = setTimeout(later, wait);
 };
}
