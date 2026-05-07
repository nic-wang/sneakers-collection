/* Sneakers Collection · app.js
   Single-source rendering: loads data/sneakers.json once,
   dispatches to appropriate renderer based on page.
   Image resolution priority:
     1) item.img  (local real photo path, e.g. assets/img/aj1-bred.jpg)
     2) item.palette → parametric SVG placeholder
     3) fallback solid colored block
*/

const DATA_URL = 'data/sneakers.json';

async function loadData() {
  const res = await fetch(DATA_URL, { cache: 'no-cache' });
  if (!res.ok) throw new Error('Failed to load sneakers.json');
  return res.json();
}

/* ---------- Utilities ---------- */
function qs(key) {
  return new URLSearchParams(location.search).get(key);
}
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') node.className = v;
    else if (k === 'html') node.innerHTML = v;
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else if (v !== undefined && v !== null) node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c === null || c === undefined || c === false) continue;
    if (c instanceof Node) {
      node.appendChild(c);
    } else {
      node.appendChild(document.createTextNode(String(c)));
    }
  }
  return node;
}
function formatPrice(usd) {
  if (usd === null || usd === undefined) return '—';
  return `$${usd}`;
}
function priceRange(range) {
  if (!range || (!range.low && !range.high)) return '—';
  return `$${range.low} – $${range.high}`;
}

/* ---------- Image resolver ---------- */
function resolveImage(item, { modelLabel, colorwayName } = {}) {
  // 1. Real local photo
  if (item.img) return { src: item.img, isSVG: false };
  // 2. Legacy external URL (kept for backward compat)
  if (item.image && !item.image.startsWith('https://placeholder')) return { src: item.image, isSVG: false };
  if (item.hero_image && !item.hero_image.startsWith('https://placeholder')) return { src: item.hero_image, isSVG: false };
  // 3. Parametric SVG
  const palette = item.palette || item.hero_palette || item.cover_palette;
  if (palette && typeof sneakerDataURI === 'function') {
    return {
      src: sneakerDataURI({
        upper: palette.upper,
        sole: palette.sole,
        accent: palette.accent,
        laces: palette.laces,
        modelLabel: palette.modelLabel || modelLabel || '',
        colorwayName: palette.colorwayName || colorwayName || item.name || '',
      }),
      isSVG: true,
    };
  }
  // 4. Fallback solid block
  return { src: sneakerDataURI({ modelLabel: modelLabel || '', colorwayName: colorwayName || item.name || '' }), isSVG: true };
}

/* Find the canonical "hero" colorway for a model.
   Priority: hero_img (legacy) > hero_colorway match > first colorway > palette SVG. */
function getHeroImage(model) {
  if (model.hero_img) return resolveImage({ img: model.hero_img }, { modelLabel: model.name });
  if (model.hero_colorway && Array.isArray(model.colorways)) {
    const cw = model.colorways.find(c => c.name === model.hero_colorway);
    if (cw) return resolveImage(cw, { modelLabel: model.name, colorwayName: cw.name });
  }
  if (Array.isArray(model.colorways) && model.colorways.length) {
    return resolveImage(model.colorways[0], { modelLabel: model.name, colorwayName: model.colorways[0].name });
  }
  return resolveImage(
    { palette: model.hero_palette },
    { modelLabel: model.name, colorwayName: 'OG' }
  );
}

/* ---------- Homepage ---------- */
function renderHome(data) {
  const container = document.getElementById('series-grid');
  if (!container) return;

  const ajCount = data.jordan.models.filter(m => m.id !== 'placeholder').length;
  const kobeCount = data.kobe.models.filter(m => m.id !== 'placeholder').length;
  const totalCW = [...data.jordan.models, ...data.kobe.models]
    .reduce((sum, m) => sum + (m.colorways?.length || 0), 0);

  document.getElementById('stat-models').textContent = (ajCount + kobeCount) || '—';
  document.getElementById('stat-colorways').textContent = totalCW || '—';
  document.getElementById('stat-years').textContent = '1985 – 2016';

  const cards = [
    {
      href: 'jordan.html',
      eyebrow: `Air Jordan · ${ajCount || '—'} Models`,
      title: 'Michael Jordan',
      meta: '1985 – 1998  ·  Peter Moore / Tinker Hatfield',
      img: data.jordan.cover_img,
      palette: data.jordan.cover_palette,
    },
    {
      href: 'kobe.html',
      eyebrow: `Nike Kobe · ${kobeCount || '施工中'} Models`,
      title: 'Kobe Bryant',
      meta: '2005 – 2016  ·  Ken Link / Eric Avar',
      img: data.kobe.cover_img,
      palette: data.kobe.cover_palette,
    },
  ];

  container.innerHTML = '';
  for (const c of cards) {
    const { src } = resolveImage({ img: c.img, palette: c.palette });
    const link = el('a', { href: c.href, class: 'series-card' });
    link.appendChild(el('img', { class: 'cover', src, alt: c.title, loading: 'lazy' }));
    link.appendChild(el('div', { class: 'overlay' },
      el('div', { class: 'eyebrow' }, c.eyebrow),
      el('h2', {}, c.title),
      el('div', { class: 'meta' }, c.meta)
    ));
    container.appendChild(link);
  }
}

