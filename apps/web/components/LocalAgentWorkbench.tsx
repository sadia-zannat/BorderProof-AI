'use client';
import React,{useEffect,useState} from 'react';
import {Bot,ShieldCheck,AlertTriangle,ArrowRight,RefreshCw} from 'lucide-react';
import {request,type PaymentCase} from '@/lib/api';
import type {Locale} from '@/lib/i18n';

type Trace={name:string;status:string;source:string};
type Run={conversation_id:string;mode:string;message:string;tool_trace:Trace[];tool_count:number;can_authorize:boolean;can_execute:boolean};
type Message={role:'user'|'assistant';content:string};
const content={
 en:{title:'AI assistant',desc:'',case:'Payment case',ask:'Ask your AI',placeholder:'Which invoice evidence is missing? Check the investigation and any quotes.',send:'Investigate with local Qwen',newChat:'New conversation',empty:'Create a student payment case first.',offline:'Ollama must be installed and qwen3:4b downloaded on this computer.',trace:'Tool activity',notice:'Unverified source data and internal synthetic quotes. No actual banking operations.',ready:'How can I help with your payment?',wait:'Consulting local model…'},
 'zh-CN':{title:'AI 助理',desc:'',case:'付款案例',ask:'咨询 AI',placeholder:'发票中还缺少哪些证据？请查看调查和报价。',send:'用本地 Qwen 分析',newChat:'新对话',empty:'请先创建付款案例。',offline:'请在电脑上安装 Ollama 并下载 qwen3:4b。',trace:'执行的金融查询工具',notice:'未验证的数据和内部模拟报价。不涉及真实银行交易。',ready:'您想查询什么付款信息？',wait:'本地模型分析中…'},
 'bn-BD':{title:'AI সহকারী',desc:'',case:'পেমেন্ট কেস',ask:'AI-কে প্রশ্ন করো',placeholder:'ইনভয়েসে কী কী তথ্য নেই? Investigation আর quotes পরীক্ষা করো।',send:'লোকাল Qwen দিয়ে যাচাই',newChat:'নতুন কথোপকথন',empty:'প্রথমে একটি পেমেন্ট কেস তৈরি করো।',offline:'কম্পিউটারে Ollama install করে qwen3:4b model download করতে হবে।',trace:'AI ব্যবহার করা financial tools',notice:'তথ্য যাচাইকৃত নয়; সব quote synthetic। আসল ব্যাংক লেনদেন হয় না।',ready:'পেমেন্টের কোন বিষয়ে সাহায্য লাগবে?',wait:'লোকাল মডেল কাজ করছে…'}
} as const;
export default function LocalAgentWorkbench({cases,csrf,locale}:{cases:PaymentCase[],csrf:string,locale:Locale}){
 const t=content[locale]||content.en;
 const [caseId,setCaseId]=useState('');const [question,setQuestion]=useState('');const [messages,setMessages]=useState<Message[]>([]);
 const [conversationId,setConversationId]=useState<string|null>(null);const [trace,setTrace]=useState<Trace[]>([]);
 const [busy,setBusy]=useState(false);const [error,setError]=useState('');const [model,setModel]=useState('qwen3:4b');
 useEffect(()=>{if(!cases.some(x=>x.id===caseId)){setCaseId(cases[0]?.id||'');setMessages([]);setConversationId(null);setTrace([])}},[cases,caseId]);
 useEffect(()=>{request<{model:string}>('/agent/capabilities').then(x=>setModel(x.model)).catch(()=>{});},[]);
 const changeCase=(v:string)=>{setCaseId(v);setConversationId(null);setTrace([]);setMessages([]);setError('')};
 const send=async(e:React.FormEvent)=>{e.preventDefault();if(!caseId||!question.trim()||busy)return;
  const msg=question.trim();setQuestion('');setError('');setBusy(true);
  try{const answer=await request<Run>(`/cases/${caseId}/agent/chat`,csrf,{method:'POST',body:JSON.stringify({message:msg,conversation_id:conversationId})});
   setMessages(x=>[...x,{role:'user',content:msg},{role:'assistant',content:answer.message}]);setConversationId(answer.conversation_id);setTrace(answer.tool_trace);
  }catch(e){setQuestion(msg);setError(e instanceof Error?e.message:String(e))}finally{setBusy(false)}
 };
 return <div className="agent-page">
   <div className="screen-heading"><div><h1>{t.title}</h1></div><span className="pill amber"><Bot size={14}/> {model}</span></div>
   <div className="agent-safety-note"><ShieldCheck size={16}/><span>{t.notice}</span></div>
   <div className="panel agent-panel"><div className="agent-toolbar"><label>{t.case}<select disabled={busy} value={caseId} onChange={e=>changeCase(e.target.value)}>{cases.map(c=><option key={c.id} value={c.id}>{c.title} · {c.currency} {c.amount}</option>)}</select></label><button className="btn outline" type="button" disabled={busy} onClick={()=>changeCase(caseId)}><RefreshCw size={14}/> {t.newChat}</button></div>
    {!cases.length?<p>{t.empty}</p>:<>
    <div className="agent-messages" role="log" aria-live="polite">
    {!messages.length&&<div className="agent-welcome"><Bot size={32}/><strong>{t.ready}</strong><p>{t.placeholder}</p></div>}
    {messages.map((m,i)=><div key={i} className={`agent-message ${m.role==='user'?'from-user':'from-model'}`}><small>{m.role==='user'?'You':'BorderProof AI'}</small><p>{m.content}</p></div>)}
    {busy&&<p className="agent-wait">{t.wait}</p>}
    </div>
    {error&&<div className="agent-error" role="alert"><AlertTriangle size={16}/><span>{error}. {t.offline}</span></div>}
    <form onSubmit={send} className="agent-form"><label htmlFor="local-agent-prompt">{t.ask}</label><textarea id="local-agent-prompt" value={question} onChange={e=>setQuestion(e.target.value)} minLength={2} maxLength={1200} rows={3} placeholder={t.placeholder} required/><button type="submit" className="btn primary" disabled={busy||!caseId||question.trim().length<2}>{busy?t.wait:t.send}<ArrowRight size={15}/></button></form>
    </>}
   </div>
   {trace.length>0&&<details className="panel agent-trace technical-details"><summary>{t.trace} · {trace.length}</summary>{trace.map((x,i)=><div key={i}><ShieldCheck size={16}/><code>{x.name}</code><span>{x.status}</span></div>)}</details>}
  </div>
}
