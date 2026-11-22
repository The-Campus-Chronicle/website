(() => {
  'use strict';
  const menu = document.querySelector('.chronicle-menu-button');
  if (!menu) return;
  const panel = document.getElementById(menu.getAttribute('aria-controls'));
  if (!panel) return;
  document.documentElement.classList.add('nav-enhanced');
  function close() {
    menu.setAttribute('aria-expanded', 'false');
    panel.classList.remove('chronicle-menu-open');
  }
  menu.addEventListener('click', () => {
    if (menu.getAttribute('aria-expanded') === 'true') close();
    else {
      menu.setAttribute('aria-expanded', 'true');
      panel.classList.add('chronicle-menu-open');
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      close();
      menu.focus();
    }
  });
})();
