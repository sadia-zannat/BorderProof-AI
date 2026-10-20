'use client';
import {useState} from 'react';
import {request} from '@/lib/api';
import type {Locale} from '@/lib/i18n';
const labels={en:{title:'FX reference',load:'Load public reference',note:'Daily reference only. Simulator pricing uses separate synthetic rates.',details:'Source details',unavailable:'Reference unavailable. No rate substituted.'},'zh-CN':{title:'汇率参考',load:'获取公开参考数据',note:'仅供每日参考。模拟器采用独立的合成汇率。',details:'来源详情',unavailable:'参考数据不可用，未替换汇率。'},'bn-BD':{title:'বিনিময় হারের রেফারেন্স',load:'প্রকাশ্য রেফারেন্স দেখুন',note:'শুধু দৈনিক রেফারেন্স। সিমুলেটর আলাদা কৃত্রিম হার ব্যবহার করে।',details:'উৎসের বিস্তারিত',unavailable:'রেফারেন্স পাওয়া যায়নি। কোনো বিকল্প হার বসানো হয়নি।'}};
type FX={base:string;date:string;rates:Record<string,string>;source_url:string;retrieved_at_utc:string;source:string;precision:string;cache_status:string};
export default function PublicReference({locale}:{locale:Locale}){
 const t=labels[locale], [value,setValue]=useState<FX|null>(null),[error,setError]=useState(''),[busy,setBusy]=useState(false);
 async function load(){setBusy(true);setError('');setValue(null);try{setValue(await request<FX>('/finance/reference-fx?base=EUR'))}catch{setError(t.unavailable)}finally{setBusy(false)}}
 return <div className="panel"><div className="panel-heading"><h2>{t.title}</h2><span className="pill amber">REFERENCE</span></div><p>{t.note}</p><button className="btn outline" disabled={busy} onClick={load}>{t.load}</button>{error&&<p role="alert">{error}</p>}{value&&<><p>1 EUR · {value.date}</p><div className="detail-list">{['GBP','USD','CAD','CNY'].filter(c=>value.rates[c]).map(c=><div key={c}><span>{c}</span><strong>{value.rates[c]}</strong></div>)}</div><details className="technical-details"><summary>{t.details}</summary><p>{value.source} · {value.cache_status}</p><p>{value.retrieved_at_utc}</p><p>{value.precision}</p><a href={value.source_url} target="_blank" rel="noreferrer">Frankfurter / ECB</a></details></>}</div>
}
