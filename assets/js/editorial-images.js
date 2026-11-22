(() => {
  'use strict';
  const fallback = document.currentScript.dataset.archivePlaceholder;
  function recover(image) {
    if (!(image instanceof HTMLImageElement)) return;
    if (image.hasAttribute('data-cover-image')) {
      image.hidden = true;
      return;
    }
    if (image.closest('.article-post') && image.getAttribute('src') && !image.dataset.archiveFallback) {
      image.dataset.archiveFallback = 'true';
      image.removeAttribute('srcset');
      if (!image.hasAttribute('alt')) image.alt = 'Archive image unavailable';
      image.src = fallback;
    }
  }
  document.addEventListener('error', event => recover(event.target), true);
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img[data-cover-image], .article-post img').forEach(image => {
      if (image.complete && !image.naturalWidth) recover(image);
    });
  }, {once: true});
})();
