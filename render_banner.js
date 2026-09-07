/**
 * Rend les SVG de docs/ en PNG, avec les polices du projet.
 *
 * GitHub affiche bien un SVG dans un README, mais sans charger de police
 * distante : le texte tomberait sur une substitution système. On livre donc un
 * PNG pour l'affichage et on garde le SVG comme source modifiable.
 *
 *   npm install --no-save puppeteer @fontsource/archivo @fontsource/ibm-plex-mono
 *   node tools/render_banner.js
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.join(__dirname, '..');
const DOCS = path.join(ROOT, 'docs');

// Fichiers à produire : source SVG, largeur affichée, facteur de rendu.
const CIBLES = [
  { svg: 'banner.svg', w: 1600, h: 470, echelle: 2 },
  { svg: 'social-preview.svg', w: 1280, h: 640, echelle: 2 },
];

function police(fichier, famille, graisse) {
  const p = path.join(ROOT, 'node_modules', fichier);
  if (!fs.existsSync(p)) throw new Error('police introuvable : ' + fichier);
  return `@font-face{font-family:'${famille}';font-weight:${graisse};font-display:block;
           src:url('data:font/woff2;base64,${fs.readFileSync(p).toString('base64')}') format('woff2')}`;
}

const POLICES = [
  police('@fontsource/archivo/files/archivo-latin-400-normal.woff2', 'Archivo', 400),
  police('@fontsource/archivo/files/archivo-latin-600-normal.woff2', 'Archivo', 600),
  police('@fontsource/archivo/files/archivo-latin-800-normal.woff2', 'Archivo', 800),
  police('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2', 'IBM Plex Mono', 400),
  police('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2', 'IBM Plex Mono', 500),
  police('@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2', 'IBM Plex Mono', 600),
].join('\n');

(async () => {
  const navigateur = await puppeteer.launch({
    executablePath: process.env.CHROME_PATH || undefined,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  for (const c of CIBLES) {
    const source = path.join(DOCS, c.svg);
    if (!fs.existsSync(source)) { console.log('ignoré (absent) :', c.svg); continue; }

    const page = await navigateur.newPage();
    await page.setViewport({ width: c.w, height: c.h, deviceScaleFactor: c.echelle });
    await page.setContent(
      `<style>${POLICES}
        html,body{margin:0;padding:0;background:transparent}
        svg{display:block;width:${c.w}px;height:${c.h}px}
       </style>${fs.readFileSync(source, 'utf8')}`,
      { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 250));

    const sortie = path.join(DOCS, c.svg.replace(/\.svg$/, '.png'));
    await page.screenshot({ path: sortie, omitBackground: false });
    await page.close();
    console.log('%s → %s (%d Ko)', c.svg, path.basename(sortie),
      Math.round(fs.statSync(sortie).size / 1024));
  }

  await navigateur.close();
})().catch(e => { console.error(e.message); process.exit(1); });
