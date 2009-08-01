$(function() {
    $('#create_report').click(function() {
        var name = "";
        while (name === "") {
            name = prompt("What should this report be named?", "");
            if (name === null) {
                return;
            }
        }
        $('#report_name').val(name);
        $('#report_form').submit();
    });
});
