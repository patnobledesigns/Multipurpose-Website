$(document).ready(()=>{
    $('.move-up span').click(()=>{
        $('html, body').animate({
            scrollTop: 0
        }, 1000);
    });

    AOS.init();

});
