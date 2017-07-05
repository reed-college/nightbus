
/* Update the NightBus statuses on Driver page */

$(function() {
  // set up an event listener for the buttons
  $('.statusbutton').bind('click', function() {
    // get the value of status button on click
    var clicked = $(this).val();
    // send HTTP request via Ajax
    $.ajax({
      url: 'update_state/',
      data: {
        'state': clicked
      },
      dataType: "json",
      type: 'GET',
      success: function() {
        console.log("Bus status updated successfully");
      },
      error: function() {
        console.log("Failed to update bus status");
      }
    });
  });
});

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

/* Close the dropdown menu if the user clicks outside of it */

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

/* driver submit status button */
function submitstatus() {
  alert("Status updated!")
}
