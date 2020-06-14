let globalNonse = new Object();
let targetIds = [];

function selectTank(tank_id) {

    // Reset form selection
    resetForm();

    $('div.targets img.spinner').show();

    $.ajax({
        url: "/match/fetchids/",   // the endpoint
        type: "POST",              // http method
        data: {tank_id: tank_id},  // data

        // Handle a successful response
        success: function(json) {
            if (json.identifiers) {
                targetIds = json.identifiers;
                validTankSelection()
            } else {
                alert("Could not fetch any registered identifiers for this tank.");
                invalidTankSelection()
            }
            // Hide loading animation
            $('div.targets img.spinner').hide()
        },
        error: function(xhr, status, msg) {
            // alert("Server error fetching registered cukes");
            invalidTankSelection();
            const html = `<h1> Server error fetching registered IDs: </h1> <br><br> <pre> ${xhr.responseText.replace('\n', '<br>').replace('\r', '<br>')} </pre>`
            const newTab = window.open('about:blank', '_blank');
            newTab.document.write(html);
            newTab.document.close();
            newTab.focus()
        },
    });
}

async function searchTargets(text) {
    // Set nonse, wait and check
    const localNonse = globalNonse = new Object();
    await new Promise((resolve) => setTimeout(resolve, 250));
    if (localNonse !== globalNonse) {
        // User still typing
        return
    }

    // Collect target ids matching user input
    let matching_ids = [];
    let selected = [];
    $('.targets .selected').children().each(function(i, item) { selected.push(item.id) })
    targetIds.forEach( function(item, i) {
        if (!selected.includes(item) & item.includes(text)) {
            matching_ids.push(item);
        }
    })

    // Populate dropdown list
    matching_ids = matching_ids.slice(0, 8);
    populateIdDropdown(matching_ids);
}

function populateIdDropdown(ids) {
    const dropdown = $('div.targets .dropdown');

    if (!ids.length) {
        dropdown.empty();
        const option = $('<div class="option blank"> No matching IDs in this tank </div>')
        dropdown.append(option);
        dropdown.css('opacity', '1');
        return
    }

    dropdown.empty();
    ids.forEach( function(item, i) {
        const option = $('<div class="option" onclick="selectTarget(this);"></div>').text(item);
        dropdown.append(option);
    });
    dropdown.css('opacity', '1');
}

function selectTarget(option) {
    // Create new button and add to "selected"
    const id = option.innerText
    const selected = $(`<div id="${ id }"> ${ id } <span onclick="$(this).parent().remove();">&times;</span> </div>`);
    $('div.targets .selected').append(selected);
    // Remove selection from options
    option.remove();
    // Return focus to text input
    $('div.targets input').focus();

    // Add to hidden input
    const targets = $('#target_ids').val();
    $('#target_ids').val(targets + '|' + id);
}
