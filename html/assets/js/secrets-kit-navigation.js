// Native details menus remain usable without JavaScript. No requests or storage.
(() => {
  const nav = document.querySelector('.seckit-nav');
  const pages = nav?.querySelector('.seckit-nav-pages');
  if (!pages) return;
  const more = nav.querySelector('.seckit-nav-more');
  const wide = window.matchMedia('(min-width: 50rem)');
  function layout() {
    const focused = document.activeElement;
    // Move focus out of content that will be hidden at the new breakpoint.
    if (!wide.matches && pages.contains(document.activeElement)) {
      pages.querySelector('summary').focus();
    }
    pages.open = wide.matches;
    if (more) more.open = false;
    nav.classList.toggle('seckit-nav--wide', wide.matches);
    if (wide.matches && focused === pages.querySelector('summary')) {
      pages.querySelector('.seckit-nav-links > a').focus();
    }
  }
  layout();
  wide.addEventListener('change', layout);
  nav.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const target = more?.open ? more : (!wide.matches && pages.open ? pages : null);
    if (!target) return;
    target.open = false;
    target.querySelector('summary').focus();
    event.preventDefault();
  });
  document.addEventListener('click', event => {
    if (more?.open && !more.contains(event.target)) more.open = false;
  });
})();
