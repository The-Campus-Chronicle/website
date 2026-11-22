(() => {
  'use strict';
  const fallback = document.currentScript.dataset.archivePlaceholder;
  function recover(image) {
    if (!(image instanceof HTMLImageElement)) return;
    if (image.hasAttribute('data-article-cover')) {
      const cover = image.closest('.classic-post-cover');
      if (cover) {
        cover.hidden = true;
        cover.closest('.classic-post-header')?.classList.add('classic-post-header--no-cover');
      }
      return;
    }
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
    document.querySelectorAll('img[data-cover-image], img[data-article-cover], .article-post img').forEach(image => {
      if (image.complete && !image.naturalWidth) recover(image);
    });
  }, {once: true});
})();
