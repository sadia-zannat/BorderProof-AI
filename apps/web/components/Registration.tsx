'use client';
import {useEffect,useState,type FormEvent} from 'react';
import Link from 'next/link';
import {request} from '@/lib/api';
import type {Locale} from '@/lib/i18n';
const labels={en:{title:'Create local account',name:'Name',email:'Email',password:'Password',submit:'Create account',note:'Local demo only. Identity and email are unverified.',disabled:'Local registration is disabled.',login:'Sign in'},'zh-CN':{title:'创建本地账户',name:'姓名',email:'电子邮件',password:'密码',submit:'创建账户',note:'仅供本地演示。身份及电子邮件未经核实。',disabled:'本地注册已禁用。',login:'登录'},'bn-BD':{title:'লোকাল অ্যাকাউন্ট তৈরি',name:'নাম',email:'ইমেইল',password:'পাসওয়ার্ড',submit:'অ্যাকাউন্ট তৈরি',note:'শুধু লোকাল ডেমো। পরিচয় ও ইমেইল যাচাই হয়নি।',disabled:'লোকাল নিবন্ধন বন্ধ আছে।',login:'সাইন ইন'}};
export default function Registration({locale,onCreated}:{locale:Locale;onCreated:()=>void}){
 const t=labels[locale];const [enabled,setEnabled]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState('');
 useEffect(()=>{request<{local_signup_enabled:boolean}>('/public/config').then(c=>setEnabled(c.local_signup_enabled)).catch(e=>setError(String(e)))},[]);
 async function submit(event:FormEvent<HTMLFormElement>){event.preventDefault();setBusy(true);setError('');const form=new FormData(event.currentTarget);
  try{await request('/auth/register',undefined,{method:'POST',body:JSON.stringify({name:form.get('name'),email:form.get('email'),password:form.get('password')})});onCreated()}
  catch(e){setError(e instanceof Error?e.message:String(e))}finally{setBusy(false)}
 }
 return <main className="auth-main"><div className="auth-left"><h1>{t.title}</h1><p>{t.note}</p></div><div className="auth-card"><h2>{t.title}</h2>{enabled?<form className="stack-form" onSubmit={submit}><label>{t.name}<input name="name" required minLength={2} maxLength={120} autoComplete="name"/></label><label>{t.email}<input name="email" type="email" required autoComplete="email"/></label><label>{t.password}<input name="password" type="password" required minLength={12} maxLength={256} autoComplete="new-password"/></label><button className="btn primary fill" disabled={busy}>{t.submit}</button></form>:<p>{t.disabled}</p>}{error&&<p role="alert">{error}</p>}<Link className="quiet-link" href="/login">{t.login}</Link></div></main>
}
