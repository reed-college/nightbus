
/* Update the NightBus statuses on Driver page */

function submitstatus() {
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
        alert("Status updated!");
        console.log("Bus status updated successfully");
      },
      error: function() {
        console.log("Failed to update bus status");
      }
    });
  });
}

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

/* form validation */

function validateForm() {
  $('form').validate({

    // place error messages in the error box
    errorPlacement: function(error, element) {
      error.appendTo($('#messageBox'));
      $('#messageBox').css({
        'display': 'block',
        'position': 'absolute',
        'width': '100%',
        'height': '33%',
        'left': '110%',
        'top': '55%',
        'text-align': 'left'
      });

      //turn off auto validate whilst typing
      element.keyup( function() {
       $('#messageBox').empty();
     });
    },

    //Specify validation rules
    rules: {
      firstname: "required",
      lastname: "required",
      username: {
        required: true,
        // check if username already exists.
        remote: {
          url: 'username_exists',
          type: 'post',
          data: {
            username: function() {
              return $("input[name=username]").val()
            }
          }
        }
      },
      email: {
        required: true,
        email: true, // Specify that email should be validated by the built-in "email" rule
        remote: {
          url: 'email_exists',
          type: 'post',
          data: {
            email: function() {
              return $('input[name=email]').val()
            }
          }
        }
      },
      password: {
        required: true,
        minlength: 5
      }
    },

    // specify validation error messages
    messages: {
      firstname: "<br>" + "Please enter your first name",
      lastname: "<br>" + "Please enter your lastname",
      username: {
        required: "<br>" + "Please enter your username",
        remote: jQuery.validator.format("<br>" + "Username is already taken")
      },
      password: {
        required: "<br>"+ "Please provide a password" ,
        minlength: "<br>" + "Your password must be at least 5 characters long"
      },
      email: {
        required: "<br>" + "Please enter an email address",
        email: "<br>"+ "Please enter a valid email address",
        remote: jQuery.validator.format("<br>" +  "Email is already registered")
      }
    },

    submitHandler: function(form) {
      form.submit();
    }
  });
}
