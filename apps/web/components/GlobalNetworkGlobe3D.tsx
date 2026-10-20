'use client';
import React,{useMemo} from 'react';
import {Canvas} from '@react-three/fiber';
import {Html,OrbitControls} from '@react-three/drei';
import * as THREE from 'three';

const LOCATIONS:Record<string,[number,number]>={
 Bangladesh:[23.7,90.35],China:[35,103.8],
 'United Kingdom':[51.5,-.12],'United States':[39,-98],
 Canada:[56,-107],'Euro Area':[50.85,4.35],
 Australia:[-25.3,133.7],Singapore:[1.35,103.82],
};
const CODES:Record<string,string>={Bangladesh:'BDT',China:'CNY','United Kingdom':'GBP','United States':'USD',Canada:'CAD','Euro Area':'EUR',Australia:'AUD',Singapore:'SGD'};
const point=(latitude:number,longitude:number,radius:number)=>{
 const phi=(90-latitude)*Math.PI/180,theta=(longitude+180)*Math.PI/180;
 return new THREE.Vector3(-radius*Math.sin(phi)*Math.cos(theta),radius*Math.cos(phi),radius*Math.sin(phi)*Math.sin(theta));
};
function Route({origin,target}:{origin:string;target:string}){
 const curve=useMemo(()=>{
  const [olat,olon]=LOCATIONS[origin], [tlat,tlon]=LOCATIONS[target];
  const a=point(olat,olon,1.63),b=point(tlat,tlon,1.63),points:THREE.Vector3[]=[];
  for(let i=0;i<=64;i++){
   const t=i/64,v=a.clone().normalize().lerp(b.clone().normalize(),t).normalize();
   const arcHeight=Math.sin(Math.PI*t)*.36;
   points.push(v.multiplyScalar(1.66+arcHeight));
  }
  return new THREE.CatmullRomCurve3(points);
 },[origin,target]);
 return <mesh><tubeGeometry args={[curve,64,.014,8,false]}/><meshBasicMaterial color="#6af9d1"/></mesh>;
}
function Sphere({origin,target,onPick}:{origin:string;target:string;onPick:(name:string)=>void}){
 return <group>
  <mesh><sphereGeometry args={[1.6,56,42]}/><meshPhongMaterial color="#0b3150" transparent opacity={.95} shininess={40}/></mesh>
  <mesh><sphereGeometry args={[1.614,34,24]}/><meshBasicMaterial color="#38abb6" transparent opacity={.22} wireframe/></mesh>
  <Route origin={origin} target={target}/>
  {Object.entries(LOCATIONS).map(([name,coords])=>{
   const at=point(...coords,1.72),selected=origin===name||target===name;
   return <group key={name} position={at.toArray()}>
    <mesh onClick={e=>{e.stopPropagation();onPick(name)}}>
     <sphereGeometry args={[selected?.10:.068,16,12]}/>
     <meshBasicMaterial color={selected?'#5ef9d4':'#92c8eb'}/>
    </mesh>
    <Html center distanceFactor={7.4} style={{pointerEvents:'auto',transform:'translateY(-18px)'}}>
      <button type="button" onClick={()=>onPick(name)} title={name} aria-label={`Select ${name}`} style={{background:'#102e46',color:'#ebffff',border:'1px solid #48bbae',borderRadius:7,fontWeight:700,fontSize:10,padding:'3px 5px',cursor:'pointer'}}>{CODES[name]}</button>
    </Html>
   </group>
  })}
 </group>;
}
export default function GlobalNetworkGlobe3D({origin,target,onPick}:{origin:string;target:string;onPick:(name:string)=>void}){
 return <div style={{height:390,width:'100%',borderRadius:16,overflow:'hidden',border:'1px solid rgba(70,180,185,.15)'}} aria-label="Drag-to-rotate 3D financial corridor globe, with clickable currencies">
 <Canvas camera={{position:[0,1,5.5],fov:47}} dpr={[1,1.5]} gl={{antialias:true,alpha:false}}>
  <color attach="background" args={['#081d31']}/>
  <ambientLight intensity={.95}/><pointLight position={[4,4,5]} intensity={25} color="#54d8dc"/>
  <Sphere origin={origin} target={target} onPick={onPick}/>
  <OrbitControls enableZoom={false} enablePan={false} autoRotate={false}/>
 </Canvas>
 </div>;
}
