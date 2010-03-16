 // linked via section_with_pblocks
function(head, req) {
  // !json templates.section
  // !json templates.section.remarks
  // !code vendor/couchapp/*.js
  // !code lib/*.js
  // !code _attachments/mustache.js
  // !code _attachments/utils.js


  provides("html",function() {
      var row;
      var doc;
      var num = 0;
      row = getRow();
      doc = row.doc;

      if (!row) {
          throw ({
              "error": "no_row",
              "reason": "getRow returns null",
              "code": 404
          });
      }
      
      log("userctx " + toJSON(req.userCtx));

      var canremark = true;
      var canedit = false;
      if (req.userCtx.name) {
          var roles = req.userCtx.roles;
          canedit = roles.some(function(elem, idx, arr) {
              return (elem == "Chief Editor" || elem == "Editors");
          });
      }

      paths.pl_view = path("pl_with_sec_view", doc.list_id);
      paths.pl_list = path("pl_with_sections", doc.list_name);
      paths.aim = ["", "pl", doc.list_id, ".", doc.list_pos].join("/");
      
      var sec = processLaTeX(row.doc);
      var sec_num = row.doc.list_pos;
      var author = row.doc.author;

      send(Mustache.to_html(templates.section.head, {
          path: paths,
          canedit: canedit,
          sec: sec,
          sec_num: sec_num,
          author: author	
      }));

      var num = 1;

      while (row = getRow()) {
          var r = row.doc;
          r.link = path("pblock", row.value._id);
          r.probtag = r.problem_tag || (sec_num + "." + num);
          r.probname = r.name;

	      			
          r.proburl = 'http://' + req.headers['X-Forwarded-Host'] + paths.pl_list + "/" + sec_num + "." + num;
          r.num = num++;
          r.probfrag = sec_num + "." + num;
          var ks = [];
          for (var k in r) {
              ks.push(k);
          }
          
          if (r.list_name.indexOf("/") >= 0) {
              canedit = false;
              canremark = false;
          }
            
          r.canremark = canremark;
          r.canedit = canedit;
          
          r = processLaTeX(r);
          
          if (!r.remarks || r.remarks.length < 1) {
            r.remarks = [];
          }
          if (r.distremark) {
             r.remarks.unshift({remark: r.distremark});
          }
         
          l = r.remarks.length;
          if (r.remarks.length < 0) {
            rmarks = "";
            
          } else {
            
            rmarks = Mustache.to_html(templates.section.remark_head, {"_id": r._id});
            
            for(i=0; i< r.remarks.length; i++) {
              log("rema " + toJSON(r.remarks[i]));
              rmarks += Mustache.to_html(templates.section.remark_row, {
                remark: r.remarks[i].remark
              });
            }
            rmarks += Mustache.to_html(templates.section.remark_footer, {});
          }
          r.rmarks = rmarks;

          send(Mustache.to_html(templates.section.row, r));
      }

      return Mustache.to_html(templates.section.footer, {
          path: paths,
          canedit: canedit,
          sec: sec,
          sec_num: sec_num
      });

  });
};
