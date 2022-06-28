'use strict';


// accordion variables
const accordionBtn = document.querySelectorAll('[data-accordion-btn]');
const accordion = document.querySelectorAll('[data-accordion]');

for (let i = 0; i < accordionBtn.length; i++) {

  accordionBtn[i].addEventListener('click', function () {

    const clickedBtn = this.nextElementSibling.classList.contains('active');

    for (let i = 0; i < accordion.length; i++) {

      if (clickedBtn) break;

      if (accordion[i].classList.contains('active')) {

        accordion[i].classList.remove('active');
        accordionBtn[i].classList.remove('active');

      }

    }

    this.nextElementSibling.classList.toggle('active');
    this.classList.toggle('active');

  });

}



if( window.location.pathname === '/home/') {
  // modal variables
  const modal = document.querySelector('[data-modal]');
  const modalCloseBtn = document.querySelector('[data-modal-close]');
  const modalCloseOverlay = document.querySelector('[data-modal-overlay]');

  // modal function
  const modalCloseFunc = function () { modal.classList.add('closed') }

  // modal eventListener
  modalCloseOverlay.addEventListener('click', modalCloseFunc);
  modalCloseBtn.addEventListener('click', modalCloseFunc);





  // notification toast variables
  const notificationToast = document.querySelector('[data-toast]');
  const toastCloseBtn = document.querySelector('[data-toast-close]');

  // notification toast eventListener
  toastCloseBtn.addEventListener('click', function () {
    notificationToast.classList.add('closed');
  });





  // mobile menu variables
  const mobileMenuOpenBtn = document.querySelectorAll('[data-mobile-menu-open-btn]');
  const mobileMenu = document.querySelectorAll('[data-mobile-menu]');
  const mobileMenuCloseBtn = document.querySelectorAll('[data-mobile-menu-close-btn]');
  const overlay = document.querySelector('[data-overlay]');

  for (let i = 0; i < mobileMenuOpenBtn.length; i++) {

    // mobile menu function
    const mobileMenuCloseFunc = function () {
      mobileMenu[i].classList.remove('active');
      overlay.classList.remove('active');
    };

    mobileMenuOpenBtn[i].addEventListener('click', function () {
      mobileMenu[i].classList.add('active');
      overlay.classList.add('active');
    });

    mobileMenuCloseBtn[i].addEventListener('click', mobileMenuCloseFunc);
    overlay.addEventListener('click', mobileMenuCloseFunc);

  }




  var notification_url = "http://127.0.0.1:8000/get_notification/"
  var toastTitle = document.getElementById('not_name');
  var toastImg   = document.getElementById('not_img');
  var toastTime  = document.getElementById('not_time');

  setInterval(function() {
    fetch(notification_url).
    then((response) => {
      response.json().then((data) => {
        toastTitle.textContent = data.name;
        toastImg.setAttribute('src',data.url);
        toastTime.children[0].textContent = data.time + " Minutes";
      })
    }).catch((error) => {
      console.log(error);
    })
  },10000)
  
  var countdown_url = "http://127.0.0.1:8000/get_countdown/"
  var elemday = document.getElementsByClassName('cd_day');
  var elemhour = document.getElementsByClassName('cd_hour');
  var elemmin = document.getElementsByClassName('cd_min');
  var elemsec = document.getElementsByClassName('cd_sec');
  
  fetch(countdown_url).then((response) => {
    response.json().then( (time) => {
      var seconds = time.seconds; 
  
      setInterval(() => {
        var day = Math.floor(seconds / (60*60*24));
        var remsec = seconds % (60*60*24);
        var hour= Math.floor(remsec / (60*60));
        remsec = remsec % (60*60);
        var min= Math.floor(remsec / 60);
        var sec = remsec % 60;
  
        Array.from(elemday).forEach( (elem) => {
          elem.textContent = day;
        });
        Array.from(elemhour).forEach( (elem) => {
          elem.textContent = hour;
        });
        Array.from(elemmin).forEach( (elem) => {
          elem.textContent = min;
        });
        Array.from(elemsec).forEach( (elem) => {
          elem.textContent = sec;
        });
        seconds -=1;
      },1000);
    })
  }).catch((error) => {
    console.log(error);
  })
}


/**************Product details page functions ************** */

const allHoverImages = document.querySelectorAll('.hover-container div img');
const imgContainer = document.querySelector('.img-container');

window.addEventListener('DOMContentLoaded', () => {
    allHoverImages[0].parentElement.classList.add('active');
});

allHoverImages.forEach((image) => {
    image.addEventListener('mouseover', () =>{
        imgContainer.querySelector('img').src = image.src;
        resetActiveImg();
        image.parentElement.classList.add('active');
    });
});

function resetActiveImg(){
    allHoverImages.forEach((img) => {
        img.parentElement.classList.remove('active');
    });
}