document.querySelector('body').classList.add('no-scroll')
let animatedElement = document.querySelectorAll('.slide-left,.slide-top,.slide-bottom,.slide-left-wel,.slide-top-wel,.slide-right-wel')
animatedElement.forEach(function(a){
    a.addEventListener('animationend', function() {
        document.body.classList.remove('no-scroll');
      });
})
