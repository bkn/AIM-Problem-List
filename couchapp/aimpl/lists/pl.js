function(head, req) {
  // !json templates
  // !json templates.toc
  // !code vendor/couchapp/*.js
  // !code lib/*.js
  // !code _attachments/mustache.js
  // !code _attachments/utils.js

  provides("html", function() {
      var is_proxy = (req.headers['X-Aimpl-Path'] && typeof req.headers['X-Aimpl-Path'] != "undefined");
      var plrow = getRow();

      if (is_proxy) {
          paths.aim = ["", "pl", plrow.doc.name].join("/");
      } else {
          paths.aim = ["", "pl", plrow.id].join("/");
      }

     authors = {
		'rhrelated': 'Brian Conrey and David Farmer',
		'rhequivalences': 'Brian Conrey and David Farmer',
	    'catalancombinatorics': 'Drew Armstrong',
	    'loweigenvalues': 'Rupert Frank and Richard Laugesen'	
     }
      // Hack to add authors which the parser/importer was not picking up for lists
      //plrow.doc.author = authors[plrow.doc.name];
      
      send(Mustache.to_html(templates.toc.head, {
          path: paths,
          pl:  processLaTeX(plrow.doc)
      }));

      while (row = getRow()) {
          if (is_proxy) {
              link = path("section_with_pblocks", row.doc.list_name, row.doc.list_pos);
          } else {
              link = path("section_with_pblocks", row.doc.list_id, row.doc.list_pos);
          }
          send(Mustache.to_html(templates.toc.row, {
              link: link,
              title: escapeLaTeX(row.doc.title),
              secnum: row.doc.list_pos
          }));
      }

      return Mustache.to_html(templates.toc.footer, {
          path: paths,
      });

  });
};