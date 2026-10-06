(function () {
  'use strict';
  function render() {
    const failures = [];
    document.querySelectorAll('[data-tex]').forEach(element => {
      try {
        katex.render(element.dataset.tex, element, {
          displayMode: element.dataset.display !== 'inline',
          throwOnError: true,
          strict: 'ignore',
          trust: false,
          macros: {
            '\\R': '\\mathcal R', '\\Hh': '\\mathcal H_T',
            '\\LPF': '\\operatorname{LPF}', '\\unwrap': '\\operatorname{unwrap}',
            '\\atan': '\\operatorname{atan2}'
          }
        });
        element.dataset.mathRendered = 'true';
      } catch (error) {
        element.dataset.mathError = 'true';
        failures.push({formula: element.dataset.tex, message: error.message});
      }
    });
    if (failures.length) console.error('Formula rendering failed', failures);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})();
