import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = {title:'BorderProof AI | Secure cross-border student finance',description:'An evidence-oriented financial planning workspace. Demonstration only; no live payments.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
