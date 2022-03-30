const height=window.screen.height;
const width=window.screen.width;
const startH=height/1080;
const startW=width/1920;
var images = document.querySelectorAll('.showcase-img,.img-fluid')

function windowSize() {
    widthPer = window.innerWidth/width;
    heightPer = window.innerHeight/height
    newW=(Math.round(350*widthPer)).toString()+'px';
    newH=(Math.round(350*widthPer)).toString()+'px';
    bs=newH+' auto'

    for(var i=0; i<images.length; i++){
        images[i].style.backgroundSize = bs;
        images[i].style.width=newW;
        images[i].style.height=newW;
    }
    

}

window.onresize = windowSize;

window.addEventListener('DOMContentLoaded', function() {
    var sec = document.getElementsByClassName('section')
    for(var i=0; i<sec.length; i++){

        if (document.getElementById('body').classList.contains('bg-dark')){
        sec[i].classList.remove('bg-light');
        sec[i].classList.add('bg-dark');
        }else
        {
        sec[i].classList.remove('bg-dark');
        sec[i].classList.add('bg-light');
        }
    }
    windowSize();
   });
