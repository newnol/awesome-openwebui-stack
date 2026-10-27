import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { CATEGORIES, TYPES, STATUS, DEFAULTS, readState, writeState, selectEntries, validateCatalog, safeExternal } from '../assets/catalog.mjs';
const entries = JSON.parse(readFileSync(new URL('../data/catalog.json', import.meta.url), 'utf8'));
const schema = JSON.parse(readFileSync(new URL('../data/catalog.schema.json', import.meta.url), 'utf8'));
const fresh = () => structuredClone(entries);
const state = overrides => ({ ...DEFAULTS, compare: [], ...overrides });
test('canonical data passes validation', () => assert.deepEqual(validateCatalog(entries), []));
test('schema and runtime enums stay aligned', () => {
  assert.deepEqual(schema.items.properties.type.enum, TYPES);
  assert.deepEqual(schema.items.properties.categories.items.enum, CATEGORIES);
  assert.deepEqual(schema.items.properties.status.enum, Object.keys(STATUS));
  assert.deepEqual([...schema.items.required].sort(), Object.keys(entries[0]).sort());
});
test('default browse excludes unavailable implementations', () => {
  assert.equal(selectEntries(entries, state()).length, 7);
  assert.ok(selectEntries(entries, state()).every(e => e.status !== 'unavailable'));
});
test('historical listings require an explicit opt-in', () => {
  assert.equal(selectEntries(entries, state({ unavailable: true })).length, 12);
  assert.equal(selectEntries(entries, state({ status: 'unavailable' })).length, 5);
});
test('search matches all terms, case-insensitively', () => {
  assert.equal(selectEntries(entries, state({ q: 'SHEETPROOF pandas' }))[0].id, 'sheetproof');
  assert.equal(selectEntries(entries, state({ q: 'no-such-package' })).length, 0);
});
test('type, category and evidence filters compose', () => {
  assert.deepEqual(selectEntries(entries, state({ type: 'integration', category: 'research', status: 'documented' })).map(e => e.id), ['searxng']);
});
test('sorting is deterministic and does not mutate data', () => {
  const before = JSON.stringify(entries);
  const result = selectEntries(entries, state());
  assert.deepEqual(result.map(e => e.name), [...result.map(e => e.name)].sort((a,b) => a.localeCompare(b, 'en')));
  assert.equal(JSON.stringify(entries), before);
});
test('query state round-trips and survives a share link', () => {
  const expected = state({ q: 'CSV & Excel', type: 'tool', category: 'productivity', status: 'documented', sort: 'reviewed', unavailable: true, compare: ['sheetproof', 'ollama'] });
  assert.deepEqual(readState(writeState(expected)), expected);
});
test('invalid URL filters and duplicate comparisons are normalized', () => {
  const result = readState('?type=script&category=invalid&status=__proto__&sort=unknown&compare=a,a,b,c,d');
  assert.deepEqual(result, state({ compare: ['a','b','c'] }));
  assert.equal(readState('?q=' + 'x'.repeat(300)).q.length, 200);
});
test('duplicate IDs and names fail validation', () => {
  const data = fresh(); data.push(data[0]);
  assert.ok(validateCatalog(data).some(e => e.includes('duplicate id')));
  assert.ok(validateCatalog(data).some(e => e.includes('duplicate name')));
});
test('unknown fields, categories and missing fields fail validation', () => {
  const data = fresh(); data[0].surprise = true; data[0].categories = ['bad']; delete data[0].risk;
  const errors = validateCatalog(data).join(' ');
  for (const word of ['unknown field', 'unknown category', 'missing risk']) assert.ok(errors.includes(word));
});
test('unsafe URLs cannot become clickable catalog links', () => {
  for (const value of ['javascript:alert(1)', 'data:text/html,x', '//evil.test', 'https://u:p@example.com', 'http://example.com']) assert.equal(safeExternal(value), false);
  const data = fresh(); data[0].guide = 'javascript:alert(1)';
  assert.ok(validateCatalog(data).some(e => e.includes('guide must')));
});
test('malformed and future review dates fail validation', () => {
  for (const date of ['2026-02-30', 'invalid', '2099-01-01']) {
    const data = fresh(); data[0].reviewed = date;
    assert.ok(validateCatalog(data, '2026-10-27').some(e => e.includes('review date')));
  }
});
test('malformed collections fail without throwing', () => {
  for (const value of [null, {}, [], [null], [1], ['text']]) assert.ok(validateCatalog(value).length);
  const data = fresh(); data[0].requirements = [null]; data[0].categories = [];
  assert.ok(validateCatalog(data).length);
});
