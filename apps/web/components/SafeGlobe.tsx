'use client';
import dynamic from 'next/dynamic';
import {useEffect,useState} from 'react';
const Globe=dynamic(()=>import('./Globe'),{ssr:false,loading:()=> <div className="fallback-globe"><span className="fallback-ring"/></div>});
export default function SafeGlobe(){const [usable,setUsable]=useState(false);useEffect(()=>{const canvas=document.createElement('canvas');const gl=canvas.getContext('webgl2');const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;setUsable(!!gl&&!reduce);},[]);return usable?<Globe/>:<div className="fallback-globe" role="img" aria-label="Financial corridor globe illustration"><span className="fallback-ring"/></div>}
