window.addEventListener('load', function() {
let slider = new Swiper("#swiperSlider", {	
    grabCursor: true,
    freeMode: true,
    slidesPerView: "auto",
	spaceBetween: 10,
});
//
// const slides = document.querySelectorAll('.swiper-slide');
//
// slides.forEach(slide => {
//    slide.addEventListener('click', function(event){
//         slides.forEach(slide => {
//             slide.classList.remove('active');
//         })
//         slide.classList.add('active');
//    });
// });

    // const quantityText = document.getElementById('quantity-text');
    //
    // const quantityPlus = document.getElementById('quantity-plus');
    //
    // const quantityMinus = document.getElementById('quantity-minus');
    // let counter = 1;
    // quantityText.textContent = counter;
    // quantityPlus.addEventListener('click', function(){
    //     counter++;
    //     quantityText.textContent = counter;
    //     quantityMinus.classList.remove('disabled');
    // });
    // quantityMinus.addEventListener('click', function(){
    //     if (counter>1){
    //      counter--;
    //     quantityText.textContent = counter;
    //     }
    //     if (counter == 1) {
    //     quantityMinus.classList.add('disabled');
    //     }
    // });

    $( '#basic-usage' ).select2({
        theme: "bootstrap-5",
        width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
        placeholder: $( this ).data( 'placeholder' ),
        selectionCssClass: 'select2--large',
    });
});


// const horizontalCards = document.querySelectorAll(".horizontal-card");
//
// horizontalCards.forEach(card => {
//    card.addEventListener('click', function(event){
//         horizontalCards.forEach(card => {
//             card.classList.remove('active');
//         })
//         card.classList.add('active');
//    });
// });
