function disable_td(button, td_class, button_text) {
  // button.innerHTML = button_text;
  button.classList.remove('button--enable');

  var td_balance_items = document.getElementsByClassName(td_class);
  for (var i = 0; i < td_balance_items.length; i++) {
    td_balance_items[i].classList.add('td_disable');
  }
}

function enable_td(button, td_class, button_text) {
  // button.innerHTML =  button_text;
  button.classList.add('button--enable');

  var td_balance_items = document.getElementsByClassName(td_class);
  for (var i = 0; i < td_balance_items.length; i++) {
    td_balance_items[i].classList.remove('td_disable');
  }
}

function switch_td() {
  if (this.button.classList.contains('button--enable')===false) {
    enable_td(this.button, this.td_class, this.button_text)
  }
  else {
    disable_td(this.button, this.td_class, this.button_text)
  }
}

function disable_main_block(item_control, item_class) {
  var menu_sidebar_items = document.getElementsByClassName('menu-sidebar');
  for (var i=0; i < menu_sidebar_items.length; i++) {
    menu_sidebar_items[i].classList.remove('menu--enable');
  }
  item_control.classList.add('menu--enable');
  var main_items = document.getElementsByClassName('main_item');
  for (var i=0; i < main_items.length; i++) {
    main_items[i].classList.add('main__block--disable');
  }
  var main_item = document.getElementsByClassName(item_class);
  main_item[0].classList.remove('main__block--disable');
}


function switch_main_block(){
  if (this.item_control.classList.contains('menu--enable')===false) {
    disable_main_block(this.item_control, this.item_class)
  }
}

// button-balance
var button_balance = document.getElementsByClassName('button-balance');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-balance',
  // button_text: 'Остаток'
});
// button-arpu
var button_arpu = document.getElementsByClassName('button-arpu');
button_arpu[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_arpu[0],
  td_class: 'td-arpu',
  // button_text: 'ARPU'
});
// button-active-user
var button_active_user = document.getElementsByClassName('button-active-user');
button_active_user[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_active_user[0],
  td_class: 'td-active-user',
  // button_text: 'Активных'
});
// button-avg-balance-active
var button_avg_balance_active = document.getElementsByClassName('button-avg-balance-active');
button_avg_balance_active[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_avg_balance_active[0],
  td_class: 'td-avg-balance-active',
  // button_text: 'Баланс активных'
});
// button-avg-balance-all
var button_avg_balance_all = document.getElementsByClassName('button-avg-balance-all');
button_avg_balance_all[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_avg_balance_all[0],
  td_class: 'td-avg-balance-all',
  // button_text: 'Баланс всех'
});

// show-table
var main_show_table = document.getElementsByClassName('show-table');
main_show_table[0].addEventListener('click', {
  handleEvent: switch_main_block,
  item_control: main_show_table[0],
  item_class: 'main__table',
});
var show_graph_pays = document.getElementsByClassName('show-graph-pays');
show_graph_pays[0].addEventListener('click', {
  handleEvent: switch_main_block,
  item_control: show_graph_pays[0],
  item_class: 'main__graph-pays',
});

var show_graph_count_pays = document.getElementsByClassName('show-graph-count-pays');
show_graph_count_pays[0].addEventListener('click', {
  handleEvent: switch_main_block,
  item_control: show_graph_count_pays[0],
  item_class: 'main__graph-count-pays',
});

var show_graph_balance = document.getElementsByClassName('show-graph-balance');
show_graph_balance[0].addEventListener('click', {
  handleEvent: switch_main_block,
  item_control: show_graph_balance[0],
  item_class: 'main__graph-balance',
});
