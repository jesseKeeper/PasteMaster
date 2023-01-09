function test() {
    return "test";
}

function addOption (text, id) {
    jQuery (
        '<p class="pcb-option" style="margin-top: 0px; margin-bottom: 0px;">' +
            '<input type="checkbox" id="' + id + '" name="' + id + '" value="' + id + '"> ' +
            '<label for="1">' + text + '</label>' +
        '</p>' 
        ) .insertAfter(jQuery('#pcb-options'));
}

jQuery(document).on('click', '.header', function () {
    window.location.replace("./index.html");
});

$(function() {
    addOption ('test', 'line');
    addOption ('test', 'line');
    addOption ('test', 'line');
    addOption ('test', 'line');
});