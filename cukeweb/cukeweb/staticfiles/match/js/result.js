function toggleResultSelect(button) {
    if (button.innerText == "Select") {
        $(button).html("&#215;");
        $(button).parent().parent('tr').addClass('selected');
    } else {
        $(button).text("Select");
        $(button).parent().parent('tr').removeClass('selected');
    }
}
