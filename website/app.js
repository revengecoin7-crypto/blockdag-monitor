const STATUS_LABEL = {
  broken: 'Broken',
  kept: 'Kept',
  pending: 'Pending',
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
      const icon = CAT_ICON[cat] || '📌';
      const url = `tracker.html?category=${encodeURIComponent(cat)}`;
      const statusLine = [
        broken    ? `<span class="cat-pill cat-pill--red">${broken} broken</span>` : '',
        c.kept    ? `<span class="cat-pill cat-pill--green">${c.kept} kept</span>` : '',
        c.pending ? `<span class="cat-pill cat-pill--yellow">${c.pending} pending</span>` : '',
      ].filter(Boolean).join('');
      return `
        <a href="${url}" class="cat-card">
          <div class="cat-card-top">
            <div class="cat-icon">${icon}</div>
            <div class="cat-count">${c.total}</div>
          </div>
          <div class="cat-name">${cat}</div>
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
  let items = PROMISES;
  if (category) items = items.filter(p => p.category === category);
  if (filter && filter !== 'all') items = items.filter(p => p.status === filter);

  table.innerHTML = items.map((p, i) => `
    <div class="promise-row" onclick="toggleDetail(this)">
      <div class="pr-num ${p.status}">${i + 1}</div>
      <div class="pr-title">${p.title}</div>
      <div class="pr-cat">${p.category}</div>
      <div class="pr-date">${p.promised}</div>
      <div><span class="pr-status ${p.status}">${STATUS_ICON[p.status]} ${STATUS_LABEL[p.status]}</span></div>
    </div>
    <div class="promise-detail">
      <div class="promise-detail-text">${p.reality}</div>
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
  list.innerHTML = TIMELINE_EVENTS.map(e => `
    <div class="timeline-item">
      <div class="timeline-dot dot-${e.type}"></div>
      <div class="timeline-card">
        <div class="timeline-date">${e.date}</div>
        <div class="timeline-text">${e.text}</div>
      </div>
    </div>
  `).join('');
}

function renderQuotes() {
  const grid = document.getElementById('quotes-grid');
  if (!grid) return;
  grid.innerHTML = NOTABLE_QUOTES.map(q => `
    <div class="notable-quote">
      <div class="notable-quote-header">
        <span class="notable-quote-date">${q.date}</span>
        <span class="notable-quote-tag tag-${q.tag}">${q.tag.toUpperCase()}</span>
      </div>
      <div class="notable-quote-text">"${q.text}"</div>
      ${q.src ? `<a href="${q.src}" target="_blank" rel="noopener noreferrer" class="notable-quote-src">🔗 View source on X</a>` : ''}
    </div>
  `).join('');
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
      <a href="tracker.html?filter=all" class="stat-box stat-box--link" style="--stat-color: var(--cyan)">
        <div class="stat-box-label">Promises tracked</div>
        <div class="stat-box-number">${total}</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:100%"></div></div>
        <div class="stat-box-hint">View all →</div>
      </a>
      <a href="tracker.html?filter=kept" class="stat-box stat-box--link" style="--stat-color: var(--green)">
        <div class="stat-box-label">Kept</div>
        <div class="stat-box-number">${kept}</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:${Math.round(kept/total*100)}%"></div></div>
        <div class="stat-box-hint">View kept →</div>
      </a>
      <a href="tracker.html?filter=broken" class="stat-box stat-box--link" style="--stat-color: var(--red)">
        <div class="stat-box-label">Broken / Misleading</div>
        <div class="stat-box-number">${broken + misleading}</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:${Math.round((broken+misleading)/total*100)}%"></div></div>
        <div class="stat-box-hint">View broken →</div>
      </a>
      <a href="tracker.html?filter=pending" class="stat-box stat-box--link" style="--stat-color: var(--yellow)">
        <div class="stat-box-label">Pending</div>
        <div class="stat-box-number">${pending}</div>
        <div class="stat-box-bar"><div class="stat-box-fill" style="width:${Math.round(pending/total*100)}%"></div></div>
        <div class="stat-box-hint">View pending →</div>
      </a>
    `;
  }
}

function renderSources() {
  const grid = document.getElementById('sources-grid');
  if (!grid) return;
  grid.innerHTML = SOURCES.map(s => `
    <div class="source-card">
      <div class="source-icon">${s.icon}</div>
      <div class="source-body">
        <div class="source-name">${s.name}</div>
        <div class="source-desc">${s.description}</div>
        <a href="${s.url}" target="_blank" rel="noopener noreferrer" class="source-link">${s.label} →</a>
      </div>
    </div>
  `).join('');
}

function renderInvestigation() {
  const verdict = document.getElementById('investigation-verdict');
  const grid = document.getElementById('investigation-grid');

  if (verdict) {
    verdict.innerHTML = `
      <div class="verdict-box">
        <div class="verdict-header">
          <div class="verdict-icon">!</div>
          <div class="verdict-title">VERDICT: FRAUD INDICATORS</div>
        </div>
        <div class="verdict-text">An independent DL News investigation reveals missing miners, unpaid employees, and breached contracts. Promised $0.05 launch price — actual: $0.0001554.</div>
        <div class="verdict-stat">
          <div class="verdict-stat-num">-99.7%</div>
          <div class="verdict-stat-label">price drop<br>vs promise</div>
        </div>
      </div>
      <div class="price-comparison">
        <div class="price-comparison-header">PROMISE VS REALITY</div>
        <div class="price-row">
          <div class="price-col">
            <div class="price-col-label">Promised price</div>
            <div class="price-col-value">$0.05</div>
          </div>
          <div class="price-arrow">→</div>
          <div class="price-col">
            <div class="price-col-label">Actual price</div>
            <div class="price-col-value">$0.0001554</div>
          </div>
        </div>
        <div class="price-row">
          <div class="price-col">
            <div class="price-col-label">Promised market cap</div>
            <div class="price-col-value">$1,000,000,000</div>
          </div>
          <div class="price-arrow">→</div>
          <div class="price-col">
            <div class="price-col-label">Actual market cap</div>
            <div class="price-col-value">$5,650,000</div>
          </div>
        </div>
      </div>
    `;
  }

  if (grid) {
    const barHeights = [60, 85, 40, 90, 55, 70, 45, 80, 35, 65, 50];
    grid.innerHTML = `
      <div class="investigation-grid-header">
        <span class="investigation-grid-title">DL NEWS FINDINGS — ${INVESTIGATION.findings.length} CONFIRMED</span>
      </div>
      ${INVESTIGATION.findings.map((f, i) => `
        <div class="investigation-card">
          <div class="investigation-num">${i + 1}</div>
          <div>
            <div class="investigation-label">${f.label}</div>
            <div class="investigation-detail">${f.detail}</div>
          </div>
          <div class="investigation-visual">
            ${[barHeights[i] || 50, Math.max(20, (barHeights[i] || 50) - 20), Math.min(95, (barHeights[i] || 50) + 15)].map(h => `<div class="inv-bar" style="height:${h}%"></div>`).join('')}
          </div>
        </div>
      `).join('')}
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

/* Auto-render whatever is on this page */
renderStats();
renderCategories();
renderPromises(urlFilter, urlCategory);
renderTimeline();
renderInvestigation();
renderQuotes();
renderSources();

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
