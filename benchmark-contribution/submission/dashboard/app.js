'use strict';
(() => {
 const D=window.DASHBOARD_DATA; const $=id=>document.getElementById(id);
 if(!D || !Array.isArray(D.rows)){ $('audit-label').textContent='Data unavailable — see downloadable artifacts'; return; }
 const levels=['Plain','Gentle','Playful','Strongest'];
 const descriptions=['No added humor instruction','One brief touch of humor','A couple of witty remarks','A short comedic bit'];
 const pct=x=>`${Number((x*100).toFixed(2))}%`;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let model='sonnet',domain='healthcare';
 let theme; try{theme=localStorage.getItem('humor-dashboard-theme')}catch{}
 if(theme==='light'||theme==='dark')document.documentElement.dataset.theme=theme;
 $('theme').onclick=()=>{const t=document.documentElement.dataset.theme==='light'?'dark':'light';document.documentElement.dataset.theme=t;try{localStorage.setItem('humor-dashboard-theme',t)}catch{}};
 const button=(label,key,selected)=>`<button type="button" data-key="${key}" aria-pressed="${selected}">${label}</button>`;
 function controls(){ $('models').innerHTML=['sonnet','haiku'].map(k=>button(k[0].toUpperCase()+k.slice(1)+' alias',k,k===model)).join(''); $('domains').innerHTML=[['healthcare','PubMedQA'],['programming','HumanEval']].map(([k,l])=>button(l,k,k===domain)).join('');
 $('models').querySelectorAll('button').forEach(b=>b.onclick=()=>{model=b.dataset.key;render()});$('domains').querySelectorAll('button').forEach(b=>b.onclick=()=>{domain=b.dataset.key;render()}); }
 function chart(rows,field,humor=false){const width=490,left=78,plot=348,top=35,dy=45;let s=`<svg class="chart" viewBox="0 0 ${width} 238" role="img" aria-label="${humor?'Model-judged funny rate':'Task accuracy'} by humor instruction; exact values in the table below">`;
 for(let tick=0;tick<=100;tick+=25){const x=left+plot*tick/100;s+=`<line class="grid" x1="${x}" y1="26" x2="${x}" y2="207"/><text x="${x}" y="228" text-anchor="middle">${tick}%</text>`;}
 rows.forEach((r,i)=>{const y=top+i*dy;const value=r[field];s+=`<text x="0" y="${y+17}">${levels[r.level]}</text><rect class="track" x="${left}" y="${y}" width="${plot}" height="25" rx="4"/><rect class="bar" x="${left}" y="${y}" width="${plot*value}" height="25" rx="4"/><text class="value" x="${left+plot+9}" y="${y+17}">${pct(value)}</text>`;});
 if(humor)[50,70].forEach(t=>{const x=left+plot*t/100;s+=`<line class="target" x1="${x}" y1="26" x2="${x}" y2="207"/><text x="${x}" y="15" text-anchor="middle">${t}% target</text>`;});return s+'</svg>'; }
 function render(){controls(); const rows=D.rows.filter(r=>r.model_alias===model&&r.domain===domain).sort((a,b)=>a.level-b.level);
 $('conditions').innerHTML=rows.map(r=>`<article class="condition"><span class="level">L${r.level} / INSTRUCTION</span><b>${levels[r.level]}</b><p>${descriptions[r.level]}</p><strong>${r.correct}/${r.n}</strong><small>correct · ${pct(r.accuracy)}</small></article>`).join('');
 $('accuracy').innerHTML=chart(rows,'accuracy');$('humor').innerHTML=chart(rows,'funny_ge3_rate',true);
 $('accuracy-note').textContent=domain==='healthcare'?'40 identical questions per arm. Answer-label exact match was independently recomputed. Each item is 2.5 percentage points.':'30 identical tasks per arm. Stored pass flags only; generated code was not re-executed in the independent audit. A 100% ceiling leaves no room to measure gains.';
 $('paired').innerHTML=rows.slice(1).map(r=>{const [w,l,t]=r.wins_losses_ties;return `<div class="pair"><div class="pair-label"><span>${levels[r.level]} vs plain</span><strong>${r.delta_percentage_points>0?'+':''}${r.delta_percentage_points} pp</strong></div><div class="pair-track" role="img" aria-label="${w} wins, ${l} losses, ${t} ties"><span class="win" style="width:${w/r.n*100}%"></span><span class="loss" style="width:${l/r.n*100}%"></span><span class="tie" style="width:${t/r.n*100}%"></span></div><div class="pair-key">${w} wins · ${l} losses · ${t} ties · paired p = ${r.exact_paired_sign_p_two_sided}</div></div>`}).join('');
 $('numbers').innerHTML=rows.map(r=>`<tr><th scope="row">L${r.level} ${levels[r.level]}</th><td>${r.correct} / ${r.n}</td><td>${pct(r.accuracy)}</td><td>${r.funny_ge3_n} / ${r.n} (${pct(r.funny_ge3_rate)})</td><td>${r.mean_humor.toFixed(3)} / 5</td><td>${r.delta_percentage_points>0?'+':''}${r.delta_percentage_points} pp</td><td>${r.wins_losses_ties.join(' / ')}</td><td>${r.level===0?'—':r.exact_paired_sign_p_two_sided}</td></tr>`).join(''); }
 $('stats').innerHTML=[[D.checks.record_count,'recorded task outputs'],[D.checks.task_count,'distinct tasks · 2 domains'],['4','instructions · 2 requested aliases'],['22.5%','highest model-judged funny rate']].map(([n,l])=>`<div class="stat"><b>${esc(n)}</b><span>${esc(l)}</span></div>`).join('');
 $('headline').textContent='Funny-rate coverage reached 22.5% at most—not the desired 50% or 70%. Healthcare scores moved in both directions. Coding was already at its stored-score ceiling.';
 $('audit-label').textContent='16 rows reconciled · source artifacts audited';$('audit-status').textContent='Counts reconciled; coding flags not rerun';
 $('audit-caveats').textContent='Model provenance: 278/280 Sonnet-alias task receipts and all 560 judge receipts list both Haiku and Sonnet usage. Requested aliases are not verified isolated checkpoints. All 56 raw JSON-format exceptions parse after documented fence/brace recovery. This is a prompt-only CLI-pipeline pilot, not a fine-tuning result.';
 render();
})();
