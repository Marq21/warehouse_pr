let elem = document.getElementById('id_current_quantity');
if (elem !== null) {
    elem.focus()
    elem.select()
}

let exp_date_elem = document.getElementsByClassName('date_of_expiration');

if (exp_date_elem !== null) {
    const date_for_red_color = Date.now() + 6;
    const current_date = Date.parse(exp_date_elem);
    print(current_date);

    if (current_date <= date_for_red_color) {
        exp_date_elem.style.color = 'red';
    }
}