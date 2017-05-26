$(document).ready(function(){
    $('#coming').click(function(){
        $('.box').append('<p>The NightBus is coming!</p>');
    })
    $(document).on('click','#coming',function() {
        $('p').remove()
        $('.box').append('<p>The NightBus is coming!</p>');
   })
        $('#here').click(function(){
        $('.box').append('<p>The NightBus is here!</p>');
    })
    $(document).on('click','#here',function() {
        $('p').remove()
        $('.box').append('<p>The NightBus is here!</p>');
   })

    $('#leaving').click(function(){
        $('.box').append('<p>The NightBus is gone!</p>');
    })
    $(document).on('click','#leaving',function() {
        $('p').remove()
        $('.box').append('<p>The NightBus is gone!</p>');
   })
})

