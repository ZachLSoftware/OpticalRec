const title=document.title
const page=document.getElementById(title)
window.addEventListener('DOMContentLoaded', function () {
    page.classList.add('active')
    });

function cropHelp(){
    alert('You can select any area of the video to crop.\n'
    + '1. Select the field you want to track, press "Crop".\n'
    + '2. Enter a Label for your selection.\n'
    + '3. If you want to select more areas press "Confirm and Add"\n'
    + '4. If you are unhappy with your selection press "Reject"\n'
    + '5. Once you have selected all areas, press finish.');
}