const $ = (s, root=document) => root.querySelector(s);
const esc = v => String(v??'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const arrow='↗', down='↓';
let catalog, currentNote, currentCollection, renderVersion=0;
const noteHref=n=>'#/note/'+n.id;
const courseHref=c=>'#/course/'+c.id;
const collectionOf=n=>catalog.collections.find(c=>c.id===n.collection);
const entries=c=>catalog.notes.filter(n=>n.collection===c.id);
const titleText=n=>n.title.replace(/^(?:Lecture )?\d+:\s*/, '');
const dateText=d=>new Date(d+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});

function navigateMenu(){
  const isHome=location.hash==='#/'||!location.hash;
  $('#navigation').innerHTML=`<a class="nav-item ${isHome?'active':''}" href="#/" ${isHome?'aria-current="page"':''}><span class="nav-icon">▦</span> All notes</a><a class="nav-item ${location.hash==='#/downloads'?'active':''}" href="#/downloads"><span class="nav-icon">↓</span> PDF downloads</a><div class="nav-heading">COURSES</div>${catalog.collections.slice(0,2).map(navCourse).join('')}<div class="nav-heading">REFERENCES</div>${catalog.collections.slice(2).map(navCourse).join('')}`;
}
function navCourse(c){
  const active=currentCollection?.id===c.id;
  return `<a class="nav-item ${active?'active':''}" href="${courseHref(c)}"><span class="nav-icon">${esc(c.symbol)}</span>${esc(c.title)}<span class="nav-count">${c.count}</span></a>${active&&currentNote?`<div class="nav-notes">${entries(c).map(n=>`<a class="nav-note ${currentNote.id===n.id?'active':''}" ${currentNote.id===n.id?'aria-current="page"':''} href="${noteHref(n)}">${n.lecture?String(n.lecture).padStart(2,'0')+'. ':''}${esc(titleText(n))}</a>`).join('')}</div>`:''}`;
}
function breadcrumb(parts){$('#breadcrumbs').innerHTML=`<a href="#/">Library</a>${parts.map((p,i)=>`<span>›</span>${p.href?`<a href="${p.href}">${esc(p.text)}</a>`:`<span class="current">${esc(p.text)}</span>`}`).join('')}`;}
function home(){
  document.title='CS Notes';breadcrumb([{text:'All notes'}]);
  $('#content').innerHTML=`<div class="page"><section><div class="section-heading"><h1>Course notes</h1></div><div class="course-grid">${catalog.collections.slice(0,2).map(courseCard).join('')}</div></section><section class="reference-section"><div class="section-heading"><h2>References</h2></div>${catalog.collections.slice(2).map(c=>`<a class="reference-row" href="${courseHref(c)}"><span class="course-symbol ${c.color}" aria-hidden="true">${c.symbol}</span><div class="reference-info"><h3>${esc(c.title)}</h3></div><div class="reference-meta"><span>${c.count} ${c.count===1?'entry':'entries'}</span><span class="row-arrow" aria-hidden="true">→</span></div></a>`).join('')}</section></div>`;
}
function courseCard(c){return `<a class="course-card" href="${courseHref(c)}"><div class="course-card-top"><span class="course-symbol ${c.color}" aria-hidden="true">${c.symbol}</span><span class="tag">${c.count} entries</span></div><h2>${esc(c.title)}<span class="row-arrow" aria-hidden="true">→</span></h2></a>`;}

