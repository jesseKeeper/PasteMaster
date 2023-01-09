function test() {
    return "test";
}


let pcb_options = [];
let pcb_count = 0;

function addOption (_text, _id) {
    let pcb_id = _id + '_' + pcb_count;
    pcb_count++;

    jQuery (
        '<p class="pcb-option" style="margin-top: 0px; margin-bottom: 0px;">' +
            '<input type="checkbox" id="' + pcb_id + '" name="' + _id + '" value="' + pcb_id + '" checked> ' +
            '<label for="1">' + _text + '</label>' +
        '</p>' 
    ) .insertAfter(jQuery('#pcb-options'));
}

jQuery(document).on('click', '.header', function () {
    window.location.replace("./index.html");
});

function returnAllCheckedPoints () {
    return pcb_options;
}


jQuery (function() {
    addOption ('test', 'line');
    addOption ('test', 'line');
    addOption ('test', 'line');
    addOption ('test', 'line');
});