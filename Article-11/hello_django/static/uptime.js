window.setInterval(function () {
    fetch(helloDjango.urls.apiMonitorList, {method: 'GET', credentials: 'include'})
        .then(function (response) {
            return response.json();
        })
        .then(function (monitors) {
            monitors.forEach(function (monitor) {
                var el = document.getElementById('monitor-' + monitor.id);
                var statusEl = el.getElementsByClassName('status')[0];
                statusEl.className = 'status status-' + monitor.status;
                statusEl.innerHTML = monitor.status_display;

                var checkedAtEl = el.getElementsByClassName('checked-at')[0];
                checkedAtEl.innerHTML = monitor.checked_at_formatted;
            });
        });
}, 1000 * 60);
