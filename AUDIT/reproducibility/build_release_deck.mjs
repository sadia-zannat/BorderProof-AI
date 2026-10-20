import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {finalizePresentation} from '/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs';
const root=process.argv[2];
if(!root)throw Error('Pass source project root');
const build='/workspace/scratch/b8babccc5586/deck_build';
const font='DejaVu Sans',ink='#ECF6FB',muted='#A3B8C6',mint='#55D6BA',navy='#071522';
const load=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const original=await load('AUDIT/evidence/research/original_reproduction/holdout_results.json');
const native=await load('AUDIT/evidence/native_final/report.json');
const extra=await load('AUDIT/evidence/research/methodology_and_results.json');
const pos=native.api_cases.find(x=>x.id==='FRESH-GBP').transfer;
let tests='Pending clean check';
try{const s=await fs.readFile(path.join(root,'AUDIT/evidence/clean/backend.log'),'utf8');tests=(s.match(/(\d+) passed/)||[])[1]||tests}catch{}
const p=Presentation.create({slideSize:{width:1280,height:720}});
function text(slide,value,x,y,w,h,size=27,color=ink,bold=false){const sh=slide.shapes.add({geometry:'textbox',name:'text-'+slide.shapes.items.length,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});sh.text=value;sh.text.style={fontSize:size,typeface:font,color,bold};return sh;}
function slide(title,notes){const s=p.slides.add();s.background.fill=navy;text(s,title,64,48,1140,90,44,ink,true);s.speakerNotes.text=notes;text(s,String(p.slides.items.length).padStart(2,'0'),1170,662,50,28,18,muted);return s;}
async function picture(s,filename,x,y,w,h){const bytes=await fs.readFile(path.join(root,'AUDIT/evidence/native_final',filename));s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:'Actual running BorderProof UI: '+filename,fit:'contain',position:{left:x,top:y,width:w,height:h}})}
function table(s,values,x=64,y=180,w=1152,h=380,widths=[430,722]){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});for(let r=0;r<values.length;r++)for(let c=0;c<values[r].length;c++){const ce=t.getCell(r,c);ce.fill=r===0?'#15384B':'#0D2435';ce.text.style={fontSize:r===0?24:23,typeface:font,color:r===0?mint:ink,bold:r===0};}return t;}
{
 const s=slide('BorderProof AI','45 seconds. Team FinVeritas, International AI Topic C. This is a real internal simulator demonstration, not a live payment product. No external partner or bank ownership verification is claimed. Source: AUDIT/FINAL_RELEASE_VERDICT.md.');
 text(s,'FinVeritas',68,190,600,64,32,mint,true);
 text(s,'Evidence-consistent assistance for international-student tuition payments',68,275,940,150,42,ink);
 text(s,'V5.3 implementation and execution evidence',68,502,1040,44,26,muted);
 text(s,'INTERNAL SIMULATION. NO REAL PAYMENTS.',68,585,1040,35,23,mint,true);
}
{
 const s=slide('The payment decision depends on evidence','60 seconds. Explain the concrete problem using this system: source invoice, payee, fee quote and student consent must agree. Different upstream facts can invalidate a previously reasonable plan. No invented market-size or fraud-savings statistic is used.');
 text(s,'An invoice can name one account while the payment plan uses another.',64,184,1080,100,36);
 text(s,'A quote can expire after the student reviews it.\nA later document can change the evidence.\nA retry can create a duplicate debit.',64,335,1080,170,31,muted);
 text(s,'The tested kernel rechecks these conditions before internal execution.',64,564,1080,76,29,mint,true);
}
{
 const s=slide('A new account starts with empty records','55 seconds. Screenshot from actual native Next.js production server. New synthetic user account before case creation; zero counts are read from backend cases/documents, not marketing counters. The same account API powers /demo. Sources: AUDIT/evidence/native_final/report.json and next_dashboard.png.');
 await picture(s,'next_dashboard.png',64,156,850,480);
 text(s,'Native browser requests\n\nZero records before case creation\n\nSame backend for both UIs',950,190,260,390,25,muted);
}
{
 const s=slide('The financial safety kernel','75 seconds. Read-only model tools cannot grant transaction consent. BPCE re-parses original bytes and compares source-set, case, payee, quote and approval. Database transactions/idempotency protect retries. These are established security techniques adapted to this scenario, not a new cryptographic protocol. Sources: services/api/app/finance.py, bpce.py, audit.py, security.py and AUDIT/FINANCIAL_SECURITY_TESTS.md.');
 table(s,[['Control','Implemented behavior'],['Evidence binding','Stored bytes, hashes, source reparse and latest-document checks'],['Human consent','Exact quote and evidence snapshot, single-use approval'],['Financial writes','Serialized updates, strict idempotency, balanced ledger'],['Model boundary','Six read-only tools, no approval or payment tool'],['Audit boundary','Local hash chain, no external signature or anchoring']],64,174,1152,410);
 text(s,'All financial execution remains inside the labelled synthetic simulator.',64,615,1100,35,23,mint);
}
{
 const s=slide('Actual internal execution and receipt','60 seconds. The displayed result is generated by the application and stored in SQLite. This is no bank or provider sandbox connection. The API acceptance also restarts Uvicorn and reads back receipt and balance. Source: native_final/FRESH-GBP_receipt.json and report.json.');
 text(s,`${pos.target_amount} ${pos.target_currency}`,64,184,670,85,58,mint,true);
 text(s,`Recorded debit: ${pos.source_debit} BDT`,64,290,1070,58,34);
 await picture(s,'next_transfer_status.png',64,390,1120,130);
 text(s,'Two ledger postings balance to zero.\nSIM references identify local software execution.',64,548,1100,84,27,muted);
}
{
 const s=slide('A conflicting invoice stays blocked','60 seconds. A separate new case receives a fresh invoice with conflicting amount labels. The parser asks for clarification and quote creation stays disabled. This screenshot is an actual browser state; no success UI was fabricated. Source: native_final/next_conflict_details.png, report.json, inputs/fresh_contradiction.txt.');
 await picture(s,'next_conflict_details.png',64,170,630,430);
 text(s,'Conflicting source values\n\nExplicit clarification\n\nNo quote or approval shortcut',760,210,430,330,30,muted);
}
{
 const s=slide('Research results expose remaining failures','80 seconds. These are authored synthetic offline policy proxies, not real LLM or AP2 implementations. Original 300 cases, 60 holdout; BPCE accepts 5/48 unsafe cases and rejects 3/12 legitimate cases. Added 96 frozen rows have 24 holdout. Same generator templates limit generalization, IDs expose families, labels are not independently adjudicated. Sources: research/original_reproduction/holdout_results.json and methodology_and_results.json. Prior art reviewed at abstract/README level: https://arxiv.org/abs/2609.00060 , https://arxiv.org/abs/2604.15367 , https://arxiv.org/abs/2406.13352 , https://aclanthology.org/2024.findings-acl.624/ , https://github.com/google-agentic-commerce/AP2 .');
 const rows=[['Original holdout policy proxy','Unsafe cases accepted / 48']];
 for(const [key,name] of [['heuristic_assistant_proxy','Heuristic assistant proxy'],['static_approval_proxy','Static approval proxy'],['ap2_inspired_proxy','AP2-inspired proxy (not AP2)'],['bpce_core_proxy','BPCE core proxy']])rows.push([name,String(original.policies[key].unsafe_acceptances)]);
 table(s,rows,64,174,1152,342,[760,392]);
 text(s,'BPCE also rejects 3 of 12 safe cases. True LLM baselines remain unmeasured.',64,550,1130,82,27,'#F4C585');
}
{
 const s=slide('Local Qwen validation is still pending','60 seconds. Actual Work localhost model probe returned connection refused. UI reports 503. We do not replace that with a canned answer. The included local script creates synthetic input and captures 8 actual Qwen requests, read-only tool traces, model identity and latency. Human answer/citation scoring is not automatic. The user laptop can run it with Ollama qwen3:4b. Sources: live_model_preflight.json and scripts/validate_local_agent.py.');
 await picture(s,'next_agent_unavailable.png',64,165,720,440);
 text(s,'Mock contracts verify tool boundaries.\n\nReal inference requires the local laptop.\n\nThe model cannot approve or execute.',840,194,365,385,27,muted);
}
{
 const s=slide('Release status and next validation','65 seconds. Readiness applies to the internal local demo. No deployment, GitHub push, organizer message, real transfer or charge occurred. Production is blocked by absent external financial/legal evidence, durable cloud document storage, executed PostgreSQL/Docker checks and live Qwen validation. Lint has 11 retained performance/dependency warnings, no lint errors. The clean evidence should be rechecked if numbers change. Sources: AUDIT/FINAL_RELEASE_VERDICT.md, FRONTEND_PRODUCTION_BUILD.md, RENDER_READINESS.md and clean logs.');
 text(s,`${tests} backend tests passed`,64,178,1100,62,40,mint,true);
 text(s,'Production Next.js build and native browser journeys verified\nOriginal 300-case corpus reproduced, plus 96 frozen challenge cases',64,279,1110,125,28);
 text(s,'READY FOR LOCAL SIMULATION DEMO',64,454,1120,46,33,mint,true);
 text(s,'Production finance and unqualified live-agent claims remain unready.',64,525,1120,76,28,'#F4C585');
}
await fs.mkdir(path.join(build,'previews'),{recursive:true});
for(const [i,s] of p.slides.items.entries()){
 const png=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(path.join(build,'previews',`slide-${i+1}.png`),new Uint8Array(await png.arrayBuffer()));
}
const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(p)).save(candidate);
const finalPath=path.join(root,'submissions/BorderProof_AI_FinVeritas_V5_3_Defense_Final.pptx');
await finalizePresentation({workspaceDir:'/workspace/scratch/b8babccc5586',candidatePath:candidate,finalPath,
 pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,
 integrityValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py',
 layoutValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_layout_geometry.py',
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','4','--require-native-table-slide','7'],
 requiredNativeTableOwnerSlides:[4,7],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,
 receiptPath:path.join(build,'deck-final-validation.json')});
console.log(finalPath);
