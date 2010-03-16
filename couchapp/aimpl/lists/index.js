function(head, req) {
  // !json templates
  // !json templates.index
  // !code vendor/couchapp/*.js
  // !code lib/*.js
  // !code _attachments/mustache.js
  // !code _attachments/utils.js
  
  provides("html", function() {
      var is_proxy = (req.headers['X-Aimpl-Path'] && typeof req.headers['X-Aimpl-Path'] != "undefined");
      paths.aim = "/";

      send(Mustache.to_html(templates.index.head, {
          path: paths
      }));

      while (row = getRow()) {
          if (is_proxy) {
              link = path("pl_with_sections", row.doc.name);
          } else {
              link = path("pl_with_sections", row.id);
          }
          
          send(Mustache.to_html(templates.index.row, {
              link: link,
              title: escapeLaTeX(row.value.title)
          }));
      }

      return Mustache.to_html(templates.index.footer, {
          path: paths
      });
  });
};