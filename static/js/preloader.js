function hidePreloader() {
    const preloader = document.getElementById("preloader")
    preloader.style.opacity = "0"
    setTimeout(() => {
        preloader.style.display = "none"
    }, 800)
}

window.addEventListener("DOMContentLoaded", hidePreloader)
