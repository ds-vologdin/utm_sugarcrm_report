function disable_td(button, td_class, button_text) {
  button.innerHTML = button_text;
  button.classList.remove('button--enable');

  var td_balance_items = document.getElementsByClassName(td_class);
  for (var i = 0; i < td_balance_items.length; i++) {
    td_balance_items[i].classList.add('td_disable');
  }
}

function enable_td(button, td_class, button_text) {
  button.innerHTML =  button_text;
  button.classList.add('button--enable');

  var td_balance_items = document.getElementsByClassName(td_class);
  for (var i = 0; i < td_balance_items.length; i++) {
    td_balance_items[i].classList.remove('td_disable');
  }
}

function switch_td() {
  console.log(this.td_class);
  if (this.button.classList.contains('button--enable')===false) {
    enable_td(this.button, this.td_class, this.button_text)
  }
  else {
    disable_td(this.button, this.td_class, this.button_text)
  }
}

// button-balance
var button_balance = document.getElementsByClassName('button-balance');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-balance',
  button_text: 'Остаток'
});
// button-arpu
var button_balance = document.getElementsByClassName('button-arpu');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-arpu',
  button_text: 'ARPU'
});
// button-active-user
var button_balance = document.getElementsByClassName('button-active-user');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-active-user',
  button_text: 'Активных'
});
// button-avg-balance-active
var button_balance = document.getElementsByClassName('button-avg-balance-active');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-avg-balance-active',
  button_text: 'Баланс активных'
});
// button-avg-balance-all
var button_balance = document.getElementsByClassName('button-avg-balance-all');
button_balance[0].addEventListener('click', {
  handleEvent: switch_td,
  button: button_balance[0],
  td_class: 'td-avg-balance-all',
  button_text: 'Баланс всех'
});
