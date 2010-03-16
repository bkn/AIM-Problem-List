function(doc) {
  if (false && doc.remarks && doc.remarks.length > 0) {
    // published remarks
    emit([doc.list_name, doc._id], doc.problem_tag);
    for (var i=0; i < doc.remarks.length; i++) {
      emit([doc.list_name, doc._id, i], doc.remarks[i]);
    };    
  }
  if (doc.type == "pblock") {
    emit([doc.list_name, doc._id], doc)
  }
  if (doc.type == "web-remark") {
    if (!doc.status) {
      emit([doc.list_name, doc.pblock_id, doc.created_at], doc)      
    }
  }
};