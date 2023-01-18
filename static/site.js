// checkmarks
let checked_pcb_options = [], unchecked_pcb_options = [], pcb_options = [];
let pcb_count = 0;

// lines
let canvas, ctx;

// func die reageert op verandering van .pcb-option
jQuery(document).on('click', '.pcb-option', function () {
    if (returnAllCheckedPoints().length !== pcb_count) {

    } else {

    }
});

function checkBoxChecked (_id) {
    if (jQuery('#' + _id).is(':checked')) {
        console.log(_id + "box checked!");
        checked_pcb_options.push(_id);
    } else {
        console.log(_id + "box unchecked!");
        unchecked_pcb_options.push(_id);
    }
}

function returnAllCheckedPoints () {
    checked_pcb_options = [];
    pcb_options.forEach(box => checkBoxChecked (box));
    return checked_pcb_options;
}

function hasCheckBox (_4dArray) {
    console.log(JSON.stringify(_4dArray));
    // console.log(jQuery('#' + _id).val());
    
    // pcb_options.forEach( function (_id) { 
    //     if (JSON.stringify(_4dArray) !== jQuery('#' + _id).val() ) {
    //         let pcb_id = pcb_count;
    //         pcb_count++;
    //         pcb_options.push(pcb_id);
        
    //         jQuery (
    //             '<p class="pcb-option" style="margin-top: 0px; margin-bottom: 0px;">' +
    //                 '<input type="checkbox" id="' + pcb_id + '" name="' + pcb_id + '" value="' + JSON.stringify(_4dArray) + '" checked> ' +
    //                 '<label>Box ' + (pcb_id + 1) + ' </label>' +
    //             '</p>' 
    //         ) .insertAfter(jQuery('#pcb-options'));
    //     }
    // });
}

function insertCanvas () {
    // jQuery ('<canvas width="550" height="413" id="canvas">The browser doesn\'t support the canvas element</canvas>').insertAfter('#pcb_image');
    jQuery ('<canvas width="380" height="413" id="canvas">The browser doesn\'t support the canvas element</canvas>').insertAfter('#pcb_image');

    var position = jQuery("#pcb_image").offset();
    if(position) {
        jQuery('#canvas').css({ position:'absolute', top:position.top, left: position.left});

        canvas = document.querySelector('#canvas');
        ctx = canvas.getContext('2d');
    }
}

function drawLine(startX, startY, endX, endY, _color = 'red', _lineWidth = 2) {
    if(jQuery('#canvas').length != 1) {
        insertCanvas();
    }

    // set line stroke and line width
    ctx.strokeStyle = _color;
    ctx.lineWidth = _lineWidth;

    // draw a red line
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
}

/** Wordt aangeroepen via JS zodat uuid kan toegevoegd worden */
function insertImage () {
    jQuery ('<img id="pcb_image" src="./pcb?' + uuidv4() + '" alt="pcb image" class="pcb-image"></img>').insertBefore('#pcb_image');
}

let arrayData, cleanString;

function getTextFile() {
    jQuery.ajax({
        url: './array?' + uuidv4(),
        method: "GET",
        success: function (data) {
            /* retrief data */
            let jsonString = data.trim().replace(/array\(/g, "").replace(/\)/g, "");

            cleanString = JSON.parse(jsonString);

            arrayData = data.trim();

            /* use data */
            drawBox(cleanString[0]);
            drawBox(cleanString[1]);
            drawBox(cleanString[2]);
        }
    });
}

/** 4dArray: array with 4 corners with x, y as array */
function drawBox (_4dArray, _color) {
    hasCheckBox(_4dArray);

    drawLine (_4dArray[0][0], _4dArray[0][1], _4dArray[1][0], _4dArray[1][1], _color); // draw top-left to top-right
    drawLine (_4dArray[1][0], _4dArray[1][1], _4dArray[2][0], _4dArray[2][1], _color); // draw top-right to bottom-right
    drawLine (_4dArray[2][0], _4dArray[2][1], _4dArray[3][0], _4dArray[3][1], _color); // draw bottem-right to bottem-left
    drawLine (_4dArray[3][0], _4dArray[3][1], _4dArray[0][0], _4dArray[0][1], _color); // draw bottem-left to top-left
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
        // insertImage ();
    }
});

function removeCanvas() {
    if (jQuery("#canvas").length == 1) {
        jQuery("#canvas").remove();
    }
}