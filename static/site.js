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

/** Wordt aangeroepen via JS zodat uuid kan toegevoegd worden */
function insertImage (update = false) {
    if(update) {
        jQuery('#pcb_image').remove();
    }
    jQuery ('<img id="pcb_image" src="./pcb?' + uuidv4() + '" alt="pcb image" class="pcb-image"></img>').insertAfter('#pcb_user');
}



/** genereer een uniek id --> zorg ervoor dat er niet gecached kan worden */
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }

/** bij .header click ga naar homepage */
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