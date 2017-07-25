
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

/* driver submit status button */
    function submitstatus() {
      alert("Status updated!")
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

/* Form Validation for Signup page */

function validateForm() {
  $('#signupForm').validate({

    // place error messages in the error box
    errorPlacement: function(error, element) {
      error.appendTo($('.messageBox'));

      //clear error messages whilst typing
      element.keyup( function() {
       $('.messageBox').empty();
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
              return $("#signupForm:input[name=username]").val()
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
              return $('#signupForm:input[name=email]').val()
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
      firstname: "Please enter your first name",
      lastname:  "Please enter your lastname",
      username: {
        required: "Please enter your username",
        remote: jQuery.validator.format( "Username is already taken")
      },
      password: {
        required: "Please provide a password" ,
        minlength: "Your password must be at least 5 characters long"
      },
      email: {
        required: "Please enter an email address",
        email: "Please enter a valid email address",
        remote: jQuery.validator.format("Email is already registered")
      }
    },

    submitHandler: function(form) {
      form.submit();
    }
  });
}

/* Form Validation for Rider page */

function validateMissing() {
  $("#report-missing").validate({

    errorPlacement: function(error, element) {
      error.appendTo($('#missing-errors'));
      $('#missing-errors').show();
      //clear error messages whilst typing
        element.keyup( function() {
         $('#missing-errors').empty().hide();
       });
      },
      rules: {
        name: "required",
        email: {
          required: true,
          email: true
        }
      },
      messages: {
        name: "<br>"+ "Please enter your name",
        email: {
          required: "<br><br>"+ "Please enter your email address",
          email: "<br><br>"+ "Please enter a valid email address"
        }
      },
      submitHandler: function(form) {
        $.ajax({
            url: "https://script.google.com/macros/s/AKfycbyjGWQhgB2aWIm0WiGr-cNxYmPLI3LNAHrNCMImGOoFNcOPpYeS/exec",
            data: $(form).serialize(),
            type: "POST",
            dataType: "json",
            success: function(data) {
                alert('Your report has been received');
                // clear form input after submit
                document.getElementById('report-missing').reset();
                console.log('Submission successful');
            },
            error: function(xhr, status, error) {
                alert("Oops, something's wrong. Please try again");
                console.log('Submission failed: ' + error);
            }
        });
      }
    });
}

function validateLate() {
  $("#late-notice").validate({

    errorPlacement: function(error, element) {
      error.appendTo($('#late-errors'));
      $('#late-errors').show();
      //clear error messages whilst typing
        element.keyup( function() {
         $('#late-errors').empty().hide();
       });
      },
      rules: {
        name: "required",
        email: {
          required: true,
          email: true
        }
      },
      messages: {
        name: "<br>"+ "Please enter your name",
        email: {
          required:"<br><br>"+ "Please enter your email address",
          email: "<br><br>"+ "Please enter a valid email address"
        }
      },
      submitHandler: function(form) {

        $.ajax({
            url: "https://script.google.com/macros/s/AKfycbzjwNLeHqatAsZVkRZf4mmibkplaHAxarPx1MHafy2HORV-mXVR/exec",
            data: $(form).serialize(),
            type: "POST",
            dataType: "json",
            success: function(data) {
                alert('Your request has been received');
                // clear form input after submit
                document.getElementById('late-notice').reset();
                console.log('Submission successful');

            },
            error: function(xhr, status, error) {
                alert("Oops, something's wrong. Please try again.");
                console.log('Submission failed: ' + error);
            }
          });
          return false;
        }
      });
  }
