(function ($) {
	"use strict";
	/*smart header fixed*/
	var fixedHeader = function () {
		var lastScrollTop = 0;
		$(window).on("scroll", function () {
			var st = $(this).scrollTop();
			if (st > 500) {
				if (st < lastScrollTop) {
					$("body").addClass("header-fixed");
					$(".main-header").addClass("fixed");
					$(".main-header").removeClass("relative");
				} else {
					$("body").removeClass("header-fixed");
					$(".main-header").removeClass("fixed");
					$(".main-header").addClass("relative");
				}
			} else {
				$("body").removeClass("header-fixed");
				$(".main-header").removeClass("fixed");
				$(".main-header").addClass("relative");
			}
			lastScrollTop = st;
		});
	};
	$(".has-children").on("click", function (event) {
		$(this).find(".sub-menu").toggleClass("visible");
		$(".has-children").not(this).find(".sub-menu").removeClass("visible");
	});
	/*Search box*/
	$(".search-icon").on("click", function (event) {
		event.stopPropagation(); // Prevents the event from bubbling up the DOM tree
		$(".search-box-content").toggleClass("open");
	});
	$(document).on("click", function (event) {
		if (
			!$(event.target).closest(".search-box-content").length &&
			!$(event.target).closest(".search-icon").length
		) {
			$(".search-box-content").removeClass("open");
		}
	});
	/*Mobile Menu*/
	// Burger menus
	document.addEventListener("DOMContentLoaded", function () {
		// open
		const burger = document.querySelectorAll(".navbar-burger");
		const menu = document.querySelectorAll(".navbar-menu");
		if (burger.length && menu.length) {
			for (var i = 0; i < burger.length; i++) {
				burger[i].addEventListener("click", function () {
					for (var j = 0; j < menu.length; j++) {
						menu[j].classList.toggle("hidden");
					}
				});
			}
		}
		// close
		const close = document.querySelectorAll(".navbar-close");
		const backdrop = document.querySelectorAll(".navbar-backdrop");
		if (close.length) {
			for (var i = 0; i < close.length; i++) {
				close[i].addEventListener("click", function () {
					for (var j = 0; j < menu.length; j++) {
						menu[j].classList.toggle("hidden");
					}
				});
			}
		}
		if (backdrop.length) {
			for (var i = 0; i < backdrop.length; i++) {
				backdrop[i].addEventListener("click", function () {
					for (var j = 0; j < menu.length; j++) {
						menu[j].classList.toggle("hidden");
					}
				});
			}
		}
	});
	/*=============================================
		=          SWIPPER SLIDER             =
	=============================================*/
	var slider = new Swiper(".post-slider-1", {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		centeredSlides: true,
		pagination: {
			el: ".swiper-pagination",
		},
		autoplay: {
			delay: 3000,
		},
		breakpoints: {
			1800: {
				slidesPerView: 1,
			},
			1200: {
				slidesPerView: 1,
			},
			992: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
	});
	var slider = new Swiper(".post-slider-4", {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 3000,
		},
		centeredSlides: true,
		breakpoints: {
			1200: {
				slidesPerView: 4,
			},
			992: {
				slidesPerView: 4,
			},
			768: {
				slidesPerView: 2,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
	});
	var slider = new Swiper(".post-slider-6", {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		autoplay: {
			delay: 3000,
		},
		centeredSlides: true,
		breakpoints: {
			1200: {
				slidesPerView: 6,
			},
			992: {
				slidesPerView: 4,
			},
			768: {
				slidesPerView: 2,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
	});
	// Scroll up to top
	var scrollToTop = function () {
		$.scrollUp({
			scrollName: "scrollUp", // Element ID
			topDistance: "300", // Distance from top before showing element (px)
			topSpeed: 300, // Speed back to top (ms)
			animation: "fade", // Fade, slide, none
			animationInSpeed: 200, // Animation in speed (ms)
			animationOutSpeed: 200, // Animation out speed (ms)
			scrollText: "<span></span>", // Text for element
			activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
		});
	};
	var languageSwitch = function () {
		$(".language").click(function () {
			$(this).toggleClass("is-open");
		});
		$(".language__el").click(function () {
			$(".language__el").removeClass("is-active");
			$(this).toggleClass("is-active");
		});
		$(document).click(function (event) {
			if (!$(event.target).closest(".language").length) {
				$(".language").removeClass("is-open");
			}
		});
	};
	$(document).ready(function () {
		fixedHeader();
		scrollToTop();
		languageSwitch();
	});
})(jQuery);
