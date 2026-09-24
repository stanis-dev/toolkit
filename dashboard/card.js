// Shared by index.html and refine.html: an agent's issues and cards, one card rendered with the page's chrome,
// remembered folds and the sidebar chrome; the card's live parts (its run bars and the drawers) are Preact components
// (preact-htm.js, loaded before this file), mounted once per card and fed by one store.
(function(){
  var cache={};
  // Where the pages dir keeps each file, as paths.py builds them; every fetch of a card's file goes through here.
  var Paths={
    card:function(a,n){return 'agents/'+a+'/cards/'+n+'/'},
    file:function(a,n,step,ext){return step==='driver'?'agents/'+a+'/driver/'+n+'.'+ext:Paths.card(a,n)+step+'/'+({json:'answer.json',md:'report.md'}[ext]||ext)},
    status:function(a,n,step){return Paths.file(a,n,step,'status.json')},
    answer:function(a,n,step){return Paths.file(a,n,step,'json')},
    runs:function(a,n,step){return step==='driver'?'agents/'+a+'/driver/runs/'+n+'/':Paths.card(a,n)+step+'/runs/'},
    chain:function(a,n){return Paths.card(a,n)+'chain.json'},
    log:function(a,n){return Paths.card(a,n)+'log.jsonl'}
  };
  var P=window.htmPreact, html=P.html, render=P.render, useState=P.useState, useEffect=P.useEffect, useLayoutEffect=P.useLayoutEffect, useRef=P.useRef, useMemo=P.useMemo;
  function pref(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){}}
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function load(agent){
    if(cache[agent]) return Promise.resolve(cache[agent]);
    var base='agents/'+agent+'/';
    var raw=fetch('sources/'+agent,{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).catch(function(){return {}});
    var list=fetch(base+'cards/').then(function(r){return r.ok?r.text():''}).catch(function(){return ''}).then(function(html){
      var nums=[],m,re=/href="(\d+)\/"/g; while((m=re.exec(html))) nums.push(+m[1]);
      return Promise.all(nums.map(function(n){return fetch(Paths.card(agent,n)+'card.html').then(function(r){return r.ok?r.text():null}).then(function(t){if(t==null)return null;
        var meta={},m2;while((m2=/^\s*<!--\s*(\w+):\s*(.*?)\s*-->/.exec(t))){meta[m2[1]]=m2[2];t=t.slice(m2[0].length)}
        // Green: the Sim Strategy has run counts and every one of them is full, repro and regressions alike.
        var res=Array.prototype.map.call(new DOMParser().parseFromString(t,'text/html').querySelectorAll('.ss .res'),function(e){return /(\d+)\s*\/\s*(\d+)/.exec(e.textContent)}).filter(Boolean);
        var green=res.length>0&&res.every(function(m){return +m[1]===+m[2]});
        return {num:n,pr:meta.pr||'',ws:meta.ws||'',batch:meta.batch||'',green:green,html:t.trim()};
      })}));
    });
    var batches=fetch(base+'batches.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():{}}).catch(function(){return {}});
    return Promise.all([raw,list,batches]).then(function(rr){
      var issues={}; Object.keys(rr[0]||{}).forEach(function(k){var d=rr[0][k],r=d.ref||{},c=r.created||'';issues[d.number]={num:d.number,kind:d.kind,title:(d.title||'').trim(),state:r.status||'OPEN',sev:r.severity||'MINOR',owner:r.owner||'',created:c.length>=10?c.slice(8,10)+'/'+c.slice(5,7):'',body:d.description||'',comments:d.comments||[],calls:d.conversations||[]}});
      Object.keys(issues).forEach(function(k){issues[k].agent=agent});
      rr[1].filter(Boolean).forEach(function(c){var i=issues[c.num]||(issues[c.num]={num:c.num,title:'#'+c.num,state:'OPEN',sev:'MINOR',owner:'',created:'',body:'',comments:[],orphan:true});i.pr=c.pr;i.ws=c.ws;i.batch=c.batch;i.green=c.green;i.card=c.html});
      return (cache[agent]={issues:issues,list:Object.keys(issues).map(function(k){return issues[k]}),batches:rr[2]||{}});
    });
  }
  // The store: what the page's poll of GET steps brings (steps, batches, resolve, chains, cost, stale, each per agent). A set
  // re-renders every component that reads it; Preact then touches only what changed.
  var Store=(function(){var s={steps:{},bst:{},res:{},chains:{},cost:{},stale:{}},subs=[];
    return {get:function(){return s},set:function(p){Object.keys(p).forEach(function(k){s[k]=p[k]});subs.slice().forEach(function(f){f()})},
      sub:function(f){subs.push(f);return function(){subs=subs.filter(function(g){return g!==f})}}}})();
  function useStore(){var f=useState(0)[1];useEffect(function(){return Store.sub(function(){f(function(x){return x+1})})},[]);return Store.get()}
  // Components mounted into a card; unmount(view) ends those inside view before the card is rebuilt.
  var roots=[];
  function mount(el,vnode){render(vnode,el);roots.push(el)}
  function unmount(view){roots=roots.filter(function(el){if(!el.isConnected||(view&&view.contains(el))){render(null,el);return false}return true})}
  // Chrome is the page's: the Analysis header, section titles, folds, block-entry folds and legacy class names.
  // Cards hold content; whatever chrome a card brings is replaced, so every card renders the current design.
  var TITLES={ss:'Sim Strategy',so:'Simulation Replay',si:'Simulation Iteration',oc:'Studio Context',oce:'Studio Context Edit',rs:'Resolution'};
  var TITLE_RE=/^(sim strategy|studio context( edit)?|simulation (replay|iteration)|regressions?)$/i;
  var CHEV='<i class="ti ti-chevron-right" aria-hidden="true"></i>';
  var known=null; fetch('sections.css').then(function(r){return r.text()}).then(function(css){known={};(css.match(/\.[a-zA-Z_][\w-]*/g)||[]).forEach(function(c){known[c.slice(1)]=1});['card','rep','secw','sh','lint','ti','sr-only','open','ok','ko','flaky','none','draft','ready','merged','other','default','released','runbar','ahd','run','chip','rbtn','rsel','bsel','sbtn2','kbtn','quiet','working','done','failed','ctx','edit','bug','improvement','rs','lane','chain','cho','chpop','stps','stp','cgo','cost','ctxb','trb','tcall','arm','rstb','rsm','prm','pp','pl','stale','rrb1','rrn','rrh','rrs','rrf','rrb','rrgo','rrall','rrm','rrw','rrt','flt'].forEach(function(c){known[c]=1})});
  function el(html){var t=document.createElement('template');t.innerHTML=html;return t.content.firstElementChild}
  function isEdit(s){return s.classList.contains('edit')||!!s.querySelector('.state, .row .del, .row .ins')}
  function norm(view,i){
    var card=view.querySelector('.card'), odd=[]; if(!card||card.classList.contains('rep')) return;
    card.querySelectorAll('.ss .sim>summary').forEach(function(s){var n=s.querySelector(':scope>.n'),nm=s.querySelector('.nm');if(n&&n.firstChild&&n.firstChild.nodeType===3)n.firstChild.textContent=n.firstChild.textContent.replace(/^\s*[+~\-\u2212]\s*/,'');if(!nm)return;var was=nm.querySelector(':scope>.was'),res=n&&n.querySelector('.res');if(was&&res&&s.parentElement.classList.contains('reg')&&was.href){var b=/(\d+)/.exec(was.textContent);var a=document.createElement('a');a.className='res';a.href=was.href;a.textContent=(b?b[1]+'\u203a':'')+res.textContent.trim();res.replaceWith(a)}nm.querySelectorAll(':scope>.sep, :scope>.was').forEach(function(e){e.remove()})});
    card.querySelectorAll('.ss .sim>summary .crumb code').forEach(function(e){var p=e.previousElementSibling;if(p&&p.classList.contains('sep'))p.remove();e.remove()});
    card.querySelectorAll('.ia .row>span>a.hl:first-child').forEach(function(e){if(!/marcad[oa] por/i.test(e.textContent))return;var b=e.nextSibling;if(b&&b.tagName==='BR')b.remove();e.remove()});
    card.querySelectorAll('.ia .row.good>.n, .ia .row.bad>.n').forEach(function(n){var l=n.lastChild;if(l&&l.nodeType===3)l.textContent=l.textContent.replace(/\s*[+\-\u2212]\s*$/,'')});
    card.querySelectorAll('.ss .exp:not(.ok):not(.ko)').forEach(function(e){var n=e.querySelector(':scope>.n'),b=e.lastElementChild;if(n&&!n.textContent.trim()&&b&&!b.querySelector('.tags, .ins-t, .del-t, .judge')&&!b.classList.contains('tags'))e.remove()});
    var rep=card.querySelector('details.card.rep'); if(rep){card.after(rep);odd.push('unclosed tag')}
    var ia=card.querySelector(':scope>.ia');
    if(ia){
      var old=ia.querySelector(':scope>header.top'), type=old&&old.querySelector('.type'), calls=i.calls||[], n=calls.length;
      var ts=calls.map(function(c){return c.timestamp||''}).filter(Boolean).sort()[0]||'', when=ts?ts.slice(8,10)+'/'+ts.slice(5,7):i.created;
      var h=el('<header class="top"><div class="id"><span class="num">#'+i.num+'</span></div><div class="meta">'+[(i.owner||'').split(/\s+/)[0],when].filter(Boolean).map(esc).join(' · ')+'</div></header>');
      if(type)h.firstChild.appendChild(type); h.firstChild.appendChild(el('<span>'+esc(i.title)+'</span>'));
      if(old)old.replaceWith(h); else ia.insertBefore(h,ia.querySelector(':scope>.top2')||ia.firstChild);
      var bar=el('<div class="runbar"></div>'); h.after(bar); mount(bar,html`<${TopBar} i=${i}/>`);
      if(i.agent){var ahd=el('<div class="ahd">Analysis<span class="runbar"></span></div>'); bar.after(ahd); mount(ahd.lastChild,html`<${RunStrip} i=${i} step="analysis"/>`)}
    }
    // Every step has its header once the analysis is there, so each run strip has a place: empty sections stand in.
    if(ia&&!card.querySelector('.ss'))card.appendChild(el('<div class="ss"></div>'));
    if(ia&&!card.querySelector('.oc.edit')&&!Array.prototype.some.call(card.querySelectorAll('.oc'),isEdit))card.appendChild(el('<div class="oc edit"></div>'));
    if(ia&&!card.querySelector('.rs'))card.appendChild(el('<div class="rs"></div>'));
    // Sections live at the card's top level, in document order; cards nest them in .ia or in a titled .part.
    Array.prototype.slice.call(card.querySelectorAll('.ss,.so,.si,.oc,.rs')).forEach(function(s){
      if(s.parentElement.closest('.ss,.so,.si,.oc,.rs')) return;
      var w=s.parentElement, wrap=w!==card&&w.classList.contains('part')&&Array.prototype.every.call(w.children,function(c){return c===s||(c.tagName==='H4'&&TITLE_RE.test(c.textContent.trim()))})?w:null;
      card.appendChild(s); if(wrap)wrap.remove();
    });
    card.querySelectorAll('div.part').forEach(function(p){
      var h4=p.querySelector(':scope>h4'); if(!h4) return;
      var d=el('<details class="part" open><summary></summary></details>');
      if(!h4.querySelector('.ti-chevron-right'))h4.insertAdjacentHTML('afterbegin',CHEV);
      d.firstChild.appendChild(h4); while(p.firstChild)d.appendChild(p.firstChild); p.replaceWith(d);
      // The Conversation part shows only the turns around the failure; its button opens the whole call.
      if(/^conversation$/i.test(h4.textContent.trim())&&i.agent){
        var conv=p.dataset.conv||((i.calls||[])[0]||{}).id; if(!conv)return;
        var rb=el('<span class="runbar"><button class="rbtn ctxb" title="What the agent model saw at its first turn: system parts, tools, messages" aria-label="Agent context at the first turn"><i class="ti ti-file-text" aria-hidden="true"></i></button><button class="rbtn trb" title="Full transcript of this call" aria-label="Full transcript of this call"><i class="ti ti-messages" aria-hidden="true"></i></button></span>');
        rb.addEventListener('click',function(e){e.stopPropagation();e.preventDefault();var b=e.target.closest('button');if(!b)return;if(b.classList.contains('ctxb'))Context.toggle(i,conv,null);else Transcript.toggle(i,conv)});
        d.firstChild.appendChild(rb);
      }
    });
    card.querySelectorAll('section.sec').forEach(function(s){
      var hd=s.querySelector(':scope>header'); if(!hd) return;
      var d=el('<details class="sec" open><summary></summary></details>'), c=hd.querySelector('.crumb');
      if(c&&!c.querySelector(':scope>.ti-chevron-right'))c.insertAdjacentHTML('afterbegin',CHEV);
      while(hd.firstChild)d.firstChild.appendChild(hd.firstChild); hd.remove();
      while(s.firstChild)d.appendChild(s.firstChild); s.replaceWith(d);
    });
    // Order: analysis and its context first, then the sim strategy and its runs, then the context edit.
    function rank(s){var c=s.classList;return c.contains('ia')?0:c.contains('oc')?(isEdit(s)?5:1):c.contains('ss')?2:c.contains('so')?3:c.contains('si')?4:c.contains('rs')?6:7}
    Array.prototype.slice.call(card.children).map(function(s,k){return [rank(s),k,s]}).sort(function(a,b){return a[0]-b[0]||a[1]-b[1]}).forEach(function(x){card.appendChild(x[2])});
    Array.prototype.slice.call(card.children).forEach(function(s){
      if(s.classList.contains('ia')) return;
      var k=Object.keys(TITLES).filter(function(c){return s.classList.contains(c)})[0];
      if(!k){odd.push('<'+s.tagName.toLowerCase()+(s.className?'.'+s.className.split(/\s+/).join('.'):'')+'>');return}
      var t=TITLES[k]; if(k==='oc'&&isEdit(s))t=TITLES.oce;
      if(k==='ss'){var own=s.querySelector(':scope>header.top');if(own)own.remove()}
      s.querySelectorAll(':scope>h4').forEach(function(h){if(TITLE_RE.test(h.textContent.trim()))h.remove()});
      var desc=s.querySelector(':scope>h2.sr-only');
      var d=el('<details class="secw" open><summary class="sh"'+(desc?' title="'+esc(desc.textContent.trim())+'"':'')+'>'+CHEV+esc(t)+'</summary></details>');
      s.replaceWith(d); d.appendChild(s);
      var step=k==='ss'?'strategy':t===TITLES.oce?'context':k==='rs'?'resolve':null;
      if(step){var rb=el('<span class="runbar"></span>'); rb.addEventListener('click',function(e){e.stopPropagation();if(e.target.tagName!=='SELECT')e.preventDefault()}); d.firstChild.appendChild(rb); mount(rb,html`<${RunStrip} i=${i} step=${step}/>`)}
    });
    if(known){var seen={};card.querySelectorAll('[class]').forEach(function(e){if(e.closest('.runbar'))return;e.classList.forEach(function(c){if(!known[c]&&!/^ti-/.test(c))seen[c]=1})});Object.keys(seen).forEach(function(c){odd.push('.'+c)})}
    if(odd.length)card.insertBefore(el('<div class="lint" title="Markup the page does not know; it renders unstyled">'+esc(odd.join(' '))+'</div>'),card.firstChild);
  }
  // Run: the play button in the Analysis header starts the issue-analysis skill on the server, the one in the Sim
  // Strategy header the sim-strategy skill; the chip next to each follows agents/<agent>/cards/<n>/<step>/status.json, fetched
  // again when the page's poll brings a new state for that step and every 2 s while the run works. The bars are
  // components mounted once per card, so a poll updates them in place.
  var STEP_LABEL={analysis:'analysis',strategy:'sim strategy',context:'context edit',resolve:'resolution'};
  var MODELS=['gpt-5.6-sol','gpt-5.6-terra'], EFFORTS=['low','medium','high','xhigh'];
  function fmtK(n){return n>=1000?Math.round(n/1000)+'k':String(n)}
  // in counts every input token the model read, the cached share in brackets; reasoning is part of out.
  function usageLine(u){return (u.context?'context '+fmtK(u.context)+' · ':'')+fmtK((u.in||0)+(u.cached||0))+' in'+(u.cached?' ('+fmtK(u.cached)+' cached)':'')+' · '+fmtK(u.out)+' out'+(u.reasoning?' ('+fmtK(u.reasoning)+' reasoning)':'')+(u.cost?' · $'+u.cost.toFixed(2):'')+' · '+(u.commands||0)+' commands'}
  function getJSON(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).catch(function(){return null})}
  function postJSON(u,body){return fetch(u,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})})}
  function errText(r){return r.text().then(function(t){var j={};try{j=JSON.parse(t)}catch(e){}return j.error||(/<p>Message: ([^<]*)/.exec(t)||[])[1]||(t||'').replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim().split('.')[0]||('server said '+r.status)})}
  function fresh(i){var d=cache[i.agent];return (d&&d.issues[i.num])||i}
  function stepState(S,i,step){return (((S.steps||{})[i.agent]||{})[i.num]||{})[step]||''}
  // A status file, fetched when key changes and every 2 s while it says working: [status, refetch].
  function useStatus(url,key){
    var s=useState(undefined), n=useState(0);
    useEffect(function(){var live=true,timer=null;
      getJSON(url).then(function(x){if(!live)return;s[1](x);if(x&&x.state==='working')timer=setTimeout(function(){n[1](function(k){return k+1})},2000)});
      return function(){live=false;if(timer)clearTimeout(timer)}},[url,key,n[0]]);
    return [s[0],function(){n[1](function(k){return k+1})}];
  }
  // A remembered choice shared by every control showing it (the card's pair and the selection bar's pair).
  function usePref(k,def){useStore();var v=pref(k)||def;return [v,function(x){pref(k,x);Store.set({})}]}
  function ModelSelect(p){var v=usePref(p.k,p.def);
    return html`<select class="rsel" id=${p.id} aria-label=${p.label} title=${p.title} value=${v[0]} onChange=${function(e){v[1](e.target.value)}}>${p.list.map(function(x){return html`<option value=${x}>${x}</option>`})}</select>`}
  function Models(){return html`<span class="run models"><${ModelSelect} k="runModel" def="gpt-5.6-terra" list=${MODELS} label="Model" title="Model for the runs started here"/><${ModelSelect} k="runEffort" def="high" list=${EFFORTS} label="Reasoning effort" title="Reasoning effort for the runs started here"/></span>`}
  function runOpts(){return {model:pref('runModel')||'gpt-5.6-terra',effort:pref('runEffort')||'high'}}
  function Icon(p){return html`<i class=${'ti '+p.n} aria-hidden="true"></i>`}
  function Chip(p){var c=p.c;return c?html`<span class=${'chip'+(c.cls?' '+c.cls:'')} title=${c.title||''}>${c.text}</span>`:html`<span class="chip" hidden></span>`}
  function dur(s){s=Math.round(s||0);return s<90?s+' s':s<5400?Math.floor(s/60)+' min'+(s%60?' '+s%60+' s':''):Math.floor(s/3600)+' h '+Math.round(s%3600/60)+' min'}
  function secsOf(st){return st.state==='working'?Math.max(0,Math.round((Date.now()-Date.parse(st.started))/1000)):st.seconds}
  function BatchSelect(p){
    var i=fresh(p.i), S=useStore(), d=cache[i.agent]||{}, pend=useState(null), NONE='No batch yet';
    var batches=(d.list||[]).map(function(x){return x.batch}).concat(Object.keys(d.batches||{}),[i.batch]).filter(function(b,k,arr){return b&&arr.indexOf(b)===k}).sort().reverse();
    var waiting=pend[0]!==null&&pend[0].v!==(i.batch||'');
    return html`<select class="rsel bsel" aria-label="Batch" title=${pend[0]&&pend[0].err||'Batch of this card'} disabled=${waiting&&!(pend[0]&&pend[0].err)} value=${waiting?pend[0].v:i.batch||''} onChange=${function(e){var v=e.target.value;pend[1]({v:v});
      postJSON('batch/'+i.agent+'/'+i.num,{batch:v}).then(function(r){if(!r.ok)pend[1]({v:v,err:'server said '+r.status})}).catch(function(){pend[1](null)})}}>
      ${batches.map(function(b){return html`<option value=${b}>${'Batch '+b}</option>`})}<option value="">${NONE}</option></select>`;
  }
  // Rerun: one of the three answers again with feedback for it, alone («rerun») or with the steps after it as a
  // sequence («rerun + later steps»). run.py first moves the issue branch back to where the step started; the server
  // refuses while the worktree has uncommitted changes and says why, shown here. When it ends and the issue's
  // resolution session is live, the server tells the session. In the resolution panel the step and the feedback come
  // prefilled from the session's latest blame in cards/<n>/resolve/stage.json.
  var PREP_STEPS=['analysis','strategy','context'];
  function blameOf(entries){
    for(var k=(entries||[]).length-1;k>=0;k--){var e=entries[k]||{};
      if((e.stage==='review'&&e.state==='wrong')||(e.stage==='fix'&&e.state==='misguided')){var step=PREP_STEPS.indexOf(e.step)>=0?e.step:PREP_STEPS.indexOf(e.note)>=0?e.note:null;
        return {step:step,note:e.note&&e.note!==step?e.note:''}}}
    return null}
  function Rerun(p){
    var agent=p.agent, num=p.num, fixed=p.step, pre=p.prefill||null;
    var sel=useState(fixed||(pre&&pre.step)||'analysis'), fb=useState(pre&&pre.note||''), touched=useRef(false), msg=useState(null);
    var src=useState(null), from=src[0]||(pre&&pre.note&&fb[0]===pre.note?'resolver':'ruling');
    useEffect(function(){if(pre&&!touched.current){if(!fixed&&pre.step)sel[1](pre.step);fb[1](pre.note||'')}},[pre&&pre.step,pre&&pre.note]);
    var step=fixed||sel[0];
    function go(later){
      var steps=later?PREP_STEPS.slice(PREP_STEPS.indexOf(step)):[step], text=fb[0].trim();
      msg[1]({cls:'working',text:'starting '+steps.map(function(k){return STEP_SHORT[k]}).join(' → ')});
      postJSON(later?'chain/'+agent+'/'+num:'run/'+agent+'/'+num+'/'+step,Object.assign(later?{steps:steps}:{},runOpts(),text?{feedback:text,from:from}:{})).then(function(r){
        if(r.ok){msg[1]({cls:'done',text:'started '+steps.map(function(k){return STEP_SHORT[k]}).join(' → ')});return}
        return errText(r).then(function(t){msg[1]({cls:'failed',text:t})})}).catch(function(){msg[1]({cls:'failed',text:'server unreachable'})});
    }
    return html`<div class="rrn">${fixed?html`<div class="rrh">${'Rerun '+STEP_LABEL[fixed]}</div>`:html`<label class="rrh">Rerun step <select class="rrs" aria-label="Step to rerun" value=${sel[0]} onChange=${function(e){touched.current=true;sel[1](e.target.value)}}>${PREP_STEPS.map(function(k){return html`<option value=${k}>${STEP_LABEL[k]}</option>`})}</select></label>`}<textarea class="rrf" rows="3" placeholder="Feedback for the step: what its answer got wrong" value=${fb[0]} onInput=${function(e){touched.current=true;fb[1](e.target.value)}}></textarea><label class="rrh">Send as <select class="rrs" aria-label="Whose feedback" value=${from} onChange=${function(e){src[1](e.target.value)}}><option value="resolver">the resolver's claim</option><option value="ruling">my ruling</option></select></label><div class="rrb"><button type="button" class="rbtn rrgo" title="Rerun this step with the feedback; the branch goes back to where it started" onClick=${function(){go(false)}}>rerun</button><button type="button" class="rbtn rrall" title="Rerun this step with the feedback, then the steps after it" disabled=${step==='context'} onClick=${function(){go(true)}}>rerun + later steps</button></div>${msg[0]?html`<div class=${'rrm '+msg[0].cls}>${msg[0].text}</div>`:null}</div>`;
  }
  // A popover hung on document.body under its anchor: a control typed into inside a fold's summary would toggle the fold.
  function Floating(p){
    var host=useRef(null);
    useLayoutEffect(function(){var h=host.current=document.createElement('div');h.className='flt';document.body.appendChild(h);
      function away(e){if(!h.contains(e.target)&&!(p.anchor.current&&p.anchor.current.contains(e.target)))p.onClose()}
      function key(e){if(e.key==='Escape'){e.stopPropagation();p.onClose()}}
      document.addEventListener('mousedown',away,true);document.addEventListener('keydown',key,true);
      return function(){document.removeEventListener('mousedown',away,true);document.removeEventListener('keydown',key,true);render(null,h);h.remove()}},[]);
    useLayoutEffect(function(){var h=host.current,a=p.anchor.current;render(p.children,h);
      if(a){var r=a.getBoundingClientRect();h.style.top=(r.bottom+window.scrollY+4)+'px';h.style.left=Math.max(8,Math.min(r.left+window.scrollX,document.documentElement.clientWidth-360))+'px'}});
    return null;
  }
  function staleOf(S,i,step){return (((S.stale||{})[i.agent]||{})[i.num]||{})[step]||null}
  function RunStrip(p){
    var i=p.i, step=p.step, agent=i.agent, S=useStore(), rr=useState(false), rrRef=useRef(null), stale=staleOf(S,i,step);
    var r=useStatus(Paths.status(agent,i.num,step),stepState(S,i,step)), st=r[0];
    var loc=useState(null), local=loc[0], setLocal=loc[1], res=useState(false);
    useEffect(function(){if(local&&!local.sticky)setLocal(null)},[st]);
    useEffect(function(){var live=true;if(step==='resolve'&&st&&st.state==='failed')getJSON('chat/'+agent+'/'+i.num+'/state').then(function(x){if(live)res[1](!!(x&&x.resumable))});else res[1](false);return function(){live=false}},[st]);
    function start(resume){
      setLocal({chip:{cls:'working',text:'starting'},busy:true});
      postJSON(step==='resolve'?'chat/'+agent+'/'+i.num+'/start':'run/'+agent+'/'+i.num+'/'+step,Object.assign(runOpts(),resume?{resume:true}:{})).then(function(x){
        if(!x.ok)return errText(x).then(function(msg){setLocal({chip:{cls:'failed',text:msg.slice(0,60),title:msg},sticky:x.status!==409});if(x.status===409)setTimeout(r[1],1500)});
        setTimeout(r[1],1500); if(step==='resolve')Session.toggle(agent,i.num,step,true);
      }).catch(function(){setLocal({chip:{cls:'failed',text:'failed',title:'server unreachable'},sticky:true})});
    }
    function stop(){setLocal({chip:{cls:(st&&st.state)||'working',text:'stopping'},stopping:true});
      postJSON(step==='resolve'?'chat/'+agent+'/'+i.num+'/stop':'kill/'+agent+'/'+i.num+'/'+step).then(function(){setTimeout(r[1],1500)}).catch(function(){setLocal(null)})}
    var working=!!(st&&st.state==='working'), chip=null;
    if(st){
      var secs=secsOf(st), u=st.usage||{}, lv=st.live||{};
      chip={cls:st.state+(working&&lv.quiet>=20&&!lv.tool?' quiet':''),title:st.state==='failed'?(st.error||''):(st.model||'')+' · '+(st.commit||'')+(u.in||u.cached?' · '+usageLine(u):''),
        text:working?(step==='resolve'?'live · ':'working · ')+dur(secs)+(lv.quiet>=20?(lv.tool?' · tool running ':' · no data ')+lv.quiet+' s':''):st.state==='done'?'done · '+dur(secs)+' · '+(st.model||'').replace('gpt-5.6-','')+' '+(st.effort||''):/^stopped/.test(st.error||'')?'stopped · '+dur(secs):'failed'};
    }
    if(local&&local.chip)chip=local.chip;
    var kbHidden=local&&local.busy?false:!working, resume=step==='resolve'&&res[0]&&!working&&!(local&&local.busy);
    return html`<span class="run">${stale?html`<span class="chip stale" title=${'Out of date: '+stale}>stale</span>`:null}<${Chip} c=${chip}/><button class="rbtn" title=${'Run '+STEP_LABEL[step]} aria-label=${'Run '+STEP_LABEL[step]} disabled=${working||!!(local&&local.busy)} onClick=${function(){start(false)}}><${Icon} n="ti-player-play"/></button>${resume?html`<button class="rbtn rsm" title="Resume the last session: pi picks up its session file where it stopped" aria-label="Resume the session" onClick=${function(){start(true)}}><${Icon} n="ti-player-track-next"/></button>`:null}<button class="rbtn kbtn" title="Stop this run" aria-label="Stop this run" hidden=${kbHidden} disabled=${!!(local&&local.stopping)} onClick=${stop}><${Icon} n="ti-player-stop"/></button><button class="rbtn sbtn2" title="Session details" aria-label="Session details" disabled=${!st} onClick=${function(){Session.toggle(agent,i.num,step)}}><${Icon} n="ti-list-details"/></button>${PREP_STEPS.indexOf(step)>=0?html`<button class=${'rbtn rrb1'+(rr[0]?' on':'')} ref=${rrRef} title="Rerun with feedback" aria-label=${'Rerun '+STEP_LABEL[step]+' with feedback'} aria-expanded=${String(rr[0])} disabled=${working} onClick=${function(){rr[1](!rr[0])}}><${Icon} n="ti-arrow-back-up"/></button>`:null}${rr[0]?html`<${Floating} anchor=${rrRef} onClose=${function(){rr[1](false)}}><${Rerun} agent=${agent} num=${i.num} step=${step}/></${Floating}>`:null}</span>`;
  }
  // Lane: the issue's own worktree and Studio workspace (setup.py). Every step runs there, so the four run buttons wait
  // for it.
  function SetupLane(p){
    var i=fresh(p.i), agent=i.agent, S=useStore();
    var r=useStatus(Paths.status(agent,i.num,'setup'),stepState(S,i,'setup')), st=r[0], loc=useState(null), local=loc[0];
    useEffect(function(){if(local&&!local.sticky)loc[1](null)},[st]);
    var bb=((cache[agent]||{}).batches||{})[i.batch]||{}, title="Set up this issue's own worktree and Studio workspace; every step runs there"+(i.batch?(bb.base?'\nBranch off '+bb.base+' (batch '+i.batch+')':'\nBatch '+i.batch+' has no base branch yet: set it in the sidebar'):'\nPut the card in a batch first');
    var chip=null, working=!!(st&&st.state==='working');
    if(st){var secs=secsOf(st);
      chip=working?{cls:'working',text:'setting up · '+(st.step||'')+' · '+dur(secs)}:st.state==='done'?{cls:'done',text:st.name||'ready',title:[st.worktree,st.branch+(st.base?' off '+st.base:'')+' @ '+(st.commit||''),st.workspace].filter(Boolean).join('\n')}:{cls:st.state,text:/^stopped/.test(st.error||'')?'stopped':'setup failed',title:st.error||''}}
    if(local&&local.chip)chip=local.chip;
    function start(){loc[1]({chip:{cls:'working',text:'starting'},busy:true});
      postJSON('setup/'+agent+'/'+i.num).then(function(x){if(!x.ok)return x.json().catch(function(){return {}}).then(function(j){loc[1]({chip:{cls:'failed',text:j.error||('server said '+x.status),title:j.error||''},sticky:true})});setTimeout(r[1],1500)}).catch(function(){loc[1]({chip:{cls:'failed',text:'setup failed',title:'server unreachable'},sticky:true})})}
    function stop(){loc[1]({chip:{cls:'working',text:'stopping'},stopping:true});postJSON('kill/'+agent+'/'+i.num+'/setup').then(function(){setTimeout(r[1],1500)}).catch(function(){loc[1](null)})}
    return html`<span class="run lane">${st&&st.state==='done'&&!(local&&local.chip)?html`<${Icon} n="ti-git-branch"/>`:null}<${Chip} c=${chip}/><button class="rbtn" title=${title} aria-label="Set up worktree and workspace" hidden=${!!(st&&st.state==='done')} disabled=${working||!!(local&&local.busy)} onClick=${start}><${Icon} n="ti-git-branch"/></button><button class="rbtn kbtn" title="Stop the setup" aria-label="Stop the setup" hidden=${!working} disabled=${!!(local&&local.stopping)} onClick=${stop}><${Icon} n="ti-player-stop"/></button></span>`;
  }
  // Steps to run in order: toggles for setup, analysis, strategy, context and resolution, and one button that runs the
  // chosen ones one after another on the server (POST chain/<agent>/<n>); while it runs, a chip says which step of how
  // many, and stop ends it after the current step. The same toggles sit in the sidebar's selection bar.
  var STEP_ORDER=['setup','analysis','strategy','context','resolve'], STEP_SHORT={setup:'setup',analysis:'analysis',strategy:'strategy',context:'context',resolve:'resolution'};
  function chosenSteps(){return (pref('chainSteps')||'analysis,strategy,context').split(',').filter(function(k){return STEP_ORDER.indexOf(k)>=0})}
  function StepToggles(p){var v=usePref('chainSteps','analysis,strategy,context'), on=v[0].split(',');
    return html`<span class="stps" id=${p.id}>${STEP_ORDER.map(function(k){var o=on.indexOf(k)>=0;return html`<button type="button" class=${'stp'+(o?' on':'')} data-s=${k} aria-pressed=${String(o)} onClick=${function(e){e.preventDefault();v[1](STEP_ORDER.filter(function(x){return x===k?!o:on.indexOf(x)>=0}).join(','))}}>${STEP_SHORT[k]}</button>`})}</span>`}
  function Chain(p){
    var i=p.i, agent=i.agent, S=useStore(), st=((S.chains||{})[agent]||{})[i.num]||null, pop=useState(false), popRef=useRef(null), loc=useState(null), local=loc[0];
    var fetched=useStatus(Paths.chain(agent,i.num),JSON.stringify(st)+(local?local.k:''))[0];
    if(fetched!==undefined&&(!st||(fetched&&fetched.started>=st.started)))st=fetched;
    useEffect(function(){if(local&&!local.sticky&&st&&st.state==='working')loc[1](null)},[st&&st.state,st&&st.at]);
    var working=!!(st&&st.state==='working'), chip=null;
    if(st&&!(st.state==='done'&&!working)){var at=st.steps.indexOf(st.at);chip={cls:st.state==='stopped'?'':st.state,text:working?(at+1)+'/'+st.steps.length+' · '+STEP_SHORT[st.at]:st.state==='stopped'?'sequence stopped':'sequence failed',title:st.steps.map(function(k){return STEP_SHORT[k]}).join(' → ')+(st.error?'\n'+st.error:'')}}
    if(local&&local.chip)chip=local.chip;
    function go(){var steps=chosenSteps();if(!steps.length)return;pop[1](false);loc[1]({chip:{cls:'working',text:'starting'},k:Date.now()});
      postJSON('chain/'+agent+'/'+i.num,Object.assign({steps:steps},runOpts())).then(function(x){return x.json().catch(function(){return {}}).then(function(j){if(!x.ok){loc[1]({chip:{cls:'failed',text:j.error||('server said '+x.status)},sticky:true});return}setTimeout(function(){loc[1]({k:Date.now()})},1000)})}).catch(function(){loc[1]({chip:{cls:'failed',text:'server unreachable'},sticky:true})})}
    function stop(){loc[1]({stopping:true,k:Date.now()});postJSON('chain/'+agent+'/'+i.num+'/stop').then(function(){loc[1]({k:Date.now()})}).catch(function(){loc[1](null)})}
    return html`<span class="run chain"><${Chip} c=${chip}/><button class="rbtn lbl cho" ref=${popRef} title="Run several steps in order" aria-label="Run several steps in order" aria-expanded=${String(pop[0])} hidden=${working} onClick=${function(){pop[1](!pop[0])}}><${Icon} n="ti-player-play"/>Run steps<${Icon} n="ti-chevron-down"/></button><button class="rbtn kbtn" title="Stop after the current step" aria-label="Stop the sequence" hidden=${!working} disabled=${!!(local&&local.stopping)} onClick=${stop}><${Icon} n="ti-player-stop"/></button>${pop[0]&&!working?html`<${Floating} anchor=${popRef} onClose=${function(){pop[1](false)}}><div class="rrn chpop"><div class="rrh">Run these steps in order</div><${StepToggles}/><div class="rrb"><button type="button" class="rbtn cgo" title="Run the chosen steps one after another" aria-label="Run the chosen steps" onClick=${go}>run</button></div></div></${Floating}>`:null}</span>`;
  }
  // What the ticket has cost so far, every model run of every step (the ledger through GET steps); the tooltip splits it.
  function Cost(p){var S=useStore(), t=((S.cost||{})[p.i.agent]||{})[p.i.num]; if(!t||!t.cost)return null;
    var names={analysis:'analysis',strategy:'sim strategy',context:'context edit',resolve:'resolution'};
    return html`<span class="chip cost" title=${'Spent on this ticket over '+t.runs+' run'+(t.runs===1?'':'s')+'\n'+Object.keys(t.steps).map(function(k){return (names[k]||k)+': $'+t.steps[k].toFixed(2)}).join('\n')+'\nList prices as pi reports them'}>$${t.cost.toFixed(2)}</span>`}
  // Reset: every step's answer and the card go to history, the card empties, a live session stops, uncommitted changes go to a git stash; the branch and workspace stay. Two clicks:
  // the first arms the button for four seconds.
  function Reset(p){var i=p.i, s=useState({}), st=s[0], T='Reset every step: the answers and the card go to history, the card empties', timer=useRef(null);
    useEffect(function(){return function(){if(timer.current)clearTimeout(timer.current)}},[]);
    function arm(title){if(timer.current)clearTimeout(timer.current);s[1]({armed:true,title:title});timer.current=setTimeout(function(){timer.current=null;s[1]({})},4000)}
    function click(){
      if(!st.armed){arm('Click again to reset every step');return}
      if(timer.current)clearTimeout(timer.current);timer.current=null;s[1]({busy:true});
      postJSON('reset/'+i.agent+'/'+i.num).then(function(r){return r.json().catch(function(){return {}}).then(function(j){
        if(!r.ok){arm(j.error||('server said '+r.status));return}
        delete cache[i.agent]; window.dispatchEvent(new Event('hashchange'));
      })}).catch(function(){s[1]({title:'server unreachable'})});
    }
    return html`<button class=${'rbtn lbl rstb'+(st.armed?' arm':'')} title=${st.title||T} aria-label="Reset every step" disabled=${!!st.busy} onClick=${click}>${st.armed?'Click again':'Reset'}</button>`}
  function TopBar(p){var i=p.i;if(!i.agent)return null;
    return html`<${SetupLane} i=${i}/><${BatchSelect} i=${i}/><span class="vsep"></span><${Models}/><span class="rgt"><${Cost} i=${i}/><span class="vsep"></span><${Chain} i=${i}/><button class="rbtn lbl hstb" title="The card's history: every event the agents' briefs index" aria-label="Card history" onClick=${function(){History.toggle(i.agent,i.num)}}><${Icon} n="ti-history"/>History</button><button class="rbtn lbl flsb" title="Every file of the card: its issue and calls, its answers, runs and history" aria-label="Card files" onClick=${function(){Files.toggle(i.agent,i.num)}}><${Icon} n="ti-folder"/>Files</button><${Reset} i=${i}/></span>`}
  // Drawers: one aside at a time on the right (the context may sit beside the transcript), each a component in a host
  // element of its own; toggle, close and state as before, state being what the card's view memory keeps.
  function Drawer(){var host=null;return {
    open:function(vnode){this.close();host=document.createElement('div');document.body.appendChild(host);render(vnode,host)},
    close:function(){if(host){render(null,host);host.remove();host=null}},
    box:function(){return host&&host.firstElementChild}}}
  // Context drawer: the compiled request the agent model saw at one turn (GET request/<agent>/<call>/<turn>): the system
  // parts split by their top-level tags, the tools, the messages, with a filter and arrows to step through the agent turns.
  // Opened from the transcript it sits beside it; otherwise it takes the transcript's place.
  var Context=(function(){
    var dw=Drawer(), cur=null, data=null, beside=false, want=null;
    function close(){dw.close();cur=null;data=null;want=null;document.body.classList.remove('ctx-beside')}
    function state(){var box=dw.box();if(!box)return null;if(want)return want;var tl=box.querySelector('.tl');return {conv:cur.split('/')[2],entry:data&&data.turn,beside:beside,q:box.querySelector('.q').value,open:Array.prototype.map.call(box.querySelectorAll('.cs'),function(d){return d.open?1:0}),scroll:tl.scrollTop}}
    function sections(text){
      // top-level <tag> … </tag> blocks of the system text; text outside any tag is its own part
      var out=[],lines=text.split('\n'),depth=0,curS=null,loose=[];
      lines.forEach(function(l){
        var o=/^<([^\s<>/]+)>\s*$/.exec(l), c=/^<\/([^\s<>/]+)>\s*$/.exec(l);
        if(o&&depth===0){if(loose.join('').trim())out.push({tag:'',lines:loose});loose=[];curS={tag:o[1],lines:[]};depth=1;return}
        if(curS){if(o)depth++; if(c){depth--; if(depth===0){out.push(curS);curS=null;return}} curS.lines.push(l);return}
        loose.push(l);
      });
      if(curS)out.push(curS); if(loose.join('').trim())out.push({tag:'',lines:loose});
      return out;
    }
    function bodyHtml(lines){
      var h=[],ul=false;
      lines.forEach(function(l){
        var o=/^\s*<([^\s<>/]+)>\s*$/.exec(l), c=/^\s*<\/[^\s<>/]+>\s*$/.exec(l);
        if(c){if(ul){h.push('</ul>');ul=false}return}
        if(o){if(ul){h.push('</ul>');ul=false}h.push('<div class="sub">'+esc(o[1])+'</div>');return}
        var b=/^\s*[-*•]\s+(.*)$/.exec(l);
        if(b){if(!ul){h.push('<ul>');ul=true}h.push('<li>'+esc(b[1])+'</li>');return}
        if(ul){h.push('</ul>');ul=false}
        if(l.trim())h.push('<p>'+esc(l)+'</p>');
      });
      if(ul)h.push('</ul>');
      return h.join('');
    }
    function partsOf(d){
      var parts=[];
      (d.system||[]).forEach(function(m){sections(m.text).forEach(function(sec){parts.push({title:sec.tag||m.role,kind:'sys',html:bodyHtml(sec.lines),text:sec.lines.join('\n')})})});
      (d.tools||[]).forEach(function(t){parts.push({title:t.name,kind:'tool',html:'<p>'+esc(t.description)+'</p>'+(t.parameters?'<pre>'+esc(JSON.stringify(t.parameters,null,1))+'</pre>':''),text:t.name+' '+t.description+' '+JSON.stringify(t.parameters||{})})});
      var msgs=(d.messages||[]).map(function(m){return '<div class="msg '+esc(m.role||'')+'"><i class="ti '+(m.role==='user'?'ti-user':'ti-robot')+'" aria-hidden="true"></i><span>'+esc(m.text)+'</span></div>'}).join('');
      parts.push({title:'messages',kind:'msgs',html:msgs,text:(d.messages||[]).map(function(m){return m.text}).join('\n')});
      return parts;
    }
    function filter(){
      var box=dw.box(); if(!box)return; var q=(box.querySelector('.q').value||'').trim().toLowerCase(), parts=box._parts||[];
      box.querySelectorAll('.cs').forEach(function(el_,k){var p=parts[k]; if(!p)return; var hit=!q||p.text.toLowerCase().indexOf(q)>=0||p.title.toLowerCase().indexOf(q)>=0; el_.hidden=!hit; if(q&&hit)el_.open=true;
        el_.querySelectorAll('mark').forEach(function(m){m.replaceWith(document.createTextNode(m.textContent))}); el_.normalize();
        if(q&&hit){var w=document.createTreeWalker(el_.querySelector('.cb'),NodeFilter.SHOW_TEXT),nodes=[],nd;while((nd=w.nextNode()))nodes.push(nd);
          nodes.forEach(function(n){var t=n.nodeValue,lo=t.toLowerCase(),i=lo.indexOf(q);if(i<0)return;var f=document.createDocumentFragment(),pos=0;while(i>=0){f.appendChild(document.createTextNode(t.slice(pos,i)));var mk=document.createElement('mark');mk.textContent=t.slice(i,i+q.length);f.appendChild(mk);pos=i+q.length;i=lo.indexOf(q,pos)}f.appendChild(document.createTextNode(t.slice(pos)));n.replaceWith(f)})}});
    }
    function Panel(p){
      var i=p.i, conv=p.conv, s=useState({loading:true}), d=s[0].d, box=useRef(null);
      function load(entry){s[1](function(x){return {loading:true,d:x.d}});
        getJSON('request/'+i.agent+'/'+i.num+'/'+conv+(entry?'/'+entry:'')).then(function(j){data=j||{error:'server unreachable',turns:[]};s[1]({d:data})})}
      useEffect(function(){api.load=load;load(p.entry)},[]);
      var parts=useMemo(function(){return d&&!d.error?partsOf(d):[]},[d]);
      useLayoutEffect(function(){var b=box.current;if(!b||!d)return;b._parts=parts;filter();
        if(want){var w=want;want=null;b.querySelectorAll('.cs').forEach(function(x,k){if(w.open&&k<w.open.length)x.open=!!w.open[k]});b.querySelector('.tl').scrollTop=w.scroll||0}},[parts]);
      var turns=(d&&d.turns)||[], at=d?turns.map(function(t){return t.turn}).indexOf(d.turn):-1;
      var sysChars=d?(d.system||[]).reduce(function(a,m){return a+m.text.length},0):0;
      var hd=s[0].loading?'loading…':d.error?null:[d.model,Object.keys(d.settings||{}).map(function(k){var v=d.settings[k];return k+' '+(typeof v==='object'?JSON.stringify(v):v)}).join(' · '),Math.round(sysChars/1000)+'k chars of system text',(d.tools||[]).length+' tools',(d.messages||[]).length+' messages','trace '+d.trace].filter(Boolean).join(' · ');
      return html`<aside class=${'sess ctx'+(beside?' beside':'')} role="dialog" aria-label="Agent context" ref=${box}><header><span class="ttl">${d?'#'+i.num+' · context at agent turn '+(at+1)+' of '+turns.length:'#'+i.num+' · context'}</span><button class="rbtn prev" title="Previous agent turn" aria-label="Previous agent turn" disabled=${!d||at<=0} onClick=${function(){if(at>0)load(turns[at-1].turn)}}><${Icon} n="ti-chevron-left"/></button><button class="rbtn next" title="Next agent turn" aria-label="Next agent turn" disabled=${!d||at<0||at>=turns.length-1} onClick=${function(){if(at<turns.length-1)load(turns[at+1].turn)}}><${Icon} n="ti-chevron-right"/></button><input class="q" type="search" placeholder="filter" aria-label="Filter the context" defaultValue=${p.q||''} onInput=${filter}/><button class="sbtn" aria-label="Close" onClick=${close}><${Icon} n="ti-x"/></button></header>
        <div class="hd2">${hd===null?html`<span class="err">${d.error}</span>`:hd}</div><div class="tl" data-n=${String(parts.length)}>${parts.map(function(x,k){return html`<details class=${'cs '+x.kind} data-k=${k} open=${x.kind==='sys'&&k<1} key=${(d&&d.turn)+'/'+k}><summary><${Icon} n="ti-chevron-right"/><span class="t">${x.title}</span><span class="cnt">${x.text.length>=1000?Math.round(x.text.length/1000)+'k':x.text.length}</span></summary><div class="cb" dangerouslySetInnerHTML=${{__html:x.html}}></div></details>`})}</div></aside>`;
    }
    var api={};
    function toggle(i,conv,entry,fromTranscript,restore){
      var k=i.agent+'/'+i.num+'/'+conv;
      if(dw.box()&&cur===k){if(entry&&data&&data.turn!==entry){api.load(entry);return}close();return}
      close(); if(!fromTranscript){Transcript.close();Session.close();History.close();Files.close()} cur=k; beside=!!fromTranscript; want=restore||null;
      if(beside)document.body.classList.add('ctx-beside');
      dw.open(html`<${Panel} i=${i} conv=${conv} entry=${entry} q=${restore&&restore.q}/>`);
    }
    return {toggle:toggle,close:close,state:state};
  })();
  // Transcript drawer: the whole linked call as the server reads it from the cache (GET call/<agent>/<call>, the same
  // parse card.py renders the card from), turns numbered as on the card, the reporter's line marked, the failure turn
  // red, agent lines the customer cut off shown with their unspoken rest.
  var Transcript=(function(){
    var dw=Drawer(), cur=null, want=null;
    function close(){if(dw.box()){dw.close();Context.close()}cur=null;want=null}
    function state(){var box=dw.box();if(!box)return null;return want||{conv:cur.split('/')[2],scroll:box.querySelector('.tl').scrollTop}}
    function toolHtml(t){return esc(t.name)+(t.args==null?'':' <span class="arg">'+esc(t.args)+'</span>')}
    function toolRow(t,q){return '<div class="row tcall"'+(q!=null?' title="tools['+q+'] of the turn below"':'')+'><span class="n"><i class="ti ti-tool" aria-hidden="true"></i></span><span>'+toolHtml(t)+'</span></div>'}
    function fmtDur(s){s=Math.round(s||0);return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
    function rowsOf(d,an,call){
      var hl={}; (call.marked||[]).forEach(function(x){hl[x.turn]=x.text||''});
      var fid=(an.failure||{}).turn||(an.failure||{}).logEntryId||'', rows=[];
      (d.rows||[]).forEach(function(e){
        if(e.tags){rows.push('<div class="row tags"><span class="n"><i class="ti ti-tag" aria-hidden="true"></i></span><span>'+esc(e.tags.join(' · '))+'</span></div>');return}
        (e.tools||[]).forEach(function(t,q){rows.push(toolRow(t,e.role?q:null))});
        if(!e.role)return;
        var text=e.text||'',h=esc(text),id=e.turn||'',n=e.n||'';
        if(id in hl){var x=hl[id];h=x&&x!==text&&text.indexOf(x)>=0?esc(text.slice(0,text.indexOf(x)))+'<span class="hl">'+esc(x)+'</span>'+esc(text.slice(text.indexOf(x)+x.length)):'<span class="hl">'+h+'</span>'}
        if(e.cut)h+=' <span class="cut" title="The customer cut in here; the rest was never spoken"><i class="ti ti-scissors" aria-hidden="true"></i>'+esc(e.cut)+'</span>';
        var nn=e.role==='assistant'&&id?'<a class="tl" href="#" data-e="'+esc(id)+'" title="What the agent model saw at this turn">'+n+'<i class="ti ti-robot" aria-hidden="true"></i></a>':n+'<i class="ti '+(e.role==='user'?'ti-user':'ti-robot')+'" aria-hidden="true"></i>';
        rows.push('<div class="row'+(id&&id===fid?' bad':'')+'"><span class="n">'+nn+'</span><span>'+h+'</span></div>');
      });
      return rows.join('');
    }
    function Panel(p){
      var i=p.i, conv=p.conv, call=(i.calls||[]).filter(function(c){return c.id===conv})[0]||{}, s=useState(null), box=useRef(null);
      useEffect(function(){
        Promise.all([
          fetch('call/'+i.agent+'/'+i.num+'/'+conv,{cache:'no-store'}).then(function(r){return r.json().then(function(j){return r.ok?j:{error:j.error||('server said '+r.status)}})}).catch(function(){return {error:'server unreachable'}}),
          getJSON(Paths.answer(i.agent,i.num,'analysis'))
        ]).then(function(rr){s[1]({d:rr[0],an:rr[1]||{}})});
      },[]);
      useLayoutEffect(function(){if(!s[0]||s[0].d.error)return;var tl=box.current.querySelector('.tl');if(want){tl.scrollTop=want.scroll||0;want=null}else{var b=tl.querySelector('.row.bad');if(b)b.scrollIntoView({block:'center'})}},[s[0]]);
      var d=s[0]&&s[0].d, md=(d&&d.metadata)||{}, ts=md.timestamp||call.timestamp||'';
      var hd=!d?'loading…':d.error?null:[ts?ts.slice(8,10)+'/'+ts.slice(5,7)+' '+ts.slice(11,16):'',md.duration!=null?fmtDur(md.duration):'',(md.message_count||0)+' messages',conv].filter(Boolean).join(' · ');
      return html`<aside class="sess conv" role="dialog" aria-label="Call transcript" ref=${box}><header><span class="ttl">${'#'+i.num+' · call'}</span><span class="st"></span>${call.url?html`<a class="rbtn" href=${call.url} target="_blank" rel="noopener" title="Open in Studio"><${Icon} n="ti-external-link"/></a>`:null}<button class="sbtn" aria-label="Close" onClick=${close}><${Icon} n="ti-x"/></button></header>
        <div class="hd2">${hd===null?html`<span class="err">${d.error}</span>`:hd}</div><div class="tl"><div class="ia"><div class="part"><div class="body" onClick=${function(ev){var a=ev.target.closest('a.tl');if(!a)return;ev.preventDefault();Context.toggle(i,conv,a.dataset.e,true)}} dangerouslySetInnerHTML=${{__html:d&&!d.error?rowsOf(d,s[0].an,call):''}}></div></div></div></div></aside>`;
    }
    function toggle(i,conv,restore){
      var k=i.agent+'/'+i.num+'/'+conv; if(dw.box()&&cur===k){close();return} close(); Session.close(); Context.close(); History.close(); Files.close(); cur=k; want=restore||null;
      dw.open(html`<${Panel} i=${i} conv=${conv}/>`);
    }
    return {toggle:toggle,close:close,state:state};
  })();
  // Session drawer: the run's status, its events as a timeline of rows, the answer and stderr. A resolution session's
  // events come from its event stream and are folded in as they arrive; another step's log is read again every 2 s
  // while it runs. Rows keep their place, so an open output fold stays open while the timeline grows.
  function fmtK0(n){return n>=1000?Math.round(n/1000)+'k':String(n||0)}
  function offOf(t,t0){var d=(Date.parse(t)-t0)/1000;return isNaN(d)?'':(d<60?d.toFixed(0)+'s':Math.floor(d/60)+'m'+('0'+Math.round(d%60)).slice(-2))}
  // The agent's reply as text to read: paragraphs, lists, headings, code spans and fenced blocks.
  function msgHtml(tx){
    var out=[],para=[],list=null,fence=null;
    function inline(x){return esc(x).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>')}
    function flush(){if(para.length){out.push('<p>'+para.map(inline).join('<br>')+'</p>');para=[]}if(list){out.push('<'+list.t+'>'+list.items.map(function(x){return '<li>'+inline(x)+'</li>'}).join('')+'</'+list.t+'>');list=null}}
    tx.split('\n').forEach(function(l){
      if(fence){if(/^\s*```/.test(l)){out.push('<pre>'+esc(fence.join('\n'))+'</pre>');fence=null}else fence.push(l);return}
      if(/^\s*```/.test(l)){flush();fence=[];return}
      var h=/^\s{0,3}#{1,6}\s+(.*)$/.exec(l), u=/^\s*[-*•]\s+(.*)$/.exec(l), o=/^\s*\d+[.)]\s+(.*)$/.exec(l);
      if(!l.trim()){flush();return}
      if(h){flush();out.push('<p><b>'+inline(h[1])+'</b></p>');return}
      if(u||o){var t=u?'ul':'ol';if(para.length||(list&&list.t!==t))flush();list=list||{t:t,items:[]};list.items.push((u||o)[1]);return}
      if(list&&/^\s+\S/.test(l)){list.items[list.items.length-1]+=' '+l.trim();return}
      if(list)flush(); para.push(l);
    });
    if(fence)out.push('<pre>'+esc(fence.join('\n'))+'</pre>'); flush();
    return '<div class="msg">'+out.join('')+'</div>';
  }
  // pi json events (docs/json.md), folded one line at a time: one row per content part or tool call, streamed deltas
  // appended as they land. rows is the timeline; a row that changes is replaced by a new object in its place.
  function PiTimeline(){
    var items={}, out=[], parts={}, msg=0, calls={}, argbuf={}, pending={};
    function row(t,icon,cls,h){return {t:t,icon:icon,cls:cls,html:h}}
    function put(id,e,icon,cls,h){if(items[id]!==undefined)out[items[id]]=row(e.t,icon,cls,h);else{items[id]=out.length;out.push(row(e.t,icon,cls,h))}}
    function partKey(ci){return 'm'+msg+'c'+ci}
    function dialogHtml(e,answer){var h='<b>'+esc(e.title||'')+'</b>'+(e.message?'<div>'+esc(e.message)+'</div>':'')+'<span class="uibs">';
      if(answer!=null)return h+'<small>'+answer+'</small></span>';
      if(e.method==='confirm')h+='<button class="rbtn uib" data-kind="confirm" data-val="yes" data-id="'+esc(e.id)+'">yes</button><button class="rbtn uib" data-kind="confirm" data-val="no" data-id="'+esc(e.id)+'">no</button>';
      else if(e.method==='select')h+=(e.options||[]).map(function(o){return '<button class="rbtn uib" data-kind="select" data-val="'+esc(o)+'" data-id="'+esc(e.id)+'">'+esc(o)+'</button>'}).join('');
      else if(e.method==='input')h+='<input type="text" placeholder="'+esc(e.placeholder||'')+'"><button class="rbtn uib" data-kind="input" data-id="'+esc(e.id)+'">ok</button>';
      return h+'<button class="rbtn uib" data-kind="cancel" data-id="'+esc(e.id)+'">dismiss</button></span>'}
    function push(l){var e;try{e=JSON.parse(l)}catch(x){return}
      var k=e.type, m=e.message||{}, a=e.assistantMessageEvent||{};
      if(k==='session')out.push(row(e.t,'ti-player-play','sys','session started · '+esc(e.id||'')));
      else if(k==='resumed')out.push(row(e.t,'ti-player-track-next','sys','session resumed from its session file'));
      else if(k==='sent')out.push(row(e.t,'ti-user','user',(e.mode==='steer'?'<small>steer</small> ':e.mode==='follow_up'?'<small>after this turn</small> ':'')+(e.text.length>1200?'<details><summary>'+esc(e.text.slice(0,160))+'…</summary><pre>'+esc(e.text)+'</pre></details>':esc(e.text).replace(/\n/g,'<br>'))));
      else if(k==='extension_ui_request'){if(e.method==='confirm'||e.method==='select'||e.method==='input'){pending[e.id]={at:out.length,e:e};out.push(row(e.t,'ti-help-circle','dialog',dialogHtml(e)))}else if(e.method==='notify')out.push(row(e.t,'ti-bell','sys',esc(e.message||e.title||'')))}
      else if(k==='ui_answer'){var pd=pending[e.id], an=e.answer||{};var txt=an.cancelled?'dismissed':an.confirmed===true?'yes':an.confirmed===false?'no':an.value!=null?esc(String(an.value)):'answered';if(pd)out[pd.at]=row(out[pd.at].t,'ti-help-circle','dialog',dialogHtml(pd.e,txt))}
      else if(k==='response'){if(e.success===false)out.push(row(e.t,'ti-alert-triangle','error',esc((e.command||'')+': '+(e.error||'failed'))))}
      else if(k==='exit')out.push(row(e.t,'ti-power','sys','session ended · exit '+esc(e.code)));
      else if(k==='stderr')out.push(row(e.t,'ti-terminal','error',esc(e.text||'')));
      else if(k==='retry')out.push(row(e.t,'ti-repeat','error','answer off schema, asking again: '+esc((e.problems||[]).join('; '))));
      else if(k==='message_start'&&m.role==='assistant')msg++;
      else if(k==='message_end'&&m.role==='assistant'){var u=m.usage||{};out.push({t:e.t,sep:true,title:'model turn done · '+fmtK0(u.input)+' in'+(u.cacheRead?' ('+fmtK0(u.cacheRead)+' cached)':'')+' · '+fmtK0(u.output)+' out'+(u.reasoning?' · '+fmtK0(u.reasoning)+' reasoning':'')+(u.cost&&u.cost.total?' · $'+u.cost.total.toFixed(3):'')+(m.stopReason&&m.stopReason!=='stop'&&m.stopReason!=='toolUse'?' · '+m.stopReason:'')+(m.errorMessage?' · '+m.errorMessage:'')})}
      else if(k==='message_update'){
        var t=a.type||'', ci=a.contentIndex;
        if(/^thinking_/.test(t)){var id=partKey(ci);parts[id]=(t==='thinking_end'&&a.content!=null)?a.content:(parts[id]||'')+(a.delta||'');put(id,e,'ti-brain','reasoning',esc(parts[id])||'<i>thinking</i>')}
        else if(/^text_/.test(t)){var id2=partKey(ci);parts[id2]=(t==='text_end'&&a.content!=null)?a.content:(parts[id2]||'')+(a.delta||'');put(id2,e,'ti-message','agent_message',msgHtml(parts[id2]||''))}
        else if(t==='toolcall_start'){var cid=a.id;calls[partKey(ci)]=cid;argbuf[cid]='';put(cid,e,'ti-terminal-2','command_execution','<code>'+esc(a.toolName||'')+'</code> <small>preparing</small>')}
        else if(t==='toolcall_delta'){var cid2=calls[partKey(ci)];if(cid2){argbuf[cid2]+=(a.delta||'');put(cid2,e,'ti-terminal-2','command_execution','<code>'+esc(argbuf[cid2].slice(0,300))+'</code> <small>preparing</small>')}}
        else if(t==='toolcall_end'){var tc=a.toolCall||{};put(tc.id,e,'ti-terminal-2','command_execution','<code>'+esc(tc.name+' '+JSON.stringify(tc.arguments||{}))+'</code> <small>queued</small>')}
      }
      else if(k==='tool_execution_start'){put(e.toolCallId,e,'ti-terminal-2','command_execution','<code>'+esc(e.toolName+' '+JSON.stringify(e.args||{}))+'</code> <small>running</small>');calls['args:'+e.toolCallId]=e.toolName+' '+JSON.stringify(e.args||{})}
      else if(k==='tool_execution_end'){var o=(e.result&&e.result.text)||'', cmd=calls['args:'+e.toolCallId]||e.toolName;put(e.toolCallId,e,'ti-terminal-2',e.isError?'error':'command_execution','<code>'+esc(cmd)+'</code> <small>'+(e.isError?'error':'done')+' · '+fmtK0(o.length)+' chars</small>'+(o?'<details><summary>output</summary><pre>'+esc(o.slice(0,4000))+(o.length>4000?'\n…':'')+'</pre></details>':''))}
      else if(k==='agent_end')out.push(row(e.t,'ti-check','sys','agent finished'));
      else if(k==='error')out.push(row(e.t,'ti-alert-triangle','error',esc(e.message||JSON.stringify(e))));
    }
    return {push:push,rows:out};
  }
  // The older runs' log (Codex item events), read whole.
  function codexRows(lines){
    var items={}, out=[];
    lines.forEach(function(l){var e;try{e=JSON.parse(l)}catch(x){return}
      var it=e.item||{}, k=e.type;
      if(k==='thread.started')out.push({t:e.t,icon:'ti-player-play',cls:'sys',html:'session started'});
      else if(k==='turn.started')out.push({t:e.t,icon:'ti-corner-down-right',cls:'sys',html:'turn'});
      else if(k==='turn.completed'){var u=e.usage||{};out.push({t:e.t,sep:true,title:'turn done · '+fmtK0(u.input_tokens)+' in'+(u.cached_input_tokens?' ('+fmtK0(u.cached_input_tokens)+' cached)':'')+' · '+fmtK0(u.output_tokens)+' out · '+fmtK0(u.reasoning_output_tokens)+' reasoning'})}
      else if(k==='item.started'||k==='item.completed'){
        var id=it.id||(out.length+''), done=k==='item.completed', h='', icon='ti-dots', cls=it.type||'';
        if(it.type==='command_execution'){var cmd=(it.command||'').replace(/^\/bin\/zsh -lc /,'');var o=it.aggregated_output||'';icon='ti-terminal-2';
          h='<code>'+esc(cmd)+'</code>'+(done?' <small>exit '+esc(it.exit_code)+' · '+fmtK0(o.length)+' chars</small>'+(o?'<details><summary>output</summary><pre>'+esc(o.slice(0,4000))+(o.length>4000?'\n…':'')+'</pre></details>':''):' <small>running</small>')}
        else if(it.type==='reasoning'){icon='ti-brain';h=it.text?esc(it.text):'<i>reasoning</i>'}
        else if(it.type==='agent_message'){icon='ti-message';h=msgHtml(it.text||'')}
        else if(it.type==='error'){icon='ti-alert-triangle';cls='error';h=esc(it.message||'')}
        else if(it.type==='mcp_tool_call'){icon='ti-plug';h=esc((it.server||'')+' '+(it.tool||''))+(done?' <small>'+esc(it.status||'')+'</small>':'')}
        else if(it.type==='web_search'){icon='ti-world-search';h=esc(it.query||'')}
        else if(it.type==='file_change'){icon='ti-file-diff';h=esc(JSON.stringify(it.changes||[]).slice(0,200))}
        else h=esc(it.type||k);
        var r={t:e.t,icon:icon,cls:cls,html:h}; if(items[id]!==undefined)out[items[id]]=r; else{items[id]=out.length;out.push(r)}
      }
      else if(k==='error')out.push({t:e.t,icon:'ti-alert-triangle',cls:'error',html:esc(e.message||JSON.stringify(e))});
    });
    return out;
  }
  function timelineRows(lines){
    if(lines.some(function(l){return /^\{"type": ?"(session|agent_start|sent)"/.test(l)})){var tl=PiTimeline();lines.forEach(tl.push);return tl.rows}
    return codexRows(lines);
  }
  function Ev(p){var r=p.r, o=offOf(r.t,p.t0);
    if(r.sep)return html`<div class="ev sep" title=${o+' · '+r.title}></div>`;
    return html`<div class=${'ev '+r.cls}><span class="t">${o}</span><i class=${'ti '+r.icon} aria-hidden="true"></i><span class="b" dangerouslySetInnerHTML=${{__html:r.html}}></span></div>`}
  var Session=(function(){
    var dw=Drawer(), cur=null, want=null;
    function close(){dw.close();cur=null;want=null}
    function state(){var box=dw.box();if(!box)return null;if(want)return want;var tl=box.querySelector('.tl'),ta=box.querySelector('.comp textarea');return {step:cur.split('/')[2],scroll:tl.scrollTop,bottom:tl.scrollTop+tl.clientHeight>=tl.scrollHeight-40,draft:ta?ta.value:''}}
    function settle(box){if(!want)return;var w=want,tl=box.querySelector('.tl');want=null;tl.scrollTop=w.bottom?tl.scrollHeight:(w.scroll||0);var ta=box.querySelector('.comp textarea');if(ta&&w.draft)ta.value=w.draft}
    // The resolution's session lives under chat/<agent>/<n>/, the batch driver's under driver/<agent>/<batch>/.
    function post(agent,num,what,body,step){return postJSON((step==='driver'?'driver/':'chat/')+agent+'/'+num+'/'+what,body)}
    // A disagreement: the resolver blamed a step, the rerun step disputed points of it, the resolver held them
    // (review contested). The latest claim, reply and rebuttal side by side, and the engineer's ruling.
    function contestOf(entries){
      for(var k=(entries||[]).length-1;k>=0;k--){var e=entries[k]||{};
        if(e.stage==='review'&&e.state==='ruled')return null;
        if(e.stage==='review'&&e.state==='contested'){var claim=null;
          for(var j=k-1;j>=0;j--){var w=entries[j]||{};if(w.stage==='review'&&w.state==='wrong'&&w.step===e.step){claim=w.note;break}}
          return {step:e.step,held:e.note,claim:claim,t:e.t}}}
      return null}
    function Dispute(p){
      var c=p.c, ans=useStatus(Paths.answer(p.agent,p.num,c.step),c.t)[0], gap=useState(false), msg=useState(null);
      var pts=((ans&&ans.feedback)||{}).points||[];
      function rule(side){msg[1]({cls:'working',text:'sending'});
        postJSON('rule/'+p.agent+'/'+p.num,{'for':side,gap:gap[0]}).then(function(r){
          if(r.ok){msg[1]({cls:'done',text:side==='step'?'resolver told the answer stands':STEP_LABEL[c.step]+' rerunning with your ruling'});return}
          return errText(r).then(function(t){msg[1]({cls:'failed',text:t})})}).catch(function(){msg[1]({cls:'failed',text:'server unreachable'})})}
      return html`<div class="dsp"><div class="dsh">${'Resolver and '+STEP_LABEL[c.step]+' disagree'}</div>
        <div class="dsr"><b>Resolver</b><span>${c.claim||''}</span></div>
        <div class="dsr"><b>${STEP_LABEL[c.step]}</b><span>${pts.map(function(x){return html`<div class=${'dsp-pt '+x.verdict}><span class="v">${x.verdict}</span> ${x.claim}${x.verdict==='disputed'?html`<div class="dsw">${x.why}${x.basis?html`<div class="dsb">${x.basis}</div>`:null}</div>`:null}</div>`})}</span></div>
        <div class="dsr"><b>Resolver</b><span>${c.held||''}</span></div>
        <div class="rrb"><button type="button" class="rbtn" onClick=${function(){rule('resolver')}}>Resolver is right</button><button type="button" class="rbtn" onClick=${function(){rule('step')}}>${STEP_LABEL[c.step]+' is right'}</button><label class="dsg"><input type="checkbox" checked=${gap[0]} onChange=${function(e){gap[1](e.target.checked)}}/> skill gap</label></div>
        ${msg[0]?html`<div class=${'rrm '+msg[0].cls}>${msg[0].text}</div>`:null}</div>`;
    }
    // What a batch's check sent back to this card: newest first, the evidence behind a fold.
    function Reopened(p){
      var log=useStatus(Paths.file(p.agent,p.num,'resolve','reopen.json'),p.k)[0]||[];
      if(!log.length)return null;
      return html`<div class="rrw rrn rop"><div class="dsh">${'Reopened by batch '+log[log.length-1].batch}</div>${log.slice().reverse().map(function(e,k){return html`<details open=${k===0}><summary>${'batch '+e.batch+' · '+String(e.t||'').replace('T',' ').replace('Z',' UTC')}</summary><pre>${e.evidence}</pre></details>`})}</div>`}
    function RerunBlock(p){
      var S=useStore(), v=((S.res||{})[p.agent]||{})[p.num]||{}, entries=useStatus(Paths.file(p.agent,p.num,'resolve','stage.json'),JSON.stringify(v.stage||null))[0];
      var blame=entries===undefined?undefined:blameOf(entries), c=entries===undefined?null:contestOf(entries);
      return html`<${Reopened} agent=${p.agent} num=${p.num} k=${JSON.stringify(v.stage||null)}/>${c?html`<div class="rrw rrn"><${Dispute} agent=${p.agent} num=${p.num} c=${c}/></div>`:null}<details class="rrw" open=${!!blame}><summary>Rerun step${blame&&blame.step?html`<span class="rrt">${' · '+STEP_LABEL[blame.step]+' blamed'}</span>`:null}</summary><${Rerun} agent=${p.agent} num=${p.num} prefill=${blame||null}/></details>`;
    }
    function Panel(p){
      var agent=p.agent, num=p.num, step=p.step, drv=step==='driver', chat=step==='resolve'||drv, box=useRef(null), tlRef=useRef(null), ta=useRef(null);
      var s=useState({}), info=s[0], n=useState(0), bump=n[1], stick=useRef(true), feed=useRef(null);
      // what the files say, read again every 2 s while the run works
      useEffect(function(){var live=true,timer=null,runs=Paths.runs(agent,num,step);
        function text(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.text():null}).catch(function(){return null})}
        function tick(){Promise.all([getJSON(Paths.status(agent,num,step)),chat?null:text(runs+'out.jsonl'),text(runs+'err.log'),chat?null:text(Paths.answer(agent,num,step))]).then(function(r){
          if(!live)return; var tl=tlRef.current; if(tl)stick.current=tl.scrollTop+tl.clientHeight>=tl.scrollHeight-8;
          s[1]({st:r[0],rows:chat?null:timelineRows((r[1]||'').split('\n')),last:chat?0:(r[1]||'').split('\n').reduce(function(m,l){var x=/"t": ?"([^"]+)"/.exec(l);return x?Math.max(m,Date.parse(x[1])):m},0),err:r[2]||'',ans:r[3],ready:!chat});
          if(r[0]&&r[0].state==='working')timer=setTimeout(tick,2000)})}
        tick(); return function(){live=false;if(timer)clearTimeout(timer)}},[]);
      // the resolution's event stream, folded into one timeline as lines land; repainted at most every 120 ms
      useEffect(function(){if(!chat)return;var tl=PiTimeline(),pt=null,src=new EventSource((drv?'driver/':'chat/')+agent+'/'+num+'/events');feed.current={tl:tl,ready:false,any:false};
        function schedule(){if(pt)return;pt=setTimeout(function(){pt=null;var el=tlRef.current;if(el)stick.current=el.scrollTop+el.clientHeight>=el.scrollHeight-40;bump(function(k){return k+1})},120)}
        src.onmessage=function(e){feed.current.any=true;tl.push(e.data);schedule()};
        src.addEventListener('ready',function(){feed.current.ready=true;schedule()});
        src.addEventListener('closed',function(){src.close();feed.current.ready=true;schedule()});
        src.onerror=function(){schedule()};
        return function(){src.close();if(pt)clearTimeout(pt)}},[]);
      var rows=chat?(feed.current?feed.current.tl.rows:[]):(info.rows||[]), ready=chat?!!(feed.current&&feed.current.ready):info.ready;
      useLayoutEffect(function(){var tl=tlRef.current;if(!tl)return;if(want&&ready){settle(box.current);return}if(stick.current)tl.scrollTop=tl.scrollHeight},[rows.length,n[0],info]);
      useEffect(function(){if(chat&&!want&&ta.current)ta.current.focus()},[]);
      var st=info.st, t0=st?Date.parse(st.started):0, secs=st?(st.state==='working'?Math.max(0,Math.round((Date.now()-t0)/1000)):st.seconds):null, u=(st&&st.usage)||{};
      var hd=st?'<div>'+esc(st.model||'')+' · '+esc(st.effort||'')+' · commit '+esc(st.commit||'')+'</div><div>started '+esc((st.started||'').replace('T',' ').replace('Z',' UTC'))+(secs!=null?' · '+secs+' s':'')+'</div>'+(st.usage?'<div>'+usageLine(u)+'</div>'+(st.usage_all?'<div>all sessions of this issue · '+usageLine(st.usage_all)+'</div>':''):'')+(st.state==='working'&&st.live?'<div class="'+(st.live.quiet>=20&&!st.live.tool?'err':'')+'">'+(st.live.tool?'a tool is running · ':'')+(st.live.quiet>=20?'no event for '+st.live.quiet+' s':'events flowing')+' · sampled '+esc((st.live.at||'').slice(11,19))+'</div>':'')+(st.error?'<div class="err">'+esc(st.error.split('\n')[0])+'</div>':''):'';
      var wait=!chat&&st&&st.state==='working'&&info.last&&Date.now()-info.last>8000;
      var tail=(info.err||'').split('\n').filter(Boolean).slice(-12).join('\n'), ans=info.ans&&st&&st.state==='done'?info.ans:null;
      var sent=!!(st&&st.asked), note=useState(null), prm=useState(null), pk=(st&&st.started||'')+'|'+(st&&st.asked||'');
      // What the model got first: the system prompt and the opening message; for the resolution, the instructions sent later too.
      useEffect(function(){if(st===undefined)return;var live=true,runs=Paths.runs(agent,num,step);
        function text(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.ok?r.text():null}).catch(function(){return null})}
        Promise.all([text(runs+'system.md'),text(runs+(chat?'brief.md':'prompt.md')),chat&&st&&st.asked?text(runs+'ask.md'):null]).then(function(r){if(!live)return;var sys=r[0],msg=r[1],ask=r[2];
          function part(label,tx){return '<div class="pl">'+esc(label)+(tx==null?' · not recorded':' · '+fmtK(tx.length)+' chars')+'</div>'+(tx==null?'':'<pre>'+esc(tx)+'</pre>')}
          prm[1](st?part('System prompt',sys)+part(chat?'First message':'Message',msg)+(ask&&msg!=null&&msg.indexOf(ask.slice(0,400))<0?part('Resolution instructions · sent '+String(st.asked).replace('T',' ').replace('Z',' UTC'),ask):''):'<div class="pl">no run yet</div>')});
        return function(){live=false}},[pk,st===undefined]);
      function send(mode){var el=ta.current,text=el.value.trim();if(!text)return;el.disabled=true;post(agent,num,'send',mode?{message:text,mode:mode}:{message:text},step).then(function(r){el.disabled=false;if(r.ok){el.value='';el.focus()}else errText(r).then(function(t){alertRow('server said '+r.status+' '+t)})}).catch(function(){el.disabled=false})}
      function alertRow(msg){if(feed.current){feed.current.tl.push(JSON.stringify({type:'error',message:msg,t:new Date().toISOString()}));bump(function(k){return k+1})}}
      function uiClick(e){var b=e.target.closest('button.uib');if(!b)return;var d=b.dataset,an={id:d.id};
        if(d.kind==='confirm')an.confirmed=d.val==='yes'; else if(d.kind==='cancel')an.cancelled=true; else if(d.kind==='select')an.value=d.val; else if(d.kind==='input'){var inp=b.parentElement.querySelector('input');an.value=inp?inp.value:''}
        Array.prototype.forEach.call(b.parentElement.querySelectorAll('button'),function(x){x.disabled=true}); post(agent,num,'ui',an,step)}
      var empty=chat?html`<div class="ev sys"><span class="t"></span><span class="b">${drv?'no session yet · press play on the batch view':'no session yet · press play in the Resolution header'}</span></div>`:html`<div class="ev sys"><span class="t"></span><span class="b">no events</span></div>`;
      return html`<aside class=${'sess'+(chat?' chat':'')} role="dialog" aria-label="Session details" ref=${box}><header><span class="ttl">${drv?'Batch '+num+' · driver':'#'+num+' · '+(STEP_LABEL[step]||step)}</span><span class=${st===undefined?'st':'st chip '+(st?st.state:'')}>${st?st.state:st===null?'no run yet':''}</span><button class="sbtn" aria-label="Close" onClick=${close}><${Icon} n="ti-x"/></button></header><div class="hd2" dangerouslySetInnerHTML=${{__html:hd}}></div><details class="prm"><summary>Prompt</summary><div class="pp" dangerouslySetInnerHTML=${{__html:prm[0]||''}}></div></details>
        <div class="tl" ref=${tlRef} onClick=${chat?uiClick:null}>${rows.length?rows.map(function(r,k){return html`<${Ev} key=${k} r=${r} t0=${t0}/>`}):(chat?(ready?empty:null):info.rows?empty:null)}${wait?html`<div class="ev sys wait"><span class="t"></span><i class="ti ti-hourglass" aria-hidden="true"></i><span class="b">${'waiting on the model · '+Math.round((Date.now()-info.last)/1000)} s since the last event</span></div>`:null}</div>
        ${chat&&!drv?html`<${RerunBlock} agent=${agent} num=${num}/>`:null}
        ${chat?html`<form class="comp" onSubmit=${function(e){e.preventDefault();send()}}><textarea rows="3" ref=${ta} placeholder="Message the agent · Enter sends, Shift+Enter for a new line" onKeyDown=${function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send()}}}></textarea><div class="cbtns"><button type="submit" class="rbtn send" title="Send now; while the agent runs it is delivered before its next model call">send</button><button type="button" class="rbtn later" title="Deliver when the agent finishes" onClick=${function(){send('follow_up')}}>after this</button>${drv?null:html`<button type="button" class="rbtn askb" title="Send the resolution instructions: review the answers, guard red, apply, guard green, report" disabled=${sent||note[0]==='sending'||!(st&&st.state==='working')} onClick=${function(){note[1]('sending');post(agent,num,'ask').then(function(r){if(r.ok)note[1]('sent');else{note[1](null);errText(r).then(function(t){alertRow('server said '+r.status+' '+t)})}}).catch(function(){note[1](null)})}}>${sent||note[0]==='sent'?'resolution sent':'resolution'}</button>`}<span class="sp"></span><button type="button" class="rbtn kbtn abort" title="Interrupt the current turn" onClick=${function(){post(agent,num,'abort',null,step)}}>interrupt</button></div></form>`:null}
        <details class="ans" hidden=${!ans}><summary>Answer</summary><pre>${ans||''}</pre></details><details class="errl" hidden=${!tail}><summary>stderr</summary><pre>${tail}</pre></details></aside>`;
    }
    function toggle(agent,num,step,keep,restore){step=step||'analysis';var k=agent+'/'+num+'/'+step; if(dw.box()&&cur===k){if(!keep)close();return} close(); History.close(); Files.close(); cur=k; want=restore||null;
      dw.open(html`<${Panel} agent=${agent} num=${num} step=${step}/>`)}
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&dw.box())close()});
    return {toggle:toggle,close:close,state:state};
  })();
  // History drawer: the card's events as the agents' briefs index them (agents/<agent>/cards/<n>/log.jsonl), newest first, read
  // again every 3 s while open; each pointer opens its file, git: commits show as text.
  var History=(function(){
    var dw=Drawer(), cur=null, want=null;
    var ICON={engineer:'ti-user',session:'ti-message',resolve:'ti-robot',analysis:'ti-file-search',strategy:'ti-flask',context:'ti-pencil',
      sims:'ti-player-play',setup:'ti-settings',pull:'ti-download',batchmerge:'ti-git-merge','batch-driver':'ti-route'};
    function close(){dw.close();cur=null;want=null}
    function state(){var box=dw.box();if(!box)return null;return want||{scroll:box.querySelector('.tl').scrollTop}}
    var TONE=/\b(misguided|wrong-reason|wrong|contested|does-not-reproduce|failed|found|holds|reproduces|solved|clean|merged|done)\b/;
    function tone(t){return String(t||'').split(TONE).map(function(w,k){return k%2?html`<span class=${/^(holds|reproduces|solved|clean|merged|done)$/.test(w)?'tok':'tbad'}>${w}</span>`:w})}
    function refNode(agent,r){
      if(/^git:/.test(r))return html`<code title="Commit in the issue's worktree">${r}</code>`;
      var m=/^(.*?)(?:@L(\d+))?$/.exec(r), path=m[1], line=m[2];
      return html`<a href=${path.charAt(0)==='/'?'file://'+path:'agents/'+agent+'/'+path} target="_blank" rel="noopener" title=${r}>${path.split('/').slice(-2).join('/')+(line?' · line '+line:'')}</a>`;
    }
    function Panel(p){
      var agent=p.agent, num=p.num, s=useState(null), box=useRef(null);
      useEffect(function(){var live=true,timer=null,last=null;
        function tick(){fetch(Paths.log(agent,num),{cache:'no-store'}).then(function(r){return r.ok?r.text():''}).catch(function(){return null}).then(function(t){
          if(!live)return; if(t!==null&&t!==last){last=t;s[1](t.split('\n').filter(Boolean).map(function(l){try{return JSON.parse(l)}catch(e){return null}}).filter(Boolean))}
          timer=setTimeout(tick,3000)})}
        tick(); return function(){live=false;clearTimeout(timer)}},[]);
      useLayoutEffect(function(){if(s[0]&&want){box.current.querySelector('.tl').scrollTop=want.scroll||0;want=null}},[s[0]]);
      var ev=(s[0]||[]).slice().sort(function(a,b){return (a.t||'')<(b.t||'')?-1:1}), lastAns={};
      ev.forEach(function(e,k){if(e.answer)lastAns[e.who]=k});
      var rows=ev.map(function(e,k){return {e:e,old:e.answer&&lastAns[e.who]!==k}}).reverse();
      return html`<aside class="sess hist" role="dialog" aria-label="Card history" ref=${box}><header><span class="ttl">${'#'+num+' · history'}</span><span class="st"></span><button class="sbtn" aria-label="Close" onClick=${close}><${Icon} n="ti-x"/></button></header>
        <div class="hd2">${s[0]===null?'loading…':ev.length?ev.length+' events · newest first · what the agents\' briefs index':'no history yet'}</div>
        <div class="tl">${rows.map(function(x){var e=x.e;return html`<div class=${'ev'+(x.old?' old':'')}><span class="t" title=${e.t}>${String(e.t||'').slice(5,16).replace('T',' ')}</span><i class=${'ti '+(ICON[e.who]||'ti-point')} title=${e.who}></i><div class="b"><b>${e.who}</b> ${tone(e.what)}${x.old?html` <small>superseded</small>`:null}${(e.refs||[]).length?html`<div class="refs">${e.refs.map(function(r){return refNode(agent,r)})}</div>`:null}</div></div>`})}</div></aside>`;
    }
    function toggle(agent,num,restore){var k=agent+'/'+num; if(dw.box()&&cur===k){close();return} closeDrawers(); cur=k; want=restore||null;
      dw.open(html`<${Panel} agent=${agent} num=${num}/>`)}
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&dw.box())close()});
    return {toggle:toggle,close:close,state:state};
  })();
  // Files drawer: every file of the card (GET files/<agent>/<n>), in paths.card_files' groups, folders folded (a folder
  // holding one file shows as that file, a folder every file of the group is in is left out); a file opens below the list as text, JSON indented.
  var Files=(function(){
    var dw=Drawer(), cur=null, CAP=300000;
    var GROUP={source:'Source',card:'Card',setup:'Setup',analysis:'Analysis',strategy:'Sim Strategy',context:'Studio Context Edit',resolve:'Resolution'};
    function close(){dw.close();cur=null}
    function size(b){return b>=1048576?(b/1048576).toFixed(1)+' MB':b>=1024?Math.round(b/1024)+' KB':b+' B'}
    function tree(files){var root={dirs:{},files:[]}, top=files[0].path.split('/')[0], cut=files.every(function(f){return f.path.indexOf(top+'/')===0})?1:0;
      files.forEach(function(f){var parts=f.path.split('/').slice(cut),node=root;
      parts.slice(0,-1).forEach(function(d){node=node.dirs[d]||(node.dirs[d]={dirs:{},files:[]})});node.files.push({name:parts[parts.length-1],f:f})});return root}
    function count(node){return node.files.length+Object.keys(node.dirs).reduce(function(m,k){return m+count(node.dirs[k])},0)}
    function Panel(p){
      var agent=p.agent, num=p.num, s=useState(null), sel=useState(null), pv=useState(null);
      useEffect(function(){getJSON('files/'+agent+'/'+num).then(function(x){s[1](x||[])})},[]);
      useEffect(function(){var f=sel[0], live=true; if(!f){pv[1](null);return}
        pv[1]({text:'loading…'});
        fetch('agents/'+agent+'/'+f.path,{cache:'no-store'}).then(function(r){return r.ok?r.text():null}).catch(function(){return null}).then(function(t){if(!live)return;
          if(t==null){pv[1]({text:'(could not read the file)'});return}
          var cut=t.length>CAP; if(!cut&&/\.json$/.test(f.path)){try{t=JSON.stringify(JSON.parse(t),null,1)}catch(e){}}
          pv[1]({text:cut?t.slice(0,CAP):t,cut:cut})});
        return function(){live=false}},[sel[0]]);
      function row(label,f){var on=sel[0]&&sel[0].path===f.path;
        return html`<button class=${'fr'+(on?' on':'')} title=${f.path} onClick=${function(){sel[1](on?null:f)}}><span class="fn">${label}</span><small>${size(f.size)}</small><small>${String(f.t).slice(5,16).replace('T',' ')}</small></button>`}
      function Node(q){var node=q.node;
        return html`${node.files.map(function(x){return row(x.name,x.f)})}${Object.keys(node.dirs).sort().map(function(d){var c=node.dirs[d];
          if(!Object.keys(c.dirs).length&&c.files.length===1)return row(d+'/'+c.files[0].name,c.files[0].f);
          return html`<details class="fd"><summary><${Icon} n="ti-folder"/>${d}<small>${count(c)}</small></summary><div class="fk"><${Node} node=${c}/></div></details>`})}`}
      var groups=[]; (s[0]||[]).forEach(function(f){var g=groups[groups.length-1]; if(!g||g.name!==f.group)groups.push(g={name:f.group,files:[]}); g.files.push(f)});
      var f=sel[0], v=pv[0];
      return html`<aside class="sess files" role="dialog" aria-label="Card files"><header><span class="ttl">${'#'+num+' · files'}</span><span class="st"></span><button class="sbtn" aria-label="Close" onClick=${close}><${Icon} n="ti-x"/></button></header>
        <div class="hd2">${s[0]===null?'loading…':s[0].length+' files · under agents/'+agent+'/'}</div>
        <div class="fl">${groups.map(function(g){return html`<details class="fg" open><summary>${GROUP[g.name]||g.name}<small>${g.files.length}</small></summary><${Node} node=${tree(g.files)}/></details>`})}</div>
        ${f?html`<div class="pv"><div class="ph"><span class="p" title=${f.path}>${f.path}</span><small>${size(f.size)}${v&&v.cut?' · first '+size(CAP)+' shown':''}</small><a href=${'agents/'+agent+'/'+f.path} target="_blank" rel="noopener" title="Open the raw file in a new tab"><${Icon} n="ti-external-link"/></a><button class="sbtn" aria-label="Close the file" onClick=${function(){sel[1](null)}}><${Icon} n="ti-x"/></button></div><pre>${v?v.text:''}</pre></div>`:null}</aside>`;
    }
    function toggle(agent,num){var k=agent+'/'+num; if(dw.box()&&cur===k){close();return} closeDrawers(); cur=k;
      dw.open(html`<${Panel} agent=${agent} num=${num}/>`)}
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&dw.box())close()});
    return {toggle:toggle,close:close};
  })();
  // The batch after its cards are done: the driver's stage per step, its session, the main workspace, the cards and the
  // latest combined check against the one before it. GET driver/<agent>/<batch>/check, again every 3 s.
  var DSTAGES=['align','check','sort','route','pr'], DHEALTH={working:'now',done:'ok',conflict:'bad',running:'now',clean:'ok',found:'warn',sent:'now',waiting:'now',back:'ok',written:'now',pushed:'ok'};
  function BatchView(p){
    var agent=p.agent, batch=p.batch, d=useState(null), n=useState(0), note=useState(null);
    useEffect(function(){var live=true,t=null;function tick(){getJSON('driver/'+agent+'/'+batch+'/check').then(function(x){if(!live)return;d[1](x);t=setTimeout(tick,3000)})}tick();return function(){live=false;if(t)clearTimeout(t)}},[agent,batch]);
    var st=useStatus(Paths.status(agent,batch,'driver'),n[0])[0], x=d[0];
    if(!x)return html`<div class="bv"><div class="ev sys">loading</div></div>`;
    var last={};(x.stage||[]).forEach(function(e){last[e.stage]=e});
    var cur=(x.stage||[]).slice(-1)[0], working=!!(st&&st.state==='working');
    function start(resume){note[1]('starting');postJSON('driver/'+agent+'/'+batch+'/start',Object.assign(runOpts(),resume?{resume:true}:{})).then(function(r){
      if(!r.ok)return errText(r).then(function(t){note[1](t)});note[1](null);n[1](function(k){return k+1});Session.toggle(agent,batch,'driver',true)}).catch(function(){note[1]('server unreachable')})}
    function stop(){postJSON('driver/'+agent+'/'+batch+'/stop').then(function(){setTimeout(function(){n[1](function(k){return k+1})},1500)})}
    var runs=x.runs||[], now=runs[runs.length-1], prev=runs[runs.length-2], pmap={};
    if(prev)prev.sims.forEach(function(s){pmap[s.name]=s});
    var sims=now?now.sims.slice().sort(function(a,b){return (a.passed/a.total||0)-(b.passed/b.total||0)}):[];
    function cnt(s){return s?html`<span class=${'cnt '+(s.passed===s.total?'ok':s.passed?'flaky':'ko')}>${s.passed+'/'+s.total}</span>`:html`<span class="dim">–</span>`}
    var m=x.main, e=x.entry||{};
    return html`<div class="bv">
      <header class="bvh"><div class="id"><span class="num">${'Batch '+batch}</span><span>${e.base||''}</span></div>
        <div class="bvc"><${ModelSelect} k="runModel" def="gpt-5.6-terra" list=${MODELS} label="Model"/><${ModelSelect} k="runEffort" def="high" list=${EFFORTS} label="Reasoning effort"/>
          ${working?html`<button class="rbtn" title="Stop the driver" onClick=${stop}><${Icon} n="ti-player-stop"/></button>`:html`<button class="rbtn" title="Start the driver with the batch brief" onClick=${function(){start(false)}}><${Icon} n="ti-player-play"/></button>${st&&st.state==='failed'?html`<button class="rbtn" title="Resume the last driver session" onClick=${function(){start(true)}}><${Icon} n="ti-player-track-next"/></button>`:null}`}
          <button class="rbtn" title="Open the driver's session" disabled=${!st} onClick=${function(){Session.toggle(agent,batch,'driver')}}><${Icon} n="ti-message"/></button>
          <span class=${'chip '+(st?st.state:'')}>${st?(working?'live':st.state):'no driver yet'}</span>${note[0]?html`<span class="dim">${note[0]}</span>`:null}</div></header>
      <div class="bvs">${DSTAGES.map(function(k){var l=last[k];return html`<div class=${'bvst '+(l?DHEALTH[l.state]||'':'')+(cur&&cur.stage===k?' cur':'')} title=${l&&l.note||''}><b>${k}</b><span>${l?l.state:'–'}</span>${l&&l.note?html`<em>${l.note}</em>`:null}</div>`})}</div>
      <div class="bvl"><span class="dim">main workspace</span> ${m?(m.state==='done'?(m.name+' · main at '+(m.commit||'?')+' · '+String(m.ended||'').replace('T',' ').replace('Z',' UTC')):m.state+(m.error?' · '+m.error.split('\n')[0]:'')):'none yet'}</div>
      <h3>Cards</h3><table class="bvt"><thead><tr><th>Issue</th><th>State</th><th>Repro</th><th>Reopened</th></tr></thead><tbody>${(x.cards||[]).map(function(c){var s=c.stage||{},r=c.reopened||[];
        return html`<tr><td><a href=${'#a='+agent+'&b='+batch+'&i='+c.n}>${'#'+c.n}</a></td><td>${s.stage?s.stage+' '+s.state:'not started'}</td><td>${c.repro?cnt({passed:c.repro[0],total:c.repro[1]}):'–'}</td><td>${r.length?r.length+'× · last '+String(r[r.length-1].t||'').slice(5,16).replace('T',' '):'–'}</td></tr>`})}</tbody></table>
      <h3>${now?'Check · run '+(now.run||now.file)+' · '+now.t.replace('T',' ').replace('Z',' UTC'):'Check · no run yet'}</h3>
      ${now?html`<table class="bvt"><thead><tr><th>Simulation</th><th>Now</th><th>${prev?'Previous check':''}</th></tr></thead><tbody>${sims.map(function(s){return html`<tr><td>${s.name}</td><td>${cnt(s)}</td><td>${prev?cnt(pmap[s.name]):null}</td></tr>`})}</tbody></table>`:null}
    </div>`;
  }
  function batchView(el,agent,batch){unmount(el);el.innerHTML='';mount(el,html`<${BatchView} agent=${agent} batch=${batch}/>`)}
  function badges(root){root.querySelectorAll('.res, .was, .cnt').forEach(function(el){var m=/(\d+)\s*\/\s*(\d+)/.exec(el.textContent);if(m)el.classList.add(+m[1]===+m[2]?'ok':+m[1]===0?'ko':'flaky')})}
  function md(s){s=esc(s).replace(/\[@([^\]]+)\]\(mention:[^)]*\)/g,'@$1').replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');return s.split(/\n{2,}/).map(function(p){return '<p>'+p.replace(/\n/g,'<br>')+'</p>'}).join('')}
  function report(i){
    return '<div class="ia">'+
      '<header class="top"><div class="id"><span class="num">#'+i.num+'</span><span>'+esc(i.title)+'</span></div><div class="meta">'+[(i.owner||'').split(/\s+/)[0],i.created,i.state!=='OPEN'?i.state.toLowerCase().replace('_',' '):''].filter(Boolean).map(esc).join(' · ')+'</div></header>'+
      '<div class="body report">'+md(i.body)+(i.comments.length?'<div class="cms">'+i.comments.map(function(c){return '<div class="cm"><span class="who">'+esc(c.author)+' · '+esc((c.time||'').slice(0,10))+'</span>'+md(c.text)+'</div>'}).join('')+'</div>':'')+'</div></div>';
  }
  function card(i){
    if(!i.card) return '<div class="card">'+report(i)+'</div>';
    return '<div class="card">'+i.card+'</div><details class="card rep"><summary>Issue as reported</summary>'+report(i)+'</details>';
  }
  // Folds: each card remembers which <details> I opened or closed, keyed by the fold's summary text.
  function foldKey(d){var sm=d.querySelector(':scope>summary'),c=sm?sm.cloneNode(true):null;if(c)c.querySelectorAll('.run,.runbar,.chip,button,select').forEach(function(x){x.remove()});var t=(c?c.textContent:'').replace(/[\d\s]+/g,' ').trim().toLowerCase();return (d.className||'').replace(/\bkf\b/,'').trim()+'|'+t}
  function foldMap(agent,num,set){var k='folds:'+agent+':'+num;try{if(set)localStorage.setItem(k,JSON.stringify(set));return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return {}}}
  function foldIds(view){var seen={},out=[];view.querySelectorAll('details').forEach(function(d){var k=foldKey(d);seen[k]=(seen[k]||0)+1;out.push([d,k+'#'+seen[k]])});return out}
  function applyFolds(view,agent,num){var m=foldMap(agent,num);foldIds(view).forEach(function(x){if(x[1] in m)x[0].open=m[x[1]]})}
  function foldToggle(view,agent,num,target){var m=foldMap(agent,num);foldIds(view).forEach(function(x){if(x[0]===target)m[x[1]]=x[0].open});foldMap(agent,num,m)}
  // Sidebar: width by dragging the gutter, hidden with the button; both remembered.
  function chrome(){
  var app=document.querySelector('.app'), gut=document.getElementById('gut');
  function setSide(w){w=Math.max(200,Math.min(560,Math.round(w)));app.style.setProperty('--side',w+'px');pref('sideW',w)}
  if(pref('sideW'))setSide(+pref('sideW')); if(pref('sideHidden')==='1')app.classList.add('nosb');
  document.getElementById('hide').addEventListener('click',function(){app.classList.add('nosb');pref('sideHidden','1')});
  document.getElementById('show').addEventListener('click',function(){app.classList.remove('nosb');pref('sideHidden','0')});
  gut.addEventListener('pointerdown',function(e){
    var x0=e.clientX,w0=app.querySelector('nav.side').getBoundingClientRect().width;app.classList.add('rs');gut.setPointerCapture(e.pointerId);
    function mv(e){setSide(w0+e.clientX-x0)} function up(){app.classList.remove('rs');gut.removeEventListener('pointermove',mv);gut.removeEventListener('pointerup',up)}
    gut.addEventListener('pointermove',mv);gut.addEventListener('pointerup',up);e.preventDefault();
  });
  }
  // The open drawer of the card on screen, and back: which drawer, its scroll, filter, open parts and unsent draft.
  function drawerState(){var s=Session.state();if(s)return {kind:'session',s:s};var h=History.state();if(h)return {kind:'history',s:h};var t=Transcript.state();if(t)return {kind:'transcript',s:t,ctx:Context.state()};var c=Context.state();return c?{kind:'context',s:c}:null}
  function closeDrawers(){Session.close();Transcript.close();Context.close();History.close();Files.close()}
  function restoreDrawer(i,d){closeDrawers();if(!d||!d.s)return;
    if(d.kind==='session')Session.toggle(i.agent,i.num,d.s.step,false,d.s);
    else if(d.kind==='history')History.toggle(i.agent,i.num,d.s);
    else if(d.kind==='transcript'){Transcript.toggle(i,d.s.conv,d.s);if(d.ctx)Context.toggle(i,d.ctx.conv,d.ctx.entry,true,d.ctx)}
    else if(d.kind==='context')Context.toggle(i,d.s.conv,d.s.entry,false,d.s)}
  window.Cards={StepToggles:StepToggles,ModelSelect:ModelSelect,MODELS:MODELS,EFFORTS:EFFORTS,chosenSteps:chosenSteps,drawerState:drawerState,closeDrawers:closeDrawers,restoreDrawer:restoreDrawer,
    batchView:batchView,store:Store,useStore:useStore,unmount:unmount,cache:cache,esc:esc,report:report,card:card,norm:norm,badges:badges,load:load,applyFolds:applyFolds,foldToggle:foldToggle,chrome:chrome};
})();
