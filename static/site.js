function test() {
    return "test";
}

jQuery(document).on('click', '.header', function () {
    window.location.replace("./index.html");
});

function addOption () {
    jQuery (
        '<p class="pcb-option">' +
            '<input type="checkbox" id="rec1" name="rec1" value="1"> ' +
            '<label for="1"> I have a boat</label>' +
        '</p>' 
        ) .insertAfter(jQuery('#pcb-options'));
}