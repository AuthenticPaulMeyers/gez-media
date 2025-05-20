// TYping animation
const dynamicText = document.querySelector(".text");
const words = ["Tools.", "Skills.", "Ideas."];

// Variables to track the position and deletion status of the word
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typeEffect = () => {
    const currentWord = words[wordIndex];
    const currentChar = currentWord.substring(0, charIndex);
    dynamicText.textContent = currentChar;
    dynamicText.classList.add("stop-blinking");

    if (!isDeleting && charIndex < currentWord.length) {
        // If condition is true, type the next character
        charIndex++;
        setTimeout(typeEffect, 200);
    } else if (isDeleting && charIndex > 0) {
        // If condition is true, remove the previous character
        charIndex--;
        setTimeout(typeEffect, 100);
    } else {
        // If word is deleted then switch to the next word
        isDeleting = !isDeleting;
        dynamicText.classList.remove("stop-blinking");
        wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
        setTimeout(typeEffect, 1200);
    }
}

typeEffect();


// Scroll animations

// custom scroll reveal animation

const scr = ScrollReveal({
    distance : '65px',
    duration : 2600,
    delay :450,
    reset : true

});

// Animation on DOM Reload

document.addEventListener('DOMContentLoaded', ()=>{
    scr.reveal('.hero-title', {delay:200, origin:'bottom'});

})

// Hero section
// scr.reveal('.hero-title', {delay:200, origin:'bottom'});
scr.reveal('.left-section', {delay:100, origin:'bottom'});
scr.reveal('.hero-section', {delay:80, origin:'bottom'});
// scr.reveal('.animate', {delay:100, origin:'bottom'});

// about section
// scr.reveal('.image-container', {delay:200, origin:'bottom'});
// scr.reveal('.about-left-section', {delay:100, origin:'bottom'});
// scr.reveal('.about-section', {delay:100, origin:'bottom'});

// scr.reveal('.review-container', {delay:100, origin:'bottom'});
// scr.reveal('.about-right-section', {delay:100, origin:'bottom'});
// scr.reveal('.about-title', {delay:100, origin:'bottom'});
// scr.reveal('.read-more-btn', {delay:100, origin:'bottom'});

// Planning section

// scr.reveal('.planning-section', {delay:100, origin:'bottom'});
// scr.reveal('.title', {delay:100, origin:'bottom'});
// scr.reveal('.planning-container', {delay:100, origin:'bottom'});

// contact section
// scr.reveal('.contact', {delay:100, origin:'bottom'});
// scr.reveal('.contact-title', {delay:100, origin:'bottom'});
// scr.reveal('.contact-details-section', {delay:100, origin:'bottom'});
// scr.reveal('.contact-description', {delay:100, origin:'bottom'});
// scr.reveal('.contact-icons', {delay:100, origin:'bottom'});
// scr.reveal('.contact-form-section', {delay:100, origin:'bottom'});

// Services section
// scr.reveal('.service-section', {delay:100, origin:'bottom'});
// scr.reveal('.we-do', {delay:100, origin:'bottom'});
// scr.reveal('.card', {delay:100, origin:'bottom'});