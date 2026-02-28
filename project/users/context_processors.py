def unread_notifications(request):
    """Добавляет количество непрочитанных уведомлений в контекст"""
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
