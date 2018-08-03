$(document).ready(function () {
    let table = $("#id_table").DataTable({
        "order": [[0, "desc"]],
        "paging": false,
        "scrollY": "400px",
        "scrollCollapse": true,
        "dom": 't',
    });

    let searchInput = $("#id_custom_search");
    searchInput.on('keyup', function () {
        table.search(searchInput.val()).draw();
    });
    $("#id_reg_toggle").change(filter_reg).trigger("change");
});

function filter_reg() {
    let rows = $("tbody").find("tr.reg");
    if (this.checked) {
        rows.hide();
    } else {
        rows.show();
    }
}
