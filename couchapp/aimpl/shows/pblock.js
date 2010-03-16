function(doc, req) {
  // !json templates
  // !code vendor/couchapp/*.js
  // !code lib/*.js
  doc.jsMath = assetPath('easyload-tex.js');
  return template(templates.pblock, doc);
};