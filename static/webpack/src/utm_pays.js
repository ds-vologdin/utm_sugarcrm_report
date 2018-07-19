function disable_td(button, td_class, button_text) {
  button.classList.remove('button--enable');

  let td_balance_items = document.getElementsByClassName(td_class);
  for (let td_balance_item of td_balance_items) {
    td_balance_item.classList.add('td_disable');
  }
}

function enable_td(button, td_class, button_text) {
  button.classList.add('button--enable');

  let td_balance_items = document.getElementsByClassName(td_class);
  for (let td_balance_item of td_balance_items) {
    td_balance_item.classList.remove('td_disable');
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
  let menu_sidebar_items = document.getElementsByClassName('menu-sidebar');
  for (let menu_sidebar_item of menu_sidebar_items) {
    menu_sidebar_item.classList.remove('menu--enable');
  }
  item_control.classList.add('menu--enable');
  let main_items = document.getElementsByClassName('main_item');
  for (let main_item of main_items) {
    main_item.classList.add('main__block--disable');
  }
  let main_item_show = document.getElementsByClassName(item_class);
  if (main_item_show.length > 0) {
    main_item_show[0].classList.remove('main__block--disable');
  }
}


function switch_main_block(){
  if (this.item_control.classList.contains('menu--enable')===false) {
    disable_main_block(this.item_control, this.item_class)
  }
}

export function set_button_handler() {
  // button-balance
  let button_balance = document.getElementsByClassName('button-balance');
  if (button_balance.length > 0) {
    button_balance[0].addEventListener('click', {
      handleEvent: switch_td,
      button: button_balance[0],
      td_class: 'td-balance',
    });
  }

  // button-arpu
  let button_arpu = document.getElementsByClassName('button-arpu');
  if (button_arpu.length > 0) {
    button_arpu[0].addEventListener('click', {
      handleEvent: switch_td,
      button: button_arpu[0],
      td_class: 'td-arpu',
    });
  }

  // button-active-user
  let button_active_user = document.getElementsByClassName('button-active-user');
  if (button_active_user.length > 0) {
    button_active_user[0].addEventListener('click', {
      handleEvent: switch_td,
      button: button_active_user[0],
      td_class: 'td-active-user',
    });
  }

  // button-avg-balance-active
  let button_avg_balance_active = document.getElementsByClassName('button-avg-balance-active');
  if (button_avg_balance_active.length > 0) {
    button_avg_balance_active[0].addEventListener('click', {
      handleEvent: switch_td,
      button: button_avg_balance_active[0],
      td_class: 'td-avg-balance-active',
    });
  }
  // button-avg-balance-all
  let button_avg_balance_all = document.getElementsByClassName('button-avg-balance-all');
  if (button_avg_balance_all.length > 0) {
    button_avg_balance_all[0].addEventListener('click', {
      handleEvent: switch_td,
      button: button_avg_balance_all[0],
      td_class: 'td-avg-balance-all',
    });
  }
}

export function set_left_menu_handler() {
  // show-table
  let main_show_table = document.getElementsByClassName('show-table');
  if (main_show_table.length > 0) {
    main_show_table[0].addEventListener('click', {
      handleEvent: switch_main_block,
      item_control: main_show_table[0],
      item_class: 'main__table',
    });
  }

  let show_graph_pays = document.getElementsByClassName('show-graph-pays');
  if (show_graph_pays.length > 0) {
    show_graph_pays[0].addEventListener('click', {
      handleEvent: switch_main_block,
      item_control: show_graph_pays[0],
      item_class: 'main__graph-pays',
    });
  }

  let show_graph_count_pays = document.getElementsByClassName('show-graph-count-pays');
  if (show_graph_count_pays.length > 0) {
    show_graph_count_pays[0].addEventListener('click', {
      handleEvent: switch_main_block,
      item_control: show_graph_count_pays[0],
      item_class: 'main__graph-count-pays',
    });
  }

  let show_graph_balance = document.getElementsByClassName('show-graph-balance');
  if (show_graph_balance.length > 0) {
    show_graph_balance[0].addEventListener('click', {
      handleEvent: switch_main_block,
      item_control: show_graph_balance[0],
      item_class: 'main__graph-balance',
    });
  }
}
