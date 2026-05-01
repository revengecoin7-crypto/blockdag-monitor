const STATUS_LABEL = {
  broken: 'Broken',
  kept: 'Kept ✓',
  pending: 'Not yet',
  misleading: 'Misleading'
};

const STATUS_ICON = {
  broken: '✕',
  kept: '✓',
  pending: '…',
  misleading: '!'
};

const CAT_ICON = {
  'Exchange Listing':    '📈',
  'Mining Hardware':     '⛏️',
  'Price':              '💰',
  'X1 App':             '📱',
  'Sponsorships':        '🤝',
  'Marketing':           '📢',
  'Staking':             '🔒',
  'Claiming':            '✋',
  'Funding':             '💵',
  'Product':             '🚀',
  'Transparency':        '👁️',
  'Presale':             '🪙',
  'Faucet / Tap Mining': '🚰',
  'Market Cap':          '📊',
  'Infrastructure':      '🏗️',
  'Operations':          '⚙️',
  'Tokenomics':          '📋',
  'Regulatory':          '⚖️',
};

function renderCategories() {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;

  const cats = {};
  PROMISES.forEach(p => {
    if (!cats[p.category]) cats[p.category] = { broken: 0, kept: 0, pending: 0, misleading: 0, total: 0 };
    cats[p.category][p.status]++;
    cats[p.category].total++;
  });

  const sorted = Object.entries(cats).sort((a, b) => b[1].total - a[1].total);
  const isHomepage = grid.classList.contains('home-cat-list');

  if (isHomepage) {
    /* Compact list for homepage sidebar */
    grid.innerHTML = sorted.map(([cat, c]) => {
      const broken = c.broken + c.misleading;
      const icon = CAT_ICON[cat] || '📌';
      const url = `tracker.html?category=${encodeURIComponent(cat)}`;
      const brokenPct = Math.round(broken    / c.total * 100);
      const keptPct   = Math.round(c.kept    / c.total * 100);
      const pendPct   = Math.round(c.pending  / c.total * 100);
      return `
        <a href="${url}" class="home-cat-row">
          <span class="home-cat-row-icon">${icon}</span>
          <span class="home-cat-row-name">${cat}</span>
          <div class="home-cat-row-bar">
            <div class="cat-bar-fill cat-bar-fill--red"    style="width:${brokenPct}%"></div>
            <div class="cat-bar-fill cat-bar-fill--green"  style="width:${keptPct}%"></div>
            <div class="cat-bar-fill cat-bar-fill--yellow" style="width:${pendPct}%"></div>
          </div>
          <span class="home-cat-row-count">${c.total}</span>
        </a>
      `;
    }).join('');
  } else {
    /* Full cards for categories.html */
    grid.innerHTML = sorted.map(([cat, c]) => {
      const broken = c.broken + c.misleading;
      const brokenPct = Math.round(broken    / c.total * 100);
      const keptPct   = Math.round(c.kept    / c.total * 100);
      const pendPct   = Math.round(c.pending  / c.total * 100);
      const url = `tracker.html?category=${encodeURIComponent(cat)}`;
      const accent = broken > c.kept
        ? 'rgba(255,59,59,0.7)'
        : c.kept > 0
          ? 'rgba(0,229,160,0.7)'
          : 'rgba(240,192,48,0.5)';
      const statusLine = [
        broken    ? `<span class="cat-pill cat-pill--red">${broken} broken</span>` : '',
        c.kept    ? `<span class="cat-pill cat-pill--green">${c.kept} kept</span>` : '',
        c.pending ? `<span class="cat-pill cat-pill--yellow">${c.pending} pending</span>` : '',
      ].filter(Boolean).join('');
      return `
        <a href="${url}" class="cat-card" style="--cat-accent:${accent}">
          <div class="cat-card-top">
            <div class="cat-name">${cat}</div>
            <div class="cat-count">${c.total}</div>
          </div>
          <div class="cat-pills">${statusLine}</div>
          <div class="cat-bar">
            <div class="cat-bar-fill cat-bar-fill--red"    style="width:${brokenPct}%"></div>
            <div class="cat-bar-fill cat-bar-fill--green"  style="width:${keptPct}%"></div>
            <div class="cat-bar-fill cat-bar-fill--yellow" style="width:${pendPct}%"></div>
          </div>
          <div class="cat-arrow">View all ${c.total} promises →</div>
        </a>
      `;
    }).join('');
  }
}

