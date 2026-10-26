// Filter the already-rendered research catalog; all entries remain usable without JS.
(() => {
  const controls = document.querySelector('[data-landscape-controls]');
  if (!controls) return;
  const query = controls.querySelector('input');
  const category = controls.querySelector('select');
  const count = document.getElementById('seckit-landscape-count');
  const entries = [...document.querySelectorAll('[data-competitor]')].map(element => ({
    element,
    text: element.textContent.toLocaleLowerCase(),
    category: element.dataset.category,
  }));
  const groups = [...document.querySelectorAll('[data-landscape-group]')];
  const empty = document.querySelector('[data-landscape-empty]');
  function filter() {
    const terms = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    entries.forEach(entry => {
      const matches = (!category.value || category.value === entry.category) && terms.every(term => entry.text.includes(term));
      entry.element.hidden = !matches;
      if (matches) visible += 1;
    });
    groups.forEach(group => { group.hidden = !group.querySelector('[data-competitor]:not([hidden])'); });
    count.textContent = `${visible} of ${entries.length} entries`;
    empty.hidden = visible !== 0;
  }
  controls.hidden = false;
  query.addEventListener('input', filter);
  category.addEventListener('change', filter);
  filter();
})();