/* ---------- List Page ---------- */
function renderList(data, series) {
  const grid = document.getElementById('model-grid');
  if (!grid) return;
  const seriesData = data[series];
  grid.innerHTML = '';

  const models = seriesData.models.filter(m => m.id !== 'placeholder');
  if (!models.length) {
    grid.innerHTML = '<div class="empty">此系列数据正在整理中，敬请期待。</div>';
    return;
  }

  for (const m of models) {
    const { src } = getHeroImage(m);
    const card = el('a', {
      class: 'model-card',
      href: `detail.html?series=${series}&id=${m.id}`,
    });
    card.appendChild(el('div', { class: 'img-wrap' },
      el('img', { src, alt: m.name, loading: 'lazy' })
    ));
    card.appendChild(el('div', { class: 'info' },
      el('span', { class: 'tag' }, `${m.id.toUpperCase()} · ${m.year}`),
      el('h3', {}, m.name),
      el('div', { class: 'year' }, m.designer || '—'),
      el('div', { class: 'count' }, `${m.colorways?.length || 0} Colorways · Retail ${formatPrice(m.original_price)}`)
    ));
    grid.appendChild(card);
  }
}

/* ---------- Detail Page ---------- */
function renderDetail(data) {
  const series = qs('series');
  const id = qs('id');
  const main = document.getElementById('detail-root');
  if (!main) return;

  const seriesData = data[series];
  const model = seriesData?.models.find(m => m.id === id);
  if (!model) {
    main.innerHTML = '<div class="empty">未找到该款式。<br/><br/><a class="back-link" href="index.html">← 返回首页</a></div>';
    return;
  }

  document.title = `${model.name} · Sneakers Collection`;
  main.innerHTML = '';

  // back link
  main.appendChild(el('a', {
    class: 'back-link',
    href: series === 'jordan' ? 'jordan.html' : 'kobe.html',
  }, `← ${series === 'jordan' ? 'Air Jordan' : 'Nike Kobe'} 系列`));

  // hero
  const { src: heroSrc } = getHeroImage(model);
  const hero = el('div', { class: 'detail-hero' });
  hero.appendChild(el('div', { class: 'img-wrap' },
    el('img', { src: heroSrc, alt: model.name })
  ));
  const info = el('div', {});
  info.appendChild(el('div', { class: 'eyebrow' }, `${model.id.toUpperCase()} · ${model.year}`));
  info.appendChild(el('h1', {}, model.name));
  if (model.subtitle) info.appendChild(el('div', { class: 'summary' }, model.subtitle));

  // facts card matrix — icons + tiered cards
  const facts = el('div', { class: 'fact-grid' });
  const factCards = [
    { label: '设计师',     value: model.designer,                      icon: '🎨' },
    { label: '首发年份',   value: model.year,                          icon: '📅' },
    { label: '货号',       value: model.style_code,                    icon: '🏷' },
    { label: '首发价',     value: formatPrice(model.original_price),   icon: '💰', cls: 'accent wide' },
    { label: '当前市价区间', value: priceRange(model.market_price),     icon: '📈', cls: 'market wide' },
  ];
  for (const f of factCards) {
    if (!f.value) continue;
    facts.appendChild(el('div', { class: `fact ${f.cls || ''}` },
      el('span', { class: 'icon' }, f.icon),
      el('div', { class: 'label' }, f.label),
      el('div', { class: 'value' }, f.value)
    ));
  }
  info.appendChild(facts);
  hero.appendChild(info);
  main.appendChild(hero);

  // key moment (highlighted quote)
  if (model.icon_moment) {
    main.appendChild(el('section', { class: 'key-moment' },
      el('div', { class: 'key-moment-card' },
        el('div', { class: 'badge' }, '⭐ 标志时刻'),
        el('div', { class: 'quote' }, model.icon_moment)
      )
    ));
  }

  // highlights chips
  if (Array.isArray(model.highlights) && model.highlights.length) {
    const section = el('section', { class: 'highlights-section' });
    section.appendChild(el('h3', {}, '关键词'));
    const chips = el('div', { class: 'highlights-chips' });
    model.highlights.forEach((h, i) => {
      chips.appendChild(el('span', { class: `hl-chip${i === 0 ? ' primary' : ''}` }, h));
    });
    section.appendChild(chips);
    main.appendChild(section);
  }

  // story
  if (model.story) {
    const story = el('section', { class: 'story-block' }, el('h2', {}, '款式故事'));
    const paras = Array.isArray(model.story) ? model.story : [model.story];
    for (const p of paras) story.appendChild(el('p', {}, p));
    main.appendChild(story);
  }

  // colorways with type filter
  if (model.colorways?.length) {
    const sec = el('section', { class: 'colorway-section' },
      el('h2', {}, `配色与复刻（${model.colorways.length}）`));

    // type filter chips
    const types = ['全部', ...Array.from(new Set(model.colorways.map(c => c.type || 'Retro')))];
    const filterBar = el('div', { class: 'cw-filter' });
    types.forEach((t, i) => {
      filterBar.appendChild(el('button', {
        class: `chip${i === 0 ? ' active' : ''}`,
        'data-type': t,
        onclick: (e) => {
          sec.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
          e.currentTarget.classList.add('active');
          const val = e.currentTarget.dataset.type;
          sec.querySelectorAll('.cw-card').forEach(card => {
            card.style.display = (val === '全部' || card.dataset.type === val) ? '' : 'none';
          });
        },
      }, t));
    });
    sec.appendChild(filterBar);

    const grid = el('div', { class: 'colorway-grid' });
    for (const cw of model.colorways) {
      const { src: cwSrc } = resolveImage(cw, { modelLabel: model.name, colorwayName: cw.name });
      const card = el('div', { class: 'cw-card', 'data-type': cw.type || 'Retro' });
      card.appendChild(el('div', { class: 'img' },
        el('img', { src: cwSrc, alt: cw.name, loading: 'lazy' })
      ));
      const meta = el('div', { class: 'meta' });
      meta.appendChild(el('div', { class: 'type' }, cw.type || 'Retro'));
      meta.appendChild(el('h4', {}, cw.name));
      meta.appendChild(el('div', { class: 'row' },
        el('span', {}, cw.release_date || cw.year || '—'),
        el('span', {}, formatPrice(cw.retail))
      ));
      if (cw.market_price) {
        meta.appendChild(el('div', { class: 'row' },
          el('span', {}, '市价'),
          el('span', {}, priceRange(cw.market_price))
        ));
      }
      if (cw.story) meta.appendChild(el('div', { class: 'story' }, cw.story));
      if (cw.sources?.length) {
        const srcRow = el('div', { class: 'sources' });
        cw.sources.forEach((s, i) => {
          srcRow.appendChild(el('a', { href: s.url, target: '_blank', rel: 'noopener' }, s.label || `来源 ${i + 1}`));
        });
        meta.appendChild(srcRow);
      }
      card.appendChild(meta);
      grid.appendChild(card);
    }
    sec.appendChild(grid);
    main.appendChild(sec);
  }
}

/* ---------- Dispatcher ---------- */
async function main() {
  try {
    const data = await loadData();
    const page = document.body.dataset.page;
    if (page === 'home') renderHome(data);
    else if (page === 'list-jordan') renderList(data, 'jordan');
    else if (page === 'list-kobe') renderList(data, 'kobe');
    else if (page === 'detail') renderDetail(data);
  } catch (err) {
    console.error(err);
    const root = document.getElementById('series-grid') || document.getElementById('model-grid') || document.getElementById('detail-root');
    if (root) root.innerHTML = `<div class="empty">数据加载失败：${err.message}</div>`;
  }
}

document.addEventListener('DOMContentLoaded', main);