function renderPromises(filter, category) {
  const table = document.getElementById('promise-table');
  if (!table) return;
  let items = PROMISES.slice().sort((a, b) => {
    if (a.isNew && !b.isNew) return -1;
    if (!a.isNew && b.isNew) return 1;
    return b.id - a.id;
  });
  if (category) items = items.filter(p => p.category === category);
  if (filter && filter !== 'all') items = items.filter(p => p.status === filter);

  table.innerHTML = items.map((p, i) => `
    <div class="promise-row promise-row--${p.status}" onclick="toggleDetail(this)">
      <div class="pr-num ${p.status}">${i + 1}</div>
      <div class="pr-title">${p.title}${p.isNew ? '<span class="badge-new">New</span>' : ''}</div>
      <div class="pr-cat">${p.category}</div>
      <div class="pr-date">${p.promised}</div>
      <div><span class="pr-status ${p.status}">${STATUS_ICON[p.status]} ${STATUS_LABEL[p.status]}</span></div>
    </div>
    <div class="promise-detail">
      <div class="promise-detail-text">${p.reality}</div>
      <a href="https://twitter.com/intent/tweet?text=${encodeURIComponent('BlockDAG promised: "' + p.title + '"\nStatus: ' + STATUS_LABEL[p.status] + '\n\nSee all 51 promises: blockdagexposed.com\n#BlockDAG #BDAG #DYOR')}" target="_blank" rel="noopener noreferrer" class="share-btn">Share on X →</a>
      ${p.quotes.length ? `
        <div class="promise-detail-toggle" onclick="event.stopPropagation(); toggleQuotesInDetail(this)">
          ▶ Show ${p.quotes.length} source quote${p.quotes.length > 1 ? 's' : ''}
        </div>
        <div class="promise-detail-quotes hidden">
          ${p.quotes.map(q => `
            <div class="quote-item">
              <div class="quote-date-row">
                <span class="quote-date">📅 ${q.date} — Official BlockDAG Network</span>
                ${q.src ? `<a href="${q.src}" target="_blank" rel="noopener noreferrer" class="quote-src-link">🔗 View source</a>` : ''}
              </div>
              <div class="quote-text">"${q.text}"</div>
            </div>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `).join('');
}

function toggleDetail(row) {
  const detail = row.nextElementSibling;
  const isOpen = detail.classList.contains('open');
  detail.classList.toggle('open', !isOpen);
  row.classList.toggle('expanded', !isOpen);
}

function toggleQuotesInDetail(toggle) {
  const quotes = toggle.nextElementSibling;
  const isHidden = quotes.classList.contains('hidden');
  quotes.classList.toggle('hidden', !isHidden);
  const count = toggle.textContent.match(/\d+/)[0];
  toggle.textContent = isHidden
    ? `▼ Hide ${count} source quote${count > 1 ? 's' : ''}`
    : `▶ Show ${count} source quote${count > 1 ? 's' : ''}`;
}

function renderTimeline() {
  const list = document.getElementById('timeline-list');
  if (!list) return;

  var TL_INFO = {
    broken:     { icon: '🔴', label: 'Promise broken',      color: 'var(--red)',    bg: 'rgba(255,59,59,0.08)',   border: 'rgba(255,59,59,0.2)' },
    kept:       { icon: '🟢', label: 'Promise kept',        color: 'var(--green)',  bg: 'rgba(0,229,160,0.07)',   border: 'rgba(0,229,160,0.2)' },
    promise:    { icon: '🔵', label: 'They promised',       color: 'var(--cyan)',   bg: 'rgba(0,212,255,0.07)',   border: 'rgba(0,212,255,0.2)' },
    misleading: { icon: '🟠', label: 'Misleading',          color: 'var(--orange)', bg: 'rgba(255,122,32,0.07)',  border: 'rgba(255,122,32,0.2)' },
    partial:    { icon: '🟡', label: 'Partially delivered', color: 'var(--yellow)', bg: 'rgba(240,192,48,0.07)',  border: 'rgba(240,192,48,0.2)' },
    warning:    { icon: '⚠️', label: 'Warning',             color: 'rgba(255,255,255,0.5)', bg: 'rgba(255,255,255,0.03)', border: 'rgba(255,255,255,0.1)' },
    note:       { icon: '📌', label: 'Note',                color: 'rgba(255,255,255,0.4)', bg: 'rgba(255,255,255,0.02)', border: 'rgba(255,255,255,0.07)' },
    promo:      { icon: '📣', label: 'Promotional',         color: 'var(--orange)', bg: 'rgba(255,122,32,0.07)',  border: 'rgba(255,122,32,0.2)' },
  };

  list.innerHTML = TIMELINE_EVENTS.slice().reverse().map(function(e) {
    var t = TL_INFO[e.type] || TL_INFO['note'];
    return '<div class="tl-card" style="--tl-color:' + t.color + ';--tl-bg:' + t.bg + ';--tl-border:' + t.border + '">'
      + '<div class="tl-top">'
      +   '<div class="tl-status">'
      +     '<span class="tl-icon">' + t.icon + '</span>'
      +     '<span class="tl-label">' + t.label + '</span>'
      +   '</div>'
      +   '<span class="tl-date">' + e.date + '</span>'
      + '</div>'
      + '<div class="tl-text">' + e.text + (e.isNew ? '<span class="badge-new">New</span>' : '') + '</div>'
      + '</div>';
  }).join('');
}

function renderQuotes() {
  const grid = document.getElementById('quotes-grid');
  if (!grid) return;

  var TAG_INFO = {
    promise:       { icon: '🔵', label: 'They promised this',    color: 'var(--cyan)',                  bg: 'rgba(0,212,255,0.08)',    border: 'rgba(0,212,255,0.2)' },
    broken:        { icon: '🔴', label: 'Broken promise',         color: 'var(--red)',                   bg: 'rgba(255,59,59,0.08)',    border: 'rgba(255,59,59,0.2)' },
    misleading:    { icon: '🟠', label: 'Misleading claim',       color: 'var(--orange)',                bg: 'rgba(255,122,32,0.08)',   border: 'rgba(255,122,32,0.2)' },
    community:     { icon: '💬', label: 'Community reaction',     color: 'var(--yellow)',                bg: 'rgba(240,192,48,0.08)',   border: 'rgba(240,192,48,0.2)' },
    warning:       { icon: '⚠️', label: 'Official warning',       color: 'rgba(255,255,255,0.5)',        bg: 'rgba(255,255,255,0.04)', border: 'rgba(255,255,255,0.1)' },
    response:      { icon: '💭', label: 'Official response',      color: 'rgba(255,255,255,0.4)',        bg: 'rgba(255,255,255,0.03)', border: 'rgba(255,255,255,0.08)' },
    claim:         { icon: '📢', label: 'Their claim',            color: 'var(--cyan)',                  bg: 'rgba(0,212,255,0.08)',    border: 'rgba(0,212,255,0.2)' },
    promo:         { icon: '📣', label: 'Promotional message',    color: 'var(--orange)',                bg: 'rgba(255,122,32,0.08)',   border: 'rgba(255,122,32,0.2)' },
    'fine-print':  { icon: '🔍', label: 'Fine print they hid',   color: 'var(--red)',                   bg: 'rgba(255,59,59,0.08)',    border: 'rgba(255,59,59,0.2)' },
    investigation: { icon: '📰', label: 'Investigation finding',  color: 'var(--red)',                   bg: 'rgba(255,59,59,0.08)',    border: 'rgba(255,59,59,0.2)' },
  };

  grid.innerHTML = NOTABLE_QUOTES.map(function(q) {
    var t = TAG_INFO[q.tag] || TAG_INFO['response'];
    return '<div class="ev-card" style="--ev-color:' + t.color + ';--ev-bg:' + t.bg + ';--ev-border:' + t.border + '">'
      + '<div class="ev-status">'
      +   '<span class="ev-status-icon">' + t.icon + '</span>'
      +   '<span class="ev-status-label">' + t.label + '</span>'
      +   '<span class="ev-date">' + q.date + '</span>'
      + '</div>'
      + '<div class="ev-quote">"' + q.text + '"</div>'
      + (q.src
          ? '<a href="' + q.src + '" target="_blank" rel="noopener noreferrer" class="ev-source-btn">View original post on X →</a>'
          : '')
      + '</div>';
  }).join('');
}

function buildGaugeSVG(pct) {
  const r = 54;
  const cx = 70, cy = 70;
  const startAngle = -220;
  const endAngle = 40;
  const totalArc = endAngle - startAngle;
  const fillArc = totalArc * (pct / 100);

  function polar(angle, radius) {
    const rad = (angle - 90) * Math.PI / 180;
    return [cx + radius * Math.cos(rad), cy + radius * Math.sin(rad)];
  }

  function arcPath(start, end, r) {
    const [x1, y1] = polar(start, r);
    const [x2, y2] = polar(end, r);
    const large = (end - start) > 180 ? 1 : 0;
    return `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`;
  }

  const trackPath = arcPath(startAngle, endAngle, r);
  const fillPath = fillArc > 0 ? arcPath(startAngle, startAngle + fillArc, r) : '';

  return `<svg class="gauge-svg" viewBox="0 0 140 140">
    <path d="${trackPath}" fill="none" stroke="#0d2035" stroke-width="10" stroke-linecap="round"/>
    ${fillPath ? `<path d="${fillPath}" fill="none" stroke="#00d4ff" stroke-width="10" stroke-linecap="round" filter="url(#glow)"/>` : ''}
    <defs>
      <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    </defs>
  </svg>`;
}

function renderStats() {
  const gaugeEl = document.getElementById('gauge-container');
  const statsEl = document.getElementById('stats-grid');
  if (!gaugeEl && !statsEl) return;

  const broken = PROMISES.filter(p => p.status === 'broken').length;
  const kept = PROMISES.filter(p => p.status === 'kept').length;
  const pending = PROMISES.filter(p => p.status === 'pending').length;
  const misleading = PROMISES.filter(p => p.status === 'misleading').length;
  const total = PROMISES.length;
  const rate = Math.round((kept / total) * 100);

  if (gaugeEl) {
    gaugeEl.innerHTML = `
      <div class="gauge-panel">
        ${buildGaugeSVG(rate)}
        <div class="gauge-value">${rate}%</div>
        <div class="gauge-label">Delivery rate</div>
      </div>
    `;
  }

  if (statsEl) {
    statsEl.innerHTML = `
      <a href="tracker.html?filter=all" class="stat-box stat-box--link reveal" style="--stat-color: var(--cyan)">
        <div class="stat-box-label">Promises tracked</div>
        <div class="stat-box-number" data-count="${total}">0</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:0%" data-width="100"></div></div>
        <div class="stat-box-hint">View all →</div>
      </a>
      <a href="tracker.html?filter=kept" class="stat-box stat-box--link reveal reveal-delay-1" style="--stat-color: var(--green)">
        <div class="stat-box-label">Kept</div>
        <div class="stat-box-number" data-count="${kept}">0</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:0%" data-width="${Math.round(kept/total*100)}"></div></div>
        <div class="stat-box-hint">View kept →</div>
      </a>
      <a href="tracker.html?filter=broken" class="stat-box stat-box--link reveal reveal-delay-2" style="--stat-color: var(--red)">
        <div class="stat-box-label">Broken / Misleading</div>
        <div class="stat-box-number" data-count="${broken + misleading}">0</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:0%" data-width="${Math.round((broken+misleading)/total*100)}"></div></div>
        <div class="stat-box-hint">View broken →</div>
      </a>
      <a href="tracker.html?filter=pending" class="stat-box stat-box--link reveal reveal-delay-3" style="--stat-color: var(--yellow)">
        <div class="stat-box-label">Pending</div>
        <div class="stat-box-number" data-count="${pending}">0</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:0%" data-width="${Math.round(pending/total*100)}"></div></div>
        <div class="stat-box-hint">View pending →</div>
      </a>
    `;

    /* Trigger counter + bar animations when stat boxes enter viewport */
    const statObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (!e.isIntersecting) return;
        const numEl = e.target.querySelector('[data-count]');
        const barEl = e.target.querySelector('[data-width]');
        if (numEl) animateCounter(numEl, parseInt(numEl.dataset.count));
        if (barEl) {
          setTimeout(function() { barEl.style.width = barEl.dataset.width + '%'; }, 100);
        }
        statObs.unobserve(e.target);
      });
    }, { threshold: 0.3 });
    statsEl.querySelectorAll('.stat-box').forEach(function(b) { statObs.observe(b); });
  }
}

