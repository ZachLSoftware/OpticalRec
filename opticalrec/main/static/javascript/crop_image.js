const alertBox = document.getElementById('alert-box')
const cropForm = document.getElementById('crop-form')
const confirmBtn = document.getElementById('confirm-btn')
const cropBtn = document.getElementById('crop-btn')
const prevBtn = document.getElementById('new-prev-btn')
const rejectBtn = document.getElementById('reject-btn')
const finishBtn = document.getElementById('fin-btn')
const cnFinBtn = document.getElementById('cnf-fin-btn')
const hideImage = document.getElementById('hide-image')
const labelForm = document.getElementById('label-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const replace = document.getElementById('replace');

window.addEventListener('DOMContentLoaded', function () {
    document.getElementById("before_crop").classList.add("show")
    var image = document.querySelector('#image');
    var image = document.getElementById('image');

    var cropper = new Cropper(image, {
        autoCropArea: .25
    });

    cropBtn.addEventListener('click', ()=>{
        document.getElementById("before_crop").classList.remove("show")
        document.getElementById("after_crop").classList.add("show")
        hideImage.classList.remove("show")
        replace.appendChild(cropper.getCroppedCanvas());
    })

    rejectBtn.addEventListener('click', ()=>{
        replace.innerHTML = '';
        document.getElementById("before_crop").classList.add("show")
        document.getElementById("after_crop").classList.remove("show")
        hideImage.classList.add("show")
    })

    cnFinBtn.addEventListener('click', ()=>{
        if (isNaN(document.getElementById("label").value ) && document.getElementById("label").value != ""){
            var temp = document.getElementById('crop-form');
            var url = temp.getAttribute('action')
            var newUrl= url.concat("/0/1");
            temp.action=newUrl;
            sendData();
        }
        else{
            document.getElementById("error").innerHTML="Please enter a valid text Label";
        }
    })

    confirmBtn.addEventListener('click', ()=>{
        if (isNaN(document.getElementById("label").value ) && document.getElementById("label").value != ""){
            sendData();
        }
        else{
            document.getElementById("error").innerHTML="Please enter a valid text Label";
        }

    })

    function sendData(){
        var data = cropper.getData(true);
        var original = cropper.getImageData(true);
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('x1', data.x);
        fd.append('y1', data.y);
        fd.append('width', data.width)
        fd.append('height', data.height)
        fd.append('nat_height', original.naturalHeight)
        fd.append('nat_width', original.naturalWidth)
        fd.append('label', document.getElementById("label").value)


            $.ajax({
                type:'POST',
                url: cropForm.action,
                enctype: 'multipart/form-data',
                data: fd,
                success: function(response){
                    if(response.status==0){
                        console.log(response.status)
                        window.location.href=response.url;
                    }
                    else{
                        alertBox.innerHTML = response.message
                    }
                },
                error: function(error){
                    console.log('error', error)
                    alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                            oops...something went wrong
                                        </div>`
                },
                cache: false,
                contentType: false,
                processData: false,
            })
        }
});