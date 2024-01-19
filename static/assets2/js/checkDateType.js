

$(function () {
    $('#id_date_type').bootstrapToggle({
        on: 'AD',
        off: 'BS'
    });
})
var date_type = $('input[name="date_type"]').val();

if (date_type == 'off') {
    $(".datepicker").nepaliDatePicker({
        dateFormat: "%y-%m-%d",
        closeOnDateSelect: true,
    });
}

$('input[name="date_type"]').change(function (e) {
    $('#id_date_type').val($(this).prop('checked'))
    
    if ($(this).val() === "true") {
        $('.datepicker').each((id, elm) => {
            $(elm).unbind().removeData();
            $(elm).flatpickr({
                dateFormat: "Y-m-d",
                allowInput: true,
            });
        })

    }
    if ($(this).val() === "false") {
        $('.datepicker').each((id, elm) => {
            $(elm).flatpickr().destroy();
            $(elm).unbind().removeData();
            $(elm).nepaliDatePicker({
                dateFormat: "%y-%m-%d",
                closeOnDateSelect: true,
            });
        });

    }
});