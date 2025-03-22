from django import template

register = template.Library()

@register.simple_tag
def render_calendar():
    return """
    <link href="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.css" rel="stylesheet" />
    <div id="calendar"></div>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.1/moment.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            fetch('/api/events/')
            .then(response => response.json())
            .then(data => {
                var calendarEl = document.getElementById('calendar');
                var calendar = new FullCalendar.Calendar(calendarEl, {
                    initialView: 'dayGridMonth',
                    events: data,
                });
                calendar.render();
            });
        });
    </script>
    """
