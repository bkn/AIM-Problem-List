var paths = {};
paths.json2 = assetPath('json2.js');
paths.jQuery = assetPath('jquery.js');
paths.jQuery = assetPath('jquery.js');
paths.jQueryCouch = assetPath('jquery.couch.js');
paths.mustache = assetPath('mustache.js');
paths.jsMath = assetPath('easyload-tex.js');
paths.appJS = assetPath('app.js');
paths.utils = assetPath('utils.js');
paths.css = assetPath('style','main.css');
paths.couchApp = assetPath('vendor','couchapp','jquery.couchapp.js');
paths.basePath = assetPath('');

var indexPath = req.headers['X-Aimpl-Indexpath'];
if (indexPath && typeof indexPath != "undefined") {
  paths.index = indexPath;
} else {
  paths.index = "/aimpl/_design/aimpl/_list/index/pls"
}

var appPaths = {
  pl_with_sections : function(id) {
    if (indexPath && typeof indexPath != "undefined")
      return ["","pl",id].join('/');
    
    return listPath("pl","pl_with_sections", {
      startkey:[id], 
      endkey:[id,{}], 
      include_docs:true
    });
  },
  pl_with_sec_view : function(id) {
    return viewPath("pl_with_sections", {
      startkey:[id], 
      endkey:[id,{}], 
      include_docs:true
    });
  },
  section_with_pblocks : function(list_id, list_pos) {
    if (indexPath && typeof indexPath != "undefined")
        return ["","pl",list_id,".",list_pos].join('/');
    return listPath("section","pl_full", {
      startkey : [list_id, list_pos],
      endkey : [list_id, list_pos, {}],
      include_docs : true
    });
  },
  
  pblock : function(id) {
    return showPath("pblock", id);
  }
};




