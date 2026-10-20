'use client';
import React,{useEffect,useState} from 'react';
import dynamic from 'next/dynamic';
const Real3DGlobe=dynamic(()=>import('./GlobalNetworkGlobe3D'),{ssr:false});
import {ArrowLeftRight,ArrowRight,ExternalLink,RefreshCcw,ShieldAlert,Globe2} from 'lucide-react';
import {request,type PaymentCase} from '@/lib/api';
import type {Locale} from '@/lib/i18n';

type Region={name:string;currency:string;flag:string;type:string};
type Corridor={origin_country:string;destination_country:string;source_currency:string;destination_currency:string;planning_supported:boolean;provider_available:boolean;legal_eligibility:string;execution_allowed:boolean};
type Catalog={regions:Region[];routes:Corridor[];directed_route_count:number;currencies:string[]};
type Reference={rate:string;source_amount:string;indicative_target_amount:string;published_date:string;retrieved_at_utc:string;source_url:string;response_sha256:string;provider:string;status:string;notices:string[]};
type Assessment={status:string;conflicts:string[];missing_or_unknown:string[];bank_beneficiary_ownership:string;university_attestation:string;result_sha256?:string;source_documents:{sha256:string}[];execution_allowed:boolean};
const flags:Record<string,string>={Bangladesh:'🇧🇩',China:'🇨🇳','United Kingdom':'🇬🇧','United States':'🇺🇸',Canada:'🇨🇦','Euro Area':'🇪🇺',Australia:'🇦🇺',Singapore:'🇸🇬'};
const labels={
 en:{title:'Global payment intelligence',desc:'Choose both directions. Routes indicate research coverage, not permission to transfer funds.',origin:'Sending from',target:'Receiving in',reference:'Load current FX reference',wait:'Requesting published rate…',unavailable:'No verifiable rate available. No quote has been invented.',status:'Financial rail unavailable · Eligibility unknown',case:'Inspect case evidence',choose:'Select an existing case',assess:'Run evidence checks',source:'Published financial reference',notQuote:'Reference only. Fees, execution and bank beneficiary ownership are not verified.',network:'Interactive route network',guide:'Select a node to set the receiving region. Choose the origin above.',regional:'Euro Area is a region; regulatory eligibility varies by country.',reverse:'Reverse direction',details:'Evidence findings',none:'Select a case to verify invoice field consistency.',blocked:'No real provider connected · No payment executed'},
 'zh-CN':{title:'全球支付信息网络',desc:'双向选择汇款区域。列出的路径不表示真实转账资格。',origin:'汇出地区',target:'汇入地区',reference:'获取公开汇率参考',wait:'正在查询公开参考汇率…',unavailable:'未获得可核实的参考汇率；未生成虚假报价。',status:'支付通道未连接 · 资格未知',case:'检查案例证据',choose:'选择已有案例',assess:'运行证据检查',source:'公开金融参考汇率',notQuote:'仅供参考，不代表执行汇率、银行账户核验或费用。',network:'交互式付款网络',guide:'点击节点选择收款地区；在上方选择汇出地区。',regional:'欧元区为区域，各成员国法规不同。',reverse:'交换方向',details:'证据核查',none:'选择案例以检查发票一致性。',blocked:'未连接真实支付服务商 · 没有进行付款'},
 'bn-BD':{title:'বৈশ্বিক পেমেন্ট নেটওয়ার্ক',desc:'উভয় দিকের রুট বেছে নিন। রুটের তালিকা বাস্তব টাকা পাঠানোর অনুমতি নয়।',origin:'যেখান থেকে',target:'যেখানে যাবে',reference:'প্রকাশিত FX রেফারেন্স আনুন',wait:'প্রকাশিত রেট যাচাই হচ্ছে…',unavailable:'যাচাইকৃত রেট পাওয়া যায়নি। বানানো quote দেখানো হবে না।',status:'ব্যাংক চ্যানেল যুক্ত নয় · যোগ্যতা অজানা',case:'কেসের প্রমাণ যাচাই',choose:'একটি কেস বেছে নিন',assess:'প্রমাণ পরীক্ষা করুন',source:'প্রকাশিত FX তথ্য',notQuote:'শুধু reference; fee, bank account ownership ও real execution যাচাই করা হয়নি।',network:'ইন্টারঅ্যাকটিভ রুট নেটওয়ার্ক',guide:'দেশের node-এ ক্লিক করে destination বেছে নিন।',regional:'Euro Area একটি অঞ্চল; সদস্যদেশ অনুযায়ী নিয়ম ভিন্ন।',reverse:'দিক উল্টো করুন',details:'প্রমাণের ফল',none:'ইনভয়েসের তথ্য যাচাই করতে একটি কেস বেছে নিন।',blocked:'বাস্তব পেমেন্ট সংযোগ নেই · কোনো টাকা পাঠানো হয়নি'},
};
export default function GlobalNetwork({locale,cases,csrf,onStartCase}:{locale:Locale;cases:PaymentCase[];csrf:string;onStartCase:(origin:string,dest:string)=>void}){
 const t=labels[locale]||labels.en;
 const [catalog,setCatalog]=useState<Catalog|null>(null),[error,setError]=useState('');
 const [webgl,setWebgl]=useState(false);
 useEffect(()=>{try{const c=document.createElement('canvas');setWebgl(!!(c.getContext('webgl2')||c.getContext('webgl'))&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches)}catch{setWebgl(false)}},[]);
 const [origin,setOrigin]=useState('Bangladesh'),[target,setTarget]=useState('China'),[amount,setAmount]=useState('12500.00');
 const [rate,setRate]=useState<Reference|null>(null),[loading,setLoading]=useState(false);
 const [caseId,setCaseId]=useState(''),[assessment,setAssessment]=useState<Assessment|null>(null);
 useEffect(()=>{let active=true;request<Catalog>('/network/corridors').then(x=>{if(active)setCatalog(x)}).catch(e=>{if(active)setError(String(e))});return()=>{active=false}},[]);
 const regionList=catalog?.regions||[];
 const countryCurrency=(name:string)=>regionList.find(r=>r.name===name)?.currency||'';
 const pair=catalog?.routes.find(x=>x.origin_country===origin&&x.destination_country===target);
 const swap=()=>{setOrigin(target);setTarget(origin);setRate(null)};
 const changeOrigin=(name:string)=>{setOrigin(name);if(name===target)setTarget(origin);setRate(null)};
 const changeTarget=(name:string)=>{if(name===origin)return;setTarget(name);setRate(null)};
 const fetchRate=async()=>{setLoading(true);setError('');setRate(null);try{const r=await request<Reference>(`/network/reference?from_currency=${encodeURIComponent(countryCurrency(origin))}&to_currency=${encodeURIComponent(countryCurrency(target))}&amount=${encodeURIComponent(amount)}`);setRate(r)}catch(e){setError(`${t.unavailable} ${e instanceof Error?e.message:''}`)}finally{setLoading(false)}};
 const assess=async()=>{if(!caseId)return;setLoading(true);setError('');setAssessment(null);try{const x=await request<Assessment>(`/network/cases/${caseId}/assessment`,csrf,{method:'POST'});setAssessment(x)}catch(e){setError(e instanceof Error?e.message:'Assessment unavailable')}finally{setLoading(false)}};
 return <div className="global-network">
 <div className="screen-heading"><div><span className="overline">FINVERITAS · EVIDENCE-FIRST</span><h1>{t.title}</h1><p style={{maxWidth:740}}>{t.desc}</p></div><span className="pill amber">{catalog?.directed_route_count??'—'} PLANNING PAIRS</span></div>
 <div className="panel" style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(250px,1fr))',gap:18}}>
 <label>{t.origin}<select value={origin} onChange={e=>changeOrigin(e.target.value)}>{regionList.map(r=><option key={r.name} value={r.name}>{r.flag} {r.name} · {r.currency}</option>)}</select></label>
 <label>{t.target}<select value={target} onChange={e=>changeTarget(e.target.value)}>{regionList.filter(r=>r.name!==origin).map(r=><option key={r.name} value={r.name}>{r.flag} {r.name} · {r.currency}</option>)}</select></label>
 <div style={{alignSelf:'end',display:'flex',gap:10,flexWrap:'wrap'}}><button className="btn outline" onClick={swap}><ArrowLeftRight size={16}/>{t.reverse}</button><button className="btn primary" disabled={!pair} onClick={()=>onStartCase(origin,target)}>+ {locale==='bn-BD'?'নতুন কেস':locale==='zh-CN'?'创建案例':'Create case'}</button></div>
 </div>
 <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(310px,1fr))',gap:18,marginTop:18}}>
 <section className="panel"><div className="panel-heading"><h2><Globe2 size={18}/> {t.network}</h2><span className="pill amber">{t.status}</span></div>
 {webgl?<Real3DGlobe origin={origin} target={target} onPick={name=>changeTarget(name)}/>:<svg viewBox="0 0 440 355" role="img" aria-label={`Selectable routes from ${origin} to ${target}`} width="100%" style={{maxHeight:385}}>
 <defs><radialGradient id="glow"><stop stopColor="#146e78" stopOpacity=".35"/><stop offset="1" stopColor="#052035" stopOpacity=".05"/></radialGradient></defs>
 <circle cx="220" cy="176" r="152" fill="url(#glow)" stroke="#3ac6c4" strokeOpacity=".3"/>
 {regionList.map((r,i)=>{const a=2*Math.PI*i/regionList.length-Math.PI/2;const x=220+142*Math.cos(a),y=176+142*Math.sin(a);const o=regionList.findIndex(n=>n.name===origin);const b=2*Math.PI*o/regionList.length-Math.PI/2;const fromX=220+142*Math.cos(b),fromY=176+142*Math.sin(b);return <g key={'edge'+r.name}>{r.name!==origin&&<path d={`M ${fromX} ${fromY} Q 220 ${176+(i%2?38:-38)} ${x} ${y}`} stroke={r.name===target?'#42dac4':'#307c95'} strokeWidth={r.name===target?3:1} opacity={r.name===target?.95:.22} fill="none"/>}</g>})}
 {regionList.map((r,i)=>{const a=2*Math.PI*i/regionList.length-Math.PI/2,x=220+142*Math.cos(a),y=176+142*Math.sin(a);return <g key={r.name} role="button" tabIndex={0} aria-label={`Select ${r.name}`} onClick={()=>changeTarget(r.name)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();changeTarget(r.name)}}} style={{cursor:'pointer'}}><circle cx={x} cy={y} r={r.name===target?28:24} fill={r.name===origin?'#1e777c':r.name===target?'#147c8b':'#102f47'} stroke={r.name===origin||r.name===target?'#6ffae1':'#2a697d'} strokeWidth={r.name===target?2.5:1.4}/><text x={x} y={y-1} fontSize="20" textAnchor="middle">{flags[r.name]}</text><text x={x} y={y+16} fontSize="9" fill="white" textAnchor="middle">{r.currency}</text><title>{r.name}</title></g>})}
 <text x="220" y="173" textAnchor="middle" fontSize="19" fill="#b8eeec" fontWeight="700">{countryCurrency(origin)} → {countryCurrency(target)}</text><text x="220" y="194" fontSize="10" fill="#8db6c1" textAnchor="middle">REVIEW REQUIRED</text>
 </svg>}<small>{t.guide} {t.regional}</small></section>
 <section className="panel"><div className="panel-heading"><h2>FX · {countryCurrency(origin)} → {countryCurrency(target)}</h2><span className="pill amber">REFERENCE ONLY</span></div>
 <label>{locale==='bn-BD'?'পরিমাণ':locale==='zh-CN'?'金额':'Amount'} ({countryCurrency(origin)})<input value={amount} onChange={e=>setAmount(e.target.value)} inputMode="decimal" placeholder="12500.00"/></label>
 <button className="btn primary" style={{marginTop:16}} onClick={fetchRate} disabled={loading||!pair}><RefreshCcw size={16}/>{loading?t.wait:t.reference}</button>
 {rate&&<div style={{marginTop:22}}><div className="overline">{t.source}</div><h2>{rate.source_amount} {countryCurrency(origin)} ≈ {rate.indicative_target_amount} {countryCurrency(target)}</h2><p>1 {countryCurrency(origin)} = {rate.rate} {countryCurrency(target)}</p><small>Published {rate.published_date} · Retrieved {rate.retrieved_at_utc}</small><p><a href={rate.source_url} rel="noreferrer" target="_blank">Frankfurter v2 <ExternalLink size={13} style={{display:'inline'}}/></a></p><small>{t.notQuote}</small><details className="technical-details"><summary>Data provenance</summary><code style={{overflowWrap:'anywhere'}}>{rate.response_sha256}</code><p>{rate.provider}</p></details></div>}
 <div className="notice-box" style={{marginTop:20}}><ShieldAlert size={19}/><span>{t.blocked}</span></div>
 </section></div>
 <div className="panel" style={{marginTop:18}}><div className="panel-heading"><h2>{t.case}</h2><span className="pill amber">NOT BANK VERIFIED</span></div><div style={{display:'flex',gap:12,flexWrap:'wrap'}}><select aria-label={t.choose} value={caseId} onChange={e=>{setCaseId(e.target.value);setAssessment(null)}} style={{flex:'1 1 250px'}}><option value="">{t.choose}</option>{cases.map(c=><option value={c.id} key={c.id}>{c.title} · {c.origin_country} → {c.destination_country}</option>)}</select><button className="btn primary" disabled={loading||!caseId} onClick={assess}>{t.assess}<ArrowRight size={16}/></button></div>
 {assessment&&<div style={{marginTop:20}}><strong>{t.details}: {assessment.status}</strong><div className="notice-box"><ShieldAlert size={20}/><span>University: {assessment.university_attestation} · Beneficiary: {assessment.bank_beneficiary_ownership}</span></div>{assessment.conflicts.length>0&&<p>Conflicts: {assessment.conflicts.join(', ')}</p>}<p>Missing/unknown: {assessment.missing_or_unknown.join(', ')||'Bank verification still required'}</p><details className="technical-details"><summary>Persisted assessment hash</summary><code style={{overflowWrap:'anywhere'}}>{assessment.result_sha256}</code></details></div>}
 {!assessment&&<p>{t.none}</p>}
 {error&&<p role="alert" style={{color:'#f4c185'}}>{error}</p>}
 </div>
 </div>;
}
