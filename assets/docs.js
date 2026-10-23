(() => {
  // Mobile navigation is a viewport-fixed drawer. Previously the sidebar was
  // displayed in the page flow, so opening it after scrolling looked broken.
  const menuButton = document.querySelector('[data-mobile-menu]');
  const sidebar = document.querySelector('[data-sidebar]');
  if (menuButton && sidebar) {
    const mobileQuery = window.matchMedia('(max-width: 920px)');
    const initialLabel = menuButton.textContent.trim() || 'Menu';
    const sidebarId = sidebar.id || 'docs-mobile-navigation';
    sidebar.id = sidebarId;
    menuButton.setAttribute('aria-controls', sidebarId);
    menuButton.setAttribute('aria-haspopup', 'true');

    const backdrop = document.createElement('div');
    backdrop.className = 'docs-nav-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.appendChild(backdrop);

    const syncTopbarHeight = () => {
      const topbar = document.querySelector('.topbar');
      const height = topbar ? Math.ceil(topbar.getBoundingClientRect().height) : 64;
      document.documentElement.style.setProperty('--docs-mobile-nav-top', `${height}px`);
    };

    const isOpen = () => sidebar.classList.contains('is-open');
    const setOpen = (open, restoreFocus = false) => {
      const shouldOpen = Boolean(open && mobileQuery.matches);
      sidebar.classList.toggle('is-open', shouldOpen);
      document.body.classList.toggle('docs-nav-open', shouldOpen);
      backdrop.classList.toggle('is-visible', shouldOpen);
      menuButton.setAttribute('aria-expanded', String(shouldOpen));
      menuButton.textContent = shouldOpen ? 'Close' : initialLabel;
      // Keep the hidden navigation out of the tab order on mobile.
      sidebar.inert = mobileQuery.matches && !shouldOpen;
      if (shouldOpen) {
        syncTopbarHeight();
        sidebar.setAttribute('tabindex', '-1');
        sidebar.focus({ preventScroll: true });
      } else if (restoreFocus && mobileQuery.matches) {
        menuButton.focus({ preventScroll: true });
      }
    };

    menuButton.addEventListener('click', () => setOpen(!isOpen(), isOpen()));
    backdrop.addEventListener('click', () => setOpen(false, true));
    sidebar.addEventListener('click', event => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', event => {
      if (!isOpen()) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        setOpen(false, true);
      }
      if (event.key === 'Tab') {
        // Trap keyboard focus within the open drawer and its close button.
        const tabbable = [menuButton, ...sidebar.querySelectorAll('a[href], button:not([disabled]), summary, input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])')]
          .filter(el => el.getClientRects().length > 0);
        if (!tabbable.length) return;
        const first = tabbable[0];
        const last = tabbable[tabbable.length - 1];
        const activeIndex = tabbable.indexOf(document.activeElement);
        if (event.shiftKey && (document.activeElement === first || activeIndex < 0)) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && (document.activeElement === last || activeIndex < 0)) {
          event.preventDefault();
          first.focus();
        }
      }
    });

    const syncBreakpoint = () => {
      syncTopbarHeight();
      if (!mobileQuery.matches) setOpen(false);
      else sidebar.inert = !isOpen();
    };
    mobileQuery.addEventListener('change', syncBreakpoint);
    window.addEventListener('resize', syncTopbarHeight, { passive: true });
    syncBreakpoint();
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
