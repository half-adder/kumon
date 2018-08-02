$(document).ready(function () {
    $('.phone').mask('(000) 000-0000');
    $('.birthdate').mask('00/00/0000', {placeholder: "MM/DD/YYYY"});

    let student_parent_address_ids = {
        // 'student_id': 'parent_id',
        'id_home_address': 'id_parent_address',
        'id_apt_or_suite': 'id_parent_apt_or_suite',
        'id_student_city': 'id_parent_city',
        'id_student_state_province': 'id_parent_state_province',
        'id_student_zip_code': 'id_parent_zip_code',
    };

    $('#id-checkbox-same-address').change(function () {
        if (this.checked) {
            Object.keys(student_parent_address_ids).forEach(function (key) {
                let student_input = $("#" + key);
                let parent_input = $("#" + student_parent_address_ids[key]);
                parent_input.val(student_input.val());
                student_input.on('keyup', function() {
                    parent_input.val(student_input.val());
                });
            });
        } else {
            Object.keys(student_parent_address_ids).forEach(function (key) {
                $("#" + student_parent_address_ids[key]).val("");
                $("#" + key).unbind();
            });
        }
    })
});
