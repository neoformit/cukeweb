function rejectMatch(button, action) {
    let undo = false;
    if (action == 'undo') {
        undo = true
    }

    const match_row = $(button).parents('tr');
    const match_td = match_row.children('td.match');
    const details_col = match_row.children('td.details').children('.col');
    const action_td = $(button).parents('td');
    const match_id = match_row[0].id;

    // Hide reject button + empty td.match
    $(button).hide();
    match_td.empty();
    details_col.empty();
    action_td.children('img.undo').remove();

    // Show loader in td.match and td.action
    const spinner1 = $('div.email img.spinner').clone();
    const spinner2 = $('div.email img.spinner').clone();
    const spinner3 = $('div.email img.spinner').clone();
    match_td.append(spinner1);
    details_col.append(spinner2)
    action_td.append(spinner3);

    // Make ajax request for next match
    $.ajax({
        url : "/match/reject/",   // the endpoint
        type : "POST",              // http method
        data : {
            'result_id': result_id,
            'match_id': match_id,
            'undo': undo,
        },

        // handle a successful response
        success : function(json) {
            // Hide loader. Return "Reject" button
            if (json.error) {
                $('table img.spinner').remove();
                alert(json.error);
                return
            }
            updateMatch(json, match_id)
        },
        error: function(xhr, status, msg) {
            // alert("Server error fetch match")
            newTabErrorMessage(xhr);
        }
    });
}

function updateMatch(data, match_id) {
    /// Update match row with replacement match following user rejection
    const row = $('#' + match_id)
    const match_td = row.children('td.match');
    const details_col = row.children('td.details').children('.col');
    const action_td = row.children('td.action');
    const match_img = $(`<img src="${ data.match_img_uri }" alt="Match image">`);
    const match_p = $(`<p> Identity: <b>${ data.identity }</b> </p>`);
    const details_p = $(`<p> Registered: <b>${ data.date_registered }</b> </p>`);
    const details_score = $(
        `<div class="score" style="background-color: ${ data.score_color };">
            <p>Score ${ data.score }</p>
        </div>`
    );

    if (data.is_target) {
        const target = $(`<div class="istarget"> Target animal </div>`)
        details_col.append(target);
    }

    // Remove loading animations
    match_td.empty();
    details_col.empty();
    action_td.children('.spinner').remove();

    // Add new elements
    match_td.append(match_img);
    match_td.append(match_p);
    details_col.append(details_p);
    details_col.append(details_score);

    // Check if first/last match for action elements
    if (!data.last) {
        action_td.children('button').show();
    }
    if (!data.first) {
        var action_undo_btn = $('div.main > img.undo').clone();
        action_undo_btn.attr('onclick', 'rejectMatch(this, "undo");');
        action_td.append(action_undo_btn);
    }
}