function course(c){
  document.title=c.title+' — CS Notes';breadcrumb([{text:c.title}]);
  $('#content').innerHTML=`<div class="page"><div class="section-intro"><div class="eyebrow">${esc(c.subtitle)}</div><h1>${esc(c.title)}</h1></div><div class="section-actions"><a class="button primary" href="${noteHref(entries(c)[0])}">Read first note <span>→</span></a><a class="button" href="${c.pdf}" download>Download collection PDF <span>${down}</span></a></div><div class="section-heading"><h2>All entries</h2><span class="small-label">${c.count} entries · ${c.populated} with content</span></div><div class="notes-list">${entries(c).map((n,i)=>`<a class="note-row" href="${noteHref(n)}"><span class="note-number">${String(n.lecture??i+1).padStart(2,'0')}</span><div class="note-info"><h2>${esc(titleText(n))}</h2><p>${n.state==='empty'?'No written content yet':n.state==='stub'?'Brief starter note':`${n.minutes} min read${n.date?' · '+dateText(n.date):''}`}</p></div>${n.state==='empty'?'<span class="note-status">Empty</span>':n.state==='stub'?'<span class="note-status">Starter</span>':''}<span class="row-arrow">→</span></a>`).join('')}</div></div>`;
}
function flattenHeadings(headings){return headings.flatMap(h=>[h,...flattenHeadings(h.children??[])]);}
function outlineLinks(n){return flattenHeadings(n.headings).filter(h=>document.getElementById(h.id)).map(h=>`<a class="${h.level>2?'sub':''}" href="#/note/${n.id}?section=${encodeURIComponent(h.id)}">${esc(stripMarkup(h.name))}</a>`).join('');}
function stripMarkup(s){const e=document.createElement('div');e.innerHTML=s;return e.textContent;}
async function note(n,section){
  const version=++renderVersion;
  const c=collectionOf(n), group=entries(c), ix=group.indexOf(n), prev=group[ix-1], next=group[ix+1];
  document.title=n.title+' — CS Notes';breadcrumb([{text:c.title,href:courseHref(c)},{text:n.lecture?'Lecture '+n.lecture:titleText(n)}]);
  $('#content').innerHTML=`<div class="reader"><div class="reader-main"><header class="reader-head"><div class="eyebrow">${esc(c.title)}${n.lecture?' / Lecture '+String(n.lecture).padStart(2,'0'):''}</div><h1>${esc(titleText(n))}</h1><div class="note-meta"><span>${esc(c.subtitle)}</span>${n.state!=='empty'?`<span>·</span><span>${n.minutes} min read</span>`:''}${n.date?`<span>·</span><span>${dateText(n.date)}</span>`:''}</div>${n.tags.length?`<div class="note-tags">${n.tags.map(t=>`<span>${esc(t)}</span>`).join('')}</div>`:''}</header><div class="reader-tools"><a class="button primary" href="${c.pdf}" download>Collection PDF <span>${down}</span></a><button class="button" id="print-note">Print note <span>↗</span></button><button class="button" id="copy-link">Copy link <span>⤴</span></button></div><details class="mobile-outline"><summary>On this page</summary><div id="mobile-outline-links"></div></details><article class="article" id="article">${n.state==='empty'?'<div class="empty-note"><strong>This note is waiting to be written.</strong><br>The entry exists in your collection, but its source file has no written content yet.</div>':n.html}</article><div class="source-notice">From your Markdown collection · <a href="source/${encodeURI(n.path)}" download>Download source</a>${n.state==='stub'?' · This is a brief starter note.':''}</div><nav class="prev-next" aria-label="Adjacent notes">${prev?`<a href="${noteHref(prev)}"><small>← Previous</small>${esc(titleText(prev))}</a>`:''}${next?`<a href="${noteHref(next)}"><small>Next →</small>${esc(titleText(next))}</a>`:''}</nav></div><aside class="outline" aria-label="On this page"><div class="outline-title">ON THIS PAGE</div><div id="outline-links"></div></aside></div>`;
  document.querySelectorAll('.article table').forEach(table=>{const wrap=document.createElement('div');wrap.className='table-wrap';table.replaceWith(wrap);wrap.append(table);});
  const links=outlineLinks(n);$('#outline-links').innerHTML=links;$('#mobile-outline-links').innerHTML=links;if(!links){$('.outline').hidden=true;$('.mobile-outline').hidden=true;}
  $('#print-note').addEventListener('click',async()=>{if(window.MathJax?.startup?.promise)await MathJax.startup.promise;window.print();});
  $('#copy-link').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);toast('Link copied');}catch{toast('Copy this page’s URL from your address bar.');}});
  try{if(window.MathJax?.startup?.promise){await MathJax.startup.promise;if(version!==renderVersion)return;MathJax.typesetClear();await MathJax.typesetPromise([$('#article')]);}}catch(error){console.warn('Math rendering issue',error);}
  if(section&&version===renderVersion){document.getElementById(section)?.scrollIntoView({block:'start'});}
}
function downloads(){
  document.title='PDF downloads — CS Notes';breadcrumb([{text:'PDF downloads'}]);
  const rows=[{id:'all-notes',title:'The complete notebook',description:`All ${catalog.notes.length} entries across ${catalog.collections.length} collections`,pdf:'pdfs/all-notes.pdf'},...catalog.collections.map(c=>({...c,description:c.count+' entries · '+c.subtitle}))];
  $('#content').innerHTML=`<div class="page"><div class="section-intro"><div class="eyebrow">Take your notes with you</div><h1>Ready for offline reading.</h1><p>Keep a copy on your tablet, annotate a lecture, or study away from your screen. Download a collection or the complete notebook.</p></div><div class="download-list">${rows.map(c=>`<div class="download-row"><div class="download-icon">PDF</div><div class="download-info"><h2>${esc(c.title)}</h2><p>${esc(c.description)}</p></div><a class="button ${c.id==='all-notes'?'primary':''}" href="${c.pdf}" download>Download <span>${down}</span></a></div>`).join('')}</div><div class="info-box">PDFs preserve the notes, equations, and tables from your collection. Empty entries are labeled in each export. To save just one note, open it and choose <strong>Print note → Save as PDF</strong>.</div></div>`;
}
function render(){
  if(!catalog)return;
  ++renderVersion;
  const [path,query='']=(location.hash.slice(1)||'/').split('?');const parts=path.split('/').filter(Boolean);
  currentNote=null;currentCollection=null;
  if(parts[0]==='note') {currentNote=catalog.notes.find(n=>n.id===parts[1]);if(currentNote)currentCollection=collectionOf(currentNote);}
  if(parts[0]==='course')currentCollection=catalog.collections.find(c=>c.id===parts[1]);
  navigateMenu();closeMenu();
  if(currentNote)note(currentNote,new URLSearchParams(query).get('section'));
  else if(currentCollection)course(currentCollection);
  else if(parts[0]==='downloads')downloads();
  else if(parts.length){document.title='Note not found — CS Notes';breadcrumb([{text:'Not found'}]);$('#content').innerHTML='<div class="page"><div class="section-intro"><h1>That page isn’t in this notebook.</h1><p>The link may have changed. Browse the library or search for a topic.</p><a class="button primary" href="#/">Back to all notes →</a></div></div>';}
  else home();
  if(!query)window.scrollTo(0,0);
}
function toast(message){$('#toast').textContent=message;$('#toast').classList.add('visible');setTimeout(()=>$('#toast').classList.remove('visible'),2600);}
function openSearch(){if(!catalog)return;$('#search-dialog').showModal();$('#search-input').value='';search('');$('#search-input').focus();}
function search(term){
  const q=term.trim().toLowerCase();
  if(!q){$('#search-results').innerHTML='<div class="search-empty">What are you working through?<br>Try “lambda”, “NP”, or “dynamic programming”.</div>';return;}
  const terms=q.split(/\s+/);
  const matches=catalog.notes.map(n=>({n,hay:(n.title+' '+n.collection+' '+n.tags.join(' ')+' '+n.text).toLowerCase()})).filter(({hay})=>terms.every(t=>hay.includes(t))).sort((a,b)=>(b.n.title.toLowerCase().includes(q)?1:0)-(a.n.title.toLowerCase().includes(q)?1:0));
  $('#search-results').innerHTML=matches.length?matches.slice(0,30).map(({n})=>{const excerpt=n.excerpt||n.text;let at=excerpt.toLowerCase().indexOf(q);let snippet=excerpt.slice(Math.max(0,at-55),Math.max(0,at-55)+170);return `<a class="search-result" href="${noteHref(n)}"><small>${esc(collectionOf(n).title)}${n.lecture?' / Lecture '+n.lecture:''}</small><h3>${highlight(n.title,q)}</h3><p>${highlight(snippet,q)}${snippet.length===170?'…':''}</p></a>`;}).join(''):`<div class="search-empty">No notes found for “${esc(term)}”.<br>Try a broader term or a course code.</div>`;
  document.querySelectorAll('.search-result').forEach(a=>a.addEventListener('click',()=>$('#search-dialog').close()));
}
function highlight(text,term){const at=text.toLowerCase().indexOf(term);return at<0?esc(text):esc(text.slice(0,at))+'<mark>'+esc(text.slice(at,at+term.length))+'</mark>'+esc(text.slice(at+term.length));}
function closeMenu(){$('#sidebar').classList.remove('open');$('#scrim').classList.remove('visible');$('#menu').setAttribute('aria-expanded','false');}
document.querySelectorAll('[data-search]').forEach(b=>b.addEventListener('click',openSearch));
$('.skip').addEventListener('click',e=>{e.preventDefault();$('#content').focus();$('#content').scrollIntoView({block:'start'});});
$('#close-search').addEventListener('click',()=>$('#search-dialog').close());
$('#search-input').addEventListener('input',e=>search(e.target.value));
$('#search-input').addEventListener('keydown',e=>{if(e.key==='Enter'){const first=$('.search-result');if(first){first.click();}}if(e.key==='ArrowDown'){e.preventDefault();$('.search-result')?.focus();}});
$('#search-dialog').addEventListener('click',e=>{if(e.target===$('#search-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openSearch();}if(e.key==='Escape')closeMenu();});
$('#menu').addEventListener('click',()=>{const open=$('#sidebar').classList.toggle('open');$('#scrim').classList.toggle('visible',open);$('#menu').setAttribute('aria-expanded',String(open));});
$('#scrim').addEventListener('click',closeMenu);
window.addEventListener('hashchange',render);
fetch('assets/catalog.json').then(r=>{if(!r.ok)throw new Error('Unable to load notes');return r.json();}).then(data=>{catalog=data;render();}).catch(()=>{$('#content').innerHTML='<div class="page"><h1>The notebook could not be opened.</h1><p>Please reload the page to try again.</p></div>';});
