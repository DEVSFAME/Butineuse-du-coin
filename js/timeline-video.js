document.addEventListener("DOMContentLoaded", function() {
  const videos = document.querySelectorAll("video");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.play();
      } else {
        entry.target.pause();
      }
    });
  }, {
    threshold: 0.5 // Déclenche l'observer lorsque 50% de la vidéo est visible
  });

  videos.forEach(video => {
    observer.observe(video);
  });
});
