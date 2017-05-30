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



