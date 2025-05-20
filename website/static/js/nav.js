// Toggle the menu bar in mobile

// variables

let menuEl = document.querySelectorAll('.js-menu-btn');
let menuBarEL = document.querySelector('.nav-bar ul');
let iconEl = document.querySelector('.menu button i');

// Add event listener when the menu button is clicked
menuEl.forEach(menu =>{
    menu.addEventListener('click', ()=>{
        // toggle the menu bar
        menuBarEL.classList.toggle("active");
        if(iconEl.classList.contains('fa-bars')){
            return iconEl.classList.replace('fa-bars', 'fa-times')
        }else{
            return iconEl.classList.replace('fa-times', 'fa-bars')
        }
    });
});

// Close the nav after click
// variables

let navListEl = document.querySelectorAll('.nav-list');

navListEl.forEach(nav =>{
    nav.addEventListener('click', ()=>{
        menuBarEL.classList.remove("active");
        if(iconEl.classList.contains('fa-times')){
            return iconEl.classList.replace('fa-times', 'fa-bars');
        }
    })
})


// Floating button
const floatingBtnEl = document.querySelector('.floating-btn');

window.addEventListener('scroll', ()=>{
    if(scrollY > 20){
        floatingBtnEl.style.display = 'block';
    }else{
        floatingBtnEl.style.display = 'none';
    }
})

floatingBtnEl.addEventListener('click', ()=>{
    window.scrollY = 0;
})