/** Pure catalog logic, shared by the browser, generator and Node tests. */
export const TYPES = ['tool', 'function', 'pipe', 'stack', 'integration'];
export const CATEGORIES = ['coding', 'research', 'rag', 'automation', 'productivity', 'multi-agent', 'self-hosting', 'security'];
export const STATUS = { documented: 'Source documented', example: 'Example / not runtime-tested', unavailable: 'Implementation unavailable' };
export const DEFAULTS = { q: '', type: '', category: '', status: '', sort: 'name', unavailable: false, compare: [] };
const normalize = value => String(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export function readState(search) {
  const p = new URLSearchParams(search);
  return {
    q: (p.get('q') || '').slice(0, 200),
    type: TYPES.includes(p.get('type')) ? p.get('type') : '',
    category: CATEGORIES.includes(p.get('category')) ? p.get('category') : '',
    status: Object.hasOwn(STATUS, p.get('status')) ? p.get('status') : '',
    sort: p.get('sort') === 'reviewed' ? 'reviewed' : 'name',
    unavailable: p.get('unavailable') === '1',
    compare: [...new Set((p.get('compare') || '').split(',').filter(id => /^[a-z0-9-]+$/.test(id)))].slice(0, 3),
  };
}
export function writeState(state) {
  const p = new URLSearchParams();
  for (const key of ['q', 'type', 'category', 'status']) if (state[key]) p.set(key, state[key]);
  if (state.sort === 'reviewed') p.set('sort', state.sort);
  if (state.unavailable) p.set('unavailable', '1');
  if (state.compare.length) p.set('compare', state.compare.join(','));
  return p.toString();
}
export function selectEntries(entries, state) {
  const terms = normalize(state.q).trim().split(/\s+/).filter(Boolean);
  return entries.filter(entry => {
    if (entry.status === 'unavailable' && !state.unavailable && state.status !== 'unavailable') return false;
    if (state.type && entry.type !== state.type) return false;
    if (state.category && !entry.categories.includes(state.category)) return false;
    if (state.status && entry.status !== state.status) return false;
    const text = normalize([entry.name, entry.summary, entry.type, ...entry.categories, ...entry.requirements].join(' '));
    return terms.every(term => text.includes(term));
  }).sort((a, b) => (state.sort === 'reviewed' ? b.reviewed.localeCompare(a.reviewed) : 0) || a.name.localeCompare(b.name, 'en'));
}
export function safeExternal(value) {
  try { const u = new URL(value); return u.protocol === 'https:' && !u.username && !u.password; }
  catch { return false; }
}
/** Validate data before rendering it or producing generated pages. */
export function validateCatalog(entries, today = new Date().toISOString().slice(0, 10)) {
  const errors = [];
  if (!Array.isArray(entries) || entries.length === 0) return ['Catalog must be a non-empty array.'];
  const keys = ['id', 'name', 'type', 'categories', 'summary', 'source', 'guide', 'status', 'reviewed', 'evidence', 'review_note', 'compatibility', 'requirements', 'risk', 'license'];
  const ids = new Set(); const names = new Set();
  for (const [index, e] of entries.entries()) {
    const at = `Entry ${index + 1}`;
    if (!e || typeof e !== 'object' || Array.isArray(e)) { errors.push(`${at}: expected object`); continue; }
    for (const key of keys) if (!Object.hasOwn(e, key)) errors.push(`${at}: missing ${key}`);
    for (const key of Object.keys(e)) if (!keys.includes(key)) errors.push(`${at}: unknown field ${key}`);
    for (const key of keys.filter(k => !['categories', 'requirements'].includes(k))) {
      if (typeof e[key] !== 'string' || !e[key].trim()) errors.push(`${at}: ${key} must be non-empty text`);
    }
    if (typeof e.id !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(e.id)) errors.push(`${at}: invalid id`);
    if (ids.has(e.id)) errors.push(`${at}: duplicate id ${e.id}`); ids.add(e.id);
    const name = normalize(e.name).trim();
    if (names.has(name)) errors.push(`${at}: duplicate name ${e.name}`); names.add(name);
    if (!TYPES.includes(e.type)) errors.push(`${at}: invalid type`);
    if (!Object.hasOwn(STATUS, e.status)) errors.push(`${at}: invalid status`);
    for (const key of ['categories', 'requirements']) {
      if (!Array.isArray(e[key]) || !e[key].length || e[key].some(v => typeof v !== 'string' || !v.trim()) || new Set(e[key]).size !== e[key].length) errors.push(`${at}: invalid ${key}`);
    }
    if (Array.isArray(e.categories) && e.categories.some(c => !CATEGORIES.includes(c))) errors.push(`${at}: unknown category`);
    for (const key of ['source', 'guide', 'evidence']) if (!safeExternal(e[key])) errors.push(`${at}: ${key} must be an HTTPS URL without credentials`);
    if (typeof e.reviewed !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(e.reviewed) || !Number.isFinite(Date.parse(e.reviewed)) || new Date(e.reviewed).toISOString().slice(0, 10) !== e.reviewed || e.reviewed > today) errors.push(`${at}: invalid or future review date`);
  }
  return errors;
}
