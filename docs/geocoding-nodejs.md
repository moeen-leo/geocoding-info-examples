# Geocode an address with Node.js

Disclosure: I operate Geocoding.info.

Register at https://geocoding.info/Signup.aspx , verify your email if requested, and create a key in the dashboard. Set GEOCODING_API_KEY on your server. The example requires Node.js 20+ and no external dependencies.

~~~javascript
import { pathToFileURL } from 'node:url';
export function buildUrl(operation, values, key) {
  if (!['search','reverse'].includes(operation)) throw Error('Use search or reverse.');
  if (!key) throw Error('Set GEOCODING_API_KEY.');
  const url=new URL('https://api.geocoding.info/'+operation);
  url.searchParams.set('key',key);url.searchParams.set('format','json');url.searchParams.set('accept-language','en');
  if(operation==='search'){
    if(values.length!==1 || !values[0].trim())throw Error('Provide one quoted address.');
    url.searchParams.set('q',values[0]);
  }else{
    if(values.length!==2 || values.some(v=>!v.trim()))throw Error('Provide latitude and longitude.');
    const [lat,lon]=values.map(Number);
    if(!Number.isFinite(lat)||!Number.isFinite(lon)||lat< -90||lat>90||lon< -180||lon>180)throw Error('Invalid coordinates.');
    url.searchParams.set('lat',String(lat));url.searchParams.set('lon',String(lon));
  }
  return url;
}
export async function geocode(operation,values,key,transport=fetch){
  const url=buildUrl(operation,values,key);let response;
  try{response=await transport(url,{signal:AbortSignal.timeout(20000)});}catch{throw Error('Could not reach the API.');}
  if(!response.ok)throw Error('API returned HTTP '+response.status+'. Check your key and limits.');
  try{return await response.json();}catch{throw Error('The API did not return JSON.');}
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){
 const [operation,...values]=process.argv.slice(2);
 geocode(operation,values,process.env.GEOCODING_API_KEY||'').then(v=>console.log(JSON.stringify(v,null,2))).catch(e=>{console.error(e.message);process.exitCode=1;});
}

~~~

Run: node geocode.mjs search "Paris, France"

Search returns candidate locations as a list; reverse lookup returns an object. Empty results are possible. Handle authentication errors (401), rate/quota limits (429) and temporary failures (5xx). Send requests sequentially and avoid unlimited retries. Never log full request URLs or publish your real API key.

Coverage varies with OpenStreetMap/Nominatim; reverse lookup can return a nearby mapped feature rather than an exact postal address. Preserve required attribution: https://www.openstreetmap.org/copyright . Current allowances: https://geocoding.info/Pricing.aspx .
