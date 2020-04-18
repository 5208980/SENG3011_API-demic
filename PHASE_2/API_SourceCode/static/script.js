function formatNumber(n) { return n.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,') }
function firstSentence(str) {
    let results = str.match(/[\s\S]*?(?![A-Z]+)(?:\.|\?|\!)(?!(?:\d|[A-Z]))(?! [a-z])/);
    if(results) { return results[0]; }
    return "";

}
// Counter Up with comma. Input Text: Number with comma
function animateCount() {
    console.log("Here");
    $('.count').each(function() {
        $(this).prop('counter', 0).animate({
            Counter: parseFloat($(this).text().split(',').join(''))
        }, {
            duration: 1000,
            easing: 'swing',
            step: (now) => { $(this).text(Number(Math.ceil(now)).toLocaleString('en'));
            }
        });
    });
}
