(() => {
  const menuButton = document.querySelector('[data-mobile-menu]');
  const sidebar = document.querySelector('[data-sidebar]');
  if (menuButton && sidebar) {
    menuButton.addEventListener('click', () => {
      const open = sidebar.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
    });
  }

  const search = document.querySelector('[data-doc-search]');
  const results = document.querySelector('[data-search-results]');
  if (search && results && Array.isArray(window.ADLAC_SEARCH_INDEX)) {
    const render = () => {
      const q = search.value.trim().toLowerCase();
      if (q.length < 2) {
        results.classList.remove('is-open');
        results.innerHTML = '';
        return;
      }
      const matches = window.ADLAC_SEARCH_INDEX
        .filter(item => (item.title + ' ' + item.summary + ' ' + item.keywords).toLowerCase().includes(q))
        .sort((a, b) => Number(b.title.toLowerCase().includes(q)) - Number(a.title.toLowerCase().includes(q)))
        .slice(0, 8);
      results.innerHTML = matches.length
        ? matches.map(x => {
            // Search-index links are relative to /adlac/, not to the current page.
            // Preserve root-relative links such as /privacy/.
            const href = x.href.startsWith('/') ? x.href : `/adlac/${x.href.replace(/^(\.\/)+/, '')}`;
            return `<a href="${href}"><strong>${x.title}</strong><br><span class="small">${x.summary}</span></a>`;
          }).join('')
        : '<div class="small" style="padding:10px">No documentation pages matched your search.</div>';
      results.classList.add('is-open');
    };
    search.addEventListener('input', render);
    search.addEventListener('focus', render);
    document.addEventListener('click', e => {
      if (!e.target.closest('.search-box')) results.classList.remove('is-open');
    });
  }
})();