function renderSources() {
  const grid = document.getElementById('sources-grid');
  if (!grid) return;
  grid.innerHTML = SOURCES.map(function(s, i) {
    return '<div class="src-card">'
      + '<div class="src-num">' + (i + 1) + '</div>'
      + '<div class="src-icon">' + s.icon + '</div>'
      + '<div class="src-body">'
      +   '<div class="src-name">' + s.name + '</div>'
      +   '<div class="src-desc">' + s.description + '</div>'
      +   '<a href="' + s.url + '" target="_blank" rel="noopener noreferrer" class="src-link">Visit source: ' + s.label + ' →</a>'
      + '</div>'
      + '</div>';
  }).join('');
}

function renderInvestigation() {
  const verdict = document.getElementById('investigation-verdict');
  const grid = document.getElementById('investigation-grid');

  if (verdict) {
    verdict.innerHTML = `
      <div class="inv-verdict-strip">
        <div class="inv-verdict-left">
          <div class="inv-verdict-badge">⚠️ Verdict</div>
          <h2 class="inv-verdict-title">Fraud Indicators</h2>
          <p class="inv-verdict-text">An independent DL News investigation reveals missing miners, unpaid employees, and breached contracts across multiple major sponsorships.</p>
          <div class="inv-verdict-stat">
            <span class="inv-verdict-num">−99.7%</span>
            <span class="inv-verdict-lab">price drop vs promised $0.05</span>
          </div>
        </div>
        <div class="inv-verdict-right">
          <div class="inv-price-header">Promise vs Reality</div>
          <div class="inv-price-row">
            <div class="inv-price-col">
              <div class="inv-price-label">Promised launch price</div>
              <div class="inv-price-val inv-price-val--strike">$0.05</div>
            </div>
            <div class="inv-price-arrow">→</div>
            <div class="inv-price-col">
              <div class="inv-price-label">Actual launch price</div>
              <div class="inv-price-val">$0.0001554</div>
            </div>
          </div>
          <div class="inv-price-row">
            <div class="inv-price-col">
              <div class="inv-price-label">Promised market cap</div>
              <div class="inv-price-val inv-price-val--strike">$1,000,000,000</div>
            </div>
            <div class="inv-price-arrow">→</div>
            <div class="inv-price-col">
              <div class="inv-price-label">Actual market cap</div>
              <div class="inv-price-val">$5,650,000</div>
            </div>
          </div>
          <div class="inv-price-row">
            <div class="inv-price-col">
              <div class="inv-price-label">Claimed raised</div>
              <div class="inv-price-val inv-price-val--strike">$442,000,000</div>
            </div>
            <div class="inv-price-arrow">→</div>
            <div class="inv-price-col">
              <div class="inv-price-label">On-chain (ZachXBT)</div>
              <div class="inv-price-val">&lt;$100,000,000</div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  if (grid) {
    grid.innerHTML = `
      <div class="inv-findings-header">
        <span class="inv-findings-title">DL News Findings — ${INVESTIGATION.findings.length} confirmed</span>
      </div>
      <div class="inv-findings-list">
        ${INVESTIGATION.findings.map(function(f, i) {
          return '<div class="inv-finding-card">'
            + '<div class="inv-finding-main">'
            + '<div class="inv-finding-num">' + (i + 1) + '</div>'
            + '<div class="inv-finding-body">'
            + '<div class="inv-finding-label">' + f.label + '</div>'
            + '<div class="inv-finding-detail">' + f.detail + '</div>'
            + '</div>'
            + '</div>'
            + (f.image ? '<div class="inv-finding-img-wrap"><img src="' + f.image + '" alt="' + f.imageCaption + '" class="inv-finding-img" loading="lazy" onerror="this.parentElement.style.display=\'none\'"><div class="inv-finding-img-caption">' + f.imageCaption + '</div></div>' : '')
            + '</div>';
        }).join('')}
      </div>
    `;
  }
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderPromises(btn.dataset.filter, urlCategory);
  });
});

/* Mark active nav link + inject mobile hamburger */
(function () {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === path) a.classList.add('active');
  });

  /* Build nav links list from desktop nav */
  const desktopNav = document.querySelector('.nav');
  if (!desktopNav) return;
  const links = Array.from(desktopNav.querySelectorAll('a')).map(a =>
    `<a href="${a.href}"${a.classList.contains('active') ? ' class="active"' : ''}>${a.textContent}</a>`
  ).join('');

  /* Inject hamburger button */
  const hamburger = document.createElement('button');
  hamburger.className = 'hamburger';
  hamburger.setAttribute('aria-label', 'Open menu');
  hamburger.textContent = '☰';
  desktopNav.parentElement.appendChild(hamburger);

  /* Inject mobile nav overlay */
  const mobileNav = document.createElement('div');
  mobileNav.className = 'mobile-nav';
  mobileNav.innerHTML = `<button class="mobile-nav-close" aria-label="Close menu">✕</button>${links}`;
  document.body.appendChild(mobileNav);

  hamburger.addEventListener('click', () => mobileNav.classList.add('open'));
  mobileNav.querySelector('.mobile-nav-close').addEventListener('click', () => mobileNav.classList.remove('open'));
  mobileNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobileNav.classList.remove('open')));
})();

/* Read URL params on tracker page */
const urlParams  = new URLSearchParams(location.search);
const urlFilter  = urlParams.get('filter') || 'all';
const urlCategory= urlParams.get('category') || null;


/* ── METRICS STRIP COUNTERS ── */
(function() {
  var strip = document.getElementById('metrics-strip');
  if (!strip) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (!e.isIntersecting) return;
      e.target.querySelectorAll('[data-count]').forEach(function(n) {
        animateCounter(n, parseInt(n.dataset.count), 1400);
      });
      obs.unobserve(e.target);
    });
  }, { threshold: 0.25 });
  obs.observe(strip);
})();

/* ── TICKER DUPLICATE (seamless loop) ── */
(function () {
  const track = document.getElementById('ticker-track');
  if (!track) return;
  const clone = track.innerHTML;
  track.innerHTML = clone + clone;
})();

/* ── ANIMATED COUNTER ── */
function animateCounter(el, target, duration) {
  duration = duration || 1400;
  const start = performance.now();
  const update = function(now) {
    const p = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(ease * target);
    if (p < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

/* ── SCROLL REVEAL ── */
(function () {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  const obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        e.target.classList.add('revealed');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  els.forEach(function(el) { obs.observe(el); });
})();

function renderTrackerSummary() {
  const el = document.getElementById('tracker-summary');
  if (!el) return;
  const broken = PROMISES.filter(p => p.status === 'broken').length;
  const kept = PROMISES.filter(p => p.status === 'kept').length;
  const pending = PROMISES.filter(p => p.status === 'pending').length;
  const misleading = PROMISES.filter(p => p.status === 'misleading').length;
  const total = PROMISES.length;
  const rate = Math.round(kept / total * 100);
  el.innerHTML = `
    <div class="summary-strip summary-strip--cyan">
      <div class="summary-left">
        <div class="summary-badge">📊 Tracker Summary</div>
        <h2 class="summary-title">Every promise.<br>Every result.</h2>
        <p class="summary-text">Of ${total} promises tracked, only ${kept} were actually kept. The rest were broken, misleading, or remain undelivered.</p>
        <div class="summary-stat">
          <span class="summary-num">${rate}%</span>
          <span class="summary-lab">delivery rate<br>across all tracked promises</span>
        </div>
      </div>
      <div class="summary-right">
        <div class="summary-table-header">Promise breakdown</div>
        <div class="summary-row"><span class="summary-row-label">🔵 Total tracked</span><span class="summary-row-val summary-row-val--cyan">${total}</span></div>
        <div class="summary-row"><span class="summary-row-label">✕ Broken</span><span class="summary-row-val summary-row-val--red">${broken}</span></div>
        <div class="summary-row"><span class="summary-row-label">! Misleading</span><span class="summary-row-val summary-row-val--orange">${misleading}</span></div>
        <div class="summary-row"><span class="summary-row-label">✓ Kept</span><span class="summary-row-val summary-row-val--green">${kept}</span></div>
        <div class="summary-row"><span class="summary-row-label">… Pending</span><span class="summary-row-val summary-row-val--yellow">${pending}</span></div>
      </div>
    </div>
  `;
}

function renderTimelineSummary() {
  const el = document.getElementById('timeline-summary');
  if (!el) return;
  const counts = {};
  TIMELINE_EVENTS.forEach(e => { counts[e.type] = (counts[e.type] || 0) + 1; });
  const total = TIMELINE_EVENTS.length;
  const broken = counts.broken || 0;
  el.innerHTML = `
    <div class="summary-strip summary-strip--neutral">
      <div class="summary-left">
        <div class="summary-badge">📅 Timeline Summary</div>
        <h2 class="summary-title">How it all<br>played out.</h2>
        <p class="summary-text">${total} events documenting how BlockDAG's commitments were made, repeatedly delayed, and quietly dropped.</p>
        <div class="summary-stat">
          <span class="summary-num">${broken}</span>
          <span class="summary-lab">broken deadline<br>events in timeline</span>
        </div>
      </div>
      <div class="summary-right">
        <div class="summary-table-header">Timeline events by type (≠ promise count)</div>
        ${counts.broken     ? `<div class="summary-row"><span class="summary-row-label">🔴 Broken deadline events</span><span class="summary-row-val summary-row-val--red">${counts.broken}</span></div>` : ''}
        ${counts.promise    ? `<div class="summary-row"><span class="summary-row-label">🔵 They promised</span><span class="summary-row-val summary-row-val--cyan">${counts.promise}</span></div>` : ''}
        ${counts.misleading ? `<div class="summary-row"><span class="summary-row-label">🟠 Misleading</span><span class="summary-row-val summary-row-val--orange">${counts.misleading}</span></div>` : ''}
        ${counts.kept       ? `<div class="summary-row"><span class="summary-row-label">🟢 Kept</span><span class="summary-row-val summary-row-val--green">${counts.kept}</span></div>` : ''}
        ${counts.partial    ? `<div class="summary-row"><span class="summary-row-label">🟡 Partial delivery</span><span class="summary-row-val summary-row-val--yellow">${counts.partial}</span></div>` : ''}
        ${counts.promo      ? `<div class="summary-row"><span class="summary-row-label">📣 Promotional</span><span class="summary-row-val summary-row-val--orange">${counts.promo}</span></div>` : ''}
        ${counts.warning    ? `<div class="summary-row"><span class="summary-row-label">⚠️ Warnings</span><span class="summary-row-val summary-row-val--white">${counts.warning}</span></div>` : ''}
        ${counts.note       ? `<div class="summary-row"><span class="summary-row-label">📌 Notes</span><span class="summary-row-val summary-row-val--white">${counts.note}</span></div>` : ''}
      </div>
    </div>
  `;
}

function renderEvidenceSummary() {
  const el = document.getElementById('evidence-summary');
  if (!el) return;
  const counts = {};
  NOTABLE_QUOTES.forEach(q => { counts[q.tag] = (counts[q.tag] || 0) + 1; });
  const total = NOTABLE_QUOTES.length;
  const negative = (counts.broken || 0) + (counts.misleading || 0) + (counts['fine-print'] || 0) + (counts.investigation || 0);
  el.innerHTML = `
    <div class="summary-strip summary-strip--orange">
      <div class="summary-left">
        <div class="summary-badge">💬 Evidence Summary</div>
        <h2 class="summary-title">Their words.<br>Verbatim.</h2>
        <p class="summary-text">${total} quotes sourced directly from official BlockDAG communications — Telegram, X/Twitter, and their own website. Unedited.</p>
        <div class="summary-stat">
          <span class="summary-num">${negative}</span>
          <span class="summary-lab">broken, misleading<br>or damning quotes</span>
        </div>
      </div>
      <div class="summary-right">
        <div class="summary-table-header">Quotes by type</div>
        ${counts.promise       ? `<div class="summary-row"><span class="summary-row-label">🔵 They promised this</span><span class="summary-row-val summary-row-val--cyan">${counts.promise}</span></div>` : ''}
        ${counts.broken        ? `<div class="summary-row"><span class="summary-row-label">🔴 Broken promise</span><span class="summary-row-val summary-row-val--red">${counts.broken}</span></div>` : ''}
        ${counts.misleading    ? `<div class="summary-row"><span class="summary-row-label">🟠 Misleading claim</span><span class="summary-row-val summary-row-val--orange">${counts.misleading}</span></div>` : ''}
        ${counts.claim         ? `<div class="summary-row"><span class="summary-row-label">📢 Their claim</span><span class="summary-row-val summary-row-val--cyan">${counts.claim}</span></div>` : ''}
        ${counts.promo         ? `<div class="summary-row"><span class="summary-row-label">📣 Promotional</span><span class="summary-row-val summary-row-val--orange">${counts.promo}</span></div>` : ''}
        ${counts.investigation ? `<div class="summary-row"><span class="summary-row-label">📰 Investigation finding</span><span class="summary-row-val summary-row-val--red">${counts.investigation}</span></div>` : ''}
        ${counts['fine-print'] ? `<div class="summary-row"><span class="summary-row-label">🔍 Fine print</span><span class="summary-row-val summary-row-val--red">${counts['fine-print']}</span></div>` : ''}
        ${counts.community     ? `<div class="summary-row"><span class="summary-row-label">💬 Community reaction</span><span class="summary-row-val summary-row-val--yellow">${counts.community}</span></div>` : ''}
      </div>
    </div>
  `;
}

function renderIndicators() {
  const root = document.getElementById('indicators-root');
  if (!root) return;

  const broken = PROMISES.filter(p => p.status === 'broken').length;
  const kept = PROMISES.filter(p => p.status === 'kept').length;
  const misleading = PROMISES.filter(p => p.status === 'misleading').length;
  const pending = PROMISES.filter(p => p.status === 'pending').length;
  const total = PROMISES.length;

  // Score components (each out of their max)
  const deliveryMax = 35;
  const priceMax = 25;
  const transparencyMax = 20;
  const executionMax = 20;

  // 1. Promise delivery: kept/total * max
  const deliveryScore = Math.round((kept / total) * deliveryMax);

  // 2. Price performance: actual vs promised ($0.05). Always 0 until price recovers.
  const priceScore = 0;

  // 3. Transparency: 4 major failures documented (hidden founder, whitepaper plagiarism, fund discrepancy, censorship) → 0
  const transparencyScore = 2;

  // 4. Development execution: (kept + partial) / total * max
  const partials = TIMELINE_EVENTS.filter(e => e.type === 'partial').length;
  const executionScore = Math.round(((kept * 2 + partials) / (total + partials)) * executionMax);

  const total_score = Math.min(100, deliveryScore + priceScore + transparencyScore + executionScore);

  const scoreColor = total_score < 20 ? '#ff3b3b' :
                     total_score < 40 ? '#ff7a20' :
                     total_score < 60 ? '#f0c030' :
                     total_score < 80 ? '#80c940' : '#00e5a0';

  const scoreLabel = total_score < 20 ? 'Extreme Risk' :
                     total_score < 40 ? 'High Risk' :
                     total_score < 60 ? 'Moderate Risk' :
                     total_score < 80 ? 'Cautious' : 'Trustworthy';

  // Build SVG gauge (semicircle)
  function buildTrustGauge(score, color) {
    const cx = 130, cy = 110, r = 90;
    function polar(deg) {
      const rad = (deg - 180) * Math.PI / 180;
      return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)];
    }
    function arc(startDeg, endDeg, stroke) {
      const [x1, y1] = polar(startDeg);
      const [x2, y2] = polar(endDeg);
      const large = endDeg - startDeg > 180 ? 1 : 0;
      return `<path d="M${x1},${y1} A${r},${r} 0 ${large} 1 ${x2},${y2}" fill="none" stroke="${stroke}" stroke-width="14" stroke-linecap="round"/>`;
    }
    const scoreDeg = score * 1.8;
    const segments = [
      [0,36,'rgba(255,59,59,0.25)'], [36,72,'rgba(255,100,20,0.25)'],
      [72,108,'rgba(240,192,48,0.25)'], [108,144,'rgba(128,201,64,0.25)'],
      [144,180,'rgba(0,229,160,0.25)']
    ];
    const segSVG = segments.map(([s,e,c]) => arc(s, e, c)).join('');
    const fillSVG = scoreDeg > 0 ? arc(0, Math.min(scoreDeg, 179.9), color) : '';
    const [nx, ny] = polar(scoreDeg);
    const needle = `<line x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.9"/>
      <circle cx="${cx}" cy="${cy}" r="5" fill="white" opacity="0.9"/>`;
    return `<svg class="ind-gauge-svg" viewBox="0 0 260 120">
      ${segSVG}
      <defs><filter id="glow2"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      <g filter="url(#glow2)">${fillSVG}</g>
      ${needle}
      <text x="14" y="118" fill="rgba(255,255,255,0.25)" font-size="9" font-family="monospace">0</text>
      <text x="238" y="118" fill="rgba(255,255,255,0.25)" font-size="9" font-family="monospace">100</text>
    </svg>`;
  }

  function compBar(score, max, color) {
    const pct = Math.round((score / max) * 100);
    return `<div class="ind-comp-bar-track"><div class="ind-comp-bar-fill" style="width:${pct}%;background:${color}"></div></div>`;
  }

  const levels = [
    { range: '0–20', name: 'Extreme Risk', color: '#ff3b3b', bg: 'rgba(255,59,59,0.08)' },
    { range: '21–40', name: 'High Risk', color: '#ff7a20', bg: 'rgba(255,122,32,0.08)' },
    { range: '41–60', name: 'Moderate', color: '#f0c030', bg: 'rgba(240,192,48,0.08)' },
    { range: '61–80', name: 'Cautious', color: '#80c940', bg: 'rgba(128,201,64,0.08)' },
    { range: '81–100', name: 'Trustworthy', color: '#00e5a0', bg: 'rgba(0,229,160,0.08)' },
  ];

  const activeIdx = total_score < 20 ? 0 : total_score < 40 ? 1 : total_score < 60 ? 2 : total_score < 80 ? 3 : 4;

  root.innerHTML = `
    <div class="ind-layout">
      <div class="ind-gauge-panel">
        <div class="ind-gauge-wrap">
          ${buildTrustGauge(total_score, scoreColor)}
          <div class="ind-score-overlay">
            <div class="ind-score-num" style="color:${scoreColor}">${total_score}</div>
            <div class="ind-score-label" style="color:${scoreColor}">${scoreLabel}</div>
          </div>
        </div>
        <div class="ind-score-sub">Out of 100 — calculated from ${total} tracked promises</div>
        <div class="ind-last-updated">Auto-updated · Based on live data</div>
      </div>

      <div class="ind-components">
        <div class="ind-comp-card">
          <div class="ind-comp-top">
            <span class="ind-comp-name">Promise Delivery</span>
            <span class="ind-comp-score" style="color:#ff3b3b">${deliveryScore}/${deliveryMax}</span>
          </div>
          ${compBar(deliveryScore, deliveryMax, '#ff3b3b')}
          <div class="ind-comp-desc">${kept} kept out of ${total} promises. ${broken} broken, ${misleading} misleading, ${pending} pending.</div>
        </div>
        <div class="ind-comp-card">
          <div class="ind-comp-top">
            <span class="ind-comp-name">Price Performance</span>
            <span class="ind-comp-score" style="color:#ff3b3b">${priceScore}/${priceMax}</span>
          </div>
          ${compBar(priceScore, priceMax, '#ff3b3b')}
          <div class="ind-comp-desc">Promised launch price: $0.05. Actual: $0.0001554. Down 99.7% from own promise.</div>
        </div>
        <div class="ind-comp-card">
          <div class="ind-comp-top">
            <span class="ind-comp-name">Transparency</span>
            <span class="ind-comp-score" style="color:#ff7a20">${transparencyScore}/${transparencyMax}</span>
          </div>
          ${compBar(transparencyScore, transparencyMax, '#ff7a20')}
          <div class="ind-comp-desc">Hidden founder for 2+ years, whitepaper plagiarism from Kaspa, $300M+ fund discrepancy, censored Telegram.</div>
        </div>
        <div class="ind-comp-card">
          <div class="ind-comp-top">
            <span class="ind-comp-name">Development Execution</span>
            <span class="ind-comp-score" style="color:#ff7a20">${executionScore}/${executionMax}</span>
          </div>
          ${compBar(executionScore, executionMax, '#ff7a20')}
          <div class="ind-comp-desc">5 missed mainnet deadlines. Staking broken 70+ days. Miners unshipped 6+ months after promise.</div>
        </div>
      </div>
    </div>

    <div class="ind-levels">
      ${levels.map((l, i) => `
        <div class="ind-level ${i === activeIdx ? 'active' : ''}" style="background:${i===activeIdx ? l.bg : 'rgba(255,255,255,0.015)'}; border-color:${i===activeIdx ? l.color : 'rgba(255,255,255,0.06)'}">
          <div class="ind-level-range" style="color:${l.color}">${l.range}</div>
          <div class="ind-level-name" style="color:${i===activeIdx ? l.color : 'rgba(255,255,255,0.3)'}">${l.name}</div>
        </div>
      `).join('')}
    </div>

    <div class="ind-disclaimer">
      ⚠️ This score is calculated automatically from the promises and data tracked on this site. It is not financial advice. The score will improve if BlockDAG delivers on outstanding promises. This is an independent community tool with no affiliation to BlockDAG Network.
    </div>
  `;
}

function renderHomeUpdates() {
  const newList = document.getElementById('home-new-list');
  const pendingList = document.getElementById('home-pending-list');

  if (newList) {
    const newItems = PROMISES.filter(p => p.isNew);
    const metaColor = { broken: 'red', misleading: 'orange', kept: 'green', pending: 'yellow' };
    const metaLabel = { broken: 'Broken', misleading: 'Misleading', kept: 'Kept', pending: 'Pending' };
    newList.innerHTML = newItems.map(p => `
      <a href="tracker.html" class="home-update-item">
        <div class="home-update-item-title">${p.title}</div>
        <span class="home-update-item-meta home-update-item-meta--${metaColor[p.status]}">${metaLabel[p.status]}</span>
      </a>
    `).join('');
  }

  if (pendingList) {
    const pending = PROMISES.filter(p => p.status === 'pending');
    pendingList.innerHTML = pending.map(p => `
      <a href="tracker.html?filter=pending" class="home-update-item">
        <div class="home-update-item-title">${p.title}</div>
        <span class="home-update-item-meta home-update-item-meta--yellow">${p.promised}</span>
      </a>
    `).join('');
  }
}

/* ── PRICE TICKER ── */
(function() {
  const ticker = document.createElement('div');
  ticker.className = 'price-ticker';
  ticker.innerHTML = `
    <div class="ticker-inner">
      <span class="ticker-label">BDAG Live</span>
      <span class="ticker-price" id="ticker-price">…</span>
      <span id="ticker-change" class="ticker-change--down"></span>
      <span class="ticker-sep">|</span>
      <span class="ticker-label">Promised</span>
      <span class="ticker-promised">$0.05</span>
      <span class="ticker-sep">|</span>
      <span class="ticker-label">Below promise</span>
      <span class="ticker-down" id="ticker-down">…</span>
    </div>`;
  document.body.insertBefore(ticker, document.body.firstChild);

  function updateTicker(data) {
    const price = data.blockdag && data.blockdag.usd;
    const change = data.blockdag && data.blockdag.usd_24h_change;
    if (!price) return false;
    document.getElementById('ticker-price').textContent = '$' + price.toFixed(8);
    if (change !== undefined) {
      const el = document.getElementById('ticker-change');
      el.textContent = (change >= 0 ? '+' : '') + change.toFixed(2) + '%';
      el.className = 'ticker-change--' + (change >= 0 ? 'up' : 'down');
    }
    const pct = ((price - 0.05) / 0.05 * 100).toFixed(1);
    document.getElementById('ticker-down').textContent = pct + '%';
    return true;
  }

  function fetchTicker(attempt) {
    fetch('https://api.coingecko.com/api/v3/simple/price?ids=blockdag&vs_currencies=usd&include_24hr_change=true')
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (!updateTicker(d) && attempt < 3) {
          setTimeout(function() { fetchTicker(attempt + 1); }, 3000);
        }
      })
      .catch(function() {
        if (attempt < 3) {
          setTimeout(function() { fetchTicker(attempt + 1); }, 3000);
        } else {
          var el = document.getElementById('ticker-price');
          el.innerHTML = '<a href="https://coinmarketcap.com/currencies/blockdag/" target="_blank" style="color:rgba(255,255,255,0.4);text-decoration:none;font-size:10px;">View on CMC →</a>';
        }
      });
  }
  fetchTicker(1);
})();

/* ── COUNTDOWN ── */
function renderCountdown() {
  const timer = document.getElementById('countdown-timer');
  if (!timer) return;
  const target = new Date('2026-05-07T00:00:00');
  function tick() {
    const diff = target - new Date();
    if (diff <= 0) {
      timer.innerHTML = '<span class="countdown-expired">DEADLINE PASSED ❌</span>';
      return;
    }
    const d = Math.floor(diff / 864e5);
    const h = Math.floor(diff % 864e5 / 36e5);
    const m = Math.floor(diff % 36e5 / 6e4);
    const s = Math.floor(diff % 6e4 / 1e3);
    document.getElementById('cd-days').textContent = String(d).padStart(2,'0');
    document.getElementById('cd-hours').textContent = String(h).padStart(2,'0');
    document.getElementById('cd-mins').textContent = String(m).padStart(2,'0');
    document.getElementById('cd-secs').textContent = String(s).padStart(2,'0');
  }
  tick();
  setInterval(tick, 1000);
}

/* ── SEARCH ── */
function initSearch() {
  const input = document.getElementById('promise-search');
  const countEl = document.getElementById('search-count');
  if (!input) return;
  input.addEventListener('input', function() {
    const q = this.value.toLowerCase().trim();
    const rows = document.querySelectorAll('.promise-row');
    let visible = 0;
    rows.forEach(function(row) {
      const detail = row.nextElementSibling;
      const text = row.textContent.toLowerCase();
      const show = !q || text.includes(q);
      row.style.display = show ? '' : 'none';
      if (detail) detail.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    if (countEl) countEl.textContent = q ? visible + ' result' + (visible !== 1 ? 's' : '') + ' for "' + this.value + '"' : '';
  });
}

/* Auto-render whatever is on this page */
renderStats();
renderHomeUpdates();
renderCountdown();
renderCategories();
renderTrackerSummary();
renderPromises(urlFilter, urlCategory);
renderTimelineSummary();
renderTimeline();
renderInvestigation();
renderEvidenceSummary();
renderQuotes();
renderSources();
renderIndicators();
initSearch();

/* Apply active filter button + category heading on tracker page */
if (document.getElementById('promise-table')) {
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.filter === urlFilter);
  });

  if (urlCategory) {
    const icon = CAT_ICON[urlCategory] || '📌';
    const heading = document.getElementById('tracker-heading');
    if (heading) heading.innerHTML = `${icon} ${urlCategory}`;
    const sub = document.getElementById('tracker-sub');
    if (sub) sub.textContent = `Showing all promises in this category. Use filters above to narrow down by status.`;
    const back = document.getElementById('tracker-back');
    if (back) { back.href = 'categories.html'; back.style.display = 'inline-flex'; }
  }
}
