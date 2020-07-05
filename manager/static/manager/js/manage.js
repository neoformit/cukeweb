// Functions for tank and cucumber management
function deleteTankDialog(tank_id) {
    $('#tankDeleteModal span.tank_id').text(tank_id);
    $('#tankDeleteModal button.danger').unbind();
    $('#tankDeleteModal button.danger').click(function() {
        deleteTankRequest(`${ tank_id }`)
    });
    $('.modal-overlay').fadeIn(250);
    $('#tankDeleteModal').fadeIn(250);
}

function deleteCukeDialog(tank_id, cuke_id) {
    $('#cukeDeleteModal span.cuke_id').text(cuke_id);
    $('#cukeDeleteModal span.tank_id').text(tank_id);
    $('#cukeDeleteModal button.danger').unbind();
    $('#cukeDeleteModal button.danger').click(function() {
        deleteCukeRequest(`${ tank_id }`, `${ cuke_id }`);
    });
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
            `<div class="detail" id="${ key }">
                <input name="${ key }" value="${ key }" placeholder="${ key }" onclick="$(this).parent().children('input').removeClass('invalid');" maxlength="255">
                <input name="value" value="${ details[key] }" placeholder="${ details[key] }" onclick="$(this).parent().children('input').removeClass('invalid');" maxlength="255">
                <div class="close" onclick="$(this).parent().empty();"> &times; </div>
            </div>`
        );
        parent.append(input);
    });

    $('.modal-overlay').fadeIn(250);
    $('#cukeEditModal').fadeIn(250);
    $('#cukeEditModal input[name="new_key"]').focus();
}

// Bind enter key to edit modal submit button
$('div.modal.edit').on('keypress', 'input', function(args) {
    if (args.keyCode == 13) {
        $('div.modal.edit button[type="submit"]').click();
        return false;
    }
});

function closeModal() {
    $('.modal-overlay').fadeOut(250);
    $('.modal').fadeOut(250);
    resetModals();
}

function resetModals() {
    $('.modal span.tank_id').text('');
    $('.modal span.cuke_id').text('');
    $('.modal form p.error-msg').text('');
    $('.modal .details').empty();
    $('.modal input').val('');
}

function validateCukeUpdate() {
    let valid = true;
    let key; let value;
    const detailDivs = $('.modal form div.detail');
    // Check detail fields which have been updated
    detailDivs.each( function(i, item) {
        if (!item.innerHTML) {
            // Field was deleted
            return
        }
        key = $(item).children('input')[0].value;
        value = $(item).children('input')[1].value;
        if (key === '' || value === '') {
            $(item).children('input').addClass('invalid');
            valid = false;
        }
    });

    key = $('form .add input[name="new_key"]')[0].value;
    value = $('form .add input[name="new_value"]')[0].value;
    if (key || value) {
        if (key === '' || value === '') {
            $('form .add input').addClass('invalid');
            valid = false;
        }
    }

    if (!valid) {
        $('.modal form p.error-msg').text('Field requires both a name and value');
        console.log('Form invalid');
        return false
    }
    console.log('Form valid');
    return true
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
    console.log('updateCukeDiv: data received:\n' + data);
    // Update cuke div with updated details
    var cuke = $(`#tank_${ tank_id } #cuke_${ cuke_id }`);
    // Update existing fields
    cuke.find('.details p').each( function(i, item) {
        let key = $(item).children('span.key').text();
        if (!Object.keys(data).includes(key)) { return }
        if (!data[key]) {
            // Field was deleted
            console.log(`updateCukeDiv: Removing p key="${ key }"`);
            item.remove();
            delete data[key];
            return
        }
        console.log(`updateCukeDiv: Updating p key="${ key }"`);
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
        console.log(`updateCukeDiv: Creating p key="${ key }"`);
        cuke.children('div.details').append(newField);
    });
}
