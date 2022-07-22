const thumbnails = document.querySelector('.thumbnail-container').children;
const carousel = document.querySelector('#mainCarousel');
const modal = document.querySelector('#modalImg');

function setModal(e) {
    if (modal.src !== e.src) {
        modal.src = e.src;
    }
}

function activateImg(e) {
    [...thumbnails].forEach(t => t.classList.remove("active"));
    e.classList.toggle("active");
}

carousel.addEventListener('slide.bs.carousel', event => {
    [...thumbnails].forEach((t, i) => {
        if (i === event.to) {
            t.classList.toggle("active");
        } else {
            t.classList.remove("active");
        }
    });
});