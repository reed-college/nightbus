$(document).ready(function(){
    $('#coming').click(function(){
        $('.statusbox').append('<p>Status updated!</p>');
    })
    $(document).on('click','#coming',function() {
        $('p').remove()
        $('.statusbox').append('<p>Status updated!</p>');
   })
        $('#here').click(function(){
        $('.statusbox').append('<p>Status updated!</p>');
    })
    $(document).on('click','#here',function() {
        $('p').remove()
        $('.statusbox').append('<p>Status updated!</p>');
   })

    $('#leaving').click(function(){
        $('.statusbox').append('<p>Status updated!</p>');
    })
    $(document).on('click','#leaving',function() {
        $('p').remove()
        $('.statusbox').append('<p>Status updated!</p>');
   })
})

