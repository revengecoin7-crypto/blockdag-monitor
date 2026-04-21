const STATUS_LABEL = {
  broken: '❌ Broken',
  kept: '✅ Kept',
  pending: '⏳ Pending',
  misleading: '⚠️ Misleading'
};

const STATUS_BADGE = {
  broken: 'badge-broken',
  kept: 'badge-kept',
  pending: 'badge-pending',
  misleading: 'badge-misleading'
};

function renderPromises(filter) {
  const grid = document.getElementById('promise-grid');
  const items = filter === 'all' ? PROMISES : PROMISES.filter(p => p.status === filter);

  grid.innerHTML = items.map(p => `
    <div class="promise-card status-${p.status}">
      <div class="promise-top">
        <div class="promise-title">${p.title}</div>
        <div class="promise-badges">
          <span class="badge badge-cat">${p.category}</span>
          <span class="badge ${STATUS_BADGE[p.status]}">${STATUS_LABEL[p.status]}</span>
        </div>
      </div>
      <div class="promise-meta">
        <div class="meta-item">
          <span class="meta-label">Promised</span>
          <span class="meta-value">${p.promised}</span>
        </div>
      </div>
      <div class="promise-reality">${p.reality}</div>
      <button class="quotes-toggle" onclick="toggleQuotes(this)">
        📋 Show ${p.quotes.length} source quote${p.quotes.length > 1 ? 's' : ''}
      </button>
      <div class="promise-quotes">
        ${p.quotes.map(q => `
          <div class="quote-item">
            <div class="quote-date">📅 ${q.date} — Official BlockDAG Network</div>
            <div class="quote-text">"${q.text}"</div>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
}

function toggleQuotes(btn) {
  const container = btn.nextElementSibling;
  const isOpen = container.classList.contains('open');
  container.classList.toggle('open', !isOpen);
  const count = btn.textContent.match(/\d+/)[0];
  btn.textContent = isOpen
    ? `📋 Show ${count} source quote${count > 1 ? 's' : ''}`
    : `📋 Hide ${count} source quote${count > 1 ? 's' : ''}`;
}

function renderTimeline() {
  const list = document.getElementById('timeline-list');
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
  grid.innerHTML = NOTABLE_QUOTES.map(q => `
    <div class="notable-quote">
      <div class="notable-quote-header">
        <span class="notable-quote-date">${q.date}</span>
        <span class="notable-quote-tag tag-${q.tag}">${q.tag.toUpperCase()}</span>
      </div>
      <div class="notable-quote-text">"${q.text}"</div>
    </div>
  `).join('');
}

function updateStats() {
  const broken = PROMISES.filter(p => p.status === 'broken').length;
  const kept = PROMISES.filter(p => p.status === 'kept').length;
  const pending = PROMISES.filter(p => p.status === 'pending').length;
  const misleading = PROMISES.filter(p => p.status === 'misleading').length;
  const total = PROMISES.length;

  document.getElementById('stat-total').textContent = total;
  document.getElementById('stat-kept').textContent = kept;
  document.getElementById('stat-broken').textContent = broken + misleading;
  document.getElementById('stat-pending').textContent = pending;
  const rate = Math.round((kept / total) * 100);
  document.getElementById('stat-percent').textContent = rate + '%';
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderPromises(btn.dataset.filter);
  });
});

renderPromises('all');
renderTimeline();
renderQuotes();
updateStats();
