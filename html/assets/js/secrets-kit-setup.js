// Copy the visible setup prompt; preserve keyboard copying if clipboard access fails.
(() => {
  const button = document.querySelector('[data-seckit-copy]');
  if (!button) return;
  const prompt = document.getElementById(button.dataset.seckitCopy);
  const status = document.getElementById('seckit-copy-status');
  if (!prompt || !status) return;

  button.hidden = false;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(prompt.value);
      status.textContent = 'Setup prompt copied.';
    } catch {
      prompt.focus();
      prompt.select();
      status.textContent = 'Prompt selected. Press Command+C or Ctrl+C to copy.';
    }
  });
})();
