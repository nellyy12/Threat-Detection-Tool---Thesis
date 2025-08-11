(function () {
  const page = window.location.pathname;

  function shouldLogInput(input) {
    const value = input.value.trim();
    if (!value) return false;
    if (input.tagName === 'SELECT' && input.selectedIndex === 0) return false;
    return true;
  }

  function collectInputs(form) {
    const timestamp = new Date().toISOString();
    const logs = [];

    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach((input) => {
      if (!shouldLogInput(input)) return;

      const name = input.name || input.id || 'unnamed_input';
      const value = input.value.trim();

      logs.push({ name, value, page, timestamp });
    });

    return logs;
  }

  function handleSubmitOnce(e) {
    const form = e.target;

    if (form.__loggedAlready) return; // block multiple logs
    form.__loggedAlready = true;

    const logs = collectInputs(form);
    if (logs.length > 0) {
      window.dispatchEvent(new CustomEvent('input-logged', { detail: logs }));
    }

    // Reset after a short delay
    setTimeout(() => {
      form.__loggedAlready = false;
    }, 1500);
  }

  function bindAllForms() {
    document.querySelectorAll('form').forEach((form) => {
      if (!form.__logBindDone) {
        form.addEventListener('submit', handleSubmitOnce);
        form.__logBindDone = true;
      }
    });
  }

  window.addEventListener('DOMContentLoaded', bindAllForms);
})();
