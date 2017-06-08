$(document).ready(function(){
    $('#coming').click(function(){
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
    })

    $(document).on('click','#coming',function() {
        $('p').remove()
        $('.statusbox').show()
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
   })
        $('#here').click(function(){
        $('p').remove()
        $('.statusbox').show()
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
    })
    $(document).on('click','#here',function() {
        $('p').remove()
        $('.statusbox').show()
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
   })

    $('#leaving').click(function(){
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
    })
    $(document).on('click','#leaving',function() {
        $('p').remove()
        $('.statusbox').show()
        $('.statusbox').append('<p>Status updated!</p>');
        $('.statusbox').fadeOut(4000)
   })
})

$(function() {
        // set up an event listener for the buttons
      $('button').bind('click', function() {
            // get the value of the clicked  button
        var clicked = $(this).val();
            alert(clicked);
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

$(function() {
        // set up an event listener for the buttons
      $('button').bind('click', function() {
            // get the value of the clicked  button
        var clicked = $(this).val();
            alert(clicked);
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
