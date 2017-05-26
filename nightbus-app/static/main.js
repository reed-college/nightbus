$(document).ready(function(){
    $('button').click(function(){
        $('.box').append('<p>The NightBus is Coming!</p>');
    })
    $(document).on('click','button',function() {
        $('p').remove()
       // $('.box').append('<p>The NightBus is Coming!</p>');
    })
})

