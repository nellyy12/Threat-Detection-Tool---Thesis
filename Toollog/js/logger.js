(function () {
  const sessionId =
    sessionStorage.getItem('session_id') || `${Date.now()}${Math.random().toString(36).substr(2)}`;
  sessionStorage.setItem('session_id', sessionId);

  const sessionData = {
    session_id: sessionId,
    user_id: localStorage.getItem('user_id') || 'guest',
    browser: navigator.userAgent.match(/(Chrome|Firefox|Safari|Edge)/)[0],
    os: navigator.platform,
    device_type: /Mobi|Android/i.test(navigator.userAgent) ? 'Mobile' : 'Desktop',
    ip_address: '',
    login_time: new Date().toISOString(),
    pages_visited: [],
    click_count: 0,
    repeated_failed_logins: 0,
    vpn_detected: false,
    transactions_initiated: 0,
    beneficiaries_added: 0,
    input_logs: [],
  };

  let lastPage = null;

  function trackPageVisit() {
    const currentPath = window.location.pathname;
    if (lastPage !== currentPath) {
      sessionData.pages_visited.push(currentPath);
      lastPage = currentPath;
    }
  }

  document.addEventListener('click', () => {
    sessionData.click_count += 1;
  });

  // Merge input logs (overwrite same input from same page)
  window.addEventListener('input-logged', (e) => {
    const newEntries = e.detail;
    newEntries.forEach((newEntry) => {
      const existingIndex = sessionData.input_logs.findIndex(
        (log) => log.name === newEntry.name && log.page === newEntry.page,
      );
      if (existingIndex === -1) {
        sessionData.input_logs.push(newEntry);
      } else {
        sessionData.input_logs[existingIndex] = newEntry;
      }
    });
  });

  trackPageVisit();

  window.addEventListener('beforeunload', () => {
    sessionData.logout_time = new Date().toISOString();
    sessionData.session_duration = Math.floor(
      (new Date(sessionData.logout_time) - new Date(sessionData.login_time)) / 1000,
    );
    console.log('Sending final session data:', sessionData);
    sendLog(sessionData);
  });

  function sendLog(data) {
    fetch('/save-log.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  }
})();
