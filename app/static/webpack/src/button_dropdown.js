function show_dropdown_menu() {
  let dropdown_menu = this.getElementsByClassName('button-dropdown__menu');
  if (dropdown_menu.length === 0) {
    return null;
  }
  dropdown_menu[0].classList.remove('dropdown--uncollapse');
}

function hide_dropdown_menu() {
  let dropdown_menu = this.getElementsByClassName('button-dropdown__menu');
  if (dropdown_menu.length === 0) {
    return null;
  }
  dropdown_menu[0].classList.add('dropdown--uncollapse');
}

export let set_button_dropdown_menu = () => {
  let dropdown_menus = document.getElementsByClassName('button-dropdown');
  if (dropdown_menus.length > 0) {
    for (let dropdown_menu of dropdown_menus) {
      dropdown_menu.addEventListener('mouseover', show_dropdown_menu.bind(dropdown_menu));
      dropdown_menu.addEventListener('mouseout', hide_dropdown_menu.bind(dropdown_menu));
    }
  }
}
