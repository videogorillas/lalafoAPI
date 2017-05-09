check = function(){
    var els = $('input:checked'), i, s = '';
    for (i=0; i < els.length; i++)
        s += els.eq(i).parent().text() + '<br>'
    $('div.checked').html('Checked: ' + els.length + '<br>' + s)
}

$().ready(function () {
    /*var imgs = $('img'), eps = 100;
    $(window).scroll(function () {
        var i, st = $(this).scrollTop(), ih = window.innerHeight;
        $.each(imgs, function(){
            var im = $(this), ot = $(im).offset().top;
            im.attr('src', (ot > st-eps && ot < st + ih + eps) ? im.attr('s') : false)
        })

    });*/
    /*$('img').on('appear', function(event, imgs) {
        console.log(imgs)
       $.each(imgs, function () {
           var im = $(this);
           im.attr('src', im.attr('s'))
       })
    });*/
    $('img').lazyload()

    $('#b-true').click(function () {
        $('.true').toggle()
    })

    $('.b-full').click(function(){
        $(this).next().toggle()
    })

    $('input:checkbox').click(check)

    check()
})
