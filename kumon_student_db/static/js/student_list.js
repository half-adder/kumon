$(document).ready(function () {
    $("#id_student_name_input").on('keyup', function () {
        var value = $(this).val().toLowerCase();
        $("#id_student_table tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    $('#id_filter_form :checkbox').change(function () {
        if (this.checked) {
            $("#id_student_table tbody tr").filter(function () {
                var row = $(this);
                let cost = parseFloat(row.find('td:eq(5)').text());
                let paid = parseFloat(row.find('td').eq(6).text());
                if (paid < cost) {
                    row.hide();
                }
            });
        } else {
            $("#id_student_table tr").filter(function () {
                $(this).show();
            });
        }
    });
});
