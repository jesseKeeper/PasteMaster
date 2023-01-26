// checkmarks
let checked_pcb_options = [], unchecked_pcb_options = [], pcb_options = [], pcb_options_value = [], pcb_printer_coords = [];
let pcb_count = 0;


// const refactoringValue = 0.3485; // 24" scherm
const refactoringValue = (0.5 * 0.6) - 0.0215; // 15" scherm

// lines
let canvas, ctx;

/* Bij het laden van de pagina */
jQuery (function() {
    /* alleen bij het start scherm */
    if (jQuery('#home-page').length === 1) {
        toggle_page('after-start');
    }

    if (jQuery('#start-page').length === 1) {
        toggle_page('hide-pcb');

        insertImage ();
        getTextFile();
    }
});

// func die reageert op verandering van .pcb-option
jQuery(document).on('click', '.pcb-option', function () {
    updateBox ()
});

// func die reageert op verandering van .pcb-option
jQuery(document).on('click', '#start-button', function () {
    jQuery('body').addClass("loading");

    toggle_page('after-init');
    toggle_page('after-start');
    // jQuery('body').addClass("loading");

    jQuery.ajax({
        url: './photo',
        method: "GET",
        success: function (data) {
            jQuery('body').removeClass("loading");

            windowToStart ()
        }
    });
});

function windowToStart () {
    window.location.replace("./start");
}

// func die reageert op verandering van .pcb-option
jQuery(document).on('click', '#start-paste', function () {
    clearCanvas();

    pcb_printer_coords = [];
    returnAllCheckedPoints().forEach(element => pcb_printer_coords.push(combinedArray[JSON.stringify(element)]));

    toggle_page('hide-options');
    toggle_page('hide-pcb');
    jQuery('body').addClass("loading");
    
    jQuery.ajax({
        url: './run',
        data : JSON.stringify(pcb_printer_coords),
        contentType : 'application/json',
        type : 'POST',       
        success: function (data) {
            jQuery('body').removeClass("loading");

            window.location.replace("./done");
        }
    });
});

// jQuery(document).on('hover', '.pcb-option', function () {
//     console.log('test');
//     ctx.fillStyle = "green";
//     ctx.fillRect(20, 10, 150, 100);
// });

function hasCheckbox (_4dArray) {
    if (pcb_options.length === 0) {
        addCheckbox(_4dArray);
    } else {
        if (!pcb_options_value.includes(JSON.stringify(_4dArray))) {
            addCheckbox(_4dArray);
        }
    }
}

function addCheckbox(_4dArray) {
    let pcb_id = pcb_count;
    pcb_count++;
    pcb_options_value.push(JSON.stringify(_4dArray));

    const inputString =         
        '<p id="' + pcb_id + '_pcb_option" class="pcb-option" style="margin-top: 0px; margin-bottom: 0px;">' +
            '<input type="checkbox" id="' + pcb_id + '" name="' + pcb_id + '" value="' + JSON.stringify(_4dArray) + '" checked> ' +
            '<label>Box ' + (pcb_id + 1) + ' </label>' +
        '</p>';
    
    if (pcb_options.length === 0) {
        jQuery ( inputString ) .insertAfter(jQuery('#pcb-options'));
    } else if (pcb_options.length % 25 == 0 ) {
        let extraDiv = 
        '<div id="_'+ (pcb_options.length / 25) +'_pcb_options" class="pcb-text"> ' + 
            inputString + 
        '</div>';
        if (pcb_options.length / 25 === 1) {
            jQuery (extraDiv) . insertAfter(jQuery('#_0_pcb_options'));
        } else {
            jQuery (extraDiv) . insertAfter(jQuery('#_'+ (pcb_options.length / 25) +'_pcb_options'));
        }
    } else {
        jQuery ( inputString ) .insertAfter(jQuery('#' + (pcb_id - 1) + '_pcb_option'));
    }

    pcb_options.push(pcb_id);
    setCheckbox(pcb_id, true);
}


let webArrayData, printerArrayData, combinedArray, cleanString, parsedJSON;
function getTextFile() {
    jQuery.ajax({
        url: './array?' + uuidv4(),
        method: "GET",
        success: function (data) {
            /* retrief data */
            parsedJSON = JSON.parse(data)

            webArrayData = parsedJSON['web_detections'];
            printerArrayData = parsedJSON['printer_detections'];
            combinedArray = [];

            for (let i = 0; i < webArrayData.length; i++) {
                combinedArray[JSON.stringify(webArrayData[i])] = JSON.parse(JSON.stringify(printerArrayData[i]));
            }

            /* use data */
            drawArrayOfBoxes(webArrayData);
        }
    });
}

