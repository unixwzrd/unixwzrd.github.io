// Optional staff-time arithmetic. No requests, persistence, or incident-risk model.
(() => {
  const planner = document.querySelector('[data-seckit-cost-planner]');
  if (!planner) return;
  const inputs = [...planner.querySelectorAll('input')];
  const result = document.getElementById('seckit-cost-result');
  if (inputs.length !== 3 || !result) return;
  const currency = new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD', minimumFractionDigits: 0, maximumFractionDigits: 2,
  });
  function calculate() {
    const values = inputs.map(input => input.valueAsNumber);
    if (inputs.some(input => !input.validity.valid) || values.some(value => !Number.isFinite(value))) {
      result.textContent = 'Enter valid values in all three fields.';
      return;
    }
    result.textContent = currency.format(values.reduce((total, value) => total * value, 1));
  }
  planner.hidden = false;
  const example = document.querySelector('[data-seckit-cost-example]');
  if (example) example.hidden = true;
  planner.addEventListener('input', calculate);
  calculate();
})();
