// Same-origin proxy preserves cookies across localhost/127.0.0.1 and deployments.
export const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || '';
export type User = {id:string;email:string;name:string;role:'student'|'reviewer'|'auditor'|'admin';institution:string;home_country:string;currency:string};
export type PaymentCase = {id:string;title:string;institution:string;origin_country:string;destination_country:string;source_currency:string;destination_currency:string;amount:string;currency:string;status:string;is_synthetic:boolean;created_at:string};
export type Doc = {id:string;case_id:string;filename:string;bytes_size:number;sha256:string;status:string;created_at:string};
export async function request<T>(path:string,csrf?:string,init:RequestInit={}):Promise<T>{
 const headers:Record<string,string> = {...(init.headers as Record<string,string> || {})};
 if(csrf)headers['X-CSRF-Token']=csrf;
 if(init.body && !(init.body instanceof FormData))headers['Content-Type']='application/json';
 let r:Response;
 try{r=await fetch(`${BASE}/api/v1${path}`,{...init,headers,credentials:'include',cache:'no-store'});}catch{throw new Error('Cannot connect to API. Start FastAPI on localhost:8000.');}
 if(!r.ok){const body=await r.json().catch(()=>({}));throw new Error(typeof body.detail==='string'?body.detail:`API error ${r.status}`)}
 return r.json() as Promise<T>;
}
