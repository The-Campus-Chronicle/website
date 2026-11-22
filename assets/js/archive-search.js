(() => {
  'use strict';
  const archive = document.querySelector('[data-search-index]');
  if (!archive) return;
  const status = archive.querySelector('#archive-search-status');
  const results = archive.querySelector('.archive-search-results');
  const query = new URLSearchParams(window.location.search);
  const input = archive.querySelector('#archive-query');
  const section = archive.querySelector('#archive-section');
  input.value = (query.get('q') || '').slice(0, 120).trim();
  section.value = query.get('section') || '';
  if (section.selectedIndex === -1) section.value = '';
  const normalize = text => String(text || '').normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  const terms = [...new Set(normalize(input.value).match(/[\p{L}\p{N}]+/gu) || [])].slice(0, 16);
  if (!terms.length && !section.value) {
    status.textContent = input.value ? 'Try a word or a writer’s name.' : 'Enter a keyword or choose a section to start.';
    return;
  }
  status.textContent = 'Searching the archive…';
  fetch(archive.dataset.searchIndex)
    .then(response => {
      if (!response.ok) throw new Error('Archive unavailable');
      return response.json();
    })
    .then(stories => {
      const ranked = stories
        .filter(story => !section.value || story.sections.includes(section.value))
        .map(story => {
          const fields = [story.title, story.authors, story.sections.join(' '), story.tags.join(' '), story.excerpt, story.text].map(normalize);
          const weights = [12, 8, 5, 4, 2, 1];
          let score = 0;
          for (const term of terms) {
            const credit = fields.reduce((sum, text, index) => sum + (text.includes(term) ? weights[index] : 0), 0);
            if (!credit) return null;
            score += credit;
          }
          if (terms.length > 1 && fields[0].includes(terms.join(' '))) score += 16;
          return {story, score};
        })
        .filter(Boolean)
        .sort((a, b) => b.score - a.score || b.story.date.localeCompare(a.story.date));
      const total = ranked.length;
      status.textContent = total ? `${total} ${total === 1 ? 'story' : 'stories'} found${total > 40 ? ' · showing the first 40' : ''}.` : 'No stories matched. Try another keyword or choose All sections.';
      for (const {story} of ranked.slice(0, 40)) {
        const href = new URL(story.url, window.location.origin);
        if (href.origin !== window.location.origin || !/^https?:$/.test(href.protocol)) continue;
        const entry = document.createElement('li');
        const heading = document.createElement('h2');
        const link = document.createElement('a');
        const meta = document.createElement('p');
        const excerpt = document.createElement('p');
        link.href = href.href;
        link.textContent = story.title;
        heading.append(link);
        meta.className = 'story-meta';
        meta.textContent = [...story.sections, story.authors, story.date].filter(Boolean).join(' · ');
        excerpt.textContent = story.excerpt;
        entry.append(heading, meta, excerpt);
        results.append(entry);
      }
    })
    .catch(() => {
      status.textContent = 'Search is temporarily unavailable. Browse by section below or try again later.';
    });
})();
