function getRowsWith(fun) {
  return function() {
    var row = getRow();
    return row && fun(row);
  };
};
