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


// console.log(window.location.pathname);
if( window.location.pathname === '/') {
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




  var notification_url    = "http://127.0.0.1:8000/store/get_notification/"
  var toastTitle          = document.getElementById('not_name');
  var toastImg            = document.getElementById('not_img');
  var toastTime           = document.getElementById('not_time');
  var toastImgHref        = document.getElementById('not_img_href');
  var toastNameHref       = document.getElementById('not_name_href');

  setInterval(function() {
    fetch(notification_url).
    then((response) => {
      response.json().then((data) => {
        toastTitle.textContent = data.name;
        toastImg.setAttribute('src',data.url);
        toastTime.children[0].textContent = data.time + " Minutes";
        toastImgHref.href = data.href;
        toastNameHref.href = data.href;
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

if( window.location.pathname.indexOf('/product_details/') >= 0 ) {

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

  const handleWishlist = function(){
    var colorelem = document.getElementById('select-color');
    var sizeelem  = document.getElementById('select-size');
    colorelem.value = olorelem.options[1].value;
    sizeelem.value = 'temp';
  }

/*  var validateSelection = function(event){
    var colorelem = document.getElementById('select-color');
    var selectedColor = colorelem.options[colorelem.selectedIndex].value;
    var sizeelem  = document.getElementById('select-size');
    var selectedSize = sizeelem.options[sizeelem.selectedIndex].value

    console.log(selectedSize,selectedColor,event)

    if(selectedSize == 'defsize') {
      alert('please select a size');

      return false;
    }

    else if(selectedColor == 'defcolor') {
      alert('please select a color');
      return false;
    }
    var addCartUrl = document.getElementById('addCart').formAction;
    console.log(addCartUrl);
    window.location.href = addCartUrl
  }

  var incart = function (fetchedvariation) {
    var res = true;
    var selectVariation = document.getElementsByClassName('select-variation');  
    if(selectVariation.length != fetchedvariation.length){
      res = false;
    }
      
    var index = 0
    Array.from(selectVariation).forEach( (variation) => {
      if(variation.value === fetchedvariation[index++]){
      }
      else{
        res = false;
      }
    })
    return res;
  }

  var selectHandler = function (){
    var cart_variation_url = 'http://127.0.0.1:8000/get_cart_variations/' + product_id.textContent
    fetch(cart_variation_url).then( (response) => {
      response.json().then( data => {
        if(incart(data.variations)){
          
        }
        })
      });
  } */
}

if(window.location.href.indexOf('register/')>=0 || window.location.href.indexOf('reset_password/')>=0){
  const container = document.querySelector(".rcontainer"),
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password"),
      signUp = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link");

    //   js code to show/hide password and change icon
    pwShowHide.forEach(eyeIcon =>{
        eyeIcon.addEventListener("click", ()=>{
            pwFields.forEach(pwField =>{
                if(pwField.type ==="password"){
                    pwField.type = "text";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                    })
                }else{
                    pwField.type = "password";

                    pwShowHide.forEach(icon =>{
                        icon.classList.replace("uil-eye", "uil-eye-slash");
                    })
                }
            }) 
        })
    })

    // js code to appear signup and login form
    // signUp.addEventListener("click", ( )=>{
    //     container.classList.add("active");
    // });
    // login.addEventListener("click", ( )=>{
    //     container.classList.remove("active");
    // });


}

const alert_toast = document.getElementById("alert-toast"),
      closeIcon = document.getElementById("alert-close"),
      alert_progress = document.getElementById("alert-progress");

      let timer1, timer2;

      document.addEventListener("DOMContentLoaded", () => {
        alert_toast.classList.add("alert-active");
        alert_progress.classList.add("alert-active");

        timer1 = setTimeout(() => {
            alert_toast.classList.remove("alert-active");
        }, 5000); //1s = 1000 milliseconds

        timer2 = setTimeout(() => {
          alert_progress.classList.remove("alert-active");
        }, 5300);
      });
      
      closeIcon.addEventListener("click", () => {
        alert_toast.classList.remove("alert-active");
        
        setTimeout(() => {
          alert_progress.classList.remove("alert-active");
        }, 300);

        clearTimeout(timer1);
        clearTimeout(timer2);
      });
