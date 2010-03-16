function escapeLaTeX(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n\n/g, '<p>')
    .replace(/\\htmladdnormallink\{(.*)}{(.*)}/g,'<a\ href=\"$2\">$1</a>')
    .replace(/\\htmladdimage\{(.*)}{(.*)}/g,'<img src=\"$2\"></a>')
}

function processLaTeX(o) {
  for (var k in o) {
    if (typeof o[k] == 'object')
      o[k] = processLaTeX(o[k]);
    else if (typeof  o[k] === 'string') 
      o[k] = escapeLaTeX(o[k]);
  }
 return o;
}