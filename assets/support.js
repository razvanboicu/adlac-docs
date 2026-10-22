(() => {
  const form = document.querySelector('[data-support-form]');
  if (!form || form.dataset.initialized === 'true') return;
  form.dataset.initialized = 'true';

  const submit = form.querySelector('[data-support-submit]');
  const status = form.querySelector('[data-support-status]');
  const fileInput = form.querySelector('input[type="file"]');
  const maxFileBytes = 5 * 1024 * 1024;

  const setStatus = (message, type = '') => {
    status.textContent = message;
    status.classList.toggle('is-success', type === 'success');
    status.classList.toggle('is-error', type === 'error');
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setStatus('');

    if (!form.reportValidity()) return;

    const file = fileInput?.files?.[0];
    if (file && file.size > maxFileBytes) {
      setStatus('The attachment is larger than 5 MB. Please choose a smaller file.', 'error');
      fileInput.focus();
      return;
    }

    const endpoint = form.dataset.endpoint;
    if (!endpoint) {
      setStatus('Support is temporarily unavailable. Please try again later.', 'error');
      return;
    }

    submit.disabled = true;
    submit.setAttribute('aria-busy', 'true');
    const originalLabel = submit.textContent;
    submit.textContent = 'Submitting…';

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: new FormData(form),
        headers: {
          'Accept': 'application/json'
        }
      });

      let payload = {};
      try {
        payload = await response.json();
      } catch (_) {}

      if (!response.ok) {
        throw new Error(payload.error || 'Unable to submit your support request.');
      }

      const ticket = payload.ticket_id ? ` Ticket ${payload.ticket_id}.` : '';
      setStatus(`Your request was received.${ticket} A confirmation email has been sent to you.`, 'success');
      form.reset();
      const theme = form.querySelector('[name="theme_name"]');
      if (theme) theme.value = 'ADLAC';
    } catch (error) {
      setStatus(error?.message || 'Unable to submit your support request. Please try again.', 'error');
    } finally {
      submit.disabled = false;
      submit.removeAttribute('aria-busy');
      submit.textContent = originalLabel;
    }
  });
})();