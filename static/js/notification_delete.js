document.addEventListener('DOMContentLoaded', notification_delete_onclick);
function notification_delete_onclick() {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
        });
    });
}