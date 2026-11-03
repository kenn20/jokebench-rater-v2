'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const dir=__dirname, data=JSON.parse(fs.readFileSync(path.join(dir,'data/dashboard.json'))), html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
assert.equal(data.rows.length,16);assert.equal(data.checks.unique_records,560);assert.equal(data.checks.unique_judgments,560);assert.equal(data.checks.task_count,70);
assert.equal(data.source_commit,'3dbbdbb838a9e0e04338828b2e12576829c06c15');
for(const row of data.rows){assert.equal(row.accuracy,row.correct/row.n);assert.equal(row.funny_ge3_rate,row.funny_ge3_n/row.n);assert.equal(row.wins_losses_ties.reduce((a,b)=>a+b,0),row.n);assert.equal(row.n,row.domain==='healthcare'?40:30);assert.equal(row.delta_percentage_points,(row.wins_losses_ties[0]-row.wins_losses_ties[1])/row.n*100);}
assert.equal(Math.max(...data.rows.map(r=>r.funny_ge3_rate)),.225);
assert.deepEqual(JSON.parse(fs.readFileSync(path.join(dir,'data/audit-results.json'))),data);
for(const m of html.matchAll(/(?:href|src)="([^"#]+)"/g)){const ref=m[1];if(!/^https?:/.test(ref))assert.ok(fs.existsSync(path.join(dir,ref)),`Missing ${ref}`);}
assert.ok(!/<(?:script|link)[^>]+(?:src|href)="https?:/.test(html),'External runtime dependency');
// Deterministic DOM contract tests: not a substitute for a browser/layout test.
class Element{constructor(){this._html='';this.textContent='';this.dataset={};this.buttons=[];}set innerHTML(s){this._html=s;this.buttons=[...s.matchAll(/data-key="(.*?)" aria-pressed="(.*?)"/g)].map(m=>({dataset:{key:m[1]},pressed:m[2],onclick:null}));}get innerHTML(){return this._html;}querySelectorAll(){return this.buttons;}}
const els={}; for(const m of html.matchAll(/id="([^"]+)"/g))els[m[1]]=new Element();
const document={documentElement:{dataset:{}},getElementById:id=>{assert.ok(els[id],`Unknown DOM id ${id}`);return els[id]}};
const context={window:{},document,localStorage:{getItem(){throw Error('storage blocked')},setItem(){throw Error('storage blocked')}}}; vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(dir,'data.js'),'utf8'),context);vm.runInContext(fs.readFileSync(path.join(dir,'app.js'),'utf8'),context);
for(const model of ['haiku','sonnet','haiku','sonnet'])for(const domain of ['healthcare','programming','healthcare']){els.models.buttons.find(b=>b.dataset.key===model).onclick();els.domains.buttons.find(b=>b.dataset.key===domain).onclick();assert.equal((els.numbers.innerHTML.match(/<tr>/g)||[]).length,4);assert.ok(els.accuracy.innerHTML.includes('<svg'));assert.ok(els.humor.innerHTML.includes('70% target'));assert.equal(els.models.buttons.find(b=>b.pressed==='true').dataset.key,model);assert.equal(els.domains.buttons.find(b=>b.pressed==='true').dataset.key,domain);}
assert.ok(els.numbers.innerHTML.includes('33 / 40'));assert.ok(els.numbers.innerHTML.includes('0.125'));assert.ok(els['audit-caveats'].textContent.includes('278/280'));els.theme.onclick();assert.equal(document.documentElement.dataset.theme,'light');els.theme.onclick();assert.equal(document.documentElement.dataset.theme,'dark');
console.log('PASS: 16-row data invariants, source pin, exact audit equality, local links, no external runtime assets, 24 repeated filter changes, SVG generation, audit caveats, theme toggle with blocked storage. Browser/layout not covered.');
