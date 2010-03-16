function(doc) {
  if (doc.type == "web-remark") {
    if (!doc.status) {
      emit(doc.list_name, doc);
    }
  }
}
