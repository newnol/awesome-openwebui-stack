import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const yml = readFileSync(new URL('../stacks/openwebui-stack/docker-compose.yml', import.meta.url), 'utf8');
const env = readFileSync(new URL('../stacks/openwebui-stack/.env.example', import.meta.url), 'utf8');

test('reference images use release tags not rolling latest', () => {
  assert.match(yml, /ghcr\.io\/open-webui\/open-webui:v\d+\.\d+\.\d+/);
  assert.match(yml, /ghcr\.io\/open-webui\/open-terminal:\d+\.\d+\.\d+/);
  assert.match(yml, /ghcr\.io\/berriai\/litellm:v\d+\.\d+\.\d+/);
  assert.doesNotMatch(yml, /main-latest|open-terminal:latest/);
});
test('datastore is not published and app ports are loopback-only', () => {
  for (const binding of ['3000:8080', '4000:4000', '18000:8000']) {
    assert.ok(yml.includes('127.0.0.1:' + binding));
  }
  assert.doesNotMatch(yml, /["']?5432:5432["']?/);
});
test('required credentials have no default values', () => {
  for (const key of ['POSTGRES_PASSWORD', 'OPEN_TERMINAL_API_KEY', 'LITELLM_MASTER_KEY', 'WEBUI_SECRET_KEY']) {
    assert.ok(yml.includes('${' + key + ':?Set ' + key + ' in .env}'));
    assert.match(env, new RegExp('^' + key + '=$', 'm'));
  }
  assert.doesNotMatch(yml, /:-dbpassword|:-change-this-key/);
});
test('LiteLLM starts only after PostgreSQL healthcheck', () => {
  assert.match(yml, /depends_on:\s*\n\s+db:\s*\n\s+condition: service_healthy/);
});
