let checked_pcb_options = [];
let pcb_options = [];
let pcb_count = 0;

function addOption (_text, _id) {
    let pcb_id = _id + '_' + pcb_count;
    pcb_count++;
    pcb_options.push(pcb_id);

    jQuery (
        '<p class="pcb-option" style="margin-top: 0px; margin-bottom: 0px;">' +
            '<input type="checkbox" id="' + pcb_id + '" name="' + _id + '" value="' + pcb_id + '" checked> ' +
            '<label for="1">' + _text + '</label>' +
        '</p>' 
    ) .insertAfter(jQuery('#pcb-options'));
}

jQuery(document).on('click', '.header', function () {
    window.location.replace("./");
});

function checkBoxChecked (_id) {
    if (jQuery('#' + _id).is(':checked')) {
        console.log(_id + "box checked!");
        checked_pcb_options.push(_id);
    } else {
        console.log(_id + "box not checked!");
    }
}

function returnAllCheckedPoints () {
    checked_pcb_options = [];
    pcb_options.forEach(box => checkBoxChecked (box));
    return checked_pcb_options;
}


jQuery (function() {
    addOption ('test', 'line');
    addOption ('line', 'test');
    addOption ('test', 'line');
    addOption ('line', 'test');
});