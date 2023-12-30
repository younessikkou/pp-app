window.onload = function () {
    bootlint.showLintReportForCurrentDocument([], {
        hasProblems: false,
        problemFree: false
    });

    $('[data-toggle="tooltip"]').tooltip();

    function formatDate(date) {
        return (
            date.getDate() +
            "/" +
            (date.getMonth() + 1) +
            "/" +
            date.getFullYear()
        );
    }

    var currentDate = formatDate(new Date());

    $(".due-date-button").datepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayHighlight: true,
        startDate: currentDate,
        orientation: "bottom right"
    });

    $(".due-date-button").on("click", function (event) {
        $(".due-date-button")
            .datepicker("show")
            .on("changeDate", function (dateChangeEvent) {
                $(".due-date-button").datepicker("hide");
                $(".due-date-label").text(formatDate(dateChangeEvent.date));
            });
    });
};


$(".ajax-call").click(function(){
    //var a = $("#ajax-data").val();
    var form = $(this).closest("form");
    var a = $(this).attr('data-value');
    console.log(a);
    $.ajax({
        url : form.attr("data-validate-ajax-url"),
        type: 'POST', 
        data : {
            'ajaxdata' : a
        },
        dataType : 'json',
        success: function(dataajax){
            var select = $("#type_pj");
            select.empty(); // Videz les options existantes
            dataajax.list_pj.forEach(function(item) {
            select.append('<option>' + item.name + '</option>');
        });
        },
        error: function(xhr, status, error) { // Error handling
        console.log("Error: " + error);
        console.log("Status: " + status);
        console.dir(xhr);
        }
    })
});




