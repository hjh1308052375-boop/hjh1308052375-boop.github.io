(function () {
  'use strict';
  const buttons = { zh: document.getElementById('zh'), en: document.getElementById('en') };
  const root = document.documentElement;
  function setLanguage(language) {
    const lang = ['zh', 'en'].includes(language) ? language : 'zh';
    root.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-zh][data-en]').forEach(element => {
      element.textContent = element.dataset[lang];
    });
    document.querySelectorAll('[data-lang]').forEach(element => {
      element.hidden = element.dataset.lang !== lang;
    });
    document.querySelectorAll('[data-alt-zh][data-alt-en]').forEach(element => {
      element.alt = element.dataset[lang === 'zh' ? 'altZh' : 'altEn'];
    });
    Object.entries(buttons).forEach(([key, button]) => {
      if (button) button.setAttribute('aria-pressed', String(key === lang));
    });
    document.title = root.dataset[lang === 'zh' ? 'titleZh' : 'titleEn'] ||
      (lang === 'zh' ? '胡俊昊 · Junhao Hu | 学术主页' : 'Junhao Hu | Geophysics & Distributed Fiber-Optic Sensing');
    const diagramTitle = document.getElementById('diagram-title');
    if (diagramTitle) diagramTitle.textContent = lang === 'zh'
      ? '井筒概念剖面：固井、水力压裂与生产剖面监测'
      : 'Conceptual wellbore cross section: cementing, hydraulic fracturing and production monitoring';
    try { localStorage.setItem('junhao-language', lang); } catch (_) { /* Private browsing can deny storage. */ }
    // Keep a shared ?lang= link consistent with subsequent language choices.
    const url = new URL(window.location.href);
    if (url.searchParams.has('lang')) {
      url.searchParams.set('lang', lang);
      try { history.replaceState(null, '', url); } catch (_) { /* Local-file previews may restrict history. */ }
    }
  }
  Object.entries(buttons).forEach(([language, button]) => {
    if (button) button.addEventListener('click', () => setLanguage(language));
  });
  let initial = 'zh';
  try { initial = localStorage.getItem('junhao-language') || initial; } catch (_) { /* Use default. */ }
  const requested = new URLSearchParams(window.location.search).get('lang');
  if (['zh', 'en'].includes(requested)) initial = requested;
  setLanguage(initial);
  // Back/Forward may restore an older page from the browser's page cache.
  window.addEventListener('pageshow', event => {
    if (!event.persisted) return;
    let saved = document.documentElement.lang === 'en' ? 'en' : 'zh';
    try { saved = localStorage.getItem('junhao-language') || saved; } catch (_) {}
    const explicit = new URLSearchParams(window.location.search).get('lang');
    setLanguage(['zh', 'en'].includes(explicit) ? explicit : saved);
  });
})();
