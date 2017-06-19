

// dropdown menu for admin page //

function dropmenu() {
      document.getElementById("admin-dropdown").classList.toggle("show");
    } 

    window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
        }
       }
      }
     }


$(function() {
        // set up an event listener for the buttons
      $('.statusbutton').bind('click', function() {
            // get the value of the clicked  button
        var clicked = $(this).val();
            // send HTTP request via Ajax
        $.ajax({
          url: 'update_state/',
          data: {'state': clicked},
          dataType: "json",
          type: 'GET',
        });
            // for testing
        $.done( function(){
          alert("success");
        });
        $.fail( function (){
          alert("error");
        });
        $.always( function (){
          alert("done");
        });
      });
    });

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
