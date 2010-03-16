function(doc) {
  switch(doc.type) {
    case "list":
      emit([doc._id], {"_id":doc._id});
      break;
    case "section":
      emit([doc.list_id, doc.list_pos], {"_id":doc._id});
      for (var i=0; i < doc.pblock_ids.length; i++) {
        emit([doc.list_id, doc.list_pos, i], {"_id":doc.pblock_ids[i]})
      };
      break;
  }
};