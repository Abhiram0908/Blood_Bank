$(document).ready(function() {
    if ($(window).width() <= 767) {
      // Initialize Slick Carousel for mobile devices
      $('.image-gallery').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        dots: true,
        swipe: true
      });
    }
  });
  