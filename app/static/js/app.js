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
 document.getElementById('solid-weight-metric').textContent = `${data.total_weight_kg.toLocaleString()} kg`;
 document.getElementById('solid-npk-metric').textContent = `${data.final_n_pct}% - ${data.final_p_pct}% - ${data.final_k_pct}%`;
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
 renderSolidNPKChart(data.final_n_pct, data.final_p_pct, data.final_k_pct, data.final_carbon_pct);

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
 grid: { color: 'rgba(255, 255, 255, 0.05)' },
 ticks: { color: '#94a3b8' }
 },
 x: {
 grid: { display: false },
 ticks: { color: '#f8fafc' }
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
 labels: { color: '#cbd5e1' }
 }
 },
 scales: {
 y: {
 min: 5,
 max: Math.max(40, initialCN + 5),
 grid: { color: 'rgba(255, 255, 255, 0.05)' },
 ticks: { color: '#94a3b8' }
 },
 x: {
 grid: { display: false },
 ticks: { color: '#cbd5e1' }
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
 <td style="color:#34d399; font-weight:700;">${m.recommended_kg} kg</td>
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
 if (inp) inp.value = m.recommended_kg;
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

// 3. Liquid Fertilizer Module (Fitur 2: Pupuk Cair & Bioaktivator)
async function initLiquidModule() {
 const pocContainer = document.getElementById('liquid-recipes-container');
 const molContainer = document.getElementById('mol-collection-container');

 try {
 const res = await fetch('/api/liquid/recipes');
 const data = await res.json();
 const pocRecipes = data.poc_recipes || [];
 const mols = data.mol_collection || [];

 if (pocContainer) {
 pocContainer.innerHTML = '';
 pocRecipes.forEach(poc => {
 const card = document.createElement('div');
 card.className = 'recipe-card';
 card.innerHTML = `
 <div class="recipe-header">
 <div class="recipe-title">${poc.title}</div>
 <span class="recipe-tag">Fermentasi: ${poc.fermentation_days}</span>
 </div>
 <p style="color:#f59e0b; font-size:0.85rem; margin-bottom:10px;"><strong>Kategori:</strong> ${poc.category}</p>
 <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:12px;">${poc.highlights}</p>
 
 <div style="font-size:0.85rem; font-weight:600; color:#38bdf8; margin-bottom:6px;"> Bahan-Bahan:</div>
 <div class="ingredient-pills">
 ${poc.materials.map(m => `<span class="pill">${m}</span>`).join('')}
 </div>

 <div style="font-size:0.85rem; font-weight:600; color:#cbd5e1; margin-bottom:6px;">️ Cara Pembuatan:</div>
 <ol class="step-list">
 ${poc.steps.map(s => `<li>${s}</li>`).join('')}
 </ol>

 ${poc.upgrade_zpt ? `
 <div style="margin-top:12px; padding:10px; background:rgba(16,185,129,0.08); border-left:3px solid var(--primary); border-radius:4px; font-size:0.85rem;">
 <strong> Upgrade ZPT & Dosis:</strong><br>
 ${poc.upgrade_zpt.vegetatif ? `• Vegetatif: ${poc.upgrade_zpt.vegetatif}<br>` : ''}
 ${poc.upgrade_zpt.generatif ? `• Generatif: ${poc.upgrade_zpt.generatif}` : ''}
 </div>
 ` : ''}
 `;
 pocContainer.appendChild(card);
 });
 }

 if (molContainer) {
 molContainer.innerHTML = '';
 mols.forEach(mol => {
 const div = document.createElement('div');
 div.className = 'recipe-card';
 div.innerHTML = `
 <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
 <strong style="color:#34d399; font-size:1.05rem;">${mol.name}</strong>
 <span class="status-badge pass">${mol.hormone}</span>
 </div>
 <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:8px;">${mol.function}</p>
 <div style="font-size:0.85rem; color:#cbd5e1; background:rgba(0,0,0,0.3); padding:8px 12px; border-radius:6px;">
 <strong>Resep:</strong> ${mol.recipe}
 </div>
 `;
 molContainer.appendChild(div);
 });
 }

 } catch (err) {
 console.error('Failed loading liquid recipes:', err);
 }

 // Liquid Dose Calculator Event
 document.getElementById('btn-calc-dose')?.addEventListener('click', calculateLiquidDose);

 // Liquid SNI Check Event
 document.getElementById('btn-check-liquid-sni')?.addEventListener('click', checkLiquidSNI);
}

async function calculateLiquidDose() {
 const pocType = document.getElementById('dose-poc-type')?.value || 'POC ROTAN Premium';
 const crop = document.getElementById('dose-crop')?.value || 'Sayuran Daun';
 const method = document.getElementById('dose-method')?.value || 'Semprot Daun (Spraying)';
 const vol = parseFloat(document.getElementById('dose-vol')?.value || '14');

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
 if (!resBox) return;

 resBox.style.display = 'block';
 resBox.innerHTML = `
 <div class="grid-3" style="margin-bottom:14px;">
 <div class="metric-box">
 <div class="metric-label">Kebutuhan POC</div>
 <div class="metric-value" style="color:#34d399;">${data.recommended_poc_cc} cc/ml</div>
 <div class="metric-sub info">Untuk ${data.water_volume_liters} Liter Air</div>
 </div>
 <div class="metric-box">
 <div class="metric-label">Rasio Pengenceran</div>
 <div class="metric-value" style="color:#38bdf8;">${data.dilution_ratio}</div>
 <div class="metric-sub">Standar Aman Daun</div>
 </div>
 <div class="metric-box">
 <div class="metric-label">Waktu Optimal</div>
 <div class="metric-value" style="font-size:1.1rem; color:#facc15;">Pagi / Sore</div>
 <div class="metric-sub success">Stomata Terbuka</div>
 </div>
 </div>
 <div style="background:rgba(15,23,42,0.6); padding:14px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle);">
 <p style="margin-bottom:6px;"><strong>️ Frekuensi Aplikasi:</strong> ${data.application_frequency}</p>
 <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:8px;"><strong> Petunjuk Teknis:</strong></p>
 <ul style="padding-left:18px; font-size:0.85rem; color:#cbd5e1;">
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

 try {
 const res = await fetch('/api/liquid/sni-check', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({
 c_organic_pct: cOrg,
 total_npk_pct: npk,
 ph: ph,
 pathogen_salmonella: salm
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
 if (!resBox) return;

 resBox.style.display = 'block';
 const isPass = data.overall_status.includes('Memenuhi');

 resBox.innerHTML = `
 <div style="padding:14px; border-radius:var(--radius-md); background:${isPass ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)'}; border:1px solid ${isPass ? 'var(--primary)' : 'var(--danger)'}; margin-bottom:14px;">
 <h4 style="color:${isPass ? '#34d399' : '#f87171'};">${isPass ? '' : '️'} ${data.overall_status}</h4>
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
 <div style="font-size:0.85rem; color:var(--text-muted); background:rgba(0,0,0,0.3); padding:10px; border-radius:6px;">
 <strong>Catatan & Saran Perbaikan:</strong><br>
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
 borderColor: 'rgba(15, 23, 42, 0.8)',
 borderWidth: 2
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: false,
 plugins: {
 legend: {
 position: 'bottom',
 labels: { color: '#cbd5e1' }
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
