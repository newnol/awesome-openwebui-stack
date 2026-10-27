import { CATEGORIES, TYPES, STATUS, DEFAULTS, readState, writeState, selectEntries, validateCatalog } from './catalog.mjs';
const $ = id => document.getElementById(id);
let entries = []; let state = readState(location.search);
const form = $('filters'); const grid = $('results'); const notice = $('notice');
function announce(text) { notice.textContent = text; }
function externalLink(element, url) { element.href = url; element.target = '_blank'; element.rel = 'noopener noreferrer'; }
function populate(id, values) {
  for (const [value, label] of values) { const option = document.createElement('option'); option.value = value; option.textContent = label; $(id).append(option); }
}
populate('type', TYPES.map(v => [v, v[0].toUpperCase() + v.slice(1)]));
populate('category', CATEGORIES.map(v => [v, v === 'rag' ? 'RAG' : v.replaceAll('-', ' ')]));
populate('status', Object.entries(STATUS));
function syncForm() {
  for (const key of ['q', 'type', 'category', 'status', 'sort']) $(key).value = state[key];
  $('unavailable').checked = state.unavailable;
}
function syncURL(push = false) {
  const query = writeState(state);
  const url = location.pathname + (query ? `?${query}` : '');
  if (url !== location.pathname + location.search) history[push ? 'pushState' : 'replaceState'](null, '', url);
}
function render() {
  const filtered = selectEntries(entries, state);
  grid.replaceChildren();
  for (const entry of filtered) {
    const card = $('entry-template').content.cloneNode(true);
    card.querySelector('article').id = entry.id;
    card.querySelector('h3').textContent = entry.name;
    card.querySelector('.kind').textContent = entry.type;
    card.querySelector('.summary').textContent = entry.summary;
    card.querySelector('.evidence').textContent = STATUS[entry.status];
    card.querySelector('.evidence').dataset.status = entry.status;
    card.querySelector('.tags').textContent = entry.categories.join(' / ');
    card.querySelector('.review').textContent = `Source checked ${entry.reviewed}. ${entry.review_note}`;
    card.querySelector('.compatibility').textContent = entry.compatibility;
    card.querySelector('.requirements').textContent = entry.requirements.join(' / ');
    card.querySelector('.risk').textContent = entry.risk;
    card.querySelector('.license').textContent = entry.license;
    externalLink(card.querySelector('.source'), entry.source);
    externalLink(card.querySelector('.guide'), entry.guide);
    externalLink(card.querySelector('.evidence-link'), entry.evidence);
    const box = card.querySelector('input');
    box.checked = state.compare.includes(entry.id);
    box.setAttribute('aria-label', `Compare ${entry.name}`);
    box.addEventListener('change', () => {
      if (box.checked && state.compare.length >= 3) { box.checked = false; announce('Compare up to three entries. Remove one first.'); return; }
      state.compare = box.checked ? [...state.compare, entry.id] : state.compare.filter(id => id !== entry.id);
      syncURL(); updateCompare(); announce('');
    });
    grid.append(card);
  }
  $('result-count').textContent = `${filtered.length} ${filtered.length === 1 ? 'entry' : 'entries'} shown`;
  $('empty').hidden = filtered.length !== 0;
  const hidden = entries.filter(e => e.status === 'unavailable').length;
  $('catalog-stats').textContent = `${entries.length - hidden} documented sources & examples / ${hidden} unavailable listings kept for transparency`;
  updateCompare();
}
function updateCompare() {
  $('compare-button').textContent = `Compare (${state.compare.length}/3)`;
  $('compare-button').disabled = state.compare.length < 2;
  $('clear-compare').disabled = state.compare.length === 0;
}
function applyForm(push = false) {
  for (const key of ['q', 'type', 'category', 'status', 'sort']) state[key] = $(key).value;
  state.unavailable = $('unavailable').checked;
  syncURL(push); render(); announce('');
}
form.addEventListener('submit', event => event.preventDefault());
$('q').addEventListener('input', () => applyForm());
form.addEventListener('change', event => { if (event.target.id !== 'q') applyForm(true); });
function reset() { state = { ...DEFAULTS, compare: state.compare }; syncForm(); syncURL(true); render(); announce('Filters cleared.'); }
$('reset').addEventListener('click', reset); $('empty-reset').addEventListener('click', reset);
for (const button of document.querySelectorAll('[data-preset]')) button.addEventListener('click', () => {
  state = { ...DEFAULTS, compare: state.compare, ...JSON.parse(button.dataset.preset) };
  syncForm(); syncURL(true); render(); $('q').focus();
});
window.addEventListener('popstate', () => { state = readState(location.search); state.compare = state.compare.filter(id => entries.some(e => e.id === id)); syncForm(); render(); });
$('clear-compare').addEventListener('click', () => { state.compare = []; syncURL(); render(); announce('Comparison cleared.'); });
$('compare-button').addEventListener('click', () => {
  const selected = state.compare.map(id => entries.find(e => e.id === id)).filter(Boolean);
  const table = $('comparison'); table.replaceChildren();
  const caption = table.createCaption(); caption.textContent = 'Evidence and requirements, side by side';
  const header = table.createTHead().insertRow();
  for (const text of ['Field', ...selected.map(e => e.name)]) { const th = document.createElement('th'); th.scope = 'col'; th.textContent = text; header.append(th); }
  const body = table.createTBody();
  for (const [key, label] of [['type', 'Type'], ['status', 'Evidence'], ['requirements', 'Requirements'], ['compatibility', 'Compatibility'], ['risk', 'Safety'], ['license', 'License'], ['reviewed', 'Source checked']]) {
    const row = body.insertRow(); const th = document.createElement('th'); th.scope = 'row'; th.textContent = label; row.append(th);
    for (const e of selected) row.insertCell().textContent = key === 'status' ? STATUS[e[key]] : Array.isArray(e[key]) ? e[key].join('; ') : e[key];
  }
  $('compare-dialog').showModal();
});
$('share').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(location.href); announce('Link copied. It includes your filters and comparison.'); }
  catch { announce('Copy the address from your browser to share these filters.'); }
});
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !document.activeElement.isContentEditable && !$('compare-dialog').open) { event.preventDefault(); $('q').focus(); }
});
const media = matchMedia('(prefers-color-scheme: dark)');
function setTheme(theme, persist = false) {
  document.documentElement.dataset.theme = theme;
  $('theme').textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
  $('theme').setAttribute('aria-pressed', String(theme === 'dark'));
  if (persist) { try { localStorage.setItem('catalog-theme', theme); } catch { /* Storage is optional. */ } }
}
let preference; try { preference = localStorage.getItem('catalog-theme'); } catch { /* Private browsing. */ }
setTheme(['dark', 'light'].includes(preference) ? preference : media.matches ? 'dark' : 'light');
$('theme').addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark', true));
syncForm();
try {
  const response = await fetch(new URL('../data/catalog.json', import.meta.url));
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  entries = await response.json();
  const errors = validateCatalog(entries);
  if (errors.length) throw new Error('Catalog metadata is invalid.');
  state.compare = state.compare.filter(id => entries.some(e => e.id === id));
  syncURL(); render(); $('loading').hidden = true;
} catch (error) {
  $('loading').hidden = true; $('load-error').hidden = false;
  $('result-count').textContent = 'Catalog could not be loaded';
  console.error('Catalog load failed:', error);
}
