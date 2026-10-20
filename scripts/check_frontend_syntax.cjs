// Syntax-only TSX/TS check. Does not resolve modules or check semantics.
const fs=require('fs'),path=require('path');
let ts;try{ts=require('typescript')}catch(e){console.error('TypeScript compiler not on NODE_PATH. Use global npm install and retry');process.exit(2)}
const root=path.join(__dirname,'..','apps','web');let files=[];
function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(fs.statSync(p).isDirectory()){if(!['node_modules','.next'].includes(f))walk(p)}else if(/\.tsx?$/.test(f))files.push(p)}}
walk(root);let errors=[];
for(const f of files){const src=fs.readFileSync(f,'utf-8');const source=ts.createSourceFile(f,src,ts.ScriptTarget.Latest,true,f.endsWith('.tsx')?ts.ScriptKind.TSX:ts.ScriptKind.TS);for(const d of (source.parseDiagnostics||[])){if(d.category===ts.DiagnosticCategory.Error)errors.push(`${f}: ${ts.flattenDiagnosticMessageText(d.messageText,' ')}`)}}
console.log(`TypeScript/TSX syntax: ${files.length} files; ${errors.length} diagnostics.`);for(const e of errors)console.log(e);process.exit(errors.length?1:0);
