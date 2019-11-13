$(document).ready(function () {

    // This is used to load programs for selected school
    $('#school').on('change', function() {
        var url = $('form').attr('prog-data-url');
        var school_id = $(this).children('option:selected').val();
        var program_input = $('#program');

        $.ajax({
            url: url,
            data: {
                'selected_school_id': school_id
            },
            type: 'GET',
                success: function(data) {
                    $(program_input).html(data);
                },
            });
        });
    });