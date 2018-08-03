$(document).ready(function () {
    let table = $("#id_student_table").DataTable({
        "order": [[0, "desc"]],
        "paging": false,
        "scrollY": "400px",
        "scrollCollapse": true,
        "dom": 't',
    });

    let searchInput = $("#id_custom_search");
    searchInput.on('keyup', function() {
        table.search(searchInput.val()).draw();
    })
});
