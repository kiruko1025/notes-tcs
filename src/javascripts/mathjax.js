window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    // Arithmatex marks only math fragments for MathJax processing.
    ignoreHtmlClass: '.*|',
    processHtmlClass: 'arithmatex',
  },
};

function typeset() {
  if (window.MathJax?.typesetPromise) {
    MathJax.startup?.output?.clearCache?.();
    MathJax.typesetClear();
    MathJax.texReset();
    return MathJax.typesetPromise();
  }
}

window.addEventListener('DOMContentLoaded', typeset);
