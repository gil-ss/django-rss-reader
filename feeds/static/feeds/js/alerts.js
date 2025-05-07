document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll('.alert.auto-dismiss');

  alerts.forEach(alert => {
    setTimeout(() => {
      alert.classList.add("fade-out");
    }, 500);  // wait before fading

    alert.addEventListener("transitionend", () => {
      alert.remove();
    });
  });
});
