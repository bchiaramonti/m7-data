/* ====================================================================
   SIPOC / DEIP page — sidebar + canvas com fit-to-frame
   Depende de window.P5_DATA (dados-P5-credito.js)
   ==================================================================== */

(function () {
  // ============ SIPOC SIDEBAR ============
  function renderSipocSidebar() {
    const list = document.getElementById('sipoc-sidebar-list');
    if (!list) return;
    const subs = window.P5_DATA.subprocessos;
    const cnt = document.getElementById('sipoc-sb-count');
    if (cnt) cnt.textContent = subs.length;
    list.innerHTML = '';
    subs.forEach(sp => {
      const btn = document.createElement('button');
      btn.className = 'sipoc-sb-item';
      btn.dataset.sipoc = sp.id;
      btn.innerHTML = `
        <div class="ssb-head">
          <span class="ssb-code">${sp.code}</span>
          <span class="ssb-name">${sp.name}</span>
        </div>
        <div class="ssb-purpose">${sp.purpose}</div>
        <div class="ssb-meta">
          <span class="pill">${sp.cadence}</span>
        </div>
      `;
      btn.addEventListener('click', () => selectSubprocess(sp.id));
      list.appendChild(btn);
    });
  }

  // ============ DEIP rendering ============
  function renderDeipInto(targetEl, sp) {
    targetEl.innerHTML = `
      <div class="deip">
        <div class="deip-objective">
          <span class="do-code">${sp.code}</span>
          <div class="do-body">
            <span class="do-label">Objetivo do subprocesso</span>
            <div class="do-name">${sp.name}</div>
            <p class="do-text">${sp.purpose}</p>
          </div>
          <div class="do-owner">
            <strong>${sp.owner}</strong>
            ${sp.cadence}
          </div>
        </div>

        <div class="deip-band regulacao">
          <span class="band-label">Regulação</span>
          <div class="band-items">
            ${sp.regulacao.map(r => `
              <div class="band-item">
                <div class="band-item-label">${r.label}</div>
                <div class="band-circle">${r.code}</div>
                <div class="band-item-detail">${r.detail}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="deip-central">
          <div class="deip-stripe left">Entradas</div>
          <div class="deip-panel left">
            <div class="panel-head"><span class="h-prov">Fornecedor</span><span class="h-mid">#</span><span class="h-art">Insumo</span></div>
            ${sp.inputs.map((i, idx) => `
              <div class="iorow">
                <div><div class="prov">${i.from}</div></div>
                <div class="circle">I${idx+1}</div>
                <div>
                  <div class="artif">${i.what}</div>
                  ${i.detail ? `<div class="artif-detail">${i.detail}</div>` : ''}
                </div>
              </div>
            `).join('')}
          </div>

          <div class="deip-core">
            <div class="macro">
              <div class="macro-label">Macrofluxo</div>
              <div class="macro-code">${sp.code}</div>
              <div class="macro-name">${sp.name}</div>
            </div>
            <div class="etapas">
              <div class="etapas-label">Etapas</div>
              ${sp.etapas.map((e, idx) => `
                <div class="etapa">
                  <span class="etapa-num">${idx+1}</span>
                  <span>${e}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="deip-panel right">
            <div class="panel-head"><span class="h-art">Produto</span><span class="h-mid">#</span><span class="h-prov">Cliente</span></div>
            ${sp.outputs.map((o, idx) => `
              <div class="iorow">
                <div>
                  <div class="artif">${o.what}</div>
                  ${o.detail ? `<div class="artif-detail">${o.detail}</div>` : ''}
                </div>
                <div class="circle">O${idx+1}</div>
                <div><div class="prov">${o.to}</div></div>
              </div>
            `).join('')}
          </div>
          <div class="deip-stripe right">Saídas</div>
        </div>

        <div class="deip-band suporte">
          <span class="band-label">Suporte</span>
          <div class="band-items">
            ${sp.suporte.map(s => `
              <div class="band-item">
                <div class="band-item-label">${s.label}</div>
                <div class="band-circle suporte">${s.code}</div>
                <div class="band-item-detail">${s.detail}</div>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="deip-foot">
          <div class="ff-block"><span class="ff-label">Cadência</span><span class="ff-value">${sp.cadence}</span></div>
          <div class="ff-block"><span class="ff-label">Dono / Time</span><span class="ff-value">${sp.owner}</span></div>
          <div class="ff-block"><span class="ff-label">Sistemas-chave</span><span class="ff-value">${sp.sistemas}</span></div>
          <div class="ff-block"><span class="ff-label">Volume / Mês</span><span class="ff-value">${sp.volume}</span></div>
        </div>
      </div>
    `;
  }

  // ============ SELECT SUBPROCESS ============
  function selectSubprocess(id) {
    const sp = window.P5_DATA.subprocessos.find(s => s.id === id);
    if (!sp) return;

    // Update URL without reload
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('sp', id);
      window.history.replaceState({}, '', url);
    } catch (e) {}

    // Active sidebar item
    document.querySelectorAll('.sipoc-sb-item').forEach(el => {
      el.classList.toggle('active', el.dataset.sipoc === id);
    });

    // Render DEIP
    const wrap = document.getElementById('sipoc-scale-wrap');
    const empty = document.getElementById('sipoc-canvas-empty');
    if (wrap) {
      renderDeipInto(wrap, sp);
      wrap.hidden = false;
    }
    if (empty) empty.style.display = 'none';

    // Fit synchronously + retries (cover layout-settle timing)
    fitSipocCanvas();
    requestAnimationFrame(fitSipocCanvas);
    setTimeout(fitSipocCanvas, 100);
  }

  // ============ FIT-TO-FRAME ============
  function fitSipocCanvas() {
    const frame = document.getElementById('sipoc-canvas-frame');
    const wrap = document.getElementById('sipoc-scale-wrap');
    if (!frame || !wrap || wrap.hidden || !wrap.firstElementChild) return;

    wrap.style.transform = 'translate(-50%, -50%) scale(1)';

    const cs = getComputedStyle(frame);
    const padL = parseFloat(cs.paddingLeft) || 0;
    const padR = parseFloat(cs.paddingRight) || 0;
    const padT = parseFloat(cs.paddingTop) || 0;
    const padB = parseFloat(cs.paddingBottom) || 0;

    const availW = Math.max(0, frame.clientWidth - padL - padR);
    const availH = Math.max(0, frame.clientHeight - padT - padB);

    const naturalW = wrap.scrollWidth || wrap.offsetWidth || 1200;
    const naturalH = wrap.scrollHeight || wrap.offsetHeight || 1;

    if (availW === 0 || availH === 0 || naturalW === 0 || naturalH === 0) return;

    const scale = Math.min(availW / naturalW, availH / naturalH, 1);
    wrap.style.transform = `translate(-50%, -50%) scale(${scale})`;
  }

  // ============ INIT ============
  function init() {
    renderSipocSidebar();

    // ResizeObserver on canvas frame
    const frame = document.getElementById('sipoc-canvas-frame');
    if (frame && window.ResizeObserver) {
      const ro = new ResizeObserver(() => requestAnimationFrame(fitSipocCanvas));
      ro.observe(frame);
    }
    window.addEventListener('resize', () => requestAnimationFrame(fitSipocCanvas));

    // Auto-select from ?sp=... or default to first
    const params = new URLSearchParams(window.location.search);
    const initial = params.get('sp') || (window.P5_DATA.subprocessos[0] && window.P5_DATA.subprocessos[0].id);
    if (initial) selectSubprocess(initial);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
