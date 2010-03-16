function(doc) {
  if (doc.type == "list") { // change to pl
      if (doc._id.indexOf("/") < 0) 
        emit(doc._id, {"title" : doc.title})
  }
};