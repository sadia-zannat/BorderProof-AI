/* AST check over every localized UI object in both frontends. No string evaluation. */
const fs=require('fs'),path=require('path');
const ts=require('../apps/web/node_modules/typescript');
const root=path.resolve(__dirname,'..');let catalogs=0;let failures=[];
function check(file,source){
 const tree=ts.createSourceFile(file,source,ts.ScriptTarget.Latest,true,file.endsWith('.tsx')?ts.ScriptKind.TSX:ts.ScriptKind.JS);
 function visit(n){
  if(ts.isObjectLiteralExpression(n)){
   const props=new Map(n.properties.filter(ts.isPropertyAssignment).map(p=>[p.name.text,p.initializer]));
   if(['en','zh-CN','bn-BD'].every(k=>props.has(k))){
    const sets=['en','zh-CN','bn-BD'].map(l=>new Set(props.get(l).properties?.filter(ts.isPropertyAssignment).map(p=>p.name.text)||[]));
    const diff=sets.map(s=>[...new Set([...sets[0],...s])].filter(k=>sets[0].has(k)!==s.has(k)));
    if(diff.some(d=>d.length))failures.push({file,diff});catalogs++;
   }
  }
  ts.forEachChild(n,visit);
 }visit(tree);
}
for(const dir of ['apps/web/components','apps/web/lib'])for(const f of fs.readdirSync(path.join(root,dir)))if(/\.tsx?$/.test(f))check(dir+'/'+f,fs.readFileSync(path.join(root,dir,f),'utf8'));
const preview=fs.readFileSync(path.join(root,'apps/preview/index.html'),'utf8');
for(const m of preview.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g))check('apps/preview/index.html',m[1]);
console.log(JSON.stringify({catalogs,failures,note:'Key parity, not proof that every technical string is translated'},null,2));
process.exitCode=failures.length?1:0;
