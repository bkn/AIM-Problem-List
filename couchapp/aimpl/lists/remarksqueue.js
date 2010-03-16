function(head, req) {
  // !json templates.remarksqueue
  // !code vendor/couchapp/*.js
  // !code lib/*.js
  // !code _attachments/mustache.js
  // !code _attachments/utils.js
  
   provides("html",function() {
     paths.aim = ["", "pl"].join("/"),
     send(Mustache.to_html(templates.remarksqueue.head, {
         path: paths
        
     }));
     
     var cur = '';
     while (r = getRow()) {
       if (r.value.type == "web-remark") {
         r = processLaTeX(r);
         log(" row : " + toJSON(r))
         var start_list, end_list = "";
         if (r.value.pl_id != cur) {
           cur = r.value.pl_id;
           start_list = Mustache.to_html(templates.remarksqueue.start_list, {
             prob: r.value.pl_title,
             path: '/pl/'+r.value.list_name+"/"+r.value.sec_num
           });
           if (cur)
            end_list = Mustache.to_html(templates.remarksqueue.end_list, {});
         }
         
         send(Mustache.to_html(templates.remarksqueue.row, {
           start_list: start_list,
           end_list: end_list,
           rem: {
             by : r.value.by || "",
             email : r.value.email || "",
             remark : r.value.remark || "",
             path : '/pl/'+r.value.list_name,
             pblock_id : r.value.pblock_id,
             rem_id : r.value._id,
           },
           denyb: r.value.pblock_id+ "!" +  r.value._id,
         }));
       }
     }
     
     end_list= "";
     if (cur)
      end_list = Mustache.to_html(templates.remarksqueue.end_list, {});
     
     return Mustache.to_html(templates.remarksqueue.footer, {
         path: paths,
         end_list: end_list
     });
  });
}