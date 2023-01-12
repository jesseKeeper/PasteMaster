let checked_pcb_options = [];
let pcb_options = [];
let pcb_count = 0;

// func die reageert op verandering van .pcb-option
// jQuery(document).on('click', '.pcb-option', function () {
    // if (returnAllCheckedPoints().length === pcb_count) {
        // if (!jQuery('#pcb-options').is(':checked')) {
        // }
    // }
    // console.log('test');
// });

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


function checkBoxChecked (_id) {
    if (jQuery('#' + _id).is(':checked')) {
        // console.log(_id + "box checked!");
        checked_pcb_options.push(_id);
    }
}

function returnAllCheckedPoints () {
    checked_pcb_options = [];
    pcb_options.forEach(box => checkBoxChecked (box));
    return checked_pcb_options;
}

function insertImage () {
    jQuery ('<img id="pcb_image" src="./pcb?' + Math.floor(Math.random() * 101) + '" alt="pcb image" class="pcb-image"></img>').insertAfter('#image');
}

/* bij .header click ga naar homepage */
jQuery(document).on('click', '.header', function () {
    window.location.replace("./");
});

/* Bij het laden van de pagina */
jQuery (function() {

    /* alleen bij het start scherm */
    if (jQuery('#start-page').length === 1) {
        insertImage ();

        addOption ('test', 'line');
        addOption ('line', 'test');
        addOption ('test', 'line');
        addOption ('line', 'test');
    }

});
