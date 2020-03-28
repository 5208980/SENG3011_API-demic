function formatNumber(n) { return n.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,') }
function firstSentence(str) { return str.match(/[\s\S]*?(?![A-Z]+)(?:\.|\?|\!)(?!(?:\d|[A-Z]))(?! [a-z])/)[0]; }
