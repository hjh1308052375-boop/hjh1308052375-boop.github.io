(function () {
  'use strict';
  const filter = document.getElementById('route-filter');
  if (!filter) return;
  const sections = ['components', 'routes', 'conventions'];
  const buttons = Array.from(document.querySelectorAll('[data-view]'));
  const status = document.getElementById('atlas-status');
  let view = 'routes';
  function render() {
    const selected = filter.value;
    sections.forEach(name => { document.getElementById('view-' + name).hidden = name !== view; });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.view === view)));
    document.querySelectorAll('.atlas-route').forEach(route => { route.hidden = selected !== 'all' && route.dataset.route !== selected; });
    let componentCount = 0;
    document.querySelectorAll('.component').forEach(component => {
      const show = selected === 'all' || component.dataset.routes.split(' ').includes(selected);
      component.hidden = !show;
      if (show) componentCount++;
    });
    const routeCount = Array.from(document.querySelectorAll('.atlas-route')).filter(route => !route.hidden).length;
    const en = document.documentElement.lang === 'en';
    status.textContent = en ? `${routeCount} ${routeCount === 1 ? 'route' : 'routes'} · ${componentCount} components` : `${routeCount} 条路线 · ${componentCount} 项元件`;
  }
  filter.addEventListener('change', render);
  buttons.forEach(button => button.addEventListener('click', () => { view = button.dataset.view; render(); }));
  new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  const routeId = location.hash.slice(1);
  if (Array.from(filter.options).some(option => option.value === routeId)) filter.value = routeId;
  const dialog = document.getElementById('atlas-zoom');
  const zoomImage = document.getElementById('zoom-image');
  let originalImage = null;
  document.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
    originalImage = button.querySelector('img');
    zoomImage.src = button.dataset.zoom;
    zoomImage.alt = originalImage.alt;
    document.getElementById('zoom-caption').textContent = originalImage.alt;
    dialog.showModal();
  }));
  document.getElementById('zoom-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => { originalImage = null; zoomImage.removeAttribute('src'); });
  render();
})();
