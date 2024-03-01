// Javascript code for the postfolio designs
window.onscroll = () => {
    // navbar color changes
    let navbar = document.querySelector('nav');
    navbar.classList.toggle('navbar-bg', window.scrollY > 100);
  
  
}

// About section fade in and fade-out code
document.addEventListener("DOMContentLoaded", function () {
  const educationBoxes = document.getElementsByClassName("education-box");
  let currentIndex = 0;

  function toggleClasses() {
    if (currentIndex === 0) {
      // If the current index is 0, show the first element for 3 seconds
      educationBoxes[0].classList.add("show");
      educationBoxes[1].classList.remove("second-show");
    } else {
      // If the current index is 1, show the second element for 3 seconds
      educationBoxes[0].classList.remove("show");
      educationBoxes[1].classList.add("second-show");
    }

    currentIndex = (currentIndex + 1) % educationBoxes.length; 
  }

  setInterval(toggleClasses, 6000); 

  // Mobile navbar background changes
  var navbarToggler = document.querySelector(".navbar-toggler");
  var sidebar = document.querySelector(".sidebar");
  var navbarBrand = document.querySelector(".navbar-brand")

  navbarToggler.addEventListener("click", function () {
    sidebar.classList.toggle("active");
    
    if (sidebar.classList.contains("active")) {
      navbarBrand.style.color = "white";
    } else {
      navbarBrand.style.color = "";
    }
  });


window.addEventListener('load', () => {
  AOS.init({
    duration: 1000,
    easing: 'linear',
    once: true,
    mirror: false
  })
});
 
/**
   * Initiate Pure Counter 
   */
new PureCounter();


// Testimonial Section using swiper
const swiper = new Swiper(".swiperCarousel", {
  slidesPerView: 3,
  centeredSlides: true,
  spaceBetween: 0.1,
  keyboard: {
    enabled: true,
  },
  loop:true,
  pagination: {
    el: ".swiper-pagination",
  },
  // Enabled autoplay mode
  autoplay: {
    delay: 3000,
    disableOnInteraction: false
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const slides = document.getElementsByClassName("swiper-slide");
for (const slide of slides) {
  slide.addEventListener("click", () => {
    const { className } = slide;
    if (className.includes("swiper-slide-next")) {
      swiper.slideNext();
    } else if (className.includes("swiper-slide-prev")) {
      swiper.slidePrev();
    }
  });
}

});

// =============  Dark Mode Icon  ============== //
let darkModeicon = document.querySelector("#darkMode-icon")

darkModeicon.onclick = () => {
  
  darkModeicon.classList.toggle("bi-moon"); 
  darkModeicon.classList.toggle("bi-brightness-high"); 
  document.body.classList.toggle("darkMode");
}


