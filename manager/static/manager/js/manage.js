// Functions for tank and cucumber management
function deleteTankDialog(tank_id) {
    $('#tankDeleteModal span.tank_id').text(tank_id);
    $('#tankDeleteModal button.danger').prop('onclick',
        `deleteTankRequest("${ tank_id }");`
    );
    $('.modal-overlay').fadeIn(250);
    $('#tankDeleteModal').fadeIn(250);
}

function deleteCukeDialog(tank_id, cuke_id) {
    $('#cukeDeleteModal span.cuke_id').text(cuke_id);
    $('#cukeDeleteModal span.tank_id').text(tank_id);
    $('#cukeDeleteModal button.danger').prop('onclick',
        `deleteCukeRequest("${ tank_id }", "${ cuke_id }")`
    );
    $('.modal-overlay').fadeIn(250);
    $('#cukeDeleteModal').fadeIn(250);
}

function editCukeDialog(tank_id, cuke_id) {
    $('#cukeEditModal span.cuke_id').text(cuke_id);
    $('#cukeEditModal span.tank_id').text(tank_id);
    const parent = $('#cukeEditModal .details');
    const details = getCukeDetails(tank_id, cuke_id);
    Object.keys(details).forEach(function(key) {
        input = $(
            `<div class="detail">
                <input name="${ key }" value="${ key }" placeholder="${ key }">
                <input name="value" value="${ details[key] }" placeholder="${ details[key] }">
            </div>`
        );
        parent.append(input);
    });

    $('.modal-overlay').fadeIn(250);
    $('#cukeEditModal').fadeIn(250);
}

function closeModal() {
    $('.modal-overlay').fadeOut(250);
    $('.modal').fadeOut(250);
    resetModals();
}

function resetModals() {
    $('.modal span.tank_id').text('');
    $('.modal span.cuke_id').text('');
    $('.modal .details').empty();
    $('.modal input').val('');
}

function getCukeDetails(tank_id, cuke_id) {
    // Copy existing fields from div.cuke
    const cuke = $(`#tank_${ tank_id } #cuke_${ cuke_id }`);
    const dkeys = cuke.find('span.key');
    let details = {};
    dkeys.each( function(i, item) {
        // assign details key: value
        details[$(item).text()] = $(item).next().text();
    })
    return details
}

function updateCukeDiv(tank_id, cuke_id, data) {
    // Update cuke div with updated details
    var cuke = $(`#tank_${ tank_id } #cuke_${ cuke_id }`);
    // Update existing fields
    cuke.find('.details p').each( function(i, item) {
        let key = $(item).children('span.key').text();
        if (!Object.keys(data).includes(key)) { return }
        $(item).children('span.key').text(data[key][0]);
        $(item).children('span.value').text(data[key][1]);
        delete data[key];
    });
    // Create new fields
    Object.keys(data).forEach( function(key, i) {
        let newField = $(
            `<p>
                <span class="key">${ data[key][0] }</span>:
                <span class="value">${ data[key][1] }</span>
            </p>`
        );
        cuke.children('div.details').append(newField);
    });
}
