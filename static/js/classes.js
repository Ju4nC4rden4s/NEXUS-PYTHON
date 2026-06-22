(function () {
    const sessionsData = JSON.parse(document.getElementById('sessions-data').textContent || '{}');
    const classSessionsData = JSON.parse(document.getElementById('available-sessions-by-class-data').textContent || '{}');
    const modal = document.getElementById('reserveModal');
    const modalClassName = document.getElementById('modalClassName');
    const modalSessionSelect = document.getElementById('modalSessionSelect');
    const modalClose = document.getElementById('modalClose');
    const modalCancel = document.getElementById('modalCancel');
    const reserveForm = document.getElementById('reserveForm');
    const detailModal = document.getElementById('classDetailModal');
    const detailModalClose = document.getElementById('detailModalClose');
    const detailClassName = document.getElementById('detailClassName');
    const detailClassBadge = document.getElementById('detailClassBadge');
    const detailDescription = document.getElementById('detailDescription');
    const detailDuration = document.getElementById('detailDuration');
    const detailSessionsList = document.getElementById('detailSessionsList');
    const detailMessage = document.getElementById('detailMessage');
    const reservationCreateUrl = reserveForm ? reserveForm.action : '/reservas/crear/';

    function formatFullDate(value) {
        const date = new Date(value);
        if (isNaN(date.getTime())) {
            return value;
        }
        return new Intl.DateTimeFormat('es-ES', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        }).format(date);
    }

    function formatTime(value) {
        const date = new Date(value);
        if (isNaN(date.getTime())) {
            const match = value.match(/(\d{2}:\d{2})/);
            return match ? match[1] : value;
        }
        return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }

    function getTimeband(value) {
        const date = new Date(value);
        if (isNaN(date.getTime())) {
            const hours = Number(value.slice(11, 13));
            if (Number.isFinite(hours)) {
                return getTimebandFromHour(hours);
            }
            return '';
        }
        return getTimebandFromHour(date.getHours());
    }

    function getTimebandFromHour(hour) {
        if (hour >= 6 && hour < 12) {
            return 'Mañana';
        }
        if (hour >= 12 && hour < 18) {
            return 'Tarde';
        }
        if (hour >= 18 && hour < 24) {
            return 'Noche';
        }
        return 'Noche';
    }

    function getTimebandEmoji(value) {
        const date = new Date(value);
        const hour = isNaN(date.getTime()) ? Number(value.slice(11, 13)) : date.getHours();
        if (hour >= 6 && hour < 12) return '';
        if (hour >= 12 && hour < 18) return '';
        return '🌙';
    }

    function openReserveModal(classId, className) {
        const sessions = sessionsData[classId] || [];
        modalClassName.textContent = className;
        modalSessionSelect.innerHTML = '<option value="">Selecciona una sesión</option>';

        sessions.forEach(function (session) {
            const option = document.createElement('option');
            option.value = session.id;
            option.textContent = session.datetime + ' — ' + session.coach + ' — ' + session.available_spots + ' cupos disponibles';
            modalSessionSelect.appendChild(option);
        });

        modal.classList.add('visible');
        modal.setAttribute('aria-hidden', 'false');
    }

    function closeReserveModal() {
        modal.classList.remove('visible');
        modal.setAttribute('aria-hidden', 'true');
        modalSessionSelect.innerHTML = '<option value="">Selecciona una sesión</option>';
    }

    function openDetailModal(classId, className, description, duration, level, levelDisplay) {
        const sessions = classSessionsData[classId] || [];
        detailClassName.textContent = className;
        detailClassBadge.textContent = levelDisplay;
        detailClassBadge.className = 'badge badge-' + level.toLowerCase();
        detailDescription.textContent = description;
        detailDuration.textContent = duration + ' min';
        detailMessage.textContent = '';
        detailMessage.className = 'detail-message';
        detailSessionsList.innerHTML = '';

        if (sessions.length === 0) {
            const noSessions = document.createElement('p');
            noSessions.className = 'detail-no-sessions';
            noSessions.textContent = 'No hay sesiones disponibles para esta clase.';
            detailSessionsList.appendChild(noSessions);
        } else {
            sessions.forEach(function (session) {
                const card = document.createElement('div');
                card.className = 'session-card';
                const timeband = getTimeband(session.datetime);
                const emoji = getTimebandEmoji(session.datetime);

                card.innerHTML = `
                    <div class="session-card-row session-card-header">
                        <span class="session-card-timeband">${emoji} ${timeband}</span>
                        <span class="session-card-spots">${session.available_spots}/${session.capacity} cupos</span>
                    </div>
                    <div class="session-card-row">
                        <span>${formatFullDate(session.datetime)}</span>
                        <span>${formatTime(session.datetime)}</span>
                    </div>
                    <div class="session-card-row session-card-coach">
                        <span>Coach: ${session.coach}</span>
                    </div>
                    <div class="session-card-footer">
                        <button type="button" class="btn-red btn-detail-reserve" data-session-id="${session.id}">Reservar esta sesión</button>
                    </div>
                `;
                detailSessionsList.appendChild(card);
            });
        }

        detailModal.classList.add('visible');
        detailModal.setAttribute('aria-hidden', 'false');
    }

    function closeDetailModal() {
        detailModal.classList.remove('visible');
        detailModal.setAttribute('aria-hidden', 'true');
        detailSessionsList.innerHTML = '';
        detailMessage.textContent = '';
    }

    function showDetailMessage(success, message) {
        detailMessage.textContent = message;
        detailMessage.className = success ? 'detail-message success' : 'detail-message error';
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function reserveByAjax(sessionId) {
        const csrfToken = getCookie('csrftoken');
        return fetch(reservationCreateUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: 'session=' + encodeURIComponent(sessionId)
        }).then(function (response) {
            return response.json ? response.json() : response.text().then(JSON.parse);
        });
    }

    function renderTimebandBadges() {
        document.querySelectorAll('.timeband-badges').forEach(function (container) {
            const classId = container.dataset.classId;
            const sessions = classSessionsData[classId] || [];
            const badges = new Set();

            sessions.forEach(function (session) {
                const emoji = getTimebandEmoji(session.datetime);
                badges.add(emoji);
            });

            container.innerHTML = '';
            badges.forEach(function (emoji) {
                const span = document.createElement('span');
                span.className = 'timeband-badge';
                span.textContent = emoji;
                container.appendChild(span);
            });
        });
    }

    document.querySelectorAll('.btn-reserve-class').forEach(function (button) {
        button.addEventListener('click', function () {
            openReserveModal(button.dataset.classId, button.dataset.className);
        });
    });

    document.querySelectorAll('.class-detail-toggle').forEach(function (element) {
        element.addEventListener('click', function () {
            openDetailModal(
                element.dataset.classId,
                element.textContent.trim(),
                element.dataset.classDescription,
                element.dataset.classDuration,
                element.dataset.classLevel,
                element.dataset.classLevelDisplay
            );
        });
    });

    document.addEventListener('click', function (event) {
        if (event.target.matches('.btn-detail-reserve')) {
            const sessionId = event.target.dataset.sessionId;
            showDetailMessage(true, 'Reservando sesión...');
            reserveByAjax(sessionId)
                .then(function (data) {
                    if (data.success) {
                        showDetailMessage(true, data.message || 'Reserva creada exitosamente.');
                        setTimeout(function () {
                            window.location.href = '/reservas/';
                        }, 1500);
                    } else {
                        showDetailMessage(false, data.message || 'No se pudo crear la reserva. Intenta de nuevo.');
                    }
                })
                .catch(function () {
                    showDetailMessage(false, 'No se pudo crear la reserva. Intenta de nuevo.');
                });
        }
    });

    modalClose.addEventListener('click', closeReserveModal);
    modalCancel.addEventListener('click', closeReserveModal);
    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeReserveModal();
        }
    });

    detailModalClose.addEventListener('click', closeDetailModal);
    detailModal.addEventListener('click', function (event) {
        if (event.target === detailModal) {
            closeDetailModal();
        }
    });

    renderTimebandBadges();
})();