/** 4dArray: array with 4 corners with x, y as array */
function drawBox (_4dArray, _color) {
    hasCheckbox(_4dArray);

    drawLine ((_4dArray[0][0] * refactoringValue), (_4dArray[0][1] * refactoringValue), (_4dArray[1][0] * refactoringValue), (_4dArray[1][1] * refactoringValue), _color); // draw top-left to top-right
    drawLine ((_4dArray[1][0] * refactoringValue), (_4dArray[1][1] * refactoringValue), (_4dArray[2][0] * refactoringValue), (_4dArray[2][1] * refactoringValue), _color); // draw top-right to bottom-right
    drawLine ((_4dArray[2][0] * refactoringValue), (_4dArray[2][1] * refactoringValue), (_4dArray[3][0] * refactoringValue), (_4dArray[3][1] * refactoringValue), _color); // draw bottem-right to bottem-left
    drawLine ((_4dArray[3][0] * refactoringValue), (_4dArray[3][1] * refactoringValue), (_4dArray[0][0] * refactoringValue), (_4dArray[0][1] * refactoringValue), _color); // draw bottem-left to top-left
}

/* SIMPLE FUCNTIONS */

/** checks if checkbox with given _id is checked */
function checkBoxChecked (_id) {
    if (jQuery('#' + _id).is(':checked')) {
        checked_pcb_options.push(JSON.parse(jQuery('#' + _id).val()));
    } else {
        unchecked_pcb_options.push(JSON.parse(jQuery('#' + _id).val()));
    }
}

function drawArrayOfBoxes (_arrayOfBoxes, _color = 'green') {
    for(let i = 0; i< _arrayOfBoxes.length; i++){
        drawBox(_arrayOfBoxes[i], _color);
    }
}

/** returns all checked checkboxes
 * unchecked can be retrieved by using unchecked_pcb_options!
 */
function returnAllCheckedPoints () {
    checked_pcb_options = [];
    unchecked_pcb_options = [];
    pcb_options.forEach(box => checkBoxChecked (box));
    return checked_pcb_options;
}

/** bij .header click ga naar homepage */
jQuery(document).on('click', '.header', function () {
    window.location.replace("./");
});

function homePrinter() {
    toggle_page('after-init');

    jQuery('body').addClass("loading");
    jQuery.ajax({
        url: './home',
        contentType : 'application/json',
        type : 'POST',       
        success: function (data) {
            jQuery('body').removeClass("loading");
            toggle_page('after-init');
            // toggle_page('printer-init');
        }
    });
}

/** genereer een uniek id --> zorg ervoor dat er niet gecached kan worden */
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

/** _id: target checkbox ID
 * state: default true 
 *      set true --> box will be set to checked
 *      set false --> box will be unchecked
 */
function setCheckbox (_id, state = true) {
    jQuery('#' + _id).prop("checked", state);
}

function drawLine(startX, startY, endX, endY, _color = 'red', _lineWidth = 2) {
    if (jQuery('#canvas').length != 1) {
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

/** Insert canvas, needed before drawLine can be used */
function insertCanvas () {
    var position = jQuery("#pcb_image").offset();

    jQuery ('<canvas width="'+ (screen.width * 0.6) +'" height="860" id="canvas">The browser doesn\'t support the canvas element</canvas>').insertAfter('#pcb_image');
    // jQuery ('<canvas width="1150" height="860" id="canvas">The browser doesn\'t support the canvas element</canvas>').insertAfter('#pcb_image');

    if(position) {
        jQuery('#canvas').css({ position:'absolute', top:position.top, left: position.left});

        canvas = document.querySelector('#canvas');
        ctx = canvas.getContext('2d');
    }
}

function updateBox () {
    clearCanvas(); // clear canvas to 'overwrite' the other draws
    drawArrayOfBoxes(returnAllCheckedPoints()); // draw the array 

    drawArrayOfBoxes(unchecked_pcb_options, 'red');
}

function toggle_page(_id) {
    var x = document.getElementById(_id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {  
        x.style.display = "none";
    }
}