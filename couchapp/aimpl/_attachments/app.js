$.CouchApp(function(app) {
    app.view("pl_with_sections", {
        startkey: [pl_id],
        endkey: [pl_id, {}],
        include_docs: true,
        success: function(view) {
            var lis = view.rows.map(function(row) {
                if (!row.doc.list_pos) return '';
                return '<li><a href="' + row.doc.list_pos + '">' + row.doc.title + '</a></li>'
            }).join('');
            $("#nav ul").append(lis);
        }
    });

    $(".editp").each(function() {
        $(this).click(function() {

            var id = $(this).attr("id").split("_")[1];
            $('#' + id + ' .probd').hide();

            var edit_link = $(this);
            $(this).hide();
            var pb = app.db.openDoc(id, {
                success: function(doc) {
                    $.get(basePath + "templates/edit_problem.html",
                    function(tpl) {
                        var form = Mustache.to_html(tpl, doc);
                        $('#' + id).append(form);

                        // cancel
                        $("#" + id + " .ce").click(function() {
                            $("#" + id + " form").remove();
                            $('#' + id + ' .probd').show();
                            edit_link.show();
                            return false;
                        });

                        // save changes
                        var f = $("#" + id + " form");
                        f.submit(function() {
                            doc.intro = f.find("[name=intro]").val();
                            doc.problem.by = f.find("[name=by]").val();
                            doc.problem.body = f.find("[name=body]").val();
                            f.append("<h4>Saving</h4>");
                            app.db.saveDoc(doc, {
                              success : function(resp) {
                                $.get(basePath + "templates/problem.html",
                                function(tpl1) {
                                  r = doc;
                                  r.probtag = r.problem_tag ;
                                  r.probname = r.name;
                                  var ks = [];
                                  for (var k in r) {
                                      ks.push(k);
                                  }
                                  r = processLaTeX(r);
                                  
                                  
                                    var edited = Mustache.to_html(tpl1, r);
                                                                        
                                    var new_content = $('#' + id + ' .probd').html(edited);
                                    $("#" + id + " form").remove();
                                    $('#' + id + ' .probd').show();
                                    edit_link.show();
                                    $('#' + id + " .xmath").each(function(){
                                       jsMath.ConvertTeX($(this)[0]);
                                       jsMath.ProcessBeforeShowing($(this)[0]);
                                    });
                                    
                                });
                              }
                            });

                            return false;
                        });
                    });
                }
            });
            return false;
        });
    });

   $.get(basePath + "templates/new_remark.html", function(form) {
        $(".probc").each(function() {
            //$(this).append('<a class="makeremark" href="#">Add a Remark</a><br class="clear"/>');
            var id = $(this).attr("id");
            var shown = false;
            $("#" + id + " .makeremark").click(function() {
                if (!shown) {
                    shown = true;
                    var pb = $('#' + id + ' .probd');
                     $("#" + id + " .makeremark").after(form);
                    var f =  $("#" + id + " form");
                    // preview
                    $("#" + id + " .pre").click(function() {
                      var rem = $("." + id + " form textarea").val();
                      $("." + id + " div.preview").text(rem);
                      var previewe = $("." + id + " div.preview")[0];
                      jsMath.ConvertTeX(previewe);
                      jsMath.ProcessBeforeShowing(previewe);  
                    });
                    
                    $("#" + id + " .cancel").click(function() {
                      f.fadeOut('slow', function() {
                        $(this).remove();
                        
                      });
                      shown = false;
                    });
                    
                    f.submit(function() {
                            var remark = {
                                by: f.find("[name=by]").val(),
                                remark: f.find("[name=remark]").val(),
                                email: f.find("[name=email]").val(),
                                pblock_id: id,
                                pl_title: $('h2').text(),
                                sec_title: $('h1').text(),
                                list_name: pl_name,
                                sec_num: sec_num,
                                created_at: new Date(),
                                type: "web-remark"
                            };
                            f.append("<h4>Saving</h4>");
                            app.db.saveDoc(remark, {
                                success: function(resp) {
                                    f.find('h4').text("Saved remark id: " + resp.id)
                                    f.fadeOut('slow', function() {
                                      $(this).remove();
                                    });
                                }
                            });
                        shown = false;
                        return false;
                    });
                }
                return false;
            });
        });
    });
},
{
    dbname: "aimpl",
    ddocname: "aimpl"
});

