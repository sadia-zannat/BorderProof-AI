import {defineConfig, globalIgnores} from 'eslint/config';
import nextVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';
export default defineConfig([...nextVitals, ...nextTypescript,
  // Existing mount-time UI initializers are retained; report this performance advisory.
  {rules:{'react-hooks/set-state-in-effect':'warn'}},
  globalIgnores(['.next/**','node_modules/**','next-env.d.ts'])]);
