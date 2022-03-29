function toggleView(tbl) {
    var x = document.getElementById(tbl);
    var tables = document.getElementsByClassName('dashboard');

    for(var i=0; i<tables.length; i++){
      if (x.classList.contains('level-2') && tables[i].classList.contains('level-1')){
        continue;
        } else if (tables[i].tagName=='BUTTON'){
              if (x.id.includes(tables[i].id)){
                tables[i].classList.add('active');
              } else {
                tables[i].classList.remove('active');
              }
        } else if (tables[i].id!=x.id){
            tables[i].classList.remove('show');
      
    }
  }
    if (x.classList.contains('show')){
      x.classList.remove('show');
    } else{
      x.classList.add('show');
    }
  } 


