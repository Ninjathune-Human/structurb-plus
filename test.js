const fs = require('fs');
const { JSDOM } = require('jsdom');

const path = require('path');
const APP = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(APP, 'utf8');
const errors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(w) {
    w.HTMLDialogElement && (w.HTMLDialogElement.prototype.showModal = function(){ this.setAttribute('open',''); });
    w.HTMLDialogElement && (w.HTMLDialogElement.prototype.close = function(){ this.removeAttribute('open'); });
    w.onerror = (m, s, l, c, e) => errors.push(String(e && e.stack || m));
  }
});
const w = dom.window, doc = w.document;
w.addEventListener('error', e => errors.push(String(e.error && e.error.stack || e.message)));

setTimeout(() => {
  const S = w.state, calcule = w.calcule || null;

  console.log('--- erreurs au chargement:', errors.length);
  errors.forEach(e => console.log('  ', e.split('\n').slice(0,3).join(' | ')));

  console.log('--- rail rendu:', doc.querySelectorAll('#rail details.step').length, 'étapes');
  console.log('--- coupes svg:', doc.querySelectorAll('svg.coupe').length);
  console.log('--- barres:', doc.querySelectorAll('.barrow').length);
  console.log('--- verdict:', (doc.querySelector('.verdict')||{textContent:''}).textContent.replace(/\s+/g,' ').trim().slice(0,220));
  console.log('--- head:', (doc.querySelector('.sheethead')||{textContent:''}).textContent.replace(/\s+/g,' ').trim());

  // tableaux détail
  doc.querySelectorAll('table.det').forEach((t,i)=>{
    if(i<2) console.log('--- det'+i+':', t.textContent.replace(/\s+/g,' ').trim().slice(0,300));
  });

  // interactions : cliquer sur chaque famille de A puis chaque structure
  const clicks = [];
  function click(sel){ const n = doc.querySelector(sel); if(n){ n.dispatchEvent(new w.MouseEvent('click',{bubbles:true})); return true;} return false; }

  // parcours exhaustif : chaque voie × chaque famille × chaque structure
  let tested = 0, fails = 0;
  const before = errors.length;
  const voies = [1,2,3,4,5,6,7];
  for (const v of voies) {
    const sel = doc.getElementById('fVoie');
    sel.value = String(v);
    sel.dispatchEvent(new w.Event('change', {bubbles:true}));
    for (const famBtn of Array.from(doc.querySelectorAll('#fFam button'))) {
      if (famBtn.disabled) continue;
      famBtn.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
      const opts = Array.from(doc.querySelectorAll('#fStruct button'));
      for (const o of opts) {
        o.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
        // toutes les PF
        for (const pfb of Array.from(doc.querySelectorAll('#fPf button'))) {
          pfb.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
          tested++;
          if (errors.length > before + fails) { fails = errors.length - before; }
        }
        // Q2
        const q2 = doc.querySelectorAll('#fQual button')[1];
        q2 && q2.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
        const q1 = doc.querySelectorAll('#fQual button')[0];
        q1 && q1.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
      }
    }
  }
  console.log('--- combinaisons testées:', tested, 'erreurs cumulées:', errors.length);

  // activer le gel
  const g = doc.querySelectorAll('#fGel button')[1];
  g && g.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  console.log('--- gel actif, erreurs:', errors.length);
  const gelTxt = Array.from(doc.querySelectorAll('.readout .r')).map(r=>r.textContent.replace(/\s+/g,' ').trim()).filter(t=>/gel/i.test(t));
  console.log('   ', gelTxt.join(' || '));

  // base carbone
  doc.getElementById('btnBase').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  console.log('--- base carbone lignes:', doc.querySelectorAll('#baseBody table.det tbody tr').length);

  // copier A -> B
  doc.getElementById('btnCopy').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  console.log('--- après copie, erreurs:', errors.length);

  console.log('=== TOTAL ERREURS:', errors.length);
  errors.slice(0,8).forEach(e=>console.log('!!', e.split('\n').slice(0,4).join(' | ')));
}, 400);